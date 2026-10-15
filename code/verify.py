"""Independent NumPy RK4/closed-form validation. Run with Python 3 + NumPy."""
from pathlib import Path
import json, csv
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
M,D,K,tau,kp,ki=5.,1.,2.,.5,2.,.5
A=np.array([[-D/M,0,K/M],[1,0,0],[-kp/tau,-ki/tau,-1/tau]])
b=np.array([-1/M,0,0])
def run(d,dt=.01,nonlinear=False,params=None):
    m,dd,kk,tt,pp,ii=params or (M,D,K,tau,kp,ki)
    t=np.arange(0,60+dt/2,dt); y=np.zeros((len(t),3))
    def f(y):
        v,z,u=y
        sensed=v+.5*v*v if nonlinear else v
        return np.array([(-dd*v+kk*u-d)/m,v,(-u-pp*sensed-ii*z)/tt])
    for j in range(1,len(t)):
        a=f(y[j-1]); c=f(y[j-1]+dt*a/2); e=f(y[j-1]+dt*c/2); g=f(y[j-1]+dt*e)
        y[j]=y[j-1]+dt*(a+2*c+2*e+g)/6
    return t,y

def metrics(t,y,d):
    v,z,u=y.T; ol=-d/D*(1-np.exp(-D*t/M))
    def settling(x,final,band):
        bad=np.flatnonzero(np.abs(x-final)>band)
        return float(t[bad[-1]+1]) if len(bad) and bad[-1]+1<len(t) else (0. if not len(bad) else None)
    peak=int(np.argmax(np.abs(v)))
    return dict(load=1+d,peak_speed=float(1+v[peak]),peak_time=float(t[peak]),peak_deviation_percent=float(100*abs(v[peak])),recovery_overshoot_percent_of_step=float(max(0,np.max(np.sign(d)*v))/abs(d)*100),settling_band=.02*abs(d),closed_settling_s=settling(v,0,.02*abs(d)),open_settling_s=settling(ol,-d/D,.02*abs(d)),closed_final_speed=float(1+v[-1]),open_asymptotic_speed=1-d/D,throttle_min=float(.6+u.min()),throttle_max=float(.6+u.max()),throttle_asymptotic=.6+d/K,level_asymptotic_m=-.01*d/(K*ki))

if __name__=='__main__':
    (ROOT/'results').mkdir(exist_ok=True)
    poles=np.linalg.eigvals(A); rows=[]; checks={}
    for d,label in [(.3,'increase'),(-.3,'decrease')]:
        t,y=run(d); _,fine=run(d,.005)
        steady=-np.linalg.solve(A,b*d)
        ev,V=np.linalg.eig(A); coeff=np.linalg.solve(V,-steady)
        exact=np.real(steady[:,None]+V@(coeff[:,None]*np.exp(ev[:,None]*t))) .T
        checks[label+'_rk4_vs_eigen']=float(np.max(np.abs(y-exact)))
        checks[label+'_step_halving']=float(np.max(np.abs(y-fine[::2])))
        assert checks[label+'_rk4_vs_eigen']<1e-8
        assert checks[label+'_step_halving']<1e-8
        assert np.max(np.abs(y[:,2]))<.4 and .6+np.min(y[:,2])>0
        rows.append(metrics(t,y,d))
        ol=1-d/D*(1-np.exp(-D*t/M))
        np.savetxt(ROOT/'results'/f'{label}.csv',np.column_stack([t,1+y[:,0],.6+y[:,2],ol,np.full_like(t,.6),.01*y[:,1]]),delimiter=',',header='time_s,closed_speed,closed_throttle,open_speed,open_throttle,level_change_m',comments='')
        tn,yn=run(d,nonlinear=True)
        checks[label+'_nonlinear_pressure_peak_difference']=float(np.max(np.abs(yn[:,0]-y[:,0])))
        np.savetxt(ROOT/'results'/f'{label}_pressure_nonlinear.csv',np.column_stack([tn,1+yn[:,0],.6+yn[:,2]]),delimiter=',',header='time_s,speed,throttle',comments='')
    checks['sign_symmetry']=float(np.max(np.abs(run(.3)[1]+run(-.3)[1])))
    # All 64 corners of a +/-20% independent parameter box; not a proof over its interior.
    margins=[]
    import itertools
    for factors in itertools.product([.8,1.2],repeat=6):
        m,dd,kk,tt,pp,ii=np.array([M,D,K,tau,kp,ki])*factors
        r=np.roots([tt*m,m+tt*dd,dd+kk*pp,kk*ii])
        margins.append(float(-np.max(r.real)))
    checks['minimum_corner_decay_rate_per_s']=min(margins)
    assert min(margins)>0
    # Deliberate high-I unstable example confirms finite stability boundary.
    checks['ki_12_poles']=[[float(x.real),float(x.imag)] for x in np.roots([2.5,5.5,5,24])]
    complex_pole=next(p for p in poles if p.imag>0)
    out=dict(parameters=dict(M=M,D=D,K=K,tau=tau,kp=kp,ki=ki),poles=[[float(p.real),float(p.imag)] for p in poles],complex_pair_wn=float(abs(complex_pole)),complex_pair_zeta=float(-complex_pole.real/abs(complex_pole)),ki_stability_limit=(M+tau*D)*(D+K*kp)/(tau*M*K),metrics=rows,checks=checks)
    (ROOT/'results'/'verified.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
