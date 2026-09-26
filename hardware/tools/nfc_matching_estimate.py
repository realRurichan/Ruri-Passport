"""Small-signal first-pass estimate only; no claim of EM extraction or RF validation."""
import json,math
from pathlib import Path
width,height,turns,trace,gap=34.,24.,4,.4,.3
do=math.sqrt(width*height)/1000
di=do-2*((turns-1)*(trace+gap)+trace)/1000
davg=(do+di)/2;rho=(do-di)/(do+di)
# Mohan square current-sheet approximation applied to equal-area square.
# A rectangular PCB coil near metal requires measured impedance, not this approximation.
L=4e-7*math.pi*turns**2*davg*1.27/2*(math.log(2.07/rho)+.18*rho+.13*rho*rho)
f=13.56e6;w=2*math.pi*f
Rant,Cant,Rq=1.5,5e-12,2.0 # UNMEASURED antenna assumptions; each damper is 2 x 1R
L0,C0,R0=160e-9,750e-12,.1
def parallel(a,b):return 1/(1/a+1/b)
def zin(c1,c2):
 za=parallel(Rant+1j*w*L,1/(1j*w*Cant))
 zb=parallel(Rq+za/2,1/(1j*w*c2*1e-12))
 return 2*(R0+1j*w*L0+parallel(1/(1j*w*c1*1e-12)+zb,1/(1j*w*C0)))
a,b=60.,200.
for _ in range(30):
 e=zin(a,b)-11
 if abs(e)<1e-8:break
 da=(zin(a+.001,b)-zin(a,b))/.001;db=(zin(a,b+.001)-zin(a,b))/.001
 det=da.real*db.imag-db.real*da.imag
 a-=(e.real*db.imag-db.real*e.imag)/det
 b-=(da.real*e.imag-e.real*da.imag)/det
initial=zin(62,200)
report={'status':'ESTIMATE ONLY - measure bare coil and final assembly before RF release',
 'geometry_mm':{'width':width,'height':height,'turns':turns,'trace':trace,'gap':gap},
 'assumptions':{'antenna_loss_ohm':Rant,'antenna_parallel_pF':Cant*1e12,'each_damper_ohm':Rq,'emc_inductor_loss_ohm':R0},
 'approx_inductance_uH':L*1e6,'emc_resonance_MHz':1/(2*math.pi*math.sqrt(L0*C0))/1e6,
 'approx_damped_coil_Q':w*L/(Rant+2*Rq),'target_differential_ohm':11,
 'calculated_each_series_pF':a,'calculated_each_shunt_pF':b,
 'initial_each_series_pF':62,'initial_each_shunt_pF':200,
 'initial_differential_ohm':{'real':initial.real,'imag':initial.imag},
 'limits':['Excludes receiver loading, PCB parasitics, enclosure metal and nonlinear driver.',
 '62/200 pF are populated trial values, not production-approved tuning.',
 'Enable/calibrate DPC; verify TX current never exceeds 250mA in loading tests.',
 'Verify AGC, RF voltage, reader and card-emulation performance in final enclosure.'],
 'sources':['https://www.nxp.com/docs/en/application-note/AN13219.pdf','https://web.stanford.edu/~boyd/papers/pdf/inductance_expressions.pdf']}
dest=Path(__file__).resolve().parents[1]/'review/nfc-matching-estimate.json'
dest.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
