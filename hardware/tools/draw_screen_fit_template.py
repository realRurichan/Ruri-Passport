"""Create a 1:1 mechanical check aid, not a released shell or FPC design."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('CheckSans','/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))
p=Path('output/pdf/screen-fit-check-1to1.pdf');p.parent.mkdir(parents=True,exist_ok=True)
c=canvas.Canvas(str(p),pagesize=(210*mm,297*mm))
c.setTitle('Ruri Passport — CL40BC264-40C 1:1 fit check')
c.setAuthor('Ruri Passport project')
def text(x,y,s,size=9,color='#172B4D'):
 c.setFillColor(color);c.setFont('CheckSans',size);c.drawString(x*mm,y*mm,s)
def line(x1,y1,x2,y2,color='#172B4D',dash=None):
 c.setStrokeColor(color);c.setLineWidth(.25*mm);c.setDash(dash or []);c.line(x1*mm,y1*mm,x2*mm,y2*mm);c.setDash([])
def rect(x,y,w,h,color='#172B4D',fill=None):
 c.setStrokeColor(color);c.setLineWidth(.25*mm)
 if fill:c.setFillColor(fill)
 c.rect(x*mm,y*mm,w*mm,h*mm,stroke=1,fill=int(bool(fill)))
def title(n,t):
 text(16,278,t,17);text(16,269,'Ruri Passport · CL40BC264-40C 非触摸版 · 2026-09-26',9)
 text(16,260,'A4 / 实际大小 / 100%打印；关闭“适合页面”。先量标尺，再核对实物。',10,'#A23B23')
 text(16,13,f'{n}/2  · 原创核对图 CERN-OHL-S-2.0 · 非制造放行图；不得据此加工外壳。',8)
def ruler(x,y):
 line(x,y,x+50,y)
 for d in range(0,51,5):line(x+d,y,x+d,y+(3 if d%10==0 else 1.5))
 text(x,y-5,'这条线必须实测为 50 mm',9)

title(1,'屏幕与主板装配核对 · 正面坐标')
x0,y0=22,78
rect(x0,y0,88,135)
rect(x0+13.56,y0+38.5,60.88,94.57,'#29658C')
text(x0+17,y0+126,'LCD外框 60.88 × 94.57',9)
for x,y in [(3,132),(84.5,132),(3.5,38),(84.5,50)]:
 c.setStrokeColor('#172B4D');c.circle((x0+x)*mm,(y0+y)*mm,1.1*mm,stroke=1)
for x,y,s in [(42,31,'上'),(42,17,'下'),(35,24,'左'),(49,24,'右'),(42,24,'OK')]:
 rect(x0+x-2.55,y0+y-2.55,5.1,5.1,'#777777');text(x0+x-1.8,y0+y-.8,s,6)
# Current J1 body reference; mouth is approximate, not a mating datum.
rect(x0+49-11.65,y0+58.35,23.3,6.5,'#A23B23')
for pin in range(1,41):
 x=x0+58.75-(pin-1)*.5;line(x,y0+58.35,x,y0+59.65,'#A23B23')
text(x0+60,y0+58,'1',8,'#A23B23');text(x0+33.5,y0+58,'40',8,'#A23B23')
line(x0+37.35,y0+65.3,x0+60.65,y0+65.3,'#A23B23',[2,2])
# Projected manufacturer fold datum; face/pin orientation intentionally unresolved.
rect(x0+33.75,y0+76,20.5,3.5,'#22816D')
line(x0+30,y0+79.5,x0+75,y0+79.5,'#22816D',[2,2])
line(x0+44,y0+38.5,x0+44,y0+86,'#22816D',[2,2])
line(x0+54.25,y0+78,119,171,'#22816D');text(120,172,'绿色：折回端参考',10,'#22816D')
text(120,166,'中心 x=44；端部 y=79.5±0.8',8)
text(120,160,'端子宽20.50；金手指长3.50',8)
text(120,154,'触点面与脚序：待实物核对',8,'#A23B23')
line(x0+60.65,y0+61,119,140,'#A23B23');text(120,140,'红色：当前PCB插座',10,'#A23B23')
text(120,134,'焊盘行中心 (49,59)',8)
text(120,128,'1脚在右，40脚在左',8)
text(120,122,'入口参考约 y=65.3，未签核',8)
text(120,113,'端部坐标不能等同焊盘坐标。',8)
text(120,107,'本图不建议直接移动或旋转座。',8)
text(x0,y0-7,'原点 (0,0)；X向右、Y向上；单位mm。',8)
text(16,237,'蓝框：屏幕外形；黑框：88 × 135 PCB；圆圈：现有M2孔。',9)
text(16,230,'将屏幕放在蓝框内，排线按自然弯曲路径放置，勿强扭或压死折线。',9)
ruler(30,44)
text(115,55,'记录：触点朝屏背 / 朝PCB？',9)
text(115,47,'插头能否平直进入并锁紧？',9)
text(115,39,'屏背到PCB间隙：______ mm',9)
text(115,31,'实际端部中心：x____ / y____',9)
c.showPage()
title(2,'屏幕排线核对 · 展开参考')
x,y=35,92;w,h=60.88,94.57
rect(x,y,w,h,'#29658C');text(x+5,y+h-9,'屏幕正面 / 显示侧',10)
# Tail is schematic except the explicitly dimensioned terminal and projection.
line(x+w/2,y,x+w/2,y-42.7,'#777777',[2,2])
rect(x+20.19,y-42.7,20.5,3.5,'#A23B23')
line(x+20.19,y-39.2,x+20.19,y,'#777777',[2,2]);line(x+40.69,y-39.2,x+40.69,y,'#777777',[2,2])
for pin in range(40):
 xx=x+20.19+.5+pin*.5;line(xx,y-42.7,xx,y-39.2,'#A23B23')
text(x+18,y-46,'1',8,'#A23B23');text(x+39.5,y-46,'40',8,'#A23B23')
line(x-5,y,x-5,y-42.7);line(x-7,y,x-3,y);line(x-7,y-42.7,x-3,y-42.7)
text(x-16,y-24,'42.70',8)
line(x,y-51,x+20.19,y-51);text(x+1,y-62,'左边到端子左边20.19',8)
line(x+20.19,y-49,x+40.69,y-49);text(x+20,y-54,'端子宽20.50',8)
text(110,176,'厂家展开图中的1/40脚方向',10)
text(110,169,'仅对应左图观察方向。',9)
text(110,160,'端子间距：0.50 mm',9)
text(110,153,'首末触点中心距：19.50 mm',9)
text(110,146,'排线端厚度：0.30±0.05 mm',9)
text(110,134,'虚线只表示宽度/投影参考，',9)
text(110,127,'不是完整FPC外形，不能裁切成',9)
text(110,120,'最终排线或推断弯曲半径。',9)
text(110,104,'到货后用笔标明金手指裸露面；',9)
text(110,97,'绕到屏背后，重新核对1/40。',9)
text(16,238,'连接器：暂用 FH12A-40S-0.5SH(55)，上接触、40pin、0.5mm。',9)
text(16,231,'闭锁高2.0mm，开启约3.6mm；需先插排线、锁扣，再固定屏幕。',9)
text(16,224,'打印纸不能验证触点接触、折弯寿命或高度干涉；仍需实物试装。',9)
ruler(126,42)
text(16,27,'尺寸依据：用户CL40BC264-40C非触摸规格第6页；本图为重新绘制的核对辅助图。',8)
c.save();print(p)
