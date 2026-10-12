"""Contêiner DAT da PlatinumGames: leitura e reempacotamento."""
import struct


def ler_dat(b):
    """Retorna lista de (nome, offset, tamanho) dos arquivos do DAT."""
    if b[:4] != b'DAT\0':
        raise ValueError('não é um arquivo DAT')
    n, po, eo, no, so = struct.unpack_from('<5I', b, 4)
    nl = struct.unpack_from('<I', b, no)[0]
    arquivos = []
    for i in range(n):
        off = struct.unpack_from('<I', b, po + 4 * i)[0]
        sz = struct.unpack_from('<I', b, so + 4 * i)[0]
        nm = b[no + 4 + i * nl:no + 4 + (i + 1) * nl].split(b'\0')[0].decode()
        arquivos.append((nm, off, sz))
    return arquivos


def membros(b):
    return {nm: b[off:off + sz] for nm, off, sz in ler_dat(b)}


def reempacotar(b, substituir):
    """Gera um novo DAT trocando os membros em `substituir` ({nome: bytes}).

    Mantém cabeçalho e tabelas, recalcula offsets e tamanhos e preserva o
    alinhamento original dos dados."""
    n, po, eo, no, so = struct.unpack_from('<5I', b, 4)
    nl = struct.unpack_from('<I', b, no)[0]
    ents = []
    for i in range(n):
        off = struct.unpack_from('<I', b, po + 4 * i)[0]
        sz = struct.unpack_from('<I', b, so + 4 * i)[0]
        nm = b[no + 4 + i * nl:no + 4 + (i + 1) * nl].split(b'\0')[0].decode()
        ents.append([i, nm, off, sz])
    vivos = [e for e in ents if e[2]]
    inicio = min(e[2] for e in vivos) if vivos else len(b)
    al = 0x1000
    while al > 1 and any(e[2] % al for e in vivos):
        al //= 2
    out = bytearray(b[:inicio])
    for e in sorted(vivos, key=lambda e: e[2]):
        dados = substituir.get(e[1], b[e[2]:e[2] + e[3]])
        out += b'\0' * ((-len(out)) % al)
        struct.pack_into('<I', out, po + 4 * e[0], len(out))
        struct.pack_into('<I', out, so + 4 * e[0], len(dados))
        out += dados
    fim = max(e[2] + e[3] for e in vivos) if vivos else inicio
    cauda = len(b) - fim
    out += b'\0' * cauda if cauda < al else b'\0' * ((-len(out)) % al)
    return bytes(out)
