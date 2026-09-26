# Rev A 制造审核草稿 — 不可直接下单

2026-09-26，嘉立创 EDA Pro 4.1.60 原生导出。全板严格电气 DRC 为 0；原始 Gerber 的若干关键几何已由独立脚本检查。**这不是制造放行或已核价的贴片订单。**

当前草稿为 **`Ruri-Passport-RevA-D4-DFM-DRAFT-20260926.zip`**，20:43导出，已修正红外LED孔径。旧文件 `Ruri-Passport-RevA-DFM-DRAFT-20260926.zip` 保留为历史检查点，孔径已过时，勿混用。新增审核与价格见 [本轮记录](../../review/assembly-quote-20260926.md)。

原创硬件及制造输出采用 CERN-OHL-S-2.0，完整许可证与 NOTICE 随包附带。源文件：<https://github.com/realRurichan/Ruri-Passport/tree/main/hardware>。

## 制造目标

- 88×135 mm，四层，名义板厚1.6 mm，顶面装配，绿色阻焊。
- 层序：Top / Inner1（GND参考）/ Inner2 / Bottom。
- EDA 已采用内置 `JLC04161H-7628`：外铜0.035 mm，内铜0.0152 mm，两侧介质各0.2104 mm，芯板介质1.065 mm。铜及介质合计1.5862 mm，不含最终表面处理/阻焊公差。
- 此参数与 [JLCPCB 公布的7628结构](https://jlcpcb.com/impedance)一致；国内订单仍须选择/确认对应叠层，不能据此声称已订购阻抗控制。

## 必须关闭的制造事项

1. J2 GCT USB4105 定位孔到铜名义0.1751 mm，低于嘉立创常规0.20 mm要求；需要针对生产稿的接受记录或经装配尺寸验证的封装修订。
2. GCT短脚PTH、钢网锡量及具体国内SMT可供料号待核准。当前ZIP不含已批准的装配BOM/CPL，不能直接用于全机贴。
3. 屏幕FPC标准折回端部与当前J1位置存在偏差，必须解决；电池/扬声器/壳体高度及D4出光方向尚待机械验证。D4孔径已修正为3.3mm。
4. 3V18新支路77.508 mm、宽0.40 mm。按内置叠层铜厚估算仅该段20°C电阻约0.1584Ω，0.60A压降约95mV，未含旧线、过孔、温升和瞬态；需结合完整供电路径与样板测试签核。
5. 全套准确BOM、额定值/降额及国内SMT供料价格尚未完成；初轮自动候选报价已明显超过¥200/套，且发现R22错配，不能采购。
6. U3散热过孔需调整跨过热焊盘区域的走线后补齐；J3的2A额定值与满负载设计额度不一致。

## 文件注意

`Drill_PTH_Through.DRL` 已包含过孔；`Drill_PTH_Through_Via.DRL` 是与其重叠的过孔参考集，CAM不可重复加工。`Drill_NPTH_Through.DRL` 含7个孔：4个M2固定孔、2个USB定位孔、1个麦克风声孔。新版另有D4封装的Ø3.3 mm圆形挖空在GKO中表达，中心(82,127) mm。

`native-bom.csv` 是EDA原生UTF-16制表符分隔输出（65组、142装配位），不代表料号已核准；`native-cpl.xlsx` 是161行原始坐标，包含19个非装配位。制造前必须按已批准BOM筛掉ANT1、C4/C5/C48–C51、R64/R65、TP1–TP10；不能仅凭文件名上传全贴。

`Gerber_DocumentLayer.GDL` 为参考标注，不能当成额外铜层或实际切割轮廓。实际板框使用GKO，铜层为GTL/G1/G2/GBL。

检查记录：`hardware/review/gerber-draft-check.json`、`drc-routed-poured.json`、`usb-footprint-correction-20260926.md`。独立脚本只核对列出的关键几何，未替代完整CAM/DFM检查。

新版记录：`hardware/review/gerber-d4-draft-check.json`、`drc-d4-hole-correction.json`。旧检查JSON的SHA仅对应旧ZIP。
