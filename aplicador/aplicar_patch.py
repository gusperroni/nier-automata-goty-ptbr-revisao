#!/usr/bin/env python3
"""Aplica o patch de revisão pt-BR sobre a tradução da Tribo Gamer Brasil (v1.00)
de NieR:Automata - Game of the YoRHa Edition (Steam).

Uso:
  aplicar_patch.py [PASTA_DO_JOGO]            aplica o patch
  aplicar_patch.py [PASTA_DO_JOGO] --verificar  só confere os arquivos, sem alterar nada
  aplicar_patch.py [PASTA_DO_JOGO] --restaurar  desfaz o patch usando o backup
  Opções: --sem-wax (não gera os arquivos para o mod WAX: script da "Mulher Estranha"
           e textos da tela de carregamento e dos itens)

Sem PASTA_DO_JOGO, usa a pasta onde o programa está (se for a pasta do jogo) ou pergunta.
A versão do patch fica em patch/manifesto.json ("versao_patch").
"""
import collections
import hashlib
import json
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from nier_ptbr import cpk, dat, mruby, mcd, tmd_smd  # noqa: E402

PASTA_BACKUP = '_backup_revisao_ptbr'
CONGELADO = getattr(sys, 'frozen', False)


def pasta_patch():
    for base in (getattr(sys, '_MEIPASS', None), os.path.dirname(AQUI), AQUI,
                 os.path.dirname(os.path.abspath(sys.executable))):
        if base and os.path.exists(os.path.join(base, 'patch', 'manifesto.json')):
            return os.path.join(base, 'patch')
    sys.exit('Não encontrei a pasta "patch" com os dados do patch.')


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for bloco in iter(lambda: f.read(1 << 20), b''):
            h.update(bloco)
    return h.hexdigest()


def sha1_texto(s):
    return hashlib.sha1(s.encode('utf-8')).hexdigest()[:12]


def sid(mid):
    """Identificador da fala sem o nome do personagem (M####_S####_G####_###)."""
    return '_'.join(mid.split('_')[:4])


def ler_jsonl(p):
    with open(p, encoding='utf-8') as f:
        return [json.loads(l) for l in f if l.strip()]


def achar_jogo(args):
    candidatos = [a for a in args if not a.startswith('--')]
    if candidatos:
        return candidatos[0]
    for d in (os.getcwd(), os.path.dirname(os.path.abspath(sys.executable)), os.path.dirname(AQUI)):
        if os.path.exists(os.path.join(d, 'NieRAutomata.exe')):
            return d
    return input('Informe a pasta do jogo (onde está o NieRAutomata.exe): ').strip().strip('"')


