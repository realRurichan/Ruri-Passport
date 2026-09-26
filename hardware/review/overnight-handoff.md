# 夜间继续工作交接（2026-09-27）

## 用户授权和目标

用户去睡觉，明确要求继续工作，完成国产/基础库优先降本选型，再画好 PCB、注意信号、去除“阑尾线”，明早希望看到成品与两套贴片报价。允许推送 realRurichan/Ruri-Passport；不购买/付款/发消息。五向键独立 GPIO、屏幕接受 SPI，硬关机保留瞬时按键，约 88×135mm，屏幕 CL40BC264-40C 非触屏 ILI9488/40pin上接，NFC读写+卡模拟、BLE/Wi-Fi、SD、麦克风/扬声器、电池约2000mAh、外壳固定孔。屏幕33.95元/块。两套全嘉立创贴片，预算希望200/套，但历史报价大幅超出。

已创建当前任务 heartbeat `passport-pcb`，每30分钟继续；只在完成/需用户/无法继续时通知，完成后暂停。用户要求1m上下文，已明确说明无法在对话中自行开启。无需重问用户。

## 当前成果与不能声称完成的地方

- 原理图 SPI / 5 keys direct GPIO / NFC VEN direct GPIO 已保存。
- 按键硬关机已在原理图新增 U10 LTC2954-1、Q10–Q15、C60–C63、R70–R76。详见 POWER.md，GPIO21=PWR_KILL，GPIO18=PWR_INT_N。
- U2 剩余未用 P00/P01/P02/P03/P04/P06/P11 已各加 R77–83 10k 下拉。已实际重新绑定 C25804 库器件，MPN0603WAF1002T5E；最新采购属性警告已不包含这七颗电阻。
- 25个新增元件已补唯一ID gge200001..gge200025 和 R/C 显示值。
- 最新 epro 在 hardware/eda/Ruri-Passport-RevA.epro，原生工程同步保存。`check_export_pin_geometry.py` 检查187位号/413引脚/0不匹配，36个有意未连接脚。这是辅助几何检查，不是原生网表，不等于全电路正确。
- 原生 DRC 最新 0 fatal/0 errors/4 warnings（2026-09-27 00:35）。六页内容平移到扩大的图框内，599条越界已消除。此前603条已过时。已通过UI导出完整明细：599个超出图框、2行采购属性不匹配、2行未放NC标记。日志见 schematic-drc-20260927.txt。必须整理图框、标注NC、修正属性。不是603个断线错误。
- 原理图采用大量命名导线，需要提升可读性，地脚电气上接GND，但部分没有可见地符号。默认sch_create_net_flag返回获取器件详情失败，不要假称已放地符号。
- **PCB 仍是旧版，未同步重布；manufacturing/latest 已标STALE，禁止下单。**不能把旧0 DRC说成当前板通过。
- 国产替换还没落实：BQ24074/TPS63802/TPS22919/MAX98357A/PN7160/TLV仍原器件。LTC2954 C683779为外国扩展例外，查询价25.37/颗，库存5，不是实时报价。SGM851搜索库存0；不要用不明用户自制库来冒充现货。
- 旧两套预报价见 assembly-quote-round2-20260926.md：历史已知约669.44/套且有缺项，已过时，不能宣称已降到200。

## 下一步优先级

1. 完成其余器件标准化（R77–83 已完成真实库重绑），给36个允许NC加原理图标记，修正图框/文本，导出原生网表验证413+引脚，不要只依赖几何。
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

## 立即继续轮次更新

- 新桥实例95eed76e，APP绑定edaApp3。
- 明确 fileType=epro 导出成功；默认不指定会得到 epro2。
- 通过 UI 导出原生网表到 review/schematic-current.enet：187元件，413引脚连接，0错误；几何检查同样413项通过。sch_get_netlist API仍45秒超时，UI导出可用。
- Controls/Power/Display/AudioStorage/NFC/Optics整体移入正坐标图框，旧坐标不可再用于编辑；元件ID和连接未变。
- 新DRC明细已更新，四条是两条采购属性汇总及两条NC汇总。显示值属性为空仍需补。

