# 主控 GPIO 分配草案

目标 ESP32-S3-WROOM-1-N16R8。GPIO 编号不是模组物理脚号。此表与核心图网络对应，外设电路尚未完成。

| GPIO | 网络 | 功能 |
| --- | --- | --- |
| 4 / 5 / 6 / 7 | LCD_D0 / D1 / D2 / D3 | 显示数据低四位 |
| 15 / 16 / 17 / 18 | LCD_D4 / D5 / D6 / D7 | 显示数据高四位 |
| 8 | LCD_WR_N | 显示写时钟 |
| 9 | LCD_DC | 命令/数据 |
| 10 | LCD_CS_N | 显示片选 |
| 21 | LCD_BL_PWM | 背光控制，必须经驱动电路 |
| 11 / 12 / 13 / 14 | SD_MOSI / SD_SCK / SD_MISO / SD_CS_N | microSD 独立 SPI |
| 19 / 20 | USB_DM_MCU / USB_DP_MCU | 原生 USB 下载与调试 |
| 39 / 40 | I2S_BCLK / I2S_WS | 音频共享时钟 |
| 41 / 42 | I2S_DOUT / I2S_DIN | 功放数据 / 麦克风数据 |
| 1 / 2 | I2C_SDA / I2C_SCL | NFC 与 GPIO 扩展器 |
| 47 | NFC_IRQ | NFC 中断 |
| 48 / 38 | IR_TX / IR_RX | 红外发射驱动 / 接收 |
| 43 | IOX_IRQ_N | GPIO 扩展器中断 |
| 44 | PWR_KILL | 电源关闭请求，极性及安全默认态待电源电路确认 |

共使用 29 个 GPIO。GPIO35/36/37 留给 N16R8 的 PSRAM；GPIO0 保留 BOOT 维护入口；GPIO3/45/46 不接外设，避免改变启动配置。GPIO43/44 已用于其他功能，不另提供 UART 调试。

LCD RESET、NFC VEN、功放关闭、SD 卡检测、上/下/确认按钮拟接 GPIO 扩展器；最终扩展器型号与引脚尚未定义。电源按钮需要独立硬件控制，不依赖软件启动才能开机。关机请求不能因 MCU 复位悬空而误动作。

LCD 已选 CL40BC264-40C 非触摸版，8 位并口写入模式：RD 拉高，TE 暂不接，IM0/IM1 拉高、IM2 拉低；详见 [屏幕定义](DISPLAY.md)。I2S 功放与麦克风必须确认时隙、位宽和共享时钟支持。

参考：[Espressif 模组数据手册](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf)。这不是最终网表，也不代表完整电路已验证。
