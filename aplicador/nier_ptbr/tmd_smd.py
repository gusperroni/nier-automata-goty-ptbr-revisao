"""Tabelas de texto TMD e legendas SMD (UTF-16)."""
import struct


def ler_tmd(b):
    n = struct.unpack_from('<I', b, 0)[0]
    p = 4
    out = []
    for _ in range(n):
        par = []
        for _ in range(2):
            l = struct.unpack_from('<I', b, p)[0]
            p += 4
            par.append(b[p:p + 2 * l].decode('utf-16-le').rstrip('\0'))
            p += 2 * l
        out.append(tuple(par))
    return out


def escrever_tmd(registros):
    out = bytearray(struct.pack('<I', len(registros)))
    for k, v in registros:
        for s in (k, v):
            e = (s + '\0').encode('utf-16-le')
            out += struct.pack('<I', len(e) // 2) + e
    return bytes(out)


def ler_smd(b):
    n = struct.unpack_from('<I', b, 0)[0]
    out = []
    for i in range(n):
        p = 4 + i * 0x888
        k = b[p:p + 0x80].decode('utf-16-le').split('\0')[0]
        v = b[p + 0x88:p + 0x888].decode('utf-16-le').split('\0')[0]
        out.append((k, v))
    return out


def escrever_smd(original, novos):
    """Altera somente as entradas cujo texto mudou ({id: texto})."""
    b = bytearray(original)
    n = struct.unpack_from('<I', b, 0)[0]
    for i in range(n):
        p = 4 + i * 0x888
        k = b[p:p + 0x80].decode('utf-16-le').split('\0')[0]
        if k not in novos:
            continue
        atual = b[p + 0x88:p + 0x888].decode('utf-16-le').split('\0')[0]
        if atual == novos[k]:
            continue
        e = novos[k].encode('utf-16-le')
        if len(e) > 0x800 - 2:
            raise ValueError('legenda longa demais: %s' % k)
        b[p + 0x88:p + 0x888] = e + b'\0' * (0x800 - len(e))
    return bytes(b)