class Patch:
    def __init__(self, jogo):
        self.jogo = jogo
        self.data = os.path.join(jogo, 'data')
        self.pp = pasta_patch()
        self.man = json.load(open(os.path.join(self.pp, 'manifesto.json'), encoding='utf-8'))
        self.backup = os.path.join(self.data, PASTA_BACKUP)

    # ---------- verificação ----------
    def situacao(self):
        """Classifica cada arquivo: 'base' (Tribo v1.00), 'aplicado', 'ausente' ou 'diferente'."""
        res = {}
        aplic = [self.man.get(k, {}).get('arquivos', {}) for k in ('resultado', 'resultado_reconstrucao')]
        for fn, h in self.man['base']['arquivos'].items():
            p = os.path.join(self.data, fn)
            if not os.path.exists(p):
                res[fn] = 'ausente'
                continue
            atual = sha256(p)
            anteriores = self.man.get('versoes_anteriores', {}).values()
            if atual == h:
                res[fn] = 'base'
            elif any(a.get(fn) == atual for a in aplic):
                res[fn] = 'aplicado'
            elif any(a.get(fn) == atual for a in anteriores):
                res[fn] = 'anterior'
            else:
                res[fn] = 'diferente'
        return res

    # ---------- aplicação ----------
    def aplicar(self, com_wax=True):
        sit = self.situacao()
        cont = collections.Counter(sit.values())
        print('Arquivos da tradução: %d originais da Tribo v1.00, %d já corrigidos, %d de uma versão anterior '
              'do patch, %d ausentes, %d diferentes'
              % (cont['base'], cont['aplicado'], cont['anterior'], cont['ausente'], cont['diferente']))
        if cont['ausente'] or cont['diferente']:
            for fn, s in sorted(sit.items()):
                if s in ('ausente', 'diferente'):
                    print('  %-10s %s' % (s, fn))
            print('\nNada foi alterado. Instale (ou reinstale) a tradução da Tribo Gamer Brasil v1.00 e tente de novo.')
            return False
        alvo = [fn for fn, s in sit.items() if s == 'base']
        alvo += self._atualizaveis(sit)
        if not alvo:
            print('O patch já está aplicado.')
        else:
            self._aplicar_textos(set(alvo))
        if com_wax:
            self.aplicar_wax()
        print('\nPronto! Backup dos arquivos originais em: %s' % self.backup)
        return True

    def _atualizaveis(self, sit):
        """Arquivos corrigidos por uma versão anterior do patch (sem reconstrução) que podem ser
        refeitos a partir dos arquivos atualizados do jogo. Volta o arquivo da Tribo do backup."""
        classico = self.man.get('resultado', {}).get('arquivos', {})
        recon = self.man.get('reconstrucao', {}).get('arquivos', {})
        base = self.man['base']['arquivos']
        candidatos = []
        anteriores = []
        for fn, s in sit.items():
            b = os.path.join(self.backup, fn)
            if not (os.path.exists(b) and sha256(b) == base[fn]):
                continue
            if s == 'anterior':
                anteriores.append(fn)
            elif s == 'aplicado' and fn in recon and sha256(os.path.join(self.data, fn)) == classico.get(fn):
                candidatos.append(fn)
        if candidatos and not self._arquivos_atualizados(set(candidatos)):
            candidatos = []
        candidatos += anteriores
        if not candidatos:
            return []
        for fn in candidatos:
            shutil.copy2(os.path.join(self.backup, fn), os.path.join(self.data, fn))
        print('Atualizando %d arquivos corrigidos por uma versão anterior do patch.' % len(candidatos))
        return candidatos

    def _guardar_backup(self, fn):
        destino = os.path.join(self.backup, fn)
        if not os.path.exists(destino):
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            shutil.copy2(os.path.join(self.data, fn), destino)

    def _aplicar_textos(self, alvo):
        grupos = collections.defaultdict(lambda: collections.defaultdict(list))
        for nome in ('scripts', 'legendas', 'textos_tmd', 'interface'):
            for r in ler_jsonl(os.path.join(self.pp, 'textos', nome + '.jsonl')):
                if r['arquivo'] in alvo:
                    grupos[r['arquivo']][r['membro']].append(r)
        kern = None
        if any(m.endswith('.mcd') for g in grupos.values() for m in g):
            kern = self._kerning()
        avisos = []
        total = 0
        reconst = self._arquivos_atualizados(alvo)
        if reconst:
            print('Jogo com a atualização de novembro/2026: %d arquivos de script serão reconstruídos '
                  'a partir das versões novas do jogo.' % len(reconst))
        todos = sorted(set(grupos) | set(reconst))
        if not todos and not any(fn.startswith('novel/') for fn in alvo):
            print('O patch já está aplicado.')
            return
        for i, fn in enumerate(todos, 1):
            membros = grupos.get(fn, {})
            p = os.path.join(self.data, fn)
            b = open(p, 'rb').read()
            atuais = dat.membros(b)
            if fn in reconst:
                base_bytes, novos, n, av = self._reconstruir(fn, reconst[fn], atuais, membros)
            else:
                base_bytes, novos, n, av = b, {}, 0, []
                for mem, regs in membros.items():
                    novos[mem], k, a = self._aplicar_membro(mem, atuais[mem], regs, kern)
                    n += k
                    av += a
            total += n
            avisos += ['%s: %s' % (fn, a) for a in av]
            self._guardar_backup(fn)
            with open(p, 'wb') as f:
                f.write(dat.reempacotar(base_bytes, novos))
            print('\r  [%d/%d] %s' % (i, len(todos), fn) + ' ' * 20, end='', flush=True)
        print()
        n_nov = self._aplicar_novels(alvo)
        print('Textos corrigidos: %d (+ %d trechos de novels)' % (total, n_nov))
        if avisos:
            print('Avisos (%d):' % len(avisos))
            for a in avisos[:50]:
                print('  ' + a)

    def _aplicar_membro(self, mem, dados, regs, kern):
        quer = {r['id']: r for r in regs}
        feitos = set()
        avisos = []

        def confere(rid, atual):
            if sha1_texto(atual) != quer[rid]['antes_sha1']:
                avisos.append('texto anterior inesperado em %s' % rid)

        if mem.endswith('.bin'):
            m = mruby.MRB(dados)
            for ir, slots, mid in m.tables():
                if mid in quer:
                    w = ir['iseq'][slots[1]]
                    confere(mid, ir['pool'][(w >> 7) & 0xffff][1].decode('utf-8', 'replace'))
                    m.set_slot(ir, slots[1], quer[mid]['texto'])
                    feitos.add(mid)
            saida = m.dump()
        elif mem.endswith('.smd'):
            for k, v in tmd_smd.ler_smd(dados):
                if k in quer:
                    confere(k, v)
                    feitos.add(k)
            saida = tmd_smd.escrever_smd(dados, {k: r['texto'] for k, r in quer.items()})
        elif mem.endswith('.tmd'):
            regs_tmd = []
            for k, v in tmd_smd.ler_tmd(dados):
                if k in quer:
                    confere(k, v)
                    feitos.add(k)
                    v = quer[k]['texto']
                regs_tmd.append((k, v))
            saida = tmd_smd.escrever_tmd(regs_tmd)
        elif mem.endswith('.mcd'):
            m = mcd.MCD(dados)
            for msg in m.msgs:
                nm = m.evname.get(msg['ev'])
                if nm not in quer:
                    continue
                confere(nm, mcd.texto_mensagem(m, msg))
                pa = msg['paras'][0]
                f1 = pa['lines'][0]['f1'] if pa['lines'] else 0.0
                try:
                    linhas = [mcd.codificar_linha(m, pa['font'], s, kern) for s in quer[nm]['texto'].split('\n')]
                except KeyError as e:
                    avisos.append('%s: %s' % (nm, e))
                    continue
                pa['lines'] = [dict(pad=0, l1=len(w), l2=len(w), f1=f1, f2=0.0, w=w) for w in linhas]
                feitos.add(nm)
            saida = m.dump()
        else:
            raise ValueError('tipo de arquivo desconhecido: ' + mem)
        for k in set(quer) - feitos:
            avisos.append('texto %s não encontrado' % k)
        return saida, len(feitos), avisos

    def _arquivos_atualizados(self, alvo):
        """Arquivos de script cuja versão atualizada (nov/2026) está nos pacotes do jogo.

        Retorna {arquivo: bytes do DAT original atualizado}."""
        cfg = self.man.get('reconstrucao', {}).get('arquivos', {})
        por_cpk = collections.defaultdict(list)
        for fn, c in cfg.items():
            if fn in alvo:
                por_cpk[c['cpk']].append(fn)
        achados = {}
        for nome_cpk, arquivos in sorted(por_cpk.items()):
            p = os.path.join(self.data, nome_cpk)
            if not os.path.exists(p):
                continue
            pacote = cpk.CPK(p)
            queremos = set(arquivos)
            for nome, reg in pacote.files():
                if nome in queremos:
                    dados = pacote.read(reg)
                    if hashlib.sha256(dados).hexdigest() == cfg[nome]['sha256_original']:
                        achados[nome] = dados
            pacote.f.close()
        return achados

    def _reconstruir(self, fn, original, tribo, membros_patch):
        """Monta o DAT a partir da versão atualizada do jogo, com o texto da Tribo e as correções."""
        cfg = self.man['reconstrucao']['arquivos'][fn]
        novos_orig = dat.membros(original)
        manter_tribo = set(cfg.get('manter_tribo', []))
        manter_en = set(cfg.get('manter_ingles_novo', []))
        saida = {}
        total = 0
        avisos = []
        for mem, dados in novos_orig.items():
            if mem in manter_tribo:
                saida[mem] = tribo[mem]
                continue
            if not mem.endswith('_scp.bin') or dados[:4] != b'RITE' or mem not in tribo:
                continue
            textos_tribo = {}
            for ir, slots, mid in mruby.MRB(tribo[mem]).tables():
                w = ir['iseq'][slots[1]]
                if (w & 0x7f) == 61:
                    textos_tribo[mid] = ir['pool'][(w >> 7) & 0xffff][1].decode('utf-8', 'replace')
            m = mruby.MRB(dados)
            mids_novos = {mid for _, _, mid in m.tables()}
            # falas renomeadas pela atualização (mesma fala, outro personagem no nome)
            por_sid = {sid(mid): t for mid, t in textos_tribo.items() if mid not in mids_novos}
            quer = {r['id']: r for r in membros_patch.get(mem, [])}
            quer_sid = {sid(k): r for k, r in quer.items() if k not in mids_novos}
            feitos = set()
            for ir, slots, mid in m.tables():
                if mid in manter_en:
                    continue
                t = textos_tribo[mid] if mid in textos_tribo else por_sid.get(sid(mid))
                r = quer[mid] if mid in quer else quer_sid.get(sid(mid))
                if r is not None:
                    if t is not None and sha1_texto(t) != r['antes_sha1']:
                        avisos.append('%s: texto anterior inesperado em %s' % (mem, mid))
                    t = r['texto']
                    feitos.add(r['id'])
                if t is not None:
                    m.set_slot(ir, slots[1], t)
            for k in set(quer) - feitos:
                avisos.append('%s: texto %s não encontrado' % (mem, k))
            total += len(feitos)
            saida[mem] = m.dump()
        return original, saida, total, avisos

    def _kerning(self):
        mcds = []
        pasta_ui = os.path.join(self.data, 'ui')
        for nome in sorted(os.listdir(pasta_ui)) if os.path.isdir(pasta_ui) else []:
            if nome.endswith('.dat'):
                for mem, d in dat.membros(open(os.path.join(pasta_ui, nome), 'rb').read()).items():
                    if mem.endswith('.mcd'):
                        mcds.append(mcd.MCD(d))
        return mcd.tabela_kerning(mcds)

    def _aplicar_novels(self, alvo):
        por_arquivo = collections.defaultdict(list)
        for r in ler_jsonl(os.path.join(self.pp, 'textos', 'novels.jsonl')):
            if r['arquivo'] in alvo:
                por_arquivo[r['arquivo']].append(r)
        n = 0
        for fn, regs in por_arquivo.items():
            p = os.path.join(self.data, fn)
            s = open(p, encoding='utf-8', newline='').read()
            for r in regs:
                if r['trecho_antes'] in s:
                    s = s.replace(r['trecho_antes'], r['trecho_depois'])
                    n += 1
                else:
                    print('  aviso: trecho não encontrado em %s: %r' % (fn, r['trecho_antes'][:40]))
            self._guardar_backup(fn)
            with open(p, 'w', encoding='utf-8', newline='') as f:
                f.write(s)
        return n

    # ---------- WAX ----------
    def _script_wax(self):
        dll = os.path.join(self.jogo, 'dxgi.dll')
        if not os.path.exists(dll):
            return None
        b = open(dll, 'rb').read()
        if b'wax::overrides' not in b:
            return None
        nome = b'7a562cb9_scp.bin'
        i = b.find(nome + b'RITE0003')
        if i < 0:
            return None
        i += len(nome)
        tam = int.from_bytes(b[i + 10:i + 14], 'big')
        return b[i:i + tam]

    def aplicar_wax(self):
        blob = self._script_wax()
        if blob is None:
            print('Mod WAX não encontrado (ou sem o script da "Mulher Estranha"): etapa do WAX ignorada.')
            return
        cfg = self.man['wax']
        dat_r110 = open(os.path.join(self.data, cfg['script_base']), 'rb').read()
        traduzido = mruby.MRB(dat.membros(dat_r110)[cfg['membro_base']])
        textos = {}
        for ir, slots, mid in traduzido.tables():
            w = ir['iseq'][slots[1]]
            textos[mid] = ir['pool'][(w >> 7) & 0xffff][1].decode('utf-8')
        for r in ler_jsonl(os.path.join(self.pp, 'textos', 'wax.jsonl')):
            textos[r['id']] = r['texto']
        m = mruby.MRB(blob)
        n = 0
        for ir, slots, mid in m.tables():
            if mid in textos:
                m.set_slot(ir, slots[1], textos[mid])
                n += 1
        destino = os.path.join(self.jogo, *cfg['arquivo_alvo'].split('/'))
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino, 'wb') as f:
            f.write(m.dump())
        print('WAX: script da "Mulher Estranha" traduzido (%d falas) em %s' % (n, destino))
        origem_mcd = os.path.join(self.pp, 'wax_mcd.json')
        if os.path.exists(origem_mcd) and cfg.get('arquivo_mcd'):
            destino_mcd = os.path.join(self.jogo, *cfg['arquivo_mcd'].split('/'))
            os.makedirs(os.path.dirname(destino_mcd), exist_ok=True)
            shutil.copyfile(origem_mcd, destino_mcd)
            print('WAX: textos do WAX (tela de carregamento e itens) traduzidos em %s' % destino_mcd)

    # ---------- restauração ----------
    def restaurar(self):
        if not os.path.isdir(self.backup):
            print('Não há backup do patch nesta pasta do jogo.')
            return
        n = 0
        for raiz, _, arqs in os.walk(self.backup):
            for a in arqs:
                origem = os.path.join(raiz, a)
                rel = os.path.relpath(origem, self.backup)
                shutil.copy2(origem, os.path.join(self.data, rel))
                n += 1
        for chave in ('arquivo_alvo', 'arquivo_mcd'):
            if chave in self.man['wax']:
                wax = os.path.join(self.jogo, *self.man['wax'][chave].split('/'))
                if os.path.exists(wax):
                    os.remove(wax)
        print('%d arquivos restaurados para a versão da Tribo Gamer.' % n)


def main(argv):
    print('Patch de revisão pt-BR para NieR:Automata (sobre a tradução da Tribo Gamer Brasil v1.00)\n')
    jogo = achar_jogo(argv)
    if not os.path.exists(os.path.join(jogo, 'NieRAutomata.exe')):
        print('NieRAutomata.exe não encontrado em: %s' % jogo)
        return 1
    p = Patch(jogo)
    print('Versão do patch: %s\nPasta do jogo: %s\n' % (p.man['versao_patch'], jogo))
    if '--restaurar' in argv:
        p.restaurar()
    elif '--verificar' in argv:
        for k, v in sorted(collections.Counter(p.situacao().values()).items()):
            print('%-10s %d arquivo(s)' % (k, v))
    else:
        return 0 if p.aplicar(com_wax='--sem-wax' not in argv) else 1
    return 0


if __name__ == '__main__':
    try:
        cod = main(sys.argv[1:])
    except Exception as e:  # mostra o erro antes de fechar a janela
        print('\nErro: %s' % e)
        cod = 1
    if CONGELADO:
        input('\nPressione Enter para sair...')
    sys.exit(cod)
