# 原理图接地与未连接引脚复核（2026-09-27）

状态：原理图阶段检查点，**不是生产放行**。PCB 尚未同步 SPI、独立五向键和硬关机修改；旧 Gerber/BOM/CPL 不可用于当前方案。几何检查不能代替 EDA 原生网表、ERC、PCB DRC 和样机验证。

## 已修复

五向键迁至 ESP32 独立 GPIO 后，U2（TCA9535）的 P00/P01/P02/P03/P04/P06/P11 留下未驱动输入。TI 明确说明该器件不带内部上拉，未使用输入应通过约 10kΩ 电阻接 VCC 或 GND。现已给 U2.4/5/6/7/8/10/14 分别增加 R77–R83、10kΩ 下拉到 GND，采购标识为 UNI-ROYAL 0603WAF1002T5E / C25804，复用基础库料。五向键本身仍直接接 ESP32。

依据：[TI TCA9535 数据手册，Pin Functions 表脚注，p4](https://www.ti.com/lit/ds/symlink/tca9535.pdf)。新增电阻的原始库 Device 仍源于相同封装的 100k 器件；显示名称、制造商型号及采购料号已改为 10k。在最终 BOM 导出前，必须重新绑定为 C25804 并核对器件属性一致性，不能仅凭显示文本放行。

## 接地核对

此次导出几何检查覆盖以下地脚和电源保持电路地脚，均连接 GND：

| 器件 | 接地引脚 |
|---|---|
| ESP32-S3 U1 | 1、40、41（EPAD） |
| TCA9535 U2 | 12；地址选择 2、3、21 也接地 |
| BQ24074 U3 | 8、17（EP）；4 为使能配置接地 |
| 主稳压 U4 | 3、8 |
| 外设负载开关 U5 | 2 |
| MAX98357A U7 | 3、11、15、17（EP）；2 为增益配置接地 |
| PN7160 U8 | 4、9、20、41（EP）；1、3、39 为配置接地 |
| 背光运放 U9 | 2 |
| LTC2954 U10 | 1、9（EP） |
| Q10、Q11、Q15 | 2（小信号 NMOS 源极） |

只证明原理图有对应 GND 网络。PCB 地平面连续性、裸焊盘实际铺铜/过孔、开关电源和射频回流仍需单独检查。

## 明确保留未连接的脚

| 器件与脚号 | 处理原因与依据 |
|---|---|
| U7.5/6/12/13 | MAX98357A TQFN 的 NC；EP 必须另接地，不能与 NC 混淆。[ADI 手册 p15](https://www.analog.com/media/en/technical-documentation/data-sheets/max98357a-max98357b.pdf) |
| U5.4 | TPS22919 的 NC，厂家要求悬空。[TI Pin Functions](https://www.ti.com/lit/ds/symlink/tps22919.pdf) |
| U3.14/15 | BQ24074 TMR/ITERM 悬空选择厂家默认定时和终止电流；是有意配置，并非漏连。[TI 手册](https://www.ti.com/lit/ds/symlink/bq24074.pdf) |
| U8.11/38 | PN7160 **HVQFN40** 的 i.c. 保留脚须悬空，不能套用 BGA 封装的接地要求。[NXP Pin description](https://www.nxp.com/docs/en/data-sheet/PN7160_PN7161.pdf) |
| U8.32–36 | NC；保留悬空。依据同上。 |
| U8.37/40 | 未使用的 DCDC_EN、CLK_REQ 输出，悬空；当前采用固定供电与晶体。 |
| U8.23/24/25 | ANT1/ANT2/VDD_HF，当前不采用关机 RF 场唤醒；最终 NFC 复核须再对照 [AN12988](https://www.nxp.com/docs/en/application-note/AN12988.pdf) 对应配置图。 |
| U1.28/29/30 | N16R8 模组的 GPIO35/36/37 被模组内部 Octal PSRAM 占用，外部不能占用或接地。[乐鑫模组手册 Pin Definitions 脚注](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf) |
| U1.15/16/26 | 未使用的 GPIO3/46/45 启动配置相关脚；保留模组默认配置，固件需处理未使用 GPIO，不能盲目接地。 |
| J1.1–4 | 非触摸版本不使用触摸引脚。 |
| J1.8/14 | FMARK 和 SPI SDO 输出未使用，允许不接；不是输入。屏幕接线依据厂家 CL40BC264-40C 规格和接线图。 |
| J2.A8/B8 | USB-C SBU，USB 2.0 设备不使用。 |
| D7.2 | 未使用的第二路 ESD 通道；最终物料核对需确认实际采购件内部拓扑。 |
| Y1.2/4 | 晶体封装 NC；最终复核必须对照实际采购晶体引脚图，不能因常见四脚晶体习惯就接地。 |

## 检查记录与未完成项

`pin-geometry-20260927.json`：从 EDA 最新导出检查 187 个带位号元件、413 条预期引脚连接，0 个不匹配，36 个未接脚已列出。ZIP CRC 通过。预期值来自现有厂家引脚表及这次 SPI/按键/硬关机修改。

尚未完成：最新原生网表检查、全部 ERC 警告审核、国产替代最终确定、新增器件库属性规范化、硬关机 USB 数据线倒灌验证、PCB 同步重布与生产一致性验证。不要把“0 个几何不匹配”解释为电路完全正确。
