#!/usr/bin/env python3
"""Gera uma planilha CSV (antes/depois) das correções do patch, para revisão.

Os textos "antes" não ficam no repositório: são lidos da tradução da Tribo
instalada na sua máquina (pasta data do jogo, ou o backup criado pelo aplicador).

Uso: exportar_revisao.py PASTA_DO_JOGO [saida.csv]
"""
import csv
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, 'aplicador'))
from nier_ptbr import dat, mruby, mcd, tmd_smd  # noqa: E402


def textos_do_membro(mem, dados):
    if mem.endswith('.bin'):
        m = mruby.MRB(dados)
        out = {}
        for ir, slots, mid in m.tables():
            w = ir['iseq'][slots[1]]
            out[mid] = ir['pool'][(w >> 7) & 0xffff][1].decode('utf-8', 'replace')
        return out
    if mem.endswith('.smd'):
        return dict(tmd_smd.ler_smd(dados))
    if mem.endswith('.tmd'):
        return dict(tmd_smd.ler_tmd(dados))
    if mem.endswith('.mcd'):
        m = mcd.MCD(dados)
        return {m.evname.get(x['ev']): mcd.texto_mensagem(m, x) for x in m.msgs}
    return {}


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    data = os.path.join(sys.argv[1], 'data')
    backup = os.path.join(data, '_backup_revisao_ptbr')
    saida = sys.argv[2] if len(sys.argv) > 2 else 'revisao.csv'
    cache = {}
    with open(saida, 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.writer(fh, delimiter=';')
        w.writerow(['tipo', 'arquivo', 'membro', 'id', 'antes (Tribo v1.00)', 'depois (revisão)'])
        for tipo in ('scripts', 'legendas', 'textos_tmd', 'interface'):
            with open(os.path.join(RAIZ, 'patch', 'textos', tipo + '.jsonl'), encoding='utf-8') as f:
                for linha in f:
                    r = json.loads(linha)
                    chave = (r['arquivo'], r['membro'])
                    if chave not in cache:
                        p = os.path.join(backup, r['arquivo'])
                        if not os.path.exists(p):
                            p = os.path.join(data, r['arquivo'])
                        cache[chave] = textos_do_membro(r['membro'], dat.membros(open(p, 'rb').read())[r['membro']])
                    w.writerow([tipo, r['arquivo'], r['membro'], r['id'], cache[chave].get(r['id'], ''), r['texto']])
    print('Planilha gerada: ' + saida)


if __name__ == '__main__':
    main()