## 国产与硬关机简化（00:59继续）

- U2已修改项目器件定义为XL9535/C561273，保留逐脚核对的项目符号与TSSOP24封装。国内页面VERIFIED ¥3.28/颗、库存5169，扩展库。详见 domestic-cost-20260927.md。
- C3/C9/C15/C16采购定义改为C15849（1uF50VX5R基础库），与C62共用；其余25个实例规范了厂家参数。SW1..5和J1随后也刷新精确厂家属性，封装没动。
- Q10和R71已删除，附属5组局部导线也删除；GPIO21现在PWR_KILL_N开漏拉低关机。check_native_netlist.py期望已修改为408项，185元件。
- 新native .enet（/private/tmp/ruri-schematic-cost-v2.enet）连接408项全部通过，但C4/C49 DNP出现错误，已定位：原生文件追加记录前缺少上一条末尾 | 会导致上一条属性和新第一条NC不被读取。这是序列化问题，不能忽略。已将所有非空记录补终止符，保留||| tombstone原样；待再次冷启动导出验证。
- 36个NC全部已写，含Y1.2/4（NXP AN14518 Table9明确），U8.23/24/25（AN12988 Fig1目视）。上轮有U1.15和D7.2未生效，同属缺分隔符问题，已修复待验证。
- CUA当前app刚启动绑定edaApp6，需单击最近工程、取消网络拖动设置、展开Mainboard后打开Controls，再Claude→ConnectClaude。旧桥f7597fc7已失效。
- epro仍是上一检查点（32个生效NC、DNP两处待修复），必须重新export fileType=epro并UI导出native enet再保存到review。尚未commit当前轮次。
- 原生文件编辑应先保存退出+server_info=0，备份zip后只改已观察格式；不要重跑旧脚本（有不可重复操作/过时选择）。
- /private/tmp/ruri-sourcing-update.py 使用项目自有Symbol/Footprint，仅采购与电气参数取完整真实库数据，不可把外部Symbol UUID直接写入项目而不嵌入库。
- 重要：旧PCB和Gerber还是STALE，尚未同步新硬关机、SPI及GPIO布线。

## 01:22 本轮最新进展（优先于上文）

- 冷启动分隔符修复已通过：185 元件、408 项原生 ENET/几何检查均 0 错误，36 NC 正常生效，C4/C49 DNP 正常。原生网表已更新至 review/schematic-current.enet。
- 原理图原生 DRC 0 fatal/0 errors/1 warning：仅 U2 采购属性；J1 MP1/MP2 为机械焊盘信息。U2 MPN/供应商已 XL9535/C561273，但 ENET DeviceName 仍旧 TCA9535，须继续修正不能假称已完全标准化。
- PCB 已通过原生 pcb_import_changes 同步，取消了“同时更新导线网络”防止拓扑变更时误改旧线。185 元件。23 个新增元件已放入板内；R77..83 最终 x=37mm，y=29..38mm 间隔1.5mm。
- 删除 401 段失效并口/按键/使能/VSYS旧线和96过孔；另删除新增布局下12段冲突旧线与2过孔。保留所有元件、机械位置及主要未改网络。铺铜已重建一次；后续仍需重建和检查。
- 源工程及 epro 已保存，但仍非成品。制造包继续 STALE。
- 用户明确要求“补新线路用freerouting”。已导出 /private/tmp/ruri-hardoff-raw.dsn，prepare_routing.py 新增 --no-seeds（避免重复历史种子），更新 VSYS_RUN 0.8mm 主电源宽度。处理后 /private/tmp/ruri-hardoff-incremental.dsn 含115网络类、Inner1 power平面、板边及16固定孔/天线障碍。
- FreeRouting 1.9.0 正在单线程补线：exec session 9571，命令 java -Xmx4g -Xss16m -jar /private/tmp/ruri-freerouting-1.9.0.jar -de /private/tmp/ruri-hardoff-incremental.dsn -do /private/tmp/ruri-hardoff-incremental.ses -mp 30 -mt 1 -da。日志同名前缀.log。首次 -mt 2 因软件提示存在已知间距问题已中止，勿再次用多线程优化。
- 当前桥 4c70dc4e，CUA edaApp6，EDA 保持打开。不得并行修改 EDA 或运行第二个路由。需要等待 SES、核对其保留线路/新线路，然后原生导入、重建铺铜并 DRC。不要用旧 import_routing.py 直接覆盖，它假设旧manifest与fresh routing，不适用于当前增量文件。
- PCB 同步前全备份 /private/tmp/ruri-before-pcb-sync-20260927.zip，导出前线/孔列表 /private/tmp/ruri-pcb-sync-*.json。最新清理前DRC /private/tmp/ruri-pcb-preroute-drc.json，44间距/103连接错误；44是清理前值，不能说清理后已无间距错误。

