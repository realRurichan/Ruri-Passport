# Rev A 硬件工程

当前优先硬件，系统开发暂停。用户已接受 **88 × 135 mm** PCB，为约4英寸非触摸屏、五向键和两组板载天线留出空间。约2000mAh保护电池，首批2套，嘉立创全机贴。¥200/套仍是目标，尚无完整报价。

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

PCB已导入全部161个元件/测试点，88×135mm板框和4个可用铜层已从原生客户端读回确认。已完成第一轮元件摆放，四匝 NFC 铜线圈及局部桥接已画入，并添加四层铜箔禁布规则。整板首轮自动布线正在处理，尚未完成关键走线和制造检查。

## 未通过制造放行

仍需完成天线馈线与整板布线、准确料号及国内SMT供料核价、电源和射频元件额定值核查、屏幕FPC折弯/上接触座装配验证、整机金属与天线净空、原生DRC和独立Gerber检查。不能据此下单。

NFC匹配值、晶体负载和背光补偿均为样板调试起点，需整机实测。已有卡兼容性取决于协议与应用，不能保证任意卡可模拟。

设计依据：[GPIO](design/PINOUT.md)、[屏幕](design/DISPLAY.md)、[电源](design/POWER.md)、[NFC](design/NFC.md)、[机械布局](design/MECHANICAL.md)。检查记录在review目录，生成与核对工具在tools目录。模板与部分基础符号源自[EasyEDA官方生成工具](https://github.com/easyeda/easyeda-eprj3-skill)，许可证见[THIRD_PARTY_LICENSE.txt](THIRD_PARTY_LICENSE.txt)。
