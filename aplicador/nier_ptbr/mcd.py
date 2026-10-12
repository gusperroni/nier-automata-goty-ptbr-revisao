"""Arquivos MCD (textos de interface) com fontes por símbolo e kerning."""
import struct
class MCD:
    def __init__(s,b):
        s.b=b
        mo,mn,so,sn,go,gn,fo,fn,eo,en=struct.unpack_from('<10I',b,0)
        s.syms=[list(struct.unpack_from('<HHI',b,so+8*i)) for i in range(sn)]
        s.glyphs=b[go:go+40*gn]; s.fonts=b[fo:fo+20*fn]; s.events_raw=b[eo:eo+40*en]
        s.events=[(struct.unpack_from('<II',b,eo+40*i)+(b[eo+40*i+8:eo+40*i+40].split(b'\0')[0].decode(),)) for i in range(en)]
        s.msgs=[]
        for i in range(mn):
            po,pn,seq,ev=struct.unpack_from('<4I',b,mo+16*i)
            paras=[]
            for j in range(pn):
                lo,ln,vp,hp,font=struct.unpack_from('<5I',b,po+20*j)
                lines=[]
                for k in range(ln):
                    to,pad,l1,l2,f1,f2=struct.unpack_from('<IIIIff',b,lo+24*k)
                    w=list(struct.unpack_from('<%dH'%l1,b,to))
                    lines.append(dict(pad=pad,l2=l2,f1=f1,f2=f2,w=w,l1=l1))
                paras.append(dict(vp=vp,hp=hp,font=font,lines=lines))
            s.msgs.append(dict(seq=seq,ev=ev,paras=paras))
        s.evname={e[0]:e[2] for e in s.events}
    def dump(s):
        out=bytearray(40)
        for m in s.msgs:
            for p in m['paras']:
                for l in p['lines']:
                    l['to']=len(out); out+=struct.pack('<%dH'%len(l['w']),*l['w'])
        out+=b'\0'*(((len(out)+4)&~3)-len(out))
        mo=len(out); out+=b'\0'*(16*len(s.msgs)); out+=b'\0'*4
        po0=len(out); np=sum(len(m['paras']) for m in s.msgs); out+=b'\0'*(20*np); out+=b'\0'*4
        lo0=len(out); nl=sum(len(p['lines']) for m in s.msgs for p in m['paras']); out+=b'\0'*(24*nl); out+=b'\0'*4
        so=len(out)
        for x in s.syms: out+=struct.pack('<HHI',*x)
        out+=b'\0'*4; go=len(out); out+=s.glyphs; out+=b'\0'*4
        fo=len(out); out+=s.fonts; out+=b'\0'*4
        eo=len(out); out+=s.events_raw
        pi=po0; li=lo0
        for i,m in enumerate(s.msgs):
            struct.pack_into('<4I',out,mo+16*i,pi,len(m['paras']),m['seq'],m['ev'])
            for p in m['paras']:
                struct.pack_into('<5I',out,pi,li,len(p['lines']),p['vp'],p['hp'],p['font']); pi+=20
                for l in p['lines']:
                    struct.pack_into('<IIIIff',out,li,l['to'],l['pad'],len(l['w']),l['l2'] if l['l2']!=l['l1'] else len(l['w']),l['f1'],l['f2']); li+=24
        struct.pack_into('<10I',out,0,mo,len(s.msgs),so,len(s.syms),go,len(s.glyphs)//40,fo,len(s.fonts)//20,eo,len(s.events_raw)//40)
        return bytes(out)


def tabela_kerning(mcds):
    """Aprende o kerning (fonte, caractere anterior, caractere) -> ajuste a partir de MCDs existentes."""
    import collections
    k = collections.defaultdict(collections.Counter)
    for m in mcds:
        for msg in m.msgs:
            for pa in msg['paras']:
                for l in pa['lines']:
                    w = l['w']
                    ant = None
                    for q in range(0, len(w) - 1, 2):
                        c = w[q]
                        cur = m.syms[c][1] if c < 0x8000 else c
                        if c < 0x8000:
                            k[(pa['font'], ant, cur)][w[q + 1]] += 1
                        ant = cur
    return {chave: cont.most_common(1)[0][0] for chave, cont in k.items()}


def codificar_linha(m, fonte, texto, kern):
    """Converte uma linha de texto nos códigos de símbolo do MCD.

    Marcas especiais no formato {xxxx:yy} (hexadecimal) são preservadas."""
    import re
    simb = {(x[0], x[1]): i for i, x in enumerate(m.syms)}
    w = []
    ant = None
    for t in re.findall(r'\{[0-9a-f]+:[0-9a-f]+\}|.', texto):
        if t.startswith('{') and len(t) > 1:
            x, y = t[1:-1].split(':')
            w += [int(x, 16), int(y, 16)]
            ant = int(x, 16)
            continue
        if t == ' ':
            w += [0x8001, fonte]
            ant = 0x8001
            continue
        i = simb.get((fonte, ord(t)))
        if i is None:
            raise KeyError('caractere %r não existe na fonte %d' % (t, fonte))
        w += [i, kern.get((fonte, ant, ord(t)), 0)]
        ant = ord(t)
    return w + [0x8000]


def texto_mensagem(m, msg):
    """Texto do primeiro parágrafo de uma mensagem (linhas separadas por \\n)."""
    linhas = []
    for l in msg['paras'][0]['lines']:
        s = ''
        w = l['w']
        q = 0
        while q < len(w) and w[q] != 0x8000:
            c = w[q]
            s += chr(m.syms[c][1]) if c < 0x8000 else (' ' if c == 0x8001 else '{%x:%x}' % (c, w[q + 1]))
            q += 2
        linhas.append(s)
    return '\n'.join(linhas)
