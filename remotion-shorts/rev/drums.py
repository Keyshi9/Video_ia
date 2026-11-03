import numpy as np, wave
sr=48000; T=20.0; n=int(sr*T); x=np.zeros(n); rng=np.random.default_rng(3)
def add(t,s,g):
    i=int(t*sr); j=min(n,i+len(s)); x[i:j]+=g*s[:j-i]
tt=np.arange(int(0.25*sr))/sr
kick=np.sin(2*np.pi*(50+90*np.exp(-tt*40))*tt)*np.exp(-tt*14)
tn=np.arange(int(0.18*sr))/sr
snare=(rng.standard_normal(len(tn))*np.exp(-tn*28))*0.8+np.sin(2*np.pi*190*tn)*np.exp(-tn*30)*0.4
k=0
while 0.1+0.5*k<T-0.3:
    t=0.1+0.5*k
    if k%2==0: add(t,kick,0.9)
    else: add(t,snare,0.7)
    if k%2==1: add(t+0.25,snare*0.35,0.5)   # little roll between steps
    k+=1
# swell: low drone fading in, ends with a final hit
env=np.minimum(1,np.arange(n)/sr/3)
drone=(np.sin(2*np.pi*110*np.arange(n)/sr)+0.5*np.sin(2*np.pi*165*np.arange(n)/sr))*0.06*env
x+=drone
x*=np.concatenate([np.ones(n-int(0.6*sr)),np.linspace(1,0,int(0.6*sr))])
x/=np.abs(x).max(); x*=0.8
w=wave.open('drums.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((x*32767).astype(np.int16).tobytes()); w.close()
