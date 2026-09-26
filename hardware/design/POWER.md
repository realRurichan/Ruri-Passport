# 按键硬关机电源方案（原理图检查点）

用户已选择保留瞬时电源按键、采用电源保持与物理断电。当前原理图已加入以下电路；PCB 尚未同步，不能使用旧 Gerber 打样。国产替代选型仍在进行。

## 电源路径

- J3：有保护板的单节 4.2V 满充锂电池，约 2000mAh；XH 2.50mm 三针，1=VBAT、2=10kΩ NTC、3=GND。插头极性必须核对。
- BQ24074 的 VSYS 保持充电与电源路径功能，供电源按键控制器 U10。
- Q12/Q13 两个 AO3401A 并联作为高边开关，切断 VSYS→VSYS_RUN。Q11 受 U10 的 PWR_EN 控制，经 R73 驱动栅极，R74 默认关闭，C63 控制开通过程。并联不等于已通过温升/浪涌验证。
- VSYS_RUN 供主升降压输入/使能、背光 LED、红外发射 LED。3V18 及 3V18_PERIPH 均在主开关之后。
- Q14/Q15 同时切断 VBAT 到电池 ADC 分压上端的路径，降低电池测量支路给断电主控倒灌的风险。R44=1MΩ、R45=330kΩ、C23=100nF 保留。

## 按键和关机

U10 暂选 LTC2954CDDB-1#TRPBF / C683779（DFN8+EP）。这是外国扩展库例外，前次查询约 25.37 元/颗、仅 5 颗库存；不是已锁定报价或已采购。国产候选尚未确认同时满足功能、库存及封装要求，继续降本核对。

SW6 接 PWR_BUTTON_N→U10 PB；不再直接接 MCU 输入。U10 INT# 经 PWR_INT_N 接 GPIO18。GPIO21 为 PWR_KILL，高电平经 Q10 拉低 U10 KILL#，请求物理断电。KILL# 由主电源 3V18 上拉，利用控制器启动屏蔽时间建立保持；必须验证升压启动、软启动和负载浪涌能在屏蔽窗口内完成。

C61=100nF 的标称开机按压时间约 0.67s；C62=1µF 的长按强制关机时间约 6.46s。这是按手册公式计算的目标，不是样机实测。强制关机不等待文件系统，可能丢失 SD 未写完的数据。

正常关机固件先停止新写入、flush/unmount SD、停止音频与屏幕，再置 PWR_KILL。外设单独断电时，仍需把跨电源域信号设为低电平或无上拉高阻。电源控制器和充电电路保持极小电流工作，因此硬关机并非电池零耗电。

## 待解决/验证

- USB D+/D− 在主电源关闭时的反向供电路径与插拔状态；不能仅依据供电开关断开宣称所有状态均完全断电。
- 上电保持窗口、PMOS 栅极 RC、主电源浪涌、并联 MOS 电流与温升、开关节点回流。
- BQ24074 EN1/EN2 默认下拉组合在关机时选择 USB 100mA 输入限流，关机充电可能较慢；换国产充电芯片时重新设计。
- 新增器件的完整属性、PCB 封装/焊盘编号和生产 BOM 一致性。
- 国产替代、实时库存和两套 SMT 总价。

## 原厂资料

- [ADI LTC2954：DFN 引脚、保持/中断、长按定时](https://www.analog.com/media/en/technical-documentation/data-sheets/2954fb.pdf)
- [AOS AO3401A：G/S/D、导通电阻与额定条件](https://www.aosmd.com/sites/default/files/res/datasheets/AO3401A.pdf)
- [TI BQ24074：电源路径和输入限流](https://www.ti.com/lit/ds/symlink/bq24074.pdf)
- [TI TPS63802](https://www.ti.com/lit/ds/symlink/tps63802.pdf)
- [TI TPS22919](https://www.ti.com/lit/ds/symlink/tps22919.pdf)
