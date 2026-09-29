"""Synthesized soundtrack for the IKEA AI 2027 concept video (32s). No samples, no licensing."""
import numpy as np, wave
SR=44100; DUR=32.0; N=int(SR*DUR); t=np.arange(N)/SR
mix=np.zeros(N); rng=np.random.default_rng(7)
def note(f): return 440*2**((f-69)/12)
def add(sig,start):
    i=int(start*SR); j=min(N,i+len(sig)); mix[i:j]+=sig[:j-i]
def env(n,a,r):
    e=np.ones(n); a=int(a*SR); r=int(r*SR)
    e[:a]=np.linspace(0,1,a); e[-r:]*=np.linspace(1,0,r); return e
# pad: warm chords, 4s each
chords=[[53,57,60,64],[48,55,60,64],[45,52,57,60],[43,50,55,59],[53,57,60,64],[48,55,60,64],[43,50,55,62],[48,52,55,60,67]]
for k,ch in enumerate(chords):
    d=4.6 if k<7 else 4.0; n=int(d*SR); tt=np.arange(n)/SR; s=np.zeros(n)
    for m in ch:
        f=note(m); s+=np.sin(2*np.pi*f*tt)+.5*np.sin(2*np.pi*f*1.003*tt)+.18*np.sin(2*np.pi*2*f*tt)
    add(.035*s*env(n,1.2,1.4),k*4)
# arpeggio plucks, 8ths at 110bpm, from 3s to 29s
step=60/110/2
for i in range(int((29-3)/step)):
    st=3+i*step; ch=chords[min(7,int(st//4))]; m=ch[i%len(ch)]+12
    n=int(.35*SR); tt=np.arange(n)/SR
    s=np.sin(2*np.pi*note(m)*tt)*np.exp(-tt*11)
    add(.05*s,st)
# soft kick on beats 3-29
beat=60/110
for i in range(int((29-3)/beat)):
    n=int(.25*SR); tt=np.arange(n)/SR
    f=50+90*np.exp(-tt*30); s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*14)
    add(.22*s,3+i*beat)
    if i%2==1:  # hat
        n2=int(.05*SR); add(.025*rng.standard_normal(n2)*np.exp(-np.arange(n2)/SR*90),3+i*beat+beat/2)
# SFX
def blip(f,d=.08,v=.18):
    n=int(d*SR); tt=np.arange(n)/SR; return v*np.sin(2*np.pi*f*tt)*np.exp(-tt*(4/d))
def tap(): n=int(.03*SR); tt=np.arange(n)/SR; return .25*np.sin(2*np.pi*2400*tt)*np.exp(-tt*200)
def whoosh(d=.45,v=.09):
    n=int(d*SR); x=rng.standard_normal(n); y=np.convolve(x,np.ones(30)/30,'same'); return v*y*np.sin(np.linspace(0,np.pi,n))**2
for s in [2.0,5.85,17.85]: add(tap(),s+.05)
for s in [1.15,2.3,6.45,9.45,12.95,15.45,18.45,21.95,25.45,29.0]: add(whoosh(),s)
add(blip(880)+0,4.5); add(blip(1320),4.62)              # lock
for s in [6.8,7.3,9.75,11.35,25.75,26.6,27.55,28.05]: add(blip(1046,.06,.08),s)  # bubbles
add(blip(660,.1,.12),5.9); add(blip(990,.12,.12),6.0)    # added
for i,s in enumerate([15.75,16.05,16.35]): add(blip(784+i*110,.07,.1),s)
add(blip(1850,.14,.2),19.85); add(blip(1850,.14,.2),20.25)  # POS scan beep
for i,s in enumerate([20.55,20.73,20.91,21.15]): add(blip(1200+i*80,.05,.08),s)
add(blip(1568,.18,.1),26.8); add(blip(2093,.18,.1),27.1)  # checks
for i,m in enumerate([72,76,79,84]): add(blip(note(m),.9,.07),29.55+i*.12)  # end chime
# master
fade=np.ones(N); fo=int(1.3*SR); fade[-fo:]=np.linspace(1,0,fo)**1.5; fade[:int(.3*SR)]=np.linspace(0,1,int(.3*SR))
mix*=fade; mix=np.tanh(mix*1.4); mix/=np.max(np.abs(mix))*1.12
st=np.stack([mix,np.roll(mix,120)],1)
with wave.open('soundtrack.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype('<i2').tobytes())
print('ok')
