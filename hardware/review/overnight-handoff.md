# 夜间继续工作交接（2026-09-27）

## 用户授权和目标

用户去睡觉，明确要求继续工作，完成国产/基础库优先降本选型，再画好 PCB、注意信号、去除“阑尾线”，明早希望看到成品与两套贴片报价。允许推送 realRurichan/Ruri-Passport；不购买/付款/发消息。五向键独立 GPIO、屏幕接受 SPI，硬关机保留瞬时按键，约 88×135mm，屏幕 CL40BC264-40C 非触屏 ILI9488/40pin上接，NFC读写+卡模拟、BLE/Wi-Fi、SD、麦克风/扬声器、电池约2000mAh、外壳固定孔。屏幕33.95元/块。两套全嘉立创贴片，预算希望200/套，但历史报价大幅超出。

已创建当前任务 heartbeat `passport-pcb`，每30分钟继续；只在完成/需用户/无法继续时通知，完成后暂停。用户要求1m上下文，已明确说明无法在对话中自行开启。无需重问用户。

## 当前成果与不能声称完成的地方

- 原理图 SPI / 5 keys direct GPIO / NFC VEN direct GPIO 已保存。
- 按键硬关机已在原理图新增 U10 LTC2954-1、Q10–Q15、C60–C63、R70–R76。详见 POWER.md，GPIO21=PWR_KILL，GPIO18=PWR_INT_N。
- U2 剩余未用 P00/P01/P02/P03/P04/P06/P11 已各加 R77–83 10k 下拉。当前 Supplier Part=C25804、MPN0603WAF1002T5E、显示10k，但 Device 来源仍是100k，需真正器件标准化/重新绑定，不能忽略采购属性警告。
- 25个新增元件已补唯一ID gge200001..gge200025 和 R/C 显示值。
- 最新 epro 在 hardware/eda/Ruri-Passport-RevA.epro，原生工程同步保存。`check_export_pin_geometry.py` 检查187位号/413引脚/0不匹配，36个有意未连接脚。这是辅助几何检查，不是原生网表，不等于全电路正确。
- 原生 DRC 0 fatal/0 errors/603 warnings。已通过UI导出完整明细：599个超出图框、2行采购属性不匹配、2行未放NC标记。日志见 schematic-drc-20260927.txt。必须整理图框、标注NC、修正属性。不是603个断线错误。
- 原理图采用大量命名导线，需要提升可读性，地脚电气上接GND，但部分没有可见地符号。默认sch_create_net_flag返回获取器件详情失败，不要假称已放地符号。
- **PCB 仍是旧版，未同步重布；manufacturing/latest 已标STALE，禁止下单。**不能把旧0 DRC说成当前板通过。
- 国产替换还没落实：BQ24074/TPS63802/TPS22919/MAX98357A/PN7160/TLV仍原器件。LTC2954 C683779为外国扩展例外，查询价25.37/颗，库存5，不是实时报价。SGM851搜索库存0；不要用不明用户自制库来冒充现货。
- 旧两套预报价见 assembly-quote-round2-20260926.md：历史已知约669.44/套且有缺项，已过时，不能宣称已降到200。

## 下一步优先级

1. 完成器件标准化（特别 R77–83 的 Device100k / MPN10k 不一致），给36个允许NC加原理图标记，修正图框/文本，导出原生网表验证413+引脚，不要只依赖几何。
2. 完成国产替代和成本取舍：充电/功放/升降压/负载开关/背光运放，优先降低扩展物料种类与贵电感。已保存的厂家手册依据见ground-and-nc/POWER和此前review。任何替换核对实际封装pin，不凭“兼容”猜测。
3. 硬关机重点：USB D+/D-断电倒灌、主电源软启动在LTC2954 400–650ms屏蔽内建立KILL上拉、并联PMOS温升与浪涌、关机BQ24074 EN1/2默认USB100mA的充电限制；确认不需要更简单便宜且可靠的电源保持方案。
4. 器件冻结后同步PCB再布线：删旧并口/按键绕线，去真正无连接stub而不误删天线、调试分支。USB差分连续地、SPI/SD时钟短/远离RF、I2S回流、电源热环、NFC匹配对称和天线净空、屏幕及按键间距、固定孔禁布。保留88×135和已确认机械约束。
5. 原生ERC/DRC、网表/封装引脚/生产包一致性通过后才导出新Gerber/BOM/CPL/epro，重新平台两套报价（不能购买）。明确裸板/SMT/物料/屏幕/电池/喇叭/未包含费用。

## 工具恢复与安全注意

本轮 EasyEDA tools 不在 ALL_TOOLS 中，但现有授权桥可用。安装目录 `/Users/ruri/.local/share/ruri-easyeda-mcp/dist` 只有编译产物。通过 `node .../dist/mcp-server/index.js`（require_escalated）恢复 daemon，extensionConnected=true。Socket `/Users/ruri/.easyeda-mcp/bridge.sock`，instance 5bfc5945。

临时 CLI `/private/tmp/ruri_eda_call.py <tool> '<json args>'` 使用已安装桥的 call_tool 协议；连接socket需要require_escalated，已审核允许。工具定义 `/private/tmp/ruri-eda-tools.json`（list_tools），不要猜接口。该CLI仅正常调用同一个已授权桥，不做未校验整页覆盖。server_info可确认连接。

本轮恢复后native调用很快；此前 sch_get_netlist/getAll/getPins 因内嵌netlist耗时曾超时，若再遇到应UI导出。旧文档整体validate=off导入曾遭自动审批拒绝，理由是已发现9条无效记录；**不要绕过校验导入**。document_validate对epro数组片段返回docType unknown/skipped，不算验证通过。优先原生编辑或正确修复schema。

文档UUID：Controls085b953d8ef47397、Power837fc436d9c95e8a、Corebee18976220fde0b、Displayad993e34b1635da7、AudioStoragec835b5e8e87752a8、Optics4908a31efcd07cbd、NFCaaef88a6bc1a8f4f、RF146936d1992206fb、PCB2de8d5754015f9ac。

CUA app路径 `/Applications/嘉立创EDA(专业版).app`（bundle id有DMG同名歧义）。当前原理图DRC面板。可UI导出警告/网表。会话若压缩先rewriteDocumentation；若新会话getApp。不要用非CUA技术操作UI。

新原生文件都是对象NDJSON，.epro里面是数组NDJSON；完整.epro要保留symbols/instances/footprints。不要因SHEET ATTR Footprint=null认为无封装，旧元件也是这样，映射可能在INSTANCE。

最近无运行的编辑脚本；当前新epro已导出。临时脚本 ruri_bias_fix.py 是一次性创建，**不可重复运行**。ruri-newparts-identifiers.py 已跑完，不必重跑。改动保存在仓库；每轮先git status检查。