## 用户最新布线决定

用户要求 FreeRouting 从头铺线，弃用增量补线。session9571已中止。185元件边界/焊盘/包络保守检查0发现；R30最终(56,35)mm。保留板框、机械、元件布局和NFC线圈本体，清旧信号/电源线路后全新路由；须更新SES导入策略避免新旧叠加。

### 01:26 全新 FreeRouting 正在运行

增量结果未导入。按用户最终指示又清除2000段剩余旧线、271过孔，仅保留ANT_A/ANT_B共17段天线馈线与3过孔以及ANT1线圈本体。完整备份 /private/tmp/ruri-before-full-reroute.zip。干净原生PCB已保存。原始DSN /private/tmp/ruri-hardoff-fresh-raw.dsn；处理DSN /private/tmp/ruri-hardoff-fresh.dsn；结果目标 /private/tmp/ruri-hardoff-fresh.ses；日志 /private/tmp/ruri-hardoff-fresh.log。正在运行exec session88950，-mp30 -mt1 -da。不要再启动第二路由或改布局；等待当前结果。原生pcb_import format=autoroute_ses可用，需导入前备份、导入后检查重复线路/天线保持/间距/连接。旧import_routing.py假设不同，不能直接使用。当前epro仍是清线前检查点，必须结果验证后重新导出同步。

用户补充：等 FreeRouting 实在补不下去再停止。当前进程PID38230，仍在计算；不能因固定等待时间中断。若30轮上限结束但仍有改善，应检查SES并继续，不把上限视为无解。CUA对Java app返回Invalid app，不能通过非CUA手段操作其UI；用CLI日志、SES和进程状态监测。

U2旧DeviceName定位：PCB嵌入DEVICE/META仍TCA9535，而Controls内已XL9535；导出project.json选择了旧PCB库定义。后续统一PCB内同UUID的库定义（需保存退出再修改或用原生库更新）并冷启动复查。C3等同理，不能只改工程导出zip。

新增 check_pcb_schematic_sync.py：比较原生PCB PAD_NET及继承DEVICE采购属性与ENET全部616焊盘，185元件、0不匹配。结果pcb-schematic-sync-20260927.json。此项不是铜连通性或DRC，不能替代布线验证。

## 用户要求停止本轮 FreeRouting（最新指示）

用户观察到路由无法继续，明确说“可以停了”。已向session88950发送中断，进程exit130，未产生 /private/tmp/ruri-hardoff-fresh.ses。不能宣称保存了部分路由，也不能导入不存在的结果。日志只有启动信息，不能单凭日志断言具体卡住的网络。不要自动原样重启这轮。下一步先诊断细间距焊盘逃线、主电源宽度及通道约束，修改有依据的问题后再继续布线。当前原生PCB保留185元件和天线铜，其余旧线按用户指示已清；同步epro为同一未布线工作状态，制造文件继续STALE。清线前全工程备份仍在/private/tmp/ruri-before-full-reroute.zip，原始旧成果也在Git历史。

## 01:38 heartbeat：路由约束筛查

