# 主控 GPIO 分配草案

目标 ESP32-S3-WROOM-1-N16R8。GPIO 编号不是模组物理脚号。此表与 2026-09-26 客户端原理图网络对应；PCB 已同步元件和网络，重新布线及 DRC 尚未完成。自定义符号内部旧功能别名尚待整理。

| GPIO | 网络 | 功能 |
| --- | --- | --- |
| 4 / 5 / 6 / 7 / 15 | KEY_UP_N / KEY_DOWN_N / KEY_LEFT_N / KEY_RIGHT_N / KEY_OK_N | 五向键独立输入，低有效，支持同时按键 |
| 16 | LCD_MOSI | 屏幕 SPI 写数据 |
| 17 | NFC_VEN | NFC 直接使能控制 |
| 18 | PWR_INT_N | LTC2954 INT#，电源按键事件输入 |
| 8 | LCD_SCK | 屏幕 SPI 时钟 |
| 9 | LCD_DC | 命令/数据 |
| 10 | LCD_CS_N | 显示片选 |
| 43 | LCD_BL_PWM | 背光控制，必须经驱动电路 |
| 11 / 12 / 13 / 14 | SD_MOSI / SD_SCK / SD_MISO / SD_CS_N | microSD 独立 SPI |
| 19 / 20 | USB_DM_MCU / USB_DP_MCU | 原生 USB 下载与调试 |
| 39 / 40 | I2S_BCLK / I2S_WS | 音频共享时钟 |
| 41 / 42 | I2S_DOUT / I2S_DIN | 功放数据 / 麦克风数据 |
| 44 / 2 | I2C_SDA / I2C_SCL | NFC 与 GPIO 扩展器 |
| 47 | NFC_IRQ | NFC 中断 |
| 48 / 38 | IR_TX / IR_RX | 红外发射驱动 / 接收 |
| 21 | PWR_KILL_N | 开漏拉低请求 LTC2954 切断主电源；正常运行高阻 |
| 1 | VBAT_SENSE | ADC1 电池电压，1M/330k 分压 |

共使用 29 个 GPIO。GPIO35/36/37 留给 N16R8 的 PSRAM；GPIO0 保留 BOOT 维护入口；GPIO3/45/46 不接外设，避免改变启动配置。GPIO43/44 已用于其他功能，不另提供 UART 调试。

LCD RESET、功放使能、SD 卡检测和充电控制暂时仍接 XL9535。五向键和 NFC VEN 直接接 ESP32；电源键 SW6 接 LTC2954 PB，控制器 INT# 接 GPIO18。GPIO21 改为 PWR_KILL_N（开漏拉低关机），不再接扩展器中断。U2 未使用的 P00/P01/P02/P03/P04/P06/P11 各用 10kΩ 下拉；扩展器仍服务于其它外设，尚未完全删除。P16=PERIPH_ENABLE、P17=REG_PWM。2026-09-27 已按用户选择加入按键硬关机原理图，参见 [电源策略](POWER.md)。PCB 已同步元件和网络，重新布线及 DRC 尚未完成。
