# Rev A 硬件草稿

当前优先硬件，系统开发暂停。目标为 88 × 125 mm、约 4 英寸非触摸屏、约 2000 mAh 电池、适中机身厚度、首批 2 套，嘉立创 PCB + SMT。¥200/套是目标，不是已确认报价。

## 工程内容

嘉立创 EDA 专业版入口：`eda/Ruri-Passport-RevA/Ruri-Passport-RevA.eprj3`。须保留整个工程目录，不能只复制入口文件。

- `sch/Mainboard/Core.esch2`：ESP32-S3-WROOM-1-N16R8 符号、去耦、EN RC、USB 串联电阻/可选电容和外设网络分配草稿。
- `pcb/Mainboard.epcb2`：板框和文档层机械区域，无元件焊盘、无布线。
- [GPIO 分配](design/PINOUT.md)：独立 USB、SD SPI、LCD 8080 和共享 I2S 时钟方案。

**禁止据此下单。** 核心模组尚未绑定生产封装，电源、USB、屏幕、SD、音频、NFC、红外和按键电路尚未完成。文件结构检查不能替代 ERC、DRC 或实机验证。生成器的坐标与原生编辑器存在兼容问题，已做调整，仍须重新验证连接；通过“打开工程”重新选择完整磁盘路径后，主控图页已在 V4.1.60 中成功显示，先前的找不到文件报错不再阻塞。原理图仍需完整电气检查。

## 屏幕选型

以下是原厂公开规格候选，尚未锁定采购型号、FPC 定义、连接器或背光电路。非触摸版本单独确认，不能用带触摸产品总尺寸直接建封装。

| 候选 | 分辨率 | 显示区 mm | 外形 mm | 接口方向 |
| --- | --- | --- | --- | --- |
| ER-TFT040-1 | 480 × 800 | 51.84 × 86.40 | 57.14 × 96.85 | NT35510，50 pin，核对 8 位 8080 模式 |
| ER-TFT040-5 | 320 × 480 | 55.68 × 83.52 | 60.88 × 94.57 | ILI9488，40 pin，核对 8 位 8080 模式 |

资料：[ER-TFT040-1 原厂规格书](https://www.buydisplay.com/download/manual/ER-TFT040-1_Datasheet.pdf)、[ER-TFT040-5 原厂页面](https://www.buydisplay.com/4-inch-tft-lcd-display-320x480-ili9488-with-optl-touch-panel-screen)。资料核查日期：2026-09-26。完整 PDF 获取尚未成功，页面信息不足以确定生产连接器。两者不保证 IPS。

## 后续必须落实

1. 获取可采购屏幕的完整引脚表、FPC 尺寸和背光参数，再锁定型号。
2. 完成 USB 输入限流、充电电源路径、保护电池与温度检测、3.3 V 升降压、硬件电源按键及强制关机设计。
3. 明确 GPIO 扩展器与复位默认状态，完成三个操作按钮及外设控制。
4. 完成全部外设电路、生产封装和精确 BOM；NFC 天线需结合屏幕/电池金属位置并预留匹配调试。
5. 在原生编辑器确认连接、ERC、PCB 布局布线、DRC、机械检查后，再导出制造文件并询价。

天线、电池与屏幕区域仅为占位，不代表无干涉。板层数仍未完成配置。首批贴片的一次性费用、屏幕、电池、运费及手工组装需要一起核价。

工程模板及部分内嵌基础符号来自 [EasyEDA 官方生成工具](https://github.com/easyeda/easyeda-eprj3-skill)，许可证见 [THIRD_PARTY_LICENSE.txt](THIRD_PARTY_LICENSE.txt)。

## USB 本次补充

R2/R3 暂选 22 Ω，C4/C5 标注 DNP（首批不装），参考 [Espressif USB 硬件指南](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/schematic-checklist.html)。这只是 PHY 周边网络，不是完整 USB-C 接口：连接器、低电容 ESD、CC1/CC2 各自下拉、VBUS 检测与输入限流仍待完成。电池供电时 USB 插拔检测需要单独设计，不能仅凭 D+/D− 可连接就认为 USB 已完工。C4/C5 的 DNP 目前只在图纸文字中标注，导出最终 BOM 时还必须明确排除。
