"""Bytecode mruby (RITE0003) dos scripts *_scp.bin: tabelas de mensagens por idioma.

O texto em português ocupa a posição do inglês (índice 1) em cada tabela."""
import struct
def crc16(data):
    wk=0
    for x in data:
        wk|=x
        for _ in range(8):
            wk<<=1
            if wk&0x1000000: wk^=0x1102100
    return (wk>>8)&0xffff
class MRB:
    def __init__(s,b):
        assert b[:8]==b'RITE0003'; s.b=b
        s.hdr=bytearray(b[:22])
        assert b[22:26]==b'IREP'
        s.secsize=struct.unpack_from('>I',b,26)[0]; s.secver=b[30:34]
        s.ireps=[]
        end=s._irep(34)
        s.irep_end=end
        assert end==22+s.secsize,(end,22+s.secsize)
        s.tail=b[end:]
    def _irep(s,p):
        b=s.b
        recsize,nlocals,nregs,rlen,ilen=struct.unpack_from('>IHHHI',b,p);p+=14
        p+=(-p)%4; iseq=list(struct.unpack_from('>%dI'%ilen,b,p)); p+=ilen*4
        plen=struct.unpack_from('>I',b,p)[0];p+=4; pool=[]
        for i in range(plen):
            t=b[p];l=struct.unpack_from('>H',b,p+1)[0];p+=3
            pool.append([t,b[p:p+l]]);p+=l
        slen=struct.unpack_from('>I',b,p)[0];p+=4; syms=[]
        for i in range(slen):
            l=struct.unpack_from('>H',b,p)[0];p+=2
            if l!=0xffff: syms.append(b[p:p+l]);p+=l+1
            else: syms.append(None)
        me=dict(recsize=recsize,nlocals=nlocals,nregs=nregs,rlen=rlen,iseq=iseq,pool=pool,syms=syms)
        me['poolsize0']=sum(3+len(x[1]) for x in pool)
        s.ireps.append(me)
        for i in range(rlen): p=s._irep(p)
        return p
    def dump(s):
        out=bytearray(s.hdr)+b'IREP'+b'\0\0\0\0'+s.secver
        for ir in s.ireps:
            ps=sum(3+len(x[1]) for x in ir['pool'])
            rs=ir['recsize']+ps-ir['poolsize0']
            out+=struct.pack('>IHHHI',rs,ir['nlocals'],ir['nregs'],ir['rlen'],len(ir['iseq']))
            out+=b'\0'*((-len(out))%4)
            out+=struct.pack('>%dI'%len(ir['iseq']),*ir['iseq'])
            out+=struct.pack('>I',len(ir['pool']))
            for t,v in ir['pool']: out+=bytes([t])+struct.pack('>H',len(v))+v
            out+=struct.pack('>I',len(ir['syms']))
            for y in ir['syms']:
                if y is None: out+=b'\xff\xff'
                else: out+=struct.pack('>H',len(y))+y+b'\0'
        struct.pack_into('>I',out,26,len(out)-22)
        out+=s.tail
        struct.pack_into('>I',out,10,len(out))
        struct.pack_into('>H',out,8,crc16(out[10:]))
        return bytes(out)
    def tables(s):
        """yield (irep, slot_instr_indices, mid) for message tables"""
        for ir in s.ireps:
            q=ir['iseq']
            for i in range(len(q)):
                if (q[i]&0x7f)==55:
                    n=(q[i]>>7)&0x7f
                    if n in (6,8) and i+1<len(q) and (q[i+1]&0x7f)==18:
                        mid=ir['syms'][(q[i+1]>>7)&0xffff]
                        yield ir,list(range(i-n,i)),(mid.decode() if mid else None)
    def set_slot(s,ir,k,text):
        q=ir['iseq']; w=q[k]
        if (w&0x7f)!=61: return False
        pi=(w>>7)&0xffff
        refs=sum(1 for x in q if (x&0x7f)==61 and (x>>7)&0xffff==pi)
        tb=text.encode('utf-8')
        if ir['pool'][pi][1]==tb: return True
        if refs==1: ir['pool'][pi][1]=tb
        else:
            ir['pool'].append([0,tb]); ni=len(ir['pool'])-1
            q[k]=(w&~(0xffff<<7))|(ni<<7)
        return True