没有重启 FreeRouting，也没有并行修改 EDA。检查原生焊盘几何发现22处“主干线宽大于直出逃线允许宽度”的组合，见 routing-escape-screening-20260927.json：U3电池/VSYS要求0.8mm而同排异网脚约只允许0.4002mm；U4电源/电感脚约0.430mm；U8电源脚约0.390mm；J1供电脚约0.380mm。不能证明这就是中断那一轮的全部原因，但这些约束应在下次路由前处理。

已生成 power-escape-plan-20260927.json，22条0.3mm短逃线后转宽主干的候选计划。尚未插入PCB，必须逐个检查对其它焊盘/器件/过孔间距，以及电源短颈的长度、温升和回路；不得全局把电源主干降为0.3mm来换取布通。U4电感与输入输出去耦回路应优先手工完成，再让FreeRouting承担其余网络。现有 generate_fanout_seeds.py 引用旧pcb-native-pinmap，不能直接跑以免重引入LCD_D0..7旧网。

另：直接统计ENET实例采购字段会漏掉多数旧自建器件（旧BOM也多为空，历史报价通过网页匹配）；当前616项同步检查的“采购一致”仅证明已有字段一致，并非所有元件都有采购编号。报价前必须补齐/核实整套采购映射，不能按缺字段把不同物料合并。U1显示名被厂商Value=2.4GHz覆盖，后续改回ESP32-S3-WROOM-1-N16R8，同时保留正确电气参数。

候选逃线进一步与全板焊盘包络比较：22条中16条无保守焊盘冲突；6条冲突已写入计划文件（U3.11-C11.1约0.1499mm；U4.1-R28.2，U4.6-L1.2，U4.10-L1.1均相交；U5.6-L1.1约0.1339mm；U10.4-C62.2约0.060mm）。应先调整局部布局/引出方向，不能直接批量插入22条计划。未启动新路由、未写新铜线。

## 最新主动继续：32段短引出线已写入，等待冷启动 DRC

22条候选改为含局部折线的32段；全板焊盘包络及候选相互间距筛查0冲突。原生pcb_create_track桥存在layer字符串直传问题，第一次创建即报错，未成功创建任何段。改用已保存退出且桥确认0连接后，在备份基础上写已观察的原生LINE格式，未使用validate=off导入。脚本/private/tmp/ruri-install-local-escapes.py已运行，**不可重复运行**。导入ID见local-escape-import-20260927.json；待EDA重开原生DRC验证。备份/private/tmp/ruri-before-escapes-and-device-sync.zip。

同时将PCB内30个同UUID自建DEVICE元数据与原理图统一（断言Symbol/Footprint身份不变），改正U1显示名。616项PCB/原理图同步检查仍0不匹配。当前CUA edaApp8刚单击最近工程，下一步取消网络拖动设置、打开PCB、Claude连接；随后原生DRC检查新引出线、刷新epro。尚未重启FreeRouting。

## 01:52 新输入已验证并启动布线

32段短引出线冷打开后原生DRC最初33项间距错误均为旧GND铺铜；重建所有地铜后间距错误0，连接错误449。完整证据pcb-escape-drc-20260927.json。epro已同步导出，几何核对185元件/408项/0错误/36NC。新原生DSN /private/tmp/ruri-escape-native-raw.dsn；prepare_routing.py --no-seeds输出 /private/tmp/ruri-escape-native.dsn（保留本次32段，未重放旧种子）。FreeRouting1.9.0单线程启动，session52793、PID42921，输出/private/tmp/ruri-escape-native.ses、日志同名前缀.log。不得同时改布局或重复启动。首个jstack确认已进入BatchAutorouter和走线优化，不是加载DSN阶段。尚无SES，不代表布通。

报价预处理已新增prepare_quote_candidates.py、quote-candidates-20260927.csv/json；166实例，55项目料号/111历史未核准候选，不可下单。实时页面复核U10 C683779 ¥25.37/1颗库存5，J1 C506795 ¥6.06/1颗库存15827，J3 C161860库存0（¥1.492仅预订参考价），需解决替代采购。见live-price-check-20260927.json。
