"""Leitura de pacotes CPK da CRI (com descompressão CRILAYLA), usados para obter os arquivos atualizados do jogo."""
import struct,sys,os
def decrypt(b):
    b=bytearray(b);m=0x655f;t=0x4115
    for i in range(len(b)):
        b[i]^=m&0xff; m=(m*t)&0xffff
    return bytes(b)
def utf(b):
    if b[:4]!=b'@UTF': b=decrypt(b)
    assert b[:4]==b'@UTF',b[:4]
    size=struct.unpack('>I',b[4:8])[0]; d=b[8:8+size]
    _,rows_off,str_off,data_off,name_off,ncol,rowlen,nrows=struct.unpack('>HHIIIHHI',d[:24])
    def s(o):
        o+=str_off; e=d.index(b'\0',o); return d[o:e].decode('utf8','replace')
    cols=[];p=24
    fmt={0:'>B',1:'>b',2:'>H',3:'>h',4:'>I',5:'>i',6:'>Q',7:'>q',8:'>f'}
    def rd(p,t):
        if t in fmt:
            n=struct.calcsize(fmt[t]); return struct.unpack(fmt[t],d[p:p+n])[0],p+n
        if t==0xA: return s(struct.unpack('>I',d[p:p+4])[0]),p+4
        if t==0xB:
            o,l=struct.unpack('>II',d[p:p+8]); return d[data_off+o:data_off+o+l],p+8
        raise ValueError(t)
    for i in range(ncol):
        fl=d[p]; nm=s(struct.unpack('>I',d[p+1:p+5])[0]); p+=5
        st=fl&0xf0; ty=fl&0x0f; c=None
        if st==0x30: c,p=rd(p,ty)
        cols.append((nm,st,ty,c))
    out=[]
    for r in range(nrows):
        p=rows_off+r*rowlen; row={}
        for nm,st,ty,c in cols:
            if st==0x50: row[nm],p=rd(p,ty)
            elif st==0x30: row[nm]=c
            else: row[nm]=None
        out.append(row)
    return out
def crilayla(src):
    usize,hoff=struct.unpack('<II',src[8:16])
    res=bytearray(usize+0x100)
    res[0:0x100]=src[hoff+0x10:hoff+0x110]
    inend=hoff+0x10-1
    # bit reader from end backwards
    pos=inend; bitpool=0; bitsleft=0
    def get(n):
        nonlocal pos,bitpool,bitsleft
        out=0
        while n>0:
            if bitsleft==0:
                bitpool=src[pos]; bitsleft=8; pos-=1
            take=min(bitsleft,n)
            out=(out<<take)|((bitpool>>(bitsleft-take))&((1<<take)-1))
            bitsleft-=take; n-=take
        return out
    outp=usize+0x100-1; outend=0x100
    vle=[2,3,5,8]
    while outp>=outend:
        if get(1):
            off=get(13)+3+outp; ln=3
            lvl=0
            while True:
                t=get(vle[lvl]); ln+=t
                if t!=(1<<vle[lvl])-1: break
                if lvl<3: lvl+=1
            for _ in range(ln):
                res[outp]=res[off]; outp-=1; off-=1
        else:
            res[outp]=get(8); outp-=1
    return bytes(res)
class CPK:
    def __init__(s,path):
        s.f=open(path,'rb'); h=s.f.read(0x800)
        assert h[:4]==b'CPK '
        hdr=utf(h[0x10:])[0]; s.hdr=hdr
        to=hdr['TocOffset']; co=hdr['ContentOffset']
        s.f.seek(to); th=s.f.read(0x10); tsz=hdr['TocSize']
        tb=s.f.read(tsz)
        s.toc=utf(tb)
        s.add=min(to,co) if co else to
    def files(s):
        for r in s.toc:
            yield ((r['DirName'] or '')+'/'+r['FileName']).lstrip('/'),r
    def read(s,r):
        s.f.seek(r['FileOffset']+s.add); b=s.f.read(r['FileSize'])
        if r['ExtractSize']!=r['FileSize'] and b[:8]==b'CRILAYLA': b=crilayla(b)
        return b
