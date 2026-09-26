# Rev A 硬件工程

原创硬件设计采用 **[CERN-OHL-S-2.0](LICENSE)**。Copyright (c) 2026 Ruri Passport contributors。源文件地址：https://github.com/realRurichan/Ruri-Passport 。许可范围、第三方材料与无担保声明见 [NOTICE.md](NOTICE.md)。

当前优先硬件，系统开发暂停。用户已接受 **88 × 135 mm** PCB，为约4英寸非触摸屏、五向键和两组板载天线留出空间。约2000mAh保护电池，首批2套，嘉立创全机贴。¥200/套仍是目标，第二轮预报价约 ¥679.92/套，尚未包含全部配件，且早于 XH 电池座变更。

嘉立创EDA专业版入口：[Ruri-Passport-RevA.eprj3](eda/Ruri-Passport-RevA/Ruri-Passport-RevA.eprj3)。须保留整个工程目录，原理图和封装库内嵌在各文档中。

## 已画入工程

| 图页 | 内容 |
| --- | --- |
| Core | ESP32-S3-WROOM-1-N16R8、去耦、EN RC、USB PHY外围 |
| Display | CL40BC264-40C非触摸屏、40pin上接触座候选、8080 8位接口 |
| Controls | TCA9535、五向键、外设使能与默认上下拉 |
| Power | USB-C、BQ24074电源路径、TPS63802升降压、TPS22919外设开关、软关机键 |
| Audio_Storage | microSD、MAX98357A、SPH0645、扬声器座、电池ADC、USB/SD保护 |
| Optics | 940nm红外发射、38kHz接收、TLV9001与AO3400A背光电流控制 |
| NFC | PN7160、27.12MHz晶体、去耦、Type 4卡模拟约束 |
| RF_Service | NFC匹配与可选接收取样、SD/VBUS补充保护、维护测试点 |

2026-09-26原生网表：161个元件/测试点，350项针脚网络断言通过；DNP、裸测试点和PCB天线已排除在装配BOM外。这只是连接核对，不等于完整ERC、DRC或性能验证。

PCB已导入全部161个元件/测试点，88×135mm板框和4个可用铜层已从原生客户端读回确认。四匝 NFC 铜线圈、局部桥接和馈线已画入，并添加四层铜箔禁布规则。全板网络已接通，顶层/内层1/底层 GND 铺铜已重建保存，2026-09-26 原生严格 DRC 为 **0 错误**，见 [检查结果](review/battery-connector-xh-20260926.json)。这是电气布线检查通过，制造检查尚未完成。

已加入4个 M2 固定孔（Ø2.2mm）及四铜层 Ø5.2mm 螺柱避让区，原生客户端读回和元件包络初筛通过。后壳预留扬声器空间及麦克风声孔；具体扬声器、电池及外壳高度仍待机械确认。参考图：[PNG](mechanical/mounting-reference.png)、[SVG](mechanical/mounting-reference.svg)、[1:1 mm DXF](mechanical/mounting-reference.dxf)。

五向键已下移：最上方开关本体与屏幕外框之间约4.95mm，十字排列中心距7mm。OK开关旋转90°以留出焊盘间距；元件包络初筛无重叠。该间隙按开关本体计算，外壳键帽尺寸还需配合这一留白。

已应用原生 `JLC04161H-7628` 四层物理叠层。Gerber、钻孔及许可文件见 [制造审核草稿](manufacturing/latest/README.md)；关键导出几何检查通过，草稿尚未放行，不可直接下单。

## 未通过制造放行

最新 [第二轮贴片预报价](review/assembly-quote-round2-20260926.md)：两套 SMT 含物料约 ¥1099.14，沿用五片裸板和两块 ¥33.95 屏幕后约 ¥679.92/套，仍缺电池、扬声器、外壳等费用。报价早于 XH 电池座变更，需重新核价。J1 屏幕座已匹配 C506795；J3 已换成 XH 2.50 mm / 3 A（22 AWG 条件），原理图和 PCB 同步，配套 XHP-3 插头。U3 热过孔和飞线已修复，严格 DRC 为 0。电池候选与采购条件见 [BATTERY.md](design/BATTERY.md)，尚未采购。

USB插座封装已按GCT图修正，但定位孔到铜的名义0.1751mm仍需嘉立创DFM确认。其余待办包括关键走线/回流路径与电源额定值核查、准确料号及国内SMT供料核价、屏幕FPC折弯/上接触座装配验证、整机金属与天线净空、独立Gerber/钻孔检查。不能仅凭DRC为0就下单。

NFC匹配值、晶体负载和背光补偿均为样板调试起点，需整机实测。已有卡兼容性取决于协议与应用，不能保证任意卡可模拟。

设计依据：[GPIO](design/PINOUT.md)、[屏幕](design/DISPLAY.md)、[电源](design/POWER.md)、[NFC](design/NFC.md)、[机械布局](design/MECHANICAL.md)。检查记录在review目录，生成与核对工具在tools目录。模板与部分基础符号源自[EasyEDA官方生成工具](https://github.com/easyeda/easyeda-eprj3-skill)，许可证见[THIRD_PARTY_LICENSE.txt](THIRD_PARTY_LICENSE.txt)。

选型硬约束：[全量基础库优先，非必要不用扩展料](design/SOURCING.md)。当前基础库优化尚未完成，扩展料例外必须逐项论证。

最新制造检查点：[最新 Gerber / BOM / CPL](manufacturing/latest/README.md)，严格 DRC 0 错误，尚待装配及采购放行。
