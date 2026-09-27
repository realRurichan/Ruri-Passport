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

检查点70159da已推送origin/main。新路由状态见freerouting-escape-20260927.json；截至启动约337秒，4次线程栈均在路由/优化算法，未见加载阶段卡死，尚无SES；不能据CPU忙判定改善。后续首先检查session52793/PID42921及输出文件，勿另开路由。结果出现后备份工程再导入SES，重建铜并查DRC与重复铜，保护ANT_A/B；无输出则继续诊断，不强称成品。POWER.md已纠正旧的“PCB尚未同步”文字。

## 02:03 用户确认空跑后的保存与导入诊断（最新）

用户认为FreeRouting空跑，已通过算法request_stop协作停止，进程exit0，成功保留241067字节SES。运行末段pass29，diffBetweenBoards最近多轮12是改线差异数，不是剩余飞线。原生pcb_import_ses返回true但损坏线宽：2263段变成默认10mil，坐标取整0.1mil；天线过孔重复3个，375间距/36连接错误。元件位置185个完全未改变。不是凭这些错误就应重布局。用户允许尝试自动布局，我判断先修导入再看局部拥挤；屏幕/键/接口/天线/孔固定。

已保存退出，桥0连接，使用备份/private/tmp/ruri-before-ses-import-20260927.zip为基底离线精确转换，脚本hardware/tools/import_ses_native.py：保留ANT17线3孔，移除32旧逃线（SES包含），新增2427线257孔（SES精确重复1段跳过），保留原始宽度和坐标。616项网表同步0错误。当前已写入PCB，edaApp10正在重新打开工程，待取消网络拖动设置、打开PCB、连接Claude、重建铜和原生DRC。当前epro仍导入前，需更新。最新DSN/SES已存hardware/routing/latest。无自动布线进程，不要原样重启。

## 用户最新最高优先级：成本驱动重构，停止旧架构布线收尾

用户明确指出降本不足，要求不惜改变电路结构、减少TI等进口器件、以省钱为第一目标。已承认前轮仅U2和电容变动不够。当前旧PCB精确SES转换后0间距/32未连接；8个via端点及696个pad端点微小对齐后仍32未连接，证明主要是断开的网络分支，不能再称只是精度问题。最新源与epro已保存，禁止发布生产包。无FreeRouting进程。

立即转为成本重构：不能再花时间完善旧昂贵架构。优先用基础离散器件替代LTC2954按键电源保持；重做BQ24074电源路径、TPS63802+Coilcraft贵电感；用离散MOS替换TPS22919；国产USB ESD替代6颗TI TVS；评估音频Codec+模拟mic+基础功放及国产连接器，减少不同扩展料数量；评估2层板降低两套分摊。保留全部用户功能，不以便宜读卡器冒充NFC卡模拟，不以不支持充电终止的边充边用偷省。所有候选先核原厂规格和国内JLC实际总价再锁定。

已查TP4056-42-ESOP8/C16581为南京拓微，国内JLC当前1颗价1.134元、库存87550，**扩展库**，不能记基础库（旧BQ历史14.51元）。Cua costTab当前tab3是该页。SGM6603是升压不是升降压，不可直接替代TPS63802；SGM62117是真正升降压候选未核价格。SY8089IAAC原厂页面100%占空2A降压，是否改变低电池截止要实算，不擅自隐瞒续航代价。

## 继续降本：用户新增硬约束与充电候选

扩展料只接受明确免换料费；必须在最终两套报价验证。板子可缩小，外壳剩余区域用于电池和扬声器，不能强制沿用88×135mm PCB。已在国内JLC当前搜索页看到C16581扩展库(免换料费)，1+1.134元库存87550；优惠订单条件尚未验证。已下载原厂REV2.4规格书/private/tmp/ruri-tp4056-primary.pdf，逐脚计划见cost-rearchitecture-20260927.json。RPROG系数1100，3k公式366.7mA但表格400mA，不能承诺精确400mA；需保守电流预算和样板测量。NTC窗口45%–80%VCC，需按实际电池NTC重算，不能直接沿用BQ外围。提出USB肖特基+电池PMOS分流，不把系统直并BAT导致终止失效。新方案尚未写入EDA，不得把芯片价差当作整板已降本。下一步核优惠条件、稳压及MOS/二极管基础料，锁定完整电源小计后重绘Power页。无路由进程，旧生产包仍STALE。

本轮新增hardware/design/COST-REVISION.md：共用LCD/SD MOSI/SCK释放GPIO16/8，分配充电状态与USB检测，彻底删除U2的候选功能去向（LCD复位随EN、SD轮询、AMP运行域、取消BQ双模式及外围域）尚需逐项验证，未改EDA。机械试算目标88×65mm，电池预留x6..57/y69..132，扬声器Ø20中心74/115；只是布局目标不是成品。官方免换料费专区https://www.jlc-smt.com/lcsc/basic有1586项和下载清单按钮；本轮按钮点击未产生下载，分类已选但应用后列表仍旧，未取得完整清单。不要称清单已下载。改用可验证的详情/清单列表继续筛选；SY8089/TPS63000本轮可见列表未找到明确免费标识，暂不锁定。

## 免费电源物料实读筛查（最新）

新增free-fee-power-screen-20260927.md，候选尚未写入EDA。CJ2305/C8549长晶0.257元库存319206，但国内页面明确收费扩展，已排除。免费基础库AO3401A/C15127 0.579元库存857940，原厂Rev3.1核到-2.5V下85mΩ；控制用国产2N7002/C8545基础免费0.109元库存1763226。不能用2N7002做主功率。AO3401A是AOS，不能称国产替换成果；应按总加工价权衡。三颗PMOS每板、两板、历史单种换料20元的条件估算，免费AO方案比收费CJ方案省18.068元/两板，不是最终报价。

CUA costTab仍用户tab1。搜索控件AX有时刷新滞后，AX单击“是”可能实际点成其它筛选；可用观察DOM的span[title="是"]点击，再等列表刷新，domSnapshot确认实际结果。免费DC-DC筛选最终返回8款，清单与不适用原因均保存；不能用XL1509最低4.5V的器件接单节电池，不能把TPS61040开关400mA当输出能力。没有合适国产免费升降压锁定。下一步应研究免费低压LDO/不同电源拓扑，以及国产免费USB ESD、音频与连接器；不要重复盲点旧专区分类。主稳压是当前待解决项，不是需要用户批准的阻碍。无布线进程，旧生产包STALE，未修改新电路或下单。

## 最新持续工作授权与费用例外

用户要求持续工作直到其明确停止；已建立active goal。用户纠正费用筛选必须选“是”，已在DOM确认音频筛选“是”6条。随后用户明确接受：保留功能，少数必要器件接受换料费，但须最低两套总价。不要再把免费料绝对限制当成阻碍，也不能滥用例外。COST-REVISION已更新。

EDA桥曾失联，已从授权已安装路径重启，EDA_BRIDGE_IDLE_EXIT_SEC=3600（0会立即退出，别用0）。当前exec session74438 PID52990，server_info验证一实例586e41b8、正确工程、extensionConnected=true。edaCostApp绑定/Applications/嘉立创EDA(专业版).app；bundleID有挂载镜像歧义须用绝对路径。当前PCB有未保存星号，任何离线修改前保存/退出/备份，避免覆盖。

CUA旧tab1失效，当前costTab为新建后台tab2，已恢复账号；准备保留handoff。免费LDO搜索9款均无适合整机的直接替代（不要用AMS1117单节供电或200mA型号）。音频功放3471结果费用属性只有“否”；音频关键词免费6条是电感/运放，不是I2S功放。未实施新电路。

降本机会：搜索0.47uH 4A得到国产功率电感，SLW4020SR47NST/C48996569顺磁，1+0.293元库存170，页面Isat7A/Irms4A/DCR22mΩ/±30%/4x4mm/收费扩展。另SFE4018A-R47N-F-HF/C22463962德立0.344库存3000，但Isat4.3A低于前者。当前贵Coilcraft历史25.85元；即便保留同一种扩展费，电感本体有约25元/板降本空间。尚未核原厂规格及尺寸焊盘，不准只改料号称替换完。TPS63802原厂RevD确认需0.47uH、按最低输入计算峰值并20%饱和余量，不能随便改1uH。下一步取得顺磁规格核Isat降感定义、DCR最大/温升、封装，再改电感符号/封装采购绑定；与此同时按键离散保持+TP4056电源重绘仍待实施。

## 费用例外确认与电感核验纠正

用户再次明确保留功能、必要少数器件接受换料费，但必须比较两套最低总价。优先免费筛选不变。电感SLW4020SR47NST的国产身份未核准（存在韩国品牌线索），不得标成国产成果。已下载厂家SLW-S Rev03系列PDF /private/tmp/ruri-sunltech-slws.pdf；其中4020表从1.0uH起，没有R47型号，不能用这份系列规格冒充R47电气确认，暂不改入EDA。

元磁CPN252012HR47NT/C52741443国内详情页实读库存0、仅支持邮寄、预订参考价0.107元；旧搜索价格0.187不能作为现货报价。该候选当前不锁定。下一步直接取得有库存C48996569的型号专属规格书，或核德立C22463962实际峰值余量；不要继续把候选价差称为已实现降本。新架构仍未实施，制造文件STALE。

## 离散电源保持原生图已生成（独立提案，非成品）

新增 hardware/tools/draw_discrete_hold_proposal.py，在独立临时工程中画原生图，输出 hardware/eda/proposals/Discrete-Hold-Proposal.esch2；未修改正在打开的主工程。四MOS、五电阻、隔离二极管及按键共26脚，独立几何读回26脚均有唯一网络，报告discrete-hold-proposal-geometry-20260927.json。此项仅几何，不是原生ERC/电气放行。GPIO21改主动高保持；GPIO18用NMOS隔离感知按键，高为按下；启动按钮与保持漏极之间D101隔离，否则保持开启会把按键状态永久拉低，这是已在图中处理的问题。主MOS沿用免费AO3401A，两颗并联；R102改1k，减小按键二极管存在时的栅压损失。

提案待核：D101免费低漏肖特基料号和最大Vf、低电池初次启动Vgs余量、2N7002低Vgs控制能力、USB倒灌、实际启动保持窗口。未加未经计算的定时电容。关机需释放按键后断电；此提案无独立崩溃强制关机定时，不能当作已实现该额外能力。消除LTC2954的约25.37元/板芯片费用是目标，未计实际新增外围/最终换料费，不称整板已报价。

C48996569页面初始预订价/库存0是异步加载占位，最终实读1+0.293元、库存170。同样C52741443上一轮库存0需要重新加载后才能最终判定；不能只凭初次快照淘汰。下载按钮打开数据手册对话框，但预览未绘制，直接下载未取得本地文件。桥server_info仍正确工程单实例586e41b8。继续先完成离散控制器件及TP4056电源分流核验，将提案变成完整Power页，再集成主工程；不要再原样完善昂贵旧PCB。

## 完整充电/按键/分流提案已扩展（最新）

Discrete-Hold-Proposal.esch2现含TP4056、背靠背电池PMOS隔离、USB肖特基供SYS_PRE、隔离的USB/充电状态输入；共71脚几何读回0错误。候选SOD123/TP4056ESOP8封装按厂家包络及推荐落脚解释生成，仍需原生库/钢网比较，不能当成已核准生产封装。新方案尚未合入主工程，也没有新生产包。生成脚本每次在独立临时副本工作，避免覆盖正在打开的EDA工程。

国内BAT54费用筛选最终确认为仅“是”13项。Playwright点击span/父li误触了“否”；原生AX明确选择“是”并删除“否”后应用成功。以后用AX或截图核对实际选中项，不要连点假设。最便宜适合双端SOD123候选宏嘉诚BAT54W/C7502705免换料费，1+0.0667元、库存154554；厂家型号专属PDF搜索索引确认0.1mA/25℃最大Vf240mV、漏电2uA@25V。curl结果是HTML不能称已下载PDF。原生lib_get_device_by_lcsc核到真实器件/符号/封装UUID；lib_symbol_open_in_editor返回false，尚未取得原生符号坐标。

TP4056ESOP8原厂REV2.4 p14已渲染，EP包络3.502×2.145mm，9脚EP在自建图接GND（编号9是自建约定，待库映射核验）；原厂p10不用的STDBY明确接GND，已照做。NTC试算仅假设外置10k/B3950，Rup6.2k、Rparallel82k、NTC串1k；实际电池/103AT-2不等同此假设，必须重核。计算及全部未决项见power-proposal-calculations-20260927.json。25℃含电阻容差及240mV压降时，2.75V按键启动Vgs不到2.5V；3.0V足够，不能宣称满温/低电池已放行。

另发现国产IP5306-I2C/C488349实读1+2.13元库存3712（初始0为异步占位）；无明确免换料费徽标，不支持电池温度检测。可能以5V升压+国产3.18V降压替代现有架构，必须比较两种扩展料费用、切换掉电、NTC外部电路、I2C版本专属资料及USB关机路径后才决策。非I2C版官方PDF不能替代I2C版；官方下载403，本轮未取得。不停止必要方案推进来等此候选。

## 主工程共用 SPI 已合入及费用例外再次确认

用户明确：保留全部功能，少数必需收费器件可以接受，但必须比较最低两套总价。主原理图 Core/Display 已由 merge_display_sd_spi.py 合并 LCD/SD MOSI/SCK 到 GPIO11/12，U1 GPIO16/8 原连线移除并标 NC，给新电源预留；五向键保持独立 GPIO。脚本一次性，勿重跑。全工程离线格式验证0错误0警告；EDA已重开连接 b4c14d2e，原生 ERC 0致命/0错误/1警告（U2/U1/J1 采购属性不匹配），MP1/MP2为屏幕座机械焊盘信息。最新epro363614字节已导出，ZIP读回确认无LCD_MOSI标签、Core/Display有SD_MOSI。原生sch_get_connectivity仍45秒超时，未取得新ENET，不能称逐脚核验完成。

PCB铜未随网络改动，禁止直接使用生产包，待新架构完成统一同步/重布。备份/private/tmp/ruri-before-shared-spi-20260927.zip。下一步核屏幕RESET时序并完成原U2控制端口去向，再删除扩展器；离散充电/保持提案仍独立文件未合入。无FreeRouting进程。

## 屏幕独立复位合入、原生新ENET已核（最新）

上一轮为实际主原理图/导出进展，非空跑。本轮取得ILI9488原厂撰写V100完整PDF /private/tmp/ruri-ili9488-primary.pdf，p300–302及308–309要求供电后有效硬件复位。决定GPIO16独立复位，GPIO8保留USB检测，不再拟把RESET直接并ESP_EN。主工程U1.9接LCD_RESET_N，U2.13原输出stub移除标NC，未动PCB铜。一次性脚本move_lcd_reset_gpio.py不要重跑，备份/private/tmp/ruri-before-lcd-reset-20260927.zip。

充电独立提案删Q107/R112，用1k+0603指示灯候选表示CHRG，LED还未选型，不能当生产封装；68脚几何0错误。主工程仍185件，U2未整体删除。原生EDA桥a6c049a7，ERC0致命0错误1采购警告，epro363617字节。UI导出hardware/review/schematic-current.enet成功，check_native_netlist.py408项关键脚0错误（含新共享SPI和独立RESET），弥补MCP45秒超时；最新ENET不再旧版。报告lcd-reset-gpio-20260927.md。

下一步完成U2剩余AMP_ENABLE、REG_PWM、CHG/USB/SD/PERIPH控制迁移及新Power页集成；然后移除U2/旧控制器外围，并统一同步PCB。当前旧PCB有打开星号；离线改前仍须保存退出。所有生产包STALE，没有FreeRouting进程，尚无新整板报价。

## 主原理图实际删除20件：U2/U5已移除（最新）

上一轮已合入独立复位并通过新ENET，是实际进展。本轮依据MAX98357原厂资料发现不能盲目把AMP_ENABLE固定高，需可靠关闭和停钟顺序；改GPIO8独立控制AMP_ENABLE、保留100k下拉R10，GPIO16仍LCDRESET。功放旧MAX暂保留，国产音频重构待做。

主工程remove_iox_cost.py一次性执行成功，删除U2、U5、C8、R8、R11–14、R24/25、R29/30/39、R77–83共20件；R6/R7I2C上拉、R9NFCVEN下拉、R10AMP下拉保留。所有3V18_PERIPH合并3V18，MODE接GND；依据TPS63802原厂输出电容无上限，但瞬态/热仍需样板。BQ暂EN1=VBUS5V、EN2GND固定USB500，7/9状态输出NC，无状态GPIO；J4.9检测开关NC，软件轮询。不是已完成国产充电替代。

原生ERC0致命0错误1采购警告U1/J1，UIENET导出成功，165件/364关键脚0错误（assert旧删除料无残留）。最新epro358423字节；新报告iox-removal-20260927.md/json。电源独立提案删Q108/R113后63脚几何0错误，GPIO8不再USB检测。备份/private/tmp/ruri-before-remove-iox-20260927.zip；EDA桥50a260b3，PCB已保存后重开，没有路由进程。

PCB仍旧185件和旧网络，不能直接生产。下一步合入新充电/离散保持Power页，核真实TP4056/二极管封装及弱USB输入电流策略；再统一同步PCB、改小板框重布局。主要LTC/BQ/贵电感尚未消除，不得把20件减量称预算达成。2套实际报价未更新。用户接受少数必需收费扩展，但必须最低总价，搜索免费优先。

## 原生电源库已取得、草拟焊盘已纠正（最新）

上一轮为主原理图删除20件和ENET实际进展。本轮解决原生库访问：lib_symbol_open_in_editor对TP4056仍false，但lib_get_device_by_lcsc完整对象+symbolUuid=otherProperty.Symbol，调用sch_create_component可从云库加载真实符号/封装。临时在RF_Service远处放置BAT54W C7502705和TP4056 C16581，均addIntoBom/PCB=false，导出/private/tmp/ruri-vendor-power-probe.epro后立即sch_delete_component两ID并sch_save，最新主epro读回确认临时器件不存在。勿把探针导出当工程。

真实库源已存hardware/eda/library/power/四份esym/efoo，证据power-native-library-20260927.json。BAT54W真实K=1/A=2；原生焊盘中心±64.374mil、宽35.827/高48.031，草拟原值±70.4724且宽高颠倒，已纠正提案。TP4056真实EP=9 GND，原生封装横向双排，1–4在y=-114.5、5–8在y=+114.5，x以50mil递进；EP129.921×94.488mil，不能沿用草拟竖排落脚。

生成脚本现直接从真实efoo提取编号/中心/宽高，无手工估算；提案新封装COST_BAT54_NATIVE_PADS、COST_TP4056_NATIVE_PADS。63脚几何0错误；独立读回2+9焊盘中心/尺寸/编号完全匹配，power-proposal-pad-match-20260927.json。仍需钢网热焊盘/热过孔及逐脚主工程集成。最新主epro366665字节，新增的是缓存库；主电气架构仍165件，尚未移除LTC/BQ，不得称完成这两项降本。

下一步可用真实库源合入Power原理图及离散保持，保留Q14/Q15电池ADC隔离；低电池/满温驱动和弱USB电源策略仍要收敛，不再以拿不到封装为由重复查询。当前EDA桥50a260b3，RF_Service已保存，PCB未同步且生产包STALE，无FreeRouting进程。

## 主工程LTC2954已真正移除（最新）

上一轮真实库源/焊盘核验是进展。本轮通过原生sch_create_component加载C7502705到Power（真实符号/封装），保存退出桥0连接后离线重构。新一次性replace_ltc_hold.py不要重跑：删U10/R70/R72/C60–63，新增D8/Q16/R84–86，R73换基础1kC21190，复用原生R48器件且拷入缺失库；原AO3401A并联主开关Q12/13和电池ADC隔离Q14/15保留。GPIO21主动高HOLD、GPIO18按键隔离高有效。D8K1=BUTTON_RAW、A2=MAIN_SWITCH_D；保持不会让按钮永远显示按下。Q15栅改HOLD，断电采样仍隔离。

新主原理图163件，源19项新关键脚几何0错误；epro361392字节，导出几何354项0错误，原生UI新ENET同为163件354项0错误、U10确实不存在。ERC0致命/0错误/1采购警告U1/J1。报告ltc-discrete-hold-20260927.md和ltc-removal-source/ltc-hold-export-geometry。PCB未动，仍旧185件网络，不能下单。

操作约束：固件必须按钮松开前拉高GPIO21；正常关机先写SD/关功放再HOLD低，释放按钮后断电；未实现独立崩溃长按强制关机定时。低栅压2N7002、二极管全温和启动保持时间仍未放行，25℃最低供电条件见现有calc，不当成板子成品。BQ/TPS/贵电感仍在，国产充电重构下一步须解决弱USB供电总电流和分流问题，不能为了TP4056便宜就删输入限流。

当前EDA桥5ae89568，Power有原生UI星号，离线修改仍须保存退出。备份/private/tmp/ruri-before-ltc-removal-20260927.zip含新D8未接线（此前完整epro366665为有效旧架构checkpoint）。Native保存最后一行ATTR没有尾|，解析器须先判断有无尾|，本轮已规范末行以供工具读入。无FreeRouting进程，生产包STALE，未有新总报价。历史LTC25.37/板、新增D8/Q16.1757+三电阻估.01差额约25.18/板仅元件费估算，不能称最终最低总价。


## 低栅压控制 MOS 原生库及两套实际档位核实（最新）

用户再次明确保留全部功能，少数必要收费器件可接受，按两套总价最低比较。AO3400A C20917取得原生真实符号/封装，存library/power/AO3400A-C20917.esym/efoo；G1/S2/D3。AOS原厂Rev3.1有2.5V栅压25℃48mΩ最大值，不能声称全温保证。此为2N7002控制端低栅压可靠性候选，不是国产降本成果，尚未替换Q11/Q15/Q16。

JLC详情实读基础库，库存1069723，1+0.52元，50+才0.417元（不是10+）。两套即使合并原Q1/Q2共10颗仍按0.52预算；三颗替换相对历史0.109约增加1.233元/板，无新增类型换料费。不要按0.304或错误10+档低估。证据ao3400-control-qualification-20260927.json。

临时RF_Service探针7ebfebf3618f23ac已保存模板/private/tmp/ruri-ao3400-native-template.esch2后删除并原生保存；导出主epro362299字节，临时器件不在主导出。网表仍163件354项0错误；清理后导出几何报告ao-library-clean-export-geometry-20260927.json。PCB仍旧铜，生产包STALE。下一步用模板真实库合入控制MOS、按差异移动连线，再完成USB弱输入下充电架构选择，主电源大头BQ/TPS/L1仍未降。不要重复临时探针。


## Q11/Q15/Q16 原生 AO3400A 替换已写入主源（最新）

上一轮为真实库/阶梯价格证据进展。本轮先正常退出EDA，server_info确认0实例，备份/private/tmp/ruri-before-control-mos-20260927.zip，然后执行一次性hardware/tools/replace_control_mos.py；不要重跑。Q11/Q15/Q16绑定原生AO3400A C20917的Device/Symbol/Footprint和完整采购参数。原2N7002与AO3400真实符号逐脚位置及G1/S2/D3完全相同，线不需要移动；独立对比所有WIRE/LINE/NC/NET记录前后完全一致，源格式validate 0错0警告。成本增加约1.233元/板是低栅压可靠性修复，不叫国产降本。

EDA已重启但启动页出现SQLITE_MISUSE加载信息，尚未取得本轮原生ERC/ENET/epro验证，不得拿上一版354项报告证明新采购/符号。当前主epro仍前版362299字节；工程源较它更新，生产包仍STALE。下一步恢复应用打开工程，原生验证后导出更新epro；不重启桥或重复修改源来掩盖启动问题。

后续现场确认：启动页SQLITE_MISUSE为暂态，应用已正常进入，点击最近工程151并确认旧路径提示232、取消设置272后已载入项目。已双击PCB237；等待编辑器加载后恢复Claude连接即可，不是外部阻碍。源替换完成，仍待原生导出验证。


## 控制 MOS 原生验证完成、NVDC 国产充电候选价格已实读（最新）

上一轮源替换为进展。本轮EDA恢复连接541e1cd9，sch_run_drc原生0致命0错误1原有采购警告；新epro362303字节导出，独立几何163件354项0错误38未接脚。导出实际Q11/Q15/Q16采购C20917和Device d255fa01e0c6cfaf正确；Footprint实例null由Device属性继承，勿误认为未绑定。report control-mos-export-geometry-20260927.json。未再导出UIENET，现enet仍上一架构，但几何逐脚独立核新导出。

SGM41511 C699848原厂RevA3 2024手册取得，NVDC输入限流+电池补电可解决TP4056草案弱USB缺陷；JLC搜索实际只有该料，是否免换料费明确“否”，库存3557，1+7.72，10+6.16。两套用7.72，不能误用后档。用户允许少数必要收费，尚未选择/替换。旧BQ14.51历史差6.79/板未含新电感/外围/类型费，不能当总节约。默认充电2.04A，关机/看门狗前安全充电约束未解决；必须硬件PSEL/输入限制或nCE策略，不能只靠上电固件降低电流。证据sgm41511-cost-candidate-20260927.json。

下一步核PSEL500mA默认及容差、NTC默认曲线、3V18关机后I2C反灌、充电电感免费候选两套总价；同时国产buckboost仍未解决，PCB不宜同步旧电源铜。生产文件STALE，无布线进程。


## SGM41511 逐脚预案及无软件充电约束边界（最新）

上一轮真实ERC/导出和候选价格为进展。本轮厂家RevA3逐脚整理hardware/review/sgm41511-pin-plan-20260927.json，包括NC8/10必须悬空，GND17/18及EP接地且EP不能作为唯一功率回流；VAC1必须VBUS24，BTST21的47nF去SW，REGN4.7uF10V，PMID10uF，真实EP编号尚待库。计划固定PSEL上拉REGN，不可上拉关机消失3V18，否则默认会变2.4A；保留现离散总开关，nQON不直接共享按钮。I2C仍用关机消失上拉，需核断电漏电而非凭经验判断。

关键新证据：500mA档在25℃有520mA最大值，不能称严格500mA；默认2.04A充电虽可受总输入功率限制，5.25V×.52/3.06V=0.8922A只是25℃稳态保守上界，非全温安全放行。默认4.208V全温最高4.232V须电池spec匹配；厂家NTC例0..60℃不能照搬给0..45℃电池。nCE安全策略未决，不能只绑低后靠MCU软件。没有更改主电路或PCB，此JSON是可实施逐脚预案，不是成品。

下一步优先找线性带powerpath国产料（SGM4056自身仅充电非powerpath，不能假等价）；若无更低总价可安全方案，完成SGM41511硬件输入策略与电池要求后合入。勿反复声称候选降本已达成。


## 无电感线性 powerpath 候选排除当前可采购方案（最新）

上一轮完成SGM41511逐脚预案为证据进展。本轮厂家线性目录找到真正powerpath SGM41562A/B，并读完整RevA1 34页：无充电电感，456mA充电，推荐IBAT到3.2A但默认IDSCHG=2A，默认NTC为PCB OTP而非直接电池保护模式，500mA输入档25℃最大620mA，不能称严格USB500。WLCSP原厂1.52mm，平台标签1.47不能当精确封装。JLC搜索7件是否免费只有否，实开C699853详情确认库存0，展示2.6参考价不是可买两套总价。证据sgm41562-linear-screen-20260927.json。未改主电源，不能称已降本。

发现ETA6002/6003厂家完整PDF：ETA6002 ESOP8电阻设充电+powerpath有成本潜力，但营销inputcurrentlimiting可能实际只开关3.5A限流，不能猜USB总500mA。下一步读取https://www.eta-semi.com/wp-content/uploads/2022/03/ETA6002_V1.5.pdf核NTC/输入限制，若不满足则不继续该分支，推进SGM41511实际合入而不是无限找候选。EDA桥541e1cd9仍开，主epro362303最新、PCB未同步，生产包STALE。


## ETA6002 分支结束、SGM41511 原生25脚和封装已取得（最新）

上一轮库存排除为证据进展。本轮读ETA6002 V1.5厂家9页：ISET只电池充电，p2内部开关限流3.5A；没有可配置/明确USB500总输入限流。未证明它加外部限流后最低成本，故不作直接替代，结束该分支。报告eta6002-screen-20260927.json。

用lib_get_device C699848真实对象加载SGM41511到RF_Service临时非BOM非PCB探针0089dbc7b7857542，保存/private/tmp/ruri-sgm41511-native-template.esch2，导出/private/tmp/ruri-sgm41511-native-probe.epro后删除探针并保存。真实esym/efoo存library/power/SGM41511-C699848.*。Device e6bfe60c68de05a2、Symbol0626805544a39843、Footprint6f722f14783ff48c；原生EP确认为25，24功能脚名称全部与厂家逐脚预案一致，pin-plan更新EP25→GND。不是用采购编号假替换，尚未主Power合入。

下一步直接做独立SGM41511电源页提案，使用真实库/既有阻容，固定REGN拉高PSEL，核nCE/电池NTC和2.2uH电感；比较两套完整增删费用后合入替代BQ。不要再无限找相同功能候选。无布线进程，PCB旧电源铜，生产文件STALE。桥541e1cd9；临时probe已删，主导出已重导仅缓存库增长。


## SGM41511 原生电源页提案已实际绘制（最新）

上一轮真实库源为进展。本轮draw_sgm41511_proposal.py生成独立临时完整工程/private/tmp/ruri-sgm-proposal-9r_tvwfa/Ruri-Passport-RevA，不改live。提案hardware/eda/proposals/SGM41511-Proposal.esch2使用真实原生Device/Symbol/Footprint及25脚，PSEL10k拉高REGN、NC8/10及可选3/7/12明确NC、GND17/18/EP25接地，bootstrap47nF、输入/PMID/REGN/BAT/SYS去耦已绘制。独立25脚线/NC几何0错误，报告sgm41511-proposal-pin-geometry-20260927.json；stage validate0错误0警告。

nCE接地是未放行的自主充电候选；NTC暂厂家103AT-2的5.23k/30.1k例（实际电池曲线和0..45C重算）；L1012.2uH为明确未绑定器件，不能生产。阻容是生成器通用库未采购绑定，原生U101才真实完整库。不称完成国产替代或费用节约。下一步选真实2.2uH免换料费电感、按电池NTC核充电约束和静态I2C，再把阻容绑定既有免费料并更新提案，厂家独立读回后合主Power替代BQ。主epro仍367996、PCB旧铜、生产包STALE。


## 充电电感免费筛选生效、NTC容差模型已更新提案（最新）

上一轮绘制原生提案为进展。本轮JLC 2.2uH搜索明确选择“是否免换料费=是”并应用，异步结果最终仅1件C1043风华CMI201209U2R2KT，1+0.126库存65893但50mA信号电感，不能用于充电开关。搜索刚点击筛选时旧6271件还显示全部价格，勿把旧结果列里顺络/长江等误判免费。报告sgm-charge-inductor-free-screen-20260927.json。此仅该搜索范围，不是所有基础库1uH/2.2uH均无候选证明。

NTC提案由厂家103AT-2的0..60C例改为条件性10kB3950 R25/B均1%假设、偏置9.1k/150k均1%。calc_sgm41511_ntc.py用厂家cold .726..739、hot .335..348各32角落：cold0.790..3.660C，hot40.680..43.584C；是beta模型非真实R/T曲线/热延迟保证，电池及外置NTC真实规格仍待选。阻容基础库绑定后可省收费类型。draw_sgm41511_proposal.py已改并重新生成独立提案，不动live；新stage路径在工具输出。

下一步核厂家允许1uH与2.2uH范围以及基本库功率电感，必要时按用户已授权少数收费例外选最低总价；不可为了免费选50mA信号电感。NTC实际part/安装仍需核，主电源未合入、PCB未同步，生产包STALE。


## 用户接受必要收费例外；充电电容及两套费用敏感性修正（最新）

最新用户答复：保留功能，少数必要器件接受换料费，但必须算出最低总价。此优先于早期只免费限制。厂家SGM41511 RevA3 p39实际建议PMID22uF，SYS补偿优化>22uF陶瓷10V X5R/X7R；原提案单标称22uF不能保证偏压后容量。独立提案更新C102为22uF候选并加C107/C108三并22uF候选，明确有效合计>22uF及采购/封装/曲线未定，不能把通用C0603当批准封装。stage /private/tmp/ruri-sgm-proposal-mp7kte0h/Ruri-Passport-RevA validate0error0warning，未动live。

费用情景：BQ历史14.51 vs SGM实观察7.72，两个芯片省13.58；若新增电感C602029 .425×2加新增一类20元费，且充电芯片换料费互抵，则两套反贵7.27，尚未算外围/损耗。是条件估算不是平台总报价，故不能因国产标签就合入或称降本。报告sgm41511-cap-fee-audit-20260927.json。下一步按输入限流必需功能及完整类型费用决定充电架构，基础功率电感可选性仍需核；有效容量绑定之后做逐脚/视觉审查。主PCB仍旧铜未同步，生产文件STALE，无布线进程。


## L1国产低价替代已有厂家曲线/焊盘及真实现货证据（最新）

上轮电容提案修正为实际进展。本轮核顺络MWSA0402S-R47MT C6331050，exact搜索1件库存820，1+1.126元；是否免换料费仅否，用户必要收费例外允许比较。原厂完整PDF9MB下载/private/tmp/ruri-sunlord-mwsa-primary.pdf，Rev2022/10/12：.47uH20%、DCRmax14mΩ、20%降感7.6A，30%典型9.5A，20C温升6.65A，40C典型7.5A均参考20C环境，勿拿平台9.5A当保证。厂家p2图视觉确认推荐焊盘1.5×2.5mm、内gap2.2mm、中心距3.7mm，不能沿用旧XFL中心距2.378。报告l1-sunlord-qualified-candidate-20260927.json。材料两套历史比较可省49.448，保守新增20费仍29.448（非完整报价/损耗量未计）。

真实lib_get_device_by_lcsc C6331050返回[]，不是阻塞可按原厂自建真实封装；尚未修改主L1。下一步按图生成独立原生封装并核转换尺寸，读取TI TPS63802实际最坏峰流/温度及L偏压曲线后完成替换，然后推进PCB同步。浏览器costTab2当前exact搜索并markHandoff，无布线进程、主PCB旧铜、生产文件STALE。


## 顺络L1真实尺寸封装已生成、隔离工程已绑定（最新）

上一轮厂家+库存证据为progress。本轮build_sunlord_l1_footprint.py生成library/power/MWSA0402S-C6331050.nativefp：保留原生PAD结构，重画1.5×2.5mm/中心±1.85mm，去旧XFL图形/source，assembly最大body4.75×4.45，courtyard5.7×4.95，paste零缩放、mask .05mm。序列化mil回读与原厂mm独立比较0error，报告l1-sunlord-footprint-readback-20260927.json。不是原生编辑器视觉核准。

隔离完整工程/private/tmp/ruri-sunlord-l1-gfrnvgbe/Ruri-Passport-RevA Power L1绑定自建Footprint b1c6331050040200和实际Sunlord采购属性，清Device旧库引用避免旧器件属性继承。未改live/PCB；主工程依旧不算替换完成。下一步原生打开隔离工程确认封装/采购属性渲染及TI电流边界后合入，不要重复造候选报告；完成后PCB同步和小板重新布局。SGM充电方案仍提案，生产包STALE，无布线进程。

隔离validate初测Device=null被识别为missing DEVICE；已删除旧Device ATTR（不是保留null），复测0error0warning。主live未改。


## 顺络隔离工程原生加载导出，真实尺寸通过但采购绑定未过（最新）

上一轮真实自建封装/隔离绑定为progress。本轮用EDA打开/private/tmp/ruri-sunlord-l1-gfrnvgbe/Ruri-Passport-RevA，项目hash702f60ccf98b810ae7d01362924d6c22ebc022a7576d79fd6b13ebe3d16bf558；桥541e1cd9已切到此隔离Power，主工程未改。原生导出/private/tmp/ruri-sunlord-native-check.epro364686bytes，实际FOOTPRINT/b1c6331050040200.efoo有两个PAD，中心±72.83465mil、59.05512×98.4252mil，独立回读1.5×2.5及中心3.7mm正确。

关键实际发现采购绑定未完成：source脚本仅更新既有ATTR，旧L1本无supplier/manufacturer属性导致未新增；原生自动Device=af35a1ba40c60f1a但无对应DEVICE文件。仅删Device不能视完成替换。报告l1-sunlord-native-roundtrip-20260927.json。下一步关闭/保存隔离再新增完整真实DEVICE doc+Supplier Part/Manufacturer Part等属性，真实导出验证后合主。不要回到候选搜索或称省钱已实现。

TI p18 Eq2明确峰流模型及20%余量，p6boost限流max5.75A(VIN>=2.5)，p7频率2.1MHz只是25Ctyp没有min。需使用限流上界加顺络7.6A@20%drop做选型并声明厂家20C基准/温升样板待测；不声称频率典型公式全温保证。生产包STALE，无布线进程。


## 顺络L1完整器件属性原生往返已通过（最新）

上轮原生封装证据为progress。本轮stage_sunlord_l1.py独立stage /private/tmp/ruri-l1-device-kqbnlitd/Ruri-Passport-RevA，新增DEVICE d1c6331050040200完整真实SupplierPartC6331050/ManufacturerPart和所有缺失ATTR，并绑定真实自建封装b1c6331050040200。validate0/0；EDA UI实际打开该stage后导出/private/tmp/ruri-l1-device-native.epro365021bytes。原生Sheet有全部采购属性，project.json devices对应记录保留真实Footprint与SupplierPart。注意导出格式DEVICE存project.json而非DEVICE/*.edev，上一轮报告“无DEVICE文件故无DEVICE”判断不充分，已更正报告；本轮实际显式属性/metadata已通过。

保存可审查源hardware/eda/proposals/Power-Sunlord-L1-Proposal.esch2。主工程仍未合，主PCB旧铜；下一步合主（先保存并关闭live，备份、只迁移L1记录与新库，导线不变），原生检查，再同步新PCB。当前EDA桥541e1cd9连隔离stage项目，任何后续修改前确认项目路径！sch_get_component单裸uuid超时一次，不代表bridge终止；project_export_file正常。生产包STALE，无布线进程。


## 顺络电感替代已实际合入主Power并更新epro（最新）

上一轮完整器件属性原生往返为progress。本轮保存并退出EDA，server_info确认0实例；备份/private/tmp/ruri-before-sunlord-main-20260927.zip。比较proposal与main所有WIRE/LINE/POLY/NO_CONNECT/NET/COMPONENT/PIN/JUNCTION页面记录完全一致后合入主Power L1：SunlordMWSA0402S-R47MT C6331050 Device d1c6331050040200 Footprint b1c6331050040200真实库。全工程validate0/0，主EDA重新打开实际仓库路径；project_export_file更新hardware/eda/Ruri-Passport-RevA.epro365033bytes，project.json真实device SupplierPart/Footprint读回正确。主main merge报告及导出pin几何报告已保存。

PCB尚未同步新封装及163件新电路，不能把旧铜拿去制造。原.47uH结构不变；TI boost max限流5.75A(VIN>=2.5V)与顺络20%降感7.6A常温基准有约32%余量，不把此称全温输出能力验证。下一步导出最新ENET/同步PCB全量元件网络，更新L1焊盘时旧铜必须重布；主电源国产芯片/充电/音频其余成本仍需架构决策，停止无限候选循环。当前桥连主仓库项目，生产包STALE。


## 主PCB已执行原生全量同步：185→163件（最新）

上轮L1合主为progress。本轮EDA主Power设计→更新/转换原理图到PCB，实际确认导入清单包括3V18_PERIPH→3V18等变更，应用修改后pcb_save。读PCB NDJSON最新record覆盖旧record、null为删除tombstone（不能当元件），163个实际COMPONENT；U2/U5/U10已无，Q16/D8/R85/R86实际新增，L1实际Footprint b1c6331050040200及SupplierPartC6331050/ManufacturerPartMWSA0402S-R47MT均保存。报告pcb-cost-sync-20260927.json。原生PCB L1 Device/DeviceName仍旧5680467994c3b365/XFL，但实例采购/footprint覆盖已更新；下一步规范Device引用以免混淆。

PCB同步是真实元件/焊盘网络变化，不是布线完成。旧铜仍要删除重布/布局，新元件可能停在板外；尚未重新导出ENET做全部PAD_NET比较。项目epro重新导出保存同步进度，生产包STALE。下一步freshENET全量比较，再小板layout/旧铜清理；当前桥主工程PCB，无freerouting进程。


## 最新原生ENET全量比对并修复3个NC残网：540检查0差异（最新）

上一轮PCB163件同步为progress。本轮sch_get_netlist全项目uuid仍45秒超时（终止已确认，不再重复）；UI原生导出嘉立创专业版.enet覆写hardware/review/schematic-current.enet成功。check_pcb_schematic_sync实际163件540padnet检查发现J4.9仍SD_DETECT_N、U3.7USB_PGOOD_N、U3.9CHG_STATUS_N三错：schematic为空。EDA退出server_info0instance后备份/private/tmp/ruri-before-nc-sync.epcb2，fix_cost_sync_nc.py实际清三脚PAD_NET并清64个废弃网络POLY/VIA等铜图元。L1旧Device/DeviceName改为真实d1c6331050040200，并补完整PCBDEVICE doc。复测163件540检查0mismatch，全工程validate0/0，报告pcb-cost-nc-repair-20260927.json、pcb-schematic-cost-sync-20260927.json。

EDA现在退出，主PCB source最新但epro仍上一轮361389bytes、需下次原生打开导出后更新；禁止称二者生产一致。其余旧铜仍需全清重布/压缩布局，尚未PCB DRC/射频/机械签核，生产包STALE。下一步闭合布局计划88×65验证固定孔/屏FPC/天线/卡座后实际摆放，不要重新反复核已0mismatch映射除非改电路。


## 163件已实际压缩摆件：88×85试布局封装筛查0项（最新）

上一轮540padnet0差异为progress。本轮EDA保持关闭；placement-draft.json根据真实163refs去掉已删元件，实际place_from_plan.py主PCB摆放163件。先88×85试布局（不冒称65尺寸已可用），保留USB/五向键/两天线/NFC原位置及屏幕FPC J1(49,59)，上半区RFservice移x-30,y-13，audio移低、IR元件移顶部且避SD。新Q16/R84/85/86不再在板外；L1按较大真实焊盘移35.5,49并重定位去耦。第一轮24项碰撞→修到0项实际conservative pads/bodies，check_placement_bounds.py增加--width/--height参数，本轮--height85输出163件0findings；仍不等于nativeDRC/机械签核。540padnet复查0差异。

注意主板框和固定孔目前仍旧88×135及旧顶部孔132，旧铜全未随元件正确重布；不可把此视成品，epro也旧。下一步实际板框85/重定位顶部固定孔82（需IR/孔净空核），修改机械图显示试板与电池空区、清旧功能走线保留NFC线圈，并生成DSN重新布线。place_from_plan备份/private/tmp/ruri-before-plan.epcb2每次覆盖，完整未摆件备份仍/private/tmp/ruri-before-nc-sync.epcb2及before-sunlord-main.zip，勿误认为单步备份是原始。生产包STALE，EDA已退出，无freerouting进程。


## 88×85实际板框/固定孔及旧走线重置已完成（最新）

上轮163件0placement为progress。本轮reset_compact_board.py在EDA关闭下备份/private/tmp/ruri-before-compact-reset.zip，实际板框POLY改88×85，删除2391旧LINE/248VIA/3POUR/3POURED/1铜FILL，保留NFC线圈POLY6dc0cc0ee7938543和端viaec8d918bb073c865，原馈线需要重新布。旧coil不能当通路完成，不要prepare_routing --fresh-wiring把保留的线圈也清空，后续nativeDSN用--no-seeds并核线圈保护。

原生规范化后旧mountID与manifest不符，初版新增出现旧顶部孔132残留；已实际清所有PCB层12孔FILL以及半径2.6圆形REGION/POLY和H标识，重建四孔。add_mounting_holes.py FILL path改[[CIRCLE...]]符合原生规范，不再flat。H1(3,82)、H2(84.5,62)、H3(3.5,38)、H4(84.5,47) Ø2.2NPTH净空5.2；最初H2(84.5,82)与SD/H4(84.5,50)与R43冲突，实际移动后pad/courtyard2D圆净空0hits。右/顶部机壳要边缘绝缘支撑，未3D签核。MECHANICAL.md开头更新最新试板，旧表明确历史。全validate0/0，163件540PADNET0差异，元件bounds0项。

主source现在无旧铜未布线，EDA仍退出；epro/Gerber旧STALE。下一步原生打开新PCB视觉+DRC，导出nativeDSN（信号类/孔/天线净空由prepare_routing补，旧seed不可复用），手布电源/USB/射频敏感路径后freerouting补其余并设实际无进展停止条件。充电SGM和音频/稳压国产仍未替换，报价未新版，不能目标完成。


## 最新用户成本策略与原生小板检查

用户明确：保留所有功能，少数必要收费扩展器件可接受，以两套完整总价最低为目标；免换料费仍优先，不为国产名义增加总成本。此前严格全部免费要求已被此偏好取代。

本轮用Cmd+O精确路径打开主仓库（近期项目误报文件不存在需绕开），桥ab7087bd。原生PCB strict/verbose DRC实际结果仅Connection Error共513条，其他类别未报；主板未布线因此不是DRC通过。报告compact-native-drc-20260927.json。原生导出最新版hardware/eda/Ruri-Passport-RevA.epro262635bytes，现含88×85试板及清旧铜进度；不能当Gerber制造一致。屏幕/电池机械文档仍有旧135参考框，后续整理以免视觉混淆。

下一步导出nativeDSN保护NFCcoil，先关键电源/USB走线后freerouting补线；原生513未连接必须闭合。国产充电提案未合主；整体新报价仍未完成，禁止说最低价已证明。旧Gerber/BOM/CPL继续STALE。


## 新88×85原生DSN与线圈保护修复（最新）

上一轮原生DRC/epro是真实progress。本轮主EDA导出hardware/routing/latest/compact-native-20260927.dsn。真实发现原生DSN wiring仅保留ANT_B via，丢锁定POLY线圈，不能直接给router。prepare_routing.py新增从实际最新非null锁定ANT_A/B POLY提取线性路径，断言恰好一条coil、保护17顶点0.4mm真实几何；拒绝其他未知形状。routing-draft板框边净空88×135改实际88×85，删除废弃3V18_PERIPH类。运行--no-seeds生成compact-router-20260927.dsn，117网络类重写、46孔/天线/固定孔keepout，未重放旧种子，线圈真实保护wire已在输出。

原生DSN使用一个synthetic u1 image承载所有绝对焊盘坐标，不是163个place，不能以place数断言漏元件。实际593pin、118class(含自动类)，17coil点及88×85boundary已读回；报告compact-dsn-check-20260927.json。完整540焊盘source→DSN覆盖仍待查，尚未运行freerouting也未新增主PCB走线。需优先完成电源/USB关键布线、手接coil端桥/匹配feed后路由补线并原生验证。不得把DSN输入校验当布线完成或生产通过。


## 新DSN完整逐焊盘映射已核：553/553正确（最新）

上一轮DSN保护修复是真实progress。本轮新增check_dsn_pad_coverage.py读取最新native COMPONENT、真实footprint PAD、PAD_NET，逐焊盘比较DSN pin绝对中心(0.02mil舍入容差)和网络。首次ID匹配失败证明原生DSN ID规则不是分别去prefix：它对cid+padid整体删除第一个字母e；实际29e3ea...e14导出293ea...e14。规则按非对称USB/SD与553实际pads坐标/网络整体校准后553checks0error。报告compact-dsn-pad-coverage-20260927.json。DSN593pins中的额外40原生POLY/via表示不拿来冒称多元件；当前540原理图pins与553实际焊盘(含壳/重复号)范围不同。

本轮未布线/未启动router，仍需电源/USB关键路线及coil端桥馈线之后freerouting补线、原生DRC和完整新报价，生产包继续STALE。


## 开关节点六段短线实际落主板（最新）

本轮原生pcb_create_track接口六次均error不能创建，wrapper退出码0不代表工具成功，未形成live铜。已退出EDA，server_info明确0instance后备份/private/tmp/ruri-before-switch-routing.epcb2。主Mainboard.epcb2实际写六段locked LINE：U4.9→L1.1 VREG_L1、U4.7→L1.2 VREG_L2，精确新焊盘中心起止，0.3mm短neck→0.6mm主干，右侧45度dogleg分开。报告compact-switch-routing-20260927.json。这六段尚未nativeDRC审核，下一轮必须原生打开确认，不得称合格；输入输出电容/GND/FB以及USB等仍未接。此前DSN不含新六段，需要重新export/patch后才能给router保护。epro也旧于本轮线路。


## 六段开关铜线原生读回检查通过，连接错误513→509（最新）

本轮精确Cmd+O打开主工程，桥78bf35f6。strict verbose原生DRC仅Connection Error509条，其他类别无；比未布线513下降4，证明两组U4-L1跨元件连接闭合。报告compact-switch-native-drc-20260927.json，routing报告已更新局部状态，不是全板DRC通过。原生epro已重新导出保存这六段线路。下一步仍要输入输出电容/GND/FB闭环，再USB和NFC手线；DSN尚未更新六段，不能拿上一版router输入替换当前手线。旧Gerber/BOM/CPL继续STALE，完整报价未完成。


## 电容/地局部真实线路追加（最新，原生待审）

上一轮509 DRC/epro是progress。本轮关闭EDA确认0instance，备份/private/tmp/ruri-before-cap-routes.epcb2。主PCB真实C12 y54→51.5缩短输入环路，placement-draft同步；163件conservative placement仍0finding。实际追加13locked LINE、3GND via，连接U4 VIN1/10到C12、VOUT6到C13；MODE2/EN3到GND8并地过孔、两电容地短线+via。报告compact-cap-routing-20260927.json。via仅接当地焊盘，不冒称地plane已存在(当前无pour)。

新增线路尚未nativeDRC，下一轮必须先原生检查，可按报告IDs撤销违规铜，备份可回退。U4GND中心via30.9,49/0.6mm可能需要核内部焊盘净距，不能跳过。C14第二输出电容、反馈/PG、其他电源和USB未完成。epro/DSN旧于本轮C12及13lines/3vias，不能作为制造一致。EDA已退出，无router进程。


## 电容支路斜线短路已实际修复，原生复检仅509连接项（最新）

本轮main桥aea9310a。首次nativeDRC报告compact-cap-native-drc-20260927.json真实3clearance：VIN支路斜线8d9f9e7d1d9741fe擦C12地焊盘/地线。通过实际pcb_modify_track修改ids[3]neckendY50.5、ids[4]横接31.825,50.5→30.175,50.5、ids[5]短接30.175,50.5→50.6，从电容下方接已有输入左支路，pcb_save真实保存。注意pcb_modify_track坐标参数有效且保留未传net/layer/width，pcb_create_track先前仍报错，勿反复失败创建。复检compact-cap-fixed-drc-20260927.json仅Connection Error509，无其他类别。三GNDvia没有被报间距违规。509不下降不是无进展：新地via还悬空于无pour板，增加connection对象抵消部分闭合，不能拿总数推出所有电源回路已闭合。

原理图↔PCB163件540padnet仍0差异；最新epro已导出含修复。还需C14第二输出cap、FB/PG、完整电源地plane、USB/NFC线路，DSN要重新导出含19lines/3vias后才能router保护。旧生产包STALE；报价未新全量。


## 新增反馈/输出电容15线2via并发现原生遗漏两段，必须先修复（最新）

本轮新增主源15LINE/2GNDvia完成FB候选走线+R26输出支路+C14。原生桥77ab0a2a DRC只有510connection无clearance，但VREG_FB三pad仍open，不能称反馈完成。native /private/tmp/ruri-feedback-live.epro真实读回审计source33LINE vsnative31，缺VSYS_RUN f9b1f40ef41ed787、FB首段819bc362388b4b8a，报告compact-native-line-roundtrip-20260927.json；native pcb_modify_track FB ID error undefined证实未载入，不应只看source。其余31geometry实际匹配。

已关闭EDA/确认0实例，备份before-line-id-repair.epcb2，将两缺LINE ID改e00000000000a101/a102，几何不变，作为ID解析假设修复，不冒称已通过。下一轮必须native reopen/export全量线geometry compare并DRC；若仍丢，则从原生支持接口/规范ticket排查，不要无限盲改。source最新，epro/DSN旧且两线缺，生产文件STALE。

自动审批拒绝工具pcb_create_track层字符串数字1（未文档支持，可能错误层），未执行该创建。后续用先前验证过原生LINE格式与原生检查继续，未绕过被拒参数；工具创建仍可仅用文档层名称，不能改数字字符串。最新用户允许少数必要paidextended以最低两套总价，不回到strict全免费。


## 原生 UI 补齐两线 + 反馈端点精度修复，实际33/33线路一致（最新）

上一轮定位两线遗漏为progress。本轮ID变更假设经原生export证伪：改ID仍缺2，报告compact-native-line-id-check。桥52073fa2。document_load_from_file严格验证失败489ATTR[21]false期望number；实际仅这些489布尔，规范为0后strict invalidCount=0，仅4FILL未知标签，四孔已独立核为既有Ø2.2/坐标与manifest一致。自动审批拒绝validate=off整体替换PCB（损坏/绕过校验风险），没有执行。安全修正格式后使用warn仍拦无效记录、仅允许已核四FILL，通过自动审查，但SDK返回Failed to set document source；独立stage project_import也Failed to import。前后native导出163COMPONENT/31LINE/6VIA/4FILL相同，确认未清空。不要重试这些本机不支持的source/import SDK路径。

最终通过UI实际成功补线：pcb_zoom_to_board，再scroll([1300,618],up,2)到~2846%U4局部。快捷alt+w未激活，必须布线菜单→单路布线文字。点底栏顶层，再菜单设置起始宽度8mil，U4FB pad屏幕1255,703→旧FBend1180,703；原生导出新增FB LINE e763确实存在。输入宽度24mil，旧VIN横干屏幕1255,478→C12VINpad1263,366，新增原生VIN线。坐标只对当轮视图有效，不要盲复用。

首次UI DRC509中FB仍3open，测得需统一原生端点精度：pcb_modify_track对6旧FB+新UI FB全部startX/startY/endX/endY round(value,4)真实成功，复检compact-fb-rounded-drc-20260927.json仅ConnectionError506，VREG_FB类别完全消失，其他clearance类别无。证明原生浮点端点一致性实际影响连接，不能用source几何重叠推断。以后新增native源码线路坐标按4mil小数并通过native端点回读；既有高精度线路也需按网络规范/检查，不能全称已闭合。

pcb_save/export更新仓库epro263427bytes。source35LINE vsnative33缺的两个旧phantom已由UI新线替代；退出EDA/server_info0后备份before-phantom-line-cleanup.epcb2，从source删除e000a101/a102两虚记录，不动真实33条。check_native_line_roundtrip.py对现main与最新版epro33source/33export/0差异；540schematic-padnet仍0差异。报告compact-ui-native-line-roundtrip-20260927.json。source/epro本轮线路一致，Gerber/BOM/CPL仍STALE。下一步补PG/电源保持/VBAT等与USB/NFC线路，再freshDSN；当前无EDA连接/无router。完整新报价和国产其余电源/音频替代未完成。


## 新小板 Freerouting 已真实启动：PID80029/session19819（最新）

上一轮33source/33native线一致与FB闭合为progress。本轮refresh_compact_dsn.py基于原生DSN真实库，逐553source pads重写坐标（C12两pad移位），以真实33LINE/6VIA重建protect wiring，prepare_routing再次添coil17点protect及46孔/天线keepout，--no-seeds。复核553pad坐标/NET零错。工具只适用当前nativeDSN库，不是通用exporter；下次换封装必须新nativeexport。

保留所有NET声明及padshape，只将GND/ANT_A/B/USB_DM/DP_MCU/CONN七net targets置空，避免unknown-net导致coilwire丢失；157GND/8ANT/14USBpins留给地pour/手工馈线/差分线，不能当它们完成。当前input compact-freerouting-20260927.dsn hash89ee28e9e749e4e7539b432ca78d5f9524beb0c1eba67e199e8d5f1b94b6ea31。

命令/usr/bin/java -Xmx4g -Xss16m -jar /private/tmp/ruri-freerouting-1.9.0.jar -de absolute input -do hardware/routing/latest/compact-freerouting-20260927.ses -mp30 -mt1 -da，日志hardware/review/compact-freerouting-20260927.log。沙箱java launch SIGABRT，escalated实际成功。当前exec19819活着，ps实际PID80029 CPU104.9%，log05:20:40 Starting auto-routing，尚无pass count/SES。初始help invocation16427已terminal0，勿混淆。JavaUI app net.java.openjdk.java/MainApplication被CUA inventory发现但getApp均invalid，所以用本机CLI实际handle/log监督，不需猜UI或重启router。

下一轮先read livehandle+PID/log/SES，不能并行修改EDA布局/电路或再启动第二路由。若pass仍改进继续；停滞需要有pass incomplete计数证据，缺日志不是零进展，遵循crash/gone/time/rate检查。30pass结束查SES保留部分，不直接声称布线完成。SES导入必须去掉与现有protected33lines/6vias相同的返回图元，保留线圈和已有手线；现import_routing.py仅保护ANT且manifest旧，不能原样套。导入前先更新dedup/所有权manifest并备份，再原生导出/DRC。

成本候选constraints同步最新用户允许必要paidextended；其余国产充电/音频未合主，完整新报价未完。旧Gerber/BOM/CPL仍STALE。


### 同轮后续：路由已终止0，已保存SES，不再RUNNING

exec19819最终terminal0，05:22:49 auto-routing completed2m9.29s，optimization9.99s，05:22:59保存SES。log提示最后20pass only18.75 changes改进有限；原30passrun自然完成，不重复未改输入。compact-freerouting-20260927.json已覆盖terminal状态。SES已解析neutral /private/tmp/ruri-compact-ses-neutral.json，尚未导入/审核。下一轮使用真实SES处理去重、保护和网络剩余连接；不要等待已终止进程、勿开第二路由或误读上面RUNNING段。


## Compact SES 实际导入并原生复检失败，勿称完成（最新）

本轮一份SES只导入一次。新工具import_compact_routing.py去重36线路/5via，过滤coil16line/1via，保留33manual/6via/coil，实际追加1284LINE/145VIA，源1317/151；390接点round4并近距sameNETsnap。备份before-compact-ses-import.epcb2。桥ed713f5b原生export1310LINE/151VIA，7源几何未完全匹配（VSYS_RUN一段、3V18五段、SD_MISO一段，其中多段仅0.015mil碎线，不能全冒称丢失或自动忽略）。报告compact-autoroute-native-line-roundtrip。

strict nativeDRC实际1Clearance SMDPad-toTrack（3V18 e1638dadcb303495与J1_5GND仅4mil需6mil），508Connection，compact-autoroute-native-drc。大量按键/普通信号焊盘仍open，不只是预留GND/USB/ANT；必须定位native连接模型/导入精度/实际铜路，不能仅凭routerSES称成功。KEY_UP_N SW1_3/1焊盘中心与源LINE端点误差<0.00005mil；原生pcb_modify_track对e298e80d1926d460设置相同round4端点成功，但复检仍508/KEY_UP4，probe报告，说明仅重复round4不能解决。无需重启router同输入。

原生pcb_save和最新epro导出，带未合格布线仅reviewdraft；生产Gerber/BOM/CPL仍STALE。EDA仍打开已连ed713f5b，下一轮先读状态，离线修改前先关EDA/确认0instance。下一步先读回真实PAD/LINE连接和单net路径，修J1clearance，再恢复地/USB/coil。最新用户授权必要少数换料费器件，按两套完整总价最低比较，不使用strict全免费硬排除；未产生新完整报价，不引用旧价称新低价。


## 0.1mil 全网原生精度修复成功：508→192，间距归零（最新）

前一轮导入读回508error是有效诊断progress。先CHG_ISET六LINE+二via统一round1，native复检该net两error完全消失（总506），证明仅round4或改单线不足。native getNetPrimitives把track坐标报1decimals，getAll却精确原值；需整个网包括vias对齐。继而对实际getAll1310tracks/151via做原生统一0.1mil（跳过ANT_A/B共1via），1460对象逐次成功，报告compact-grid-normalization。最大单坐标位移1.27µm，未触线圈。备份ruri-before-grid-normalization.epro。脚本最初屏幕逃线width字段非schema被忽略，后用正确lineWidth24成功（原31.496，长4.076mil），nativeDRC clearance从1到0。

完整strict复检compact-grid-native-drc：仅192Connection，153GND；ANT_A3/ANT_B3、USB四nets14；3V18六、VSYS_RUN二、NFC_TVDD三、XTAL1二/XTAL2二、I2C_SCL二、NFC_RXN二。多数普通网真实闭合，不再将全部508当router未接。不要重跑相同router。native pcb_save/epro更新283639bytes；163comp540padnet0mismatch。

本机native_modify会自动split/添加超短stub并改IDs，源latest1488LINE vs原生export1277，exactchecker211未匹配；独立长度统计209≤.2mil碎线，只有两长段0ad95ac90d790b65 VSYS_RUN34.45mil与e7bb25c0f113a452 3V18 95.877mil仍sourceonly。不要简单删除211，也不能声称209生产铜覆盖已证明；需铜几何coverage/独立生产文件校验。两个长段与3V18/C12剩余错误相符，是恢复候选，先实际UI补/geometry确认。

尝试原生pcb_create_pour Inner1：按工具描述以L开头invalidpolygon；查本机厂家SDK index.d.ts5260+:必须x,y,L..., 改正后仍无法创建覆铜边框（层字符串兼容问题）。未创建pour、无地plane。不要重试无效相同参数、不要用被拒数值字符串层。下一轮改原生UI或规范源码创建，并native铺铜重建/DRC。保守地pourpolygon已保存在compact-ground-pour-attempt，显式避coil x52.5…88/y0…25.5与ESP天线，既有32regions覆盖孔/天线全层。源R矩形y是上边界，其height向下减，coil区域不是25…50，已核POLYcoil真实x53.2…86.8/y1.2…24.8。

EDA仍打开桥ed713f5b；离线任何修改先close/0instance。下一步地plane+逐GND短线via、两长段补线、USB差分和NFC关键线。生产包仍STALE、完整报价未新算；国产充电/音频方案也未集成，勿称全目标完成。COST-REVISION机械文字已更新当前88×85，早期88×65及y69电池包络作废，实际2000mAh装配仍待选尺寸。


## 原生 UI 实际建立 GND 参考和顶层地铜：192→141，间距仍0（最新）

上一轮round1真实progress。本轮桥ed713f5b保持连接，无离线PCB修改。MCP pour接口字符串层仍不能用；通过UI放置→铺铜区域→矩形成功，底栏点击内层1再画矩形。第一次show56%板框screen1370…1565/y589…777，注意native scroll一页由297%降56%，不可盲用旧坐标。粗矩形画后属性弹窗自动选GND，填全且keepIsland否/8mil；实际输入改为x12.2,topY3334.3,width3440.2,height3322.1mil。UI setValue后需Tab/Returncommit并freshAX；初次宽3555未提交，后右panelsetValue+Return实际3440.2并点重建铺铜区。原生源POUR f47caef3028f89d6 GND_REFERENCE layer15，实际POURED1；DRC190仅connection151GND，无间距。

同样原生顶层绘矩形，属性GND_TOP/layer1，逐项setValue+Tab/freshAX全部确认为精确边界；确认自动生成。源POUR77565b2befeb8b2b，POURED实际2。strict native compact-top-ground-native-drc仅141Connection/102GND，无clearance；真实连上49额外地项。32已有天线/孔禁铜regions未改。内层POURED边界数据内部单位10mil，外边看有禁铜区避让，尚未完整独立铜面积/ARC分析验证，不能称天线保持制造证据已全部通过。主epro315409更新，POUR源矩形实读坐标上列无差异；compact-ground-pours报告。

下一轮继续被top走线割开的GND102项：补短fanout+off-pad过孔/适当缝合，不能粗把via打在所有SMD焊盘中心，禁止直接假定铺铜即全接地。可再做底层地pour，但inner参考层已经存在；查真实top岛/需要短地via的pin。无router活进程，不重跑相同DSN。USB14/ANT6以及3V18/VSYS_RUN/PN7160小网仍需补；两个长sourceonlyLINE缺段仍待实际恢复，209stub需要coverage校验，不能简单删除。原生EDA仍打开单bridge，先关闭才离线修改。生产包仍STALE；国产电源/音频、两套实时报价未完成，目标保持active。


## 原生地缝合孔69个实际完成：141→133；独立禁区检查552项零交叠（最新）

上一轮groundPOUR141未连接是progress。本轮GND_TOP选择状态点击右panel放置/移除缝合孔，原生dialog新增/GND/外径24mil/孔12mil/行列距200mil(5.08mm)，确认后actual getAllVIA220，相较原151新增69个且全GND，GND总74。compact-stitch-native-drc strict仅133Connection/94GND，无clearance。原生pcb_save/epro316054实导出，compact-ground-stitching记录。

独立current native new-via IDs vs before-grid实际151 IDs，逐69via disk检查8个top REGIONS(3ESP RF rectangles+coilrectangle+4screwcircle)552checks0overlap，compact-stitch-keepout-check。R topY减height已用正确，判定包括via外径半径，不仅point中心；其他信号间距通过nativeDRC，仍非全部制造铜避区proof。

查看原生扇出dialog：默认BGA/45deg/焊盘中心/忽略DRC✔，**未执行**，已取消。不应默认对全部SMD中心打via，也不应允许忽略DRC。当前UI69新缝合孔处于多选，右panel不再GND_TOP属性。若要改热焊参数先真正选中POUR边框；已有两POUR原生位置为f47...inner1/77565...top。接下来可核GND_TOP默认10mil thermal gap/10milspoke/制造优化8mil是否令小焊盘难接，局部适当缩小热焊窗口/改局部direct需确认reflow风险；或真实offpad短fanout/局部地vias连接94剩余pins，不能重复全局200mil缝合解决不到的焊盘。

保持全部功能和降本全scope，原国产充电/音频尚未最终合主、两套总报价未完成；生产文件继续STALE。USB/NFC关键手线、两个长sourceonly段仍待补。当前EDA仍开单桥ed713f5b，无router，不准离线PCB写同时开EDA。


## C1 已画地支路，132错误仍报 C1，必须先查真正地连通（最新）

上一轮69stitch/133是progress。本轮readonly离焊盘候选筛选：真实源PAD_NET+placement163bbox，保守所有层非GND铜线/所有pads避让+via disk；C25/C1/C3/C11/C15有候选，C20/C21/C24等0，不能硬放。报告compact-ground-offpad-candidates。不是路径clearanceproof（仅via点）。通过pcb_create_via **omit viaType**成功actual defaulttype0普通通孔，C1候选905.5,944.9mil /24diam12hole，id dac0882335ed3230。重建两地铜后133→132/GND93，但C1依然reported，不能称它接地。

Native UI补真实C1 pad→via10mil LINE 2d898830c3ea73dc，用getAll确认起936.9888189,944.9→905.5,944.9，后modify round1起937，其余未变；复检132不变C1仍在。再次工具→铺铜管理器→重建所有/确认，复检132仍C1，报告compact-c1-rebuild-native-drc。已有真实铜但地连通原因未解，需要查GND reference实际与via/Top island热焊关系，**不要再重复同坐标round/rebuild**。native clearance仍0，未冒称C1closed，compact-c1-ground-branch。新via有一项其它地错误减少，但C1line导致没减少，有诊断证据。

pcb_navigate_to_region left850,right1100,top1050,bottom850仅pan，不改变zoom，别误当magnify。nativeUI scroll屏幕C1小点1455,697up2让56→538%，再1446,691up1到2846%；真实C1ground1440,690/via1351,688，该视图可画短线但下次重看，不能盲复用。菜单单路布线才激活，默认10mil足够。地manager全局rebuild工具入口已知，不需要选POUR边框。当前UI无modal，C1局部2846%，顶层active；bridge仍ed713f5b。pcb_save及新epro已实际更新。

继续全scope：地93、USB14/NFC等39、两个longphantom铜、独立生产一致性和国产电源/音频/最低两套报价均未完成；不投板。不得视暂时复杂为blocked。


## 最新许可与 C1→C2 原生支路诊断（20260927）

用户最新明确：保留功能，少数必要元件接受换料费，必须算出最低总价。按两套全部机贴的元件费+换料费+PCB等完整比较；不再用全免费硬限制排除必要芯片。cost-rearchitecture记录同步；完整新报价尚未取得。

原生新增 C1→C2 Top10mil LINE 324f7820074ef06e，坐标937,944.9→937,866.1mil。getNetPrimitives实际读回新线、旧C1→via支路、普通通孔dac0882335ed3230；C1/C2 GNDpad中心分别937/944.9和937/866.1，与线路端点吻合。新线再次round1后132未变，不能再重复同坐标/rebuild。只读POURED诊断compact-ground-copper-probes用内部10mil坐标与signed ARC端点assert，C1via内层中心/四annulus样本全在GND铜内；这只是点采样，非完整连通证明。

本轮再原生pcb_save并导出最新epro316111字节；strict新复检compact-current-ground-native-drc仍132Connection/GND93，无Clearance。原生地网157pads/18tracks/75vias/330Copper/2Rect。C1/C2实际native pad中心证据上列，C1仍报，而C2不在剩余GND列表；需要独立核对原生DRC连通模型/图元关联/实际铜路径，勿继续盲补重复线。bridge ed713f5b仍打开，Top局部放大，无离线PCB修改。新C1→C2线已保存。

未完成项不变：地网、USB差分、NFC馈线、小网与两个source-only长段；独立生产一致性、国产电源/音频降本、完整两套新报价。旧生产包继续STALE，不能投板。


### 后续只读诊断：原生导出确实保留 C1 两条支线

检查本地桥源read-tools.ts+drc.ts确认pcb_run_drc真正调用eda.pcb_Drc.check(strict,ui,verbose)，非getter旧report。group探测compact-ground-copper-group-probes：Inner1共17铜组，C1via/C1pad/C2pad/U4via样本同属group0；Top313组，C1via在group9，C1/C2pad中心不在fill（可能thermal clearance，不能凭此判开路）。这缩小到原生连通/附着问题，不是明显缺内层地铜。

最新epro几何检查确认C1→via及C1→C2两LINE实际存在（export重新编号e2556/e2557，所以不能凭源ID缺失判丢线）；报告compact-c1-native-epro-presence。原生getNetPrimitives也确认对应PadIDs/coords，未修改板子。本轮进展为证据改变后续检查方向；不要再重复C1坐标/重建。后续检查真实铜连接语义/可尝试保存关闭重开验证，或先处理其他明确缺段与USB/NFC；整体132尚未合格。


## 重载验证发现重大检查不稳定：132→843（最新，覆盖旧132状态）

本轮主工程已save/epro后nativeCmdQ关闭，server_info确认0instance，再重开精确主eprj3、取消启动设置提示、Mainboard加载并ClaudeConnect成功新bridge **8f346c96**。未改任何PCB图元。strict原生DRC重新加载实际843Connection/GND492，无clearance，报告compact-reopened-native-drc。普通CHG_ISET/keys等重新出现，不能再把此前132/多数信号闭合作可靠投板证据。

只读CHG_ISET getNetPrimitives10objects，六线路两via两pad，坐标仍2017.8/472.4→435.8及1847.4/630.6，表面与round1一致；新bridge不表示图元丢失，需查原生连通在modify/重载时差异。下一轮先查此保存重载失败原因，不要再跑同DSN或盲重复round1把计数临时降低当修好。可能需原生重新计算/连接数据重建与导入格式比较，原因尚未证明。

EDA仍打开newbridge8f346c96，同主doc2de8d5754015f9ac；源文件未离线修改，latest epro仍316111草稿。制造文件STALE，真实连通未合格；成本全scope继续active，用户无需行动。

另查两CHG_ISETpad native属性expansionType2/pasteExpansion **-3937**（topSolderExpansion2），形状default31.8×34和11×33.5mil。此值异常需核SDK单位/源ATTR/原生padUI，不可直接判断或盲改全部pad；记录compact-pad-paste-expansion-probe，生产锡膏检查新增明确待办。


## 重载后铺铜重建实降843→444：GND恢复93（最新）

原生工具→铺铜管理器→重建所有→确认成功，再strictDRC compact-reloaded-repour-native-drc **444Connection/GND93**，无clearance；非GND351仍未恢复此前39。重载843中GND492实际330CopperRegion+153SMDpad+5via+4THpad，重建消除399项。因此地铜load初始化的连通数据确需重新计算，不能把843都当physical断线；其他信号pad相连问题还没证明原因。不要靠内存round1后132称制造合格，必须重新保存重载后检查。pcb_save已完成，新bridge8f346c96仍开。

锡膏源核验nativeepro R0603footprint6fc3a9e2015d7e9d PAD e14/e15顶底paste值-3937.008，非仅SDK回报；旧格式与新格式槽位不同，禁止按新NDJSONslot盲改旧efoo。原生UI解释和全板锡膏出口待检，异常记录已补原始证据。

下一步普通信号351对比源LINE/PAD关联和重载geometry，或使用原生UI单网验证并保存重载持续性；仍须降本电源音频/USB/NFC/生产一致性/最低新报价，不停goal。


### 单元件连接刷新排除项：R22 原坐标 native move 无改善

本轮读取bridge track.ts确认modify直接调用pcb_PrimitiveLine.modify(property)，无wrapper单位换算。CHG_ISET两pad DRC位置内部10mil与getter中心mil正确对应：R22_2 201.7848976/47.2440945→2017.848976/472.440944，U3_16 182.08687/59.0551→1820.8687/590.5511。普通线路端点到pad实际仅0.05mil，不能用明显位置错误解释断路。

试用pcb_move_component原位置x1988.188976377953/y472.4409448818898刷新R22（没有移动布局），接口成功、pads e7→CHG_ISET/e8→GND保持；strict再检仍444/CHG_ISET2，compact-r22-pad-refresh-native-drc。因此单component缓存刷新也不能解决，勿遍历全163件重复此动作。pcb_save完成，bridge8f346c96开。

下一检查重点为native UI真实Pad连接/导线显示与SDKsource模型差异、锡膏-3937的原生UI意义；或独立Gerber几何诊断包（必须标明非生产合格）核实际铜。全目标仍未完成，不将单试验失败作为blocked。


## 原生UI确认并实际修复R22_2锡膏扩展（最新）

只读nativegerber export_to_file default失败Failed to export file，无诊断包；未绕过DRC/未发生产文件。定位R22，scroll181→1731%（中心约1458,697），原生pad边缘单击1478,678选到PAD（doubleclick是开始布线需Escape两次取消，未加线）。UI确实PAD2/netCHG_ISET/31.8×34mil/x2017.8/y472.4，阻焊助焊自定义，阻焊2mil、**助焊-3937mil**。确认并非SDK sentinel回报，是真异常属性。实际UIsetValue助焊0mil+Return，freshUI显示0mil；pcb_save和latest epro导出完成。报告compact-pad-paste-expansion-probe补nativeUI证据。

修复范围仅R22_2，另一R22pad以及大量其他库pad还待全板统计/原生修改。不能冒称全板锡膏修完，也不把paste错误当444连接原因（未证明）。SDKnativegetterglobalID与UIid表现不同（R22padUI e196e7），要通过nativepad实际属性读回再批量改，不凭重编号epro IDs修改。当前EDA8f346c96开，R22PAD选中，1731%Top；下一轮freshAX再操作。


## 全库锡膏异常统计完成（实例仍待修）

最新epro footprint oldPAD索引19/20为top/bottom paste（注意不是20/21，21是下一槽），根据R22UI校准。全库306pad：143跟随规则null/null，104零扩展0/0，34为-3937/-3937，22为-3937.008/-3937.008，另3为-100/-100待单独核是否封装专用。异常<-100共56库pad，关联主板66个component instances，compact-library-paste-expansion-audit含完整名单。这是library-based潜在affected统计，实例R22单pad已有override修好，不能说所有这些实例都未修/已修。专用散热开窗要保留，不能全改所有paste为0。

下一步通过原生属性覆盖这些异常pad或规范更新56库pad+同步真实封装（离线必须关EDA），再export实例paste及锡膏文件复核。当前8f346c96仍开，无本轮PCB修改，连接444仍未通过；完整降本/报价/生产scope继续。


## 56库pad+1实例pad锡膏源修复已落盘，需重开验证（最新）

EDA实际关闭server_info0。备份/private/tmp/ruri-before-library-paste-repair.epcb2。仅FOOTPRINT doc PAD topPasteExpansion/bottomPasteExpansion<-100mil改0，共114fields/57pads：此前epro56库pads加R22 UIoverride生成doc2de8d5754015f9ac_95d45bb3fce2ce56内另一未修pad1。初始assert预期112发现114，在写入前中止，随后只读定位额外instancepad，确认后修复；没有盲增数量。几何/网络/阻焊/特殊FILL窗未改。报告compact-library-paste-repair含逐项。

下一轮重开精确主eprj3并新bridge，native export统计库和instancepaste确认，再重建地铜及DRC；旧bridge8f346c96已断。当前source已修，不得把旧epro315689称包含本次批量修复，它待重新导出。生产仍STALE，连接444未解决，完整scope仍active。


## 批量锡膏修复重载验证部分生效，新bridge84c190a1（最新）

精确主工程重开并导出latest epro315770bytes。native库306pad分布143null/null、3 -100/-100、156zero、**4仍-3937.008**。剩余两个库R0603 6fc3a9e2015d7e9d与cdcb5e0533824b1a每库2pad：说明库export仍有旧版本，源epcb2已经无-3937，仅源更改不能证明native所有实例修完。报告compact-paste-reloaded-native-verification verifiedfalse。其他52库pads已nativeexport变0，不能全盘否定也不能称全修好。

下一步查实际instance paste/API/本地project元件库原始封装，区分unused原始库和主板引用版本。新bridge84c190a1开、doc2de8d5754015f9ac，重载后的地铜仍需native重建（尚未本轮DRC复检）；勿使用旧444/132当当前验证。降本/信号/制造/完整报价未完成。

同轮actual CHG_ISET native两pad R22_2/U3_16均paste0，GND157pad分布{'0': 142, '-3937': 14, '-100': 1}，<-100异常14。compact-paste-instance-probe仅这159pads证据，不支持全板540pad合格；库4旧值与instance已0可能原始未用版本，需完成全实例枚举。


## 全553原生pad检查+114SDK修改：读回零异常，但持久化未证明（最新）

pcb_get_all_primitives typepad实际553pads（包含componentpads），114bad paste<-100；报告compact-native-all-pad-paste-audit。SDK原始属性为solderMaskAndPasteMaskExpansion {topSolderMask,bottomSolderMask,topPasteMask,bottomPasteMask}。试改单pad5a2df9411e662f97e7值0读回成功，继而临时脚本ruri_fix_instance_paste.py逐114pad改仅异常paste，逐项返回值验证，全部成功，fresh getAll553pad异常0。pcb_save/epro导出已调，但export仍315770bytes，旧库-3937仍存在：**SDK读回零不是持久化证明**，报告status已改SDK_READBACK_ONLY_PERSISTENCE_NOT_PROVEN。不得称全114已落盘合格。

调查官方本地SDK index.d.ts：IPCB_PrimitivePad.done()注释将更改应用到画布，componentPad.done()也支持，而目前bridge document.ts pcb.modify.pad只return pcb_PrimitivePad.modify，没有调用.done()；trackmodify同样。这可能解释多轮修改读回/DRC变好但重载恢复。尚未验证，不可断言rootcause。必须优先补规范commit验证或nativeUI提交，禁止再靠SDK读回计数声称制造可用。现tools无done/eval入口；有document_set_source但之前加载失败/禁止绕格式验证。安装扩展更新仍需遵守现授权和电脑操作规则，不擅自安装来源不明软件。

新bridge84c190a1还开。下一轮应以原生UI抽查实际badpad是否变0/是否source产生override，或在已授权桥源码按SDKdone规范准备修复并验证；整体电气/成本未完成。


## SDK显式done提交补丁已准备并构建，尚未安装/实机验证

本地bridge源码document/track/via三个modifyhandler现加await primitive.done()，未触其他操作/权限；patch仓库hardware/tools/bridge-patches/commit-pcb-modifications.patch，diagnostic /private/tmp/ruri-easyeda-commit-fixed.js构建成功。Mock三handler每次done恰好一次、undefined不done共6检查通过。报告bridge-commit-patch记录SHA和限制。原装liveextension未更新，所以本地改源码不会自动影响当前bridge。

下一步需要将这项现有扩展更新装入EDA，然后用单pad/单track实际source/epro/save-reload验证，才能全量重放必要修改。明确不是已证明rootcause，勿写“已修好桥接”或“114pad已持久化”。前SDK读回零依旧未证实。新source只/tmp原已安装repo，真正板源暂无本轮变动；live84c190a1仍开。


## 本地扩展修订包完成，安装确认待回复（最新）

/private/tmp/easyeda-agent_v1.1.6-local-commit.eext由已安装原1.1.5包保留全部资源/UUID/权限、仅换已构建dist/index.js，manifest1.1.6并description明确Localcommitfix非upstreamrelease。桥补丁三个modify显式done，未其他权限。原包保留。bridge-commit-patch记录packageSHA。电脑UI非官方修订包安装前action-time确认要求适用，已async向用户询问允许更新并验证或继续原生UI；**未安装**。用户此前同意的是原1.1.5，不能把此次修订包安装当再次获批准。等回复期间可做独立只读/原生UI/成本检查；别声称blocked，勿擅自安装。live84c190a1仍运行原扩展。


## 等扩展确认期间独立功放国产候选核对

原生桥仍未更新，pending安装确认没有回复，不视goal continuation为批准。继续独立成本选型：纳芯威NS4168/C910588原厂产品页https://nsiway.com.cn/list_40/138.html确认I2S单声道功放，JLC官方目录https://jlcpcb.com/partdetail/Nsiway-NS4168/C910588标Extended/ESOP8EP。尚无大陆免换料费、实际库存价或全pin规格放行；未改U7或谎称省钱。候选报告ns4168-cost-candidate含来源和成本比较公式，必须算移除旧feeder费与增加新费差，不仅凭国产名/芯片价选。原厂家细节页大量图片，无text完整电气数据；JLC下载signedPDF链接工具fetch失败，别重复过期链接。待取得原厂PDF及大陆真实SKU报价再决策。


## NS4168大陆实时价/fee核对有证据（最新）

CUA现有iabtab2 ampCostTab搜索NS4168成功3SKU；免换料费筛选只有否，C910588 Nsiway ESOP8EP扩展库，1+ **4.53元**/10+3.7/30+3.28，真实公共库存**7629**。邮寄专用C9900199618排除；C5246378价/库存未读，不假定更便宜；private共享不是publicstock。tab2已markHandoff，下一轮沿该tab继续。候选ns4168-cost-candidate已记录大陆观察值。

对比旧MAX8.09参考，两块纯材料条件省7.12元；若新增20换料费且旧fee未移除则不划算。必须用实际旧新feeder差费+外围比较，旧MAX价格需新查；不能称已选/已省。原厂镜像PDFwebopen超时，厂家产品详情图片链接已读，无完整pin电气核算。可继续prim厂家图或JLC详情datasheet。扩展安装确认尚无回复，原bridge84c190a1不变，115padSDK读回不等于持久化。


## 功放旧新实时两套比较成立：条件材料省7.12（最新）

nativeU7name MAX98357AETE+T确认，supplierId投影未返回所以通过型号检索大陆JLC。CUA ampCostTab现MAX查询：C910544 ADI/MAXIM TQFN16EP1+8.09元、公库存28697，扩展库免换料费只有否。和C910588 NS4168已核4.53两者均paid：若移除旧料种换料费且加新种同额，差费0，两套芯片16.18→9.06条件省7.12，不再错误额外加20。是否实际remove/add须正式quote确认；外围/供电改造未核，没有选定/合主。报告ns4168-cost-candidate同步旧SKU实时证据。

注意NS4168候选输入VIH需原厂完整规格，若0.7VDD则当前VSYS_RUN供电不能直接假设ESP GPIO全条件驱动，应核3V18供电方案及总稳压负载，防止电路省芯片却加贵电源件。不得擅自降功能。下一轮确认datasheet及供电、mic替换；扩展安装确认仍待用户，不视自动goal消息为批准。iabtab2已handoff currentMAXsearch。


## NS4168原厂PDF逐脚电平核对完成，仍未放行替换

镜像厂家PDF下载成功2,481,578bytes，Apr2023 V1.2，pypdf提取并视觉核对p2引脚、p3极限、p4电气。pin1CTRL/2LRCLK/3BCLK/4SDATA/5VoN/6VDD/7GND/8VoP。VIH0.7VDD明确，不能VSYS_RUN直接替换。3V18供电候选待稳压负载/瞬态/ESP VOH和声音功率核算，不能只为7.12元材料差贸然改供电。p3极限2.8..5.0与p4工作3..5.5冲突，视觉确认非OCR，绝不凭p4用5.5；EP表未给，须另核。p9典型100uF+1uF外围成本须计。报告ns4168-cost-candidate已更新并清理旧价格未验证的陈旧文字。未改主原理图。

最新用户明确保留全部功能，少数必要付费料可接受但须算最低两套总价，覆盖旧strict fee-free目标文字。扩展修订安装确认仍未回，不能擅装；有独立成本/电路工作所以不blocked。生产STALE，当前有效连接444而非132。下一轮继续电源总预算/音频候选、原生持久化排查和真实报价。


## 当前原生音频供电更正及固件关键文档同步

重新运行check_export_pin_geometry当前epro：163件354项0对应错误，报告current-doc-pin-audit。明确U7.7/8=3V18、MIC1.5=3V18；此前NS4168候选假设旧功放VSYS_RUN错误，已纠正报告。共享电源静态GPIO VOH0.8VDD vs NS VIH0.7VDD有0.1VDD名义裕量，厂家S3原始datasheet链接记录；不得据此放行全温动态。NS候选仍需3Vmin瞬态/负载、EP和100uF外围成本。

发现POWER/PINOUT文档仍写旧U2/U5/LTC2954，更新两份按实际导出对应GPIO16 RESET/8 AMP_ENABLE/18按下高/21保持高，共用SPI，固定充电EN/MODE和分立开关机；删除失效6.46秒强制定时说明。未改主EDA或安装扩展。下一轮继续真实音频选型与保存持久化；国产NS8002+PWM方案仅找到原厂产品和Esp官方S3 PWM音频支持文档，未核SKU/fee/手册，不算已选方案。安装确认仍待回，生产未放行。


## 原生UI同值提交R2.2：旧格式导出已变化，重载仍待核

CUA实际R22.1GND paste0；R2.2USB_DM_CONN paste0（前SDK内存值），对R2.2原生属性助焊字段0 Enter、CmdS提交。project_export_file须显式fileType=epro，否则导出epro2/epru455945不可直接比较。旧格式新导出/tmp/ruri-native-pad-ui-commit-v1.epro315935（旧315770），差异报告native-ui-pad-commit记录；尚未重开，不称持久化。当前UI选R2.2约700%视口，工程开、bridge原84c190a1。下一轮先核报告INSTANCE新增字段/PCB diff，保存后精确重开同工程验证该pad以及全部114，不能擅装pending修订包。主latest epro未替换，生产STALE。


## 原生单pad保存重开验证完成：R2.2落盘，余113bad

CmdS后立即CmdQ曾提示未保存，选择留在页面没有丢弃；原生文件→保存全部并观察星号消失，再CmdQ退出成功，精确主工程重开，旧扩展重连cbc92750。freshall 553pads，<-100异常113。R2.2(895.8,1122)读回0，说明原生UI同值提交真正落盘；其余SDK批量不能认定已保存。新临时epro315973 /tmp/ruri-pad-reload-ui-commit.epro，repo latest尚未替换。报告native-ui-pad-commit更新singleonly。下一轮可原生UI选bad全部批量属性提交（需校验选择范围保留天线-100），或等修订扩展确认后明确done。DRC需重建地铜后刷新，不引用旧444作新验证。仍无可生产包/新报价。


## 113异常pad实例专用封装修复已写磁盘，待重开验证

原生Find焊盘含/等于负3937mil以及无条件都没选任何内部pad，撤销筛选未改板。查实际epcb2，两个R0603库+已有R2副本引用57组件对应113bad。EDA原生CmdQ退出确认Appquit后安全离线：保留全部原始行及删除tombstones，不重写失活数据；56组件复制原Footprint文档为main_doc_component_id并改Footprint属性，R2已有副本补剩1pad。仅<-100paste改0，solder/几何/network/特殊FILL保持，ticket新增不重用，原库保留。脚本/tmp/ruri_clone_bad_instance_pads.py断言57组件113pad通过，备份/tmp/ruri-before-instance-footprint-fix.epcb2，报告instance-footprint-paste-repair reloadpending。首尝试parser碰到tombstone停止在写入前，后用保原始行方案，未损失旧数据。当前EDA退出，桥cbc92750已断。下一轮精确主eprj3重开并新桥，fresh553pads bad应0且三-100保留；保存再重开第二次验证以及导出网表/几何一致后才可更新repo最新epro。当前生产仍STALE，不称113已完成持久化。pending修订扩展仍未获回复，未安装。


## 113锡膏异常已两次保存重开验证，latest epro更新

第一次重开桥e5c17a20全部553pads bad0；与前113bad snapshot比较，仅允许的226paste字段变化（113pad两面），网络/坐标/padnum/solder无任何其他变化。12个实际实例-100保持，之前3是库pad数不能误说只3实例。原生save观察后CmdQ退出再次重开，桥127bd528，fresh553属性与第一次全部相等，bad0/special12。导出旧格式epro320770已更新仓库hardware/eda/Ruri-Passport-RevA.epro；关键引脚163件354项0错报告instance-override-export-pin-audit。仅锡膏缺陷关闭，不把原始unused两库4bad作为实例仍坏，不算布线/ERC/生产放行。桥修订包仍未安装/未获回复，当前原桥127bd528运行。PCB重载尚未重建地铜/DRC，本轮不引用旧444作当前计数。下一轮重建所有地铜并freshstrictDRC，然后解决实飞线和信号问题；成本选型报价继续，生产包STALE。


## 锡膏修复后地铜重建严格DRC：444连接+1网表差异

原生Tools铺铜管理器重建所有并确认。fresh pcb_run_drc strict/ui/verbose：Connection444/GND93，同原有效数；额外Netlist Error1。报告paste-fixed-repour-drc。原生Design从原理图导入变更只读预览显示增加R1/R3/R4/R5/R6/R7/R9共7元件，不是57专用封装差异；已取消未自动同步，避免重复件。savedsource vs prior schematic-current.enet checker163件540padchecks0mismatch，但旧ENET不足证明当前native associations。下一轮务必检查fresh native全工程ENET、这7件UniqueID/ConverttoPCB/器件footprint属性和PCB继承属性，明确为什么原生判missing，再同步。不要把0mismatch当全板通过。铜仍未修，锡膏553bad0已两次核验维持。当前桥127bd528/PCBdoc2de8d5754015f9ac，EDA打开，禁止离线改板。重建后未再覆盖latest epro，repo320770仍是此前二次锡膏核验导出。生产STALE，报价未更新；goalactive，未安装pending扩展。


## 新鲜原生全板ENET取得：排除7电阻Unique/Channel差异

此前MCP sch_get_netlist Core请求45000ms超时，未重试同一路径。改用原生导出菜单，范围Board1:Mainboard，专业版ENET，成功导出/tmp/ruri-native-sync-current.enet 365635bytes，原生日志致命0/错误0/警告1（L1/U1/J1属性供应商不匹配）及J1机械焊盘信息。更新schematic-current.enet；fresh-native-sync报告163PCB件540pin-net检查0差异，仅网表和采购属性对应，不证明布线通。七电阻及对照R2逐项Unique ID、Channel ID、Device与新鲜ENET完全一致；PCB专用封装引用与原理图原R0603引用不同，但R2也相同模式且没有被判新增，所以不能凭这点断言原因。fresh-native-seven-resistor-associations保存8件证据。同步新增7仍未应用，未放重复元件。下一步检查原生导入匹配设置和实例隐藏关联/删除记录，或只读对照原生导出关联；EDA当前Core页打开，桥127bd528，勿离线改活动工程。444连接/1网表提示仍未关闭，生产包STALE，报价未完成；扩展修订包仍未安装。


## 原生同步预览及实例封装来源差异进一步排查

PCB当前DRC UI445=444连接+1网表。点击导入更新后只读预览仍仅R1/R3/R4/R5/R6/R7/R9增加；对话框分组动作/对象、包含设计规则、同时更新导线网络、优先库工程系统，没有显示身份匹配选择。再次取消，未同步重复件。源COMPONENT直接记录Unique/Channel/DeviceName与fresh ENET一致。发现native UI生成R2实例Footprint META.source=原封装uuid|当前projectId，离线复制实例保留原库外部source；全58专用副本中56存在这个差异，R2/R22原生创建匹配。异常7不是唯一不匹配者，因此此来源字段只能作为待验证假设，不能认定根因。全实例证据instance-footprint-source-associations-20260927.json保存。下一轮可关闭EDA后备份，仅7副本META.source按原生惯例修复做最小实验，重开预览及DRC并验证锡膏/几何；若无效应恢复，不全量猜改。当前EDA主PCB打开，禁止直接改epcb2。原扩展仍127bd528，更新审批待回复；生产STALE/报价未更新。


## 七封装来源最小实验已写入并原生重开

原生CmdS确认后CmdQ Appquit。备份/tmp/ruri-before-seven-source-experiment.epcb2，仅7副本META.source改为fresh ENET原封装uuid|项目uuid，报告seven-source-experiment；未动geometry/paste/network。离线sync163件540pin0差异。重开主工程（启动短暂SQLITE_MISUSE文本随后正常进入主页，不当terminal失败），recent明确repo路径，取消非必要prefs，主PCB成功加载。Design从原理图导入变更已点击，最新UI0%处理，预览结果待下一轮读取；不能称修复有效或无效。当前EDA主PCB打开，旧127桥已随退出断，新桥待读取。若7仍新增，先关闭EDA恢复备份再继续其他原因，不保留未证实实验作为制造结果。生产STALE/444前计数未刷新；不安装pending扩展。


## 七来源修复原生实验有效，剩49同规则源修复待整板重开

本轮fresh UI确认导入预览原7 R1/R3/R4/R5/R6/R7/R9完全消失，新增显示下一7 R10/R15/R16/R17/R18/R19/R20，未应用。seven-source-experiment记录原7消失；支持META.source关联问题，但未全DRC证明。取消预览，CmdQ明确Appquit。备份/tmp/ruri-before-all-source-repair.epcb2；依据原生R2/R22 source惯例，剩49封装副本仅META.source改为fresh ENET原footprintuuid|projectId，断言49，已有7及原生2不重复改。报告all-instance-source-repair待reload，sync163件540pin0对应错误。当前EDA已退出，勿用旧桥127；下一轮直接重开精确repo工程，原生Design导入预览应无新增，若仍有差异继续查，不擅加duplicate。然后fresh553pad paste audit、repour+strictDRC及latest epro导出；尚未做，不能声称1网表错误已关闭或444连接减少。旧epro320770未含来源修复。生产STALE，报价及降本仍待，扩展更新未装未获确认。


## 全来源修复重开验证：原生网表错误已消失

本轮source diff与七实验前backup逐行对比56 META.source变化，其余每条含tombstones完全一致，all-source-only-diff证据。精确repo重开PCB成功，AltI处理后未出现新增预览。原生Design检查DRC刚返回0/50%是中间态，未采用；完成后fresh UI全843=连接843/GND492，**没有网表错误**，旧1网表差异已关闭。当前尚未重建地铜，不能把843与上轮postrepour444比较或叫线路恶化；下一轮Tools铺铜管理器重建所有确认后严格DRC应核真实数。原有Claude Connect成功新bridge1aff846c（无需扩展更新）；主PCB打开。需native553pad重新核paste、latest epro重新导出包含56source；旧epro320770尚未更新。当前报告all-instance-source-repair状态RELOADED_NATIVE_NETLIST_ERROR_CLEARED。生产STALE、降本/真实quote仍未完成，未安装pending本地扩展。


## 来源修复后原生repour+fresh严格DRC与全pad验证

原生Tools铺铜管理器重建所有等待进度消失、确认完成；fresh strict/ui/verbose pcb_run_drc已完成，报告source-fixed-repour-drc详细分类{'Connection Error': 444}。553原生pad重新读出，异常paste0，特殊-100共12保持，报告source-fixed-pad-audit。来源修复未破坏锡膏。现live原桥1aff846c/PCB2de8d5754015f9ac；工程打开，禁止离线改。下一步按fresh DRC实际对象修线/回流，勿再查已关闭META.source网表问题；latest epro320770尚未包含来源修复/repour，需后续保存并显式epro导出。生产STALE，fullquote未更新，扩展pending未安装。


## 当前铜线覆盖核查及最新版epro更新

fresh native tracks1278；multiPad且无track网络7：ANT_A/ANT_B/USB_DM_MCU/USB_DP_MCU/USB_DP_CONN/USB_DM_CONN/NFC_RXN。天线需包括poly/via/pour，不能凭无track叫完全未布。NFC_RXN native2pads2679.1,1368.1和2846.5,1141.7，track0，savedsourceLINE/VIA/POLY也0；是真未布，非rounding端点问题。四USB无tracks需专门差分布线；其他网络大多有tracks待断点/过孔定位。报告current-unrouted-network-inventory。显式fileTypeepro导出/tmp/ruri-source-fixed-latest.epro320683bytes成功，更新repo latest epro，随后check_export_pin_geometry报告source-fixed-export-pin-audit。这是工程检查点，不是生产包：strict444连接仍未修、制造STALE/fullquote未完成。下一轮针对NFC_RXN短模拟接收连接及USB专线布局，先查邻近障碍/尺寸，再原生或有commit可靠途径布线并freshDRC，避免只导出列表。桥1aff846c/PCB2de8d5754015f9ac打开，扩展更新pending未装。


## NFC_RXN局部几何路径检查：顶层候选未找到，未强行补线

fresh原桥1aff846c读全部553pad几何/1278track宽度/221via位置，缓存/tmp/ruri-routing-pad-shapes.json、ruri-routing-track-shapes.json、ruri-routing-vias.json。NFC_RXN U8实际pad11.4x35.4 rotation90坐标2679.1,1368.1，C46另一pad31.5x35.4坐标2846.5,1141.7。局部2.5mil网格顶层A*考虑所有异网pad旋转保守bbox、track宽度、via直径，6mil线宽5milspacing（障碍8mil及track/via额外step裕量），窗口x2500..3100/y1000..1550；两个端点均未blocked，但无顶层路径。首次遇POLYGON pad形状停止未写，改保守世界bbox后完成。报告nfc-rxn-routing-candidate NO_TOP_PATH_IN_LOCAL_WINDOW；工具plan_nfc_rxn_local_route.py保留复现（依赖/tmp输入，非通用正式router；未考虑poly/keepout，原生DRC仍必要）。未创建短路线，无DRC减少可宣称。下一步优先观察接收C46/U8周边、移动C46缩短模拟接收线并保持其另一net/GND，或规划安全topescape+inner换层再原生commit+Drc；勿反复同局部planner求相同解。总体strict444连接、生产STALE/报价未完成；工程打开，禁止离线改活动epcb2。


## C46接收电容移位候选已完成pad/track/via碰撞预检

当前C46另一端不是GND，是RF_RX_A，有多段现存线路含原pad2901.6,1141.7→2927.6,1141.7。不能只移动后留下RF_RX_A断连。构造30个近U8位置，两pad5mil间距bbox检查仅3候选2750/2755/2760,y1375通过pad；随后对这3实际Toptrack宽度矩形交叉及via圆边距预检，结果写nfc-c46-placement-candidates-20260927.json。未移动元件，未创建线路，不称DRC已减。下一轮读取候选trackConflicts/viaConflicts；仅全部无冲突者再核body/keepout并计划短RXN/RF_RX_A接线，若冲突需要调整局部铜线而非盲移。当前live1aff846c/PCB打开，strict444连接/生产STALE/fullquote未完成。

## NFC_RXN两端逃逸与内层候选几何检查（未应用）

候选过孔2703,1368.1和2810,1141.7，16mil焊盘/8mil孔此前全层track/via和矩形pad无冲突。新增两端6mil线宽/5mil间距引出检查包含POLYGON保守bbox，0.09125mil最大采样步距，异网pad/Toptrack/via冲突均0，报告nfc-rxn-escape-check。内层16局部A*找到路径，但有较多2.5mil阶梯，应先做连续线段可见性简化，再核实际内层铜和native DRC，不直接照抄阶梯。

读取原生32个region实际complexPolygon和SDK枚举，5NO_WIRES/6NO_FILLS/7NO_POURS/8NO_INNER_ELECTRICAL_LAYERS。NFC region16为R2078.7402,996.063,1366.1417,976.378。原生R坐标是xMin,yMax,width,height（add_antenna_keepouts.py明确），实际y19.685..996.063；路径y>=1141.7在外。初始误读yMin导致错误拒绝，已立即更正报告与用户说明，未改电路。nfc-rxn-inner-routing-candidate状态CANDIDATE_PENDING_ESCAPE_AND_NATIVE_DRC，保留坐标解释和依据。

没有创建铜线/过孔，没有新增DRC合格或连接减少证据；当前444连接仍有效。下一步读取pour/fill实际几何及create/delete可靠持久化方式，简化内层候选后备份、补线、strict DRC和保存重开验证。主工程打开、bridge1aff846c；扩展修订仍未安装。最新epro工程检查点可用但Gerber/BOM/CPL仍旧，完整报价未完成。用户起床状态回复已坦承未完成/未达预算；继续优先实际修线和可落实降本。

## NFC实际试布、制造规则失败并撤回

create_track桥metadata虽标layer string，实际传TopLayer或字符串1均失败；数值layer1/16成功，未安装扩展修订。两16/8mil试过孔及三6mil短线实际创建，先repour后DRC442Connection+2Physical，规则孔径最小19.7/11.8。不能据442称完成。删除试孔换20/12后repour并CmdS，strict449=4Clearance+445Connection。标准过孔U8端到TVDD/RXP线只有5.8mil，实际规则要求6mil（此前几何预检5mil低于原生规则）；另外两项须读取nfc-rxn-trial-drc完整证据。立即成功删除全部3track和2标准via，原小孔已先删除。需再repour/save/freshDRC验证恢复444，再规划移动U8侧TVDD/RXP局部段或更外侧过孔。新铜没有验收，不能保留原报告候选合格状态。已得到创建工具数值图层参数和真实6mil及标准孔径约束，后续规划按6mil间距+20/12mil过孔，不能改规则迁就线路。当前工程已撤回试铜但还未repour/save确认恢复，下一轮优先完成此步，不直接导出生产包。latest仓库epro未覆盖，仍此前320683工程点；成本报价未完成。

## 失败试布完全撤回后严格基线恢复、标准孔候选扫描

原生重建所有地铜完成、确认、CmdS，fresh严格DRC恢复仅Connection444，没有Clearance/Physical/Netlist；报告nfc-rxn-restored-drc证明撤回完整。进一步读trial四间距问题：U8端标准孔同时与TVDD/RXP铜线5.8mil及邻pad5.3mil（规则6），不只两条线。必须按pad+track一起解决，不能简单微移坐标。

全层pad（包括polygon bbox）、track实际宽度、via圆检查20mil外径/12mil孔、6.25mil间距保守候选：U8附近x2705..2770/y1350..1380零合法孔位；扩展x2699..2859/y1300..1450后最近2751,1428，已到RXP线下方，不能直线引出穿越RXP。C46端2810,1141.7标准孔预检通过。报告nfc-rxn-standard-via-candidates。下一步应局部重构U8接收/TVDD引出或整体NFC匹配布局，而非在U8邻pin间硬塞不合制造规则的小孔。原生create_track数值layer1/16可用，不再反复尝试字符串。现工程保存、旧原桥1aff846c/2de8d5754015f9ac，NFC_RXN仍未布，生产STALE/报价未完。新增缓存脚本/tmp/ruri-rxn-standard-via-scan.py及wide版本，仅诊断，非生产路由器。

## NFC局部改线已应用：无新增间距/物理错误、RXN错误0

新方案保留TVDD/RXP原宽7.874mil，仅在U8右侧少量绕开；RXN6mil引出2706,1368.1标准20/12milvia，Inner2直连2810,1141.7via再Top接C46。6.25mil保守预检新pad/track/via全无冲突。按数值layer创建17新primitive后删除旧6段，但原生自动在交点分割了旧线，原ID删除并不包含新fragment！fresh严格DRC4Clearance指向残余旧段。通过native精确坐标读回确认e37bb0822c435434/e1ae7efbdf653b1c/dc083ed8889a93f4/76f02c6ee3567256四段仅为被替代的旧路径，成功删掉，不是任意删functional线路。

原生repour后clean严格DRC仅Connection443（此前444），无Clearance/Physical/Netlist，全DRC叶项中NFC_RXN出现0。报告nfc-local-rewire-application和nfc-local-rewire-drc保存。注意未重开验证持久化，不能称线路最终验收；GND repour影响连接数所以不按差值推断全部NFC完工。原生CmdS后导出/tmp/ruri-nfc-rewire-latest.epro320896，关键pin检查163/354/0通过，更新repo最新epro工程检查点。生产Gerber/BOM/CPL仍STALE，完整报价未完。

下一步先关闭/重开工程验证NFC新线实际落盘（create正常保存但不能凭内存断言），repour+strictDRC，再处理USB差分四未布net和其余443飞线；国产音频电源成本重构仍未完，不能只盯单线。当前EDA打开bridge1aff846c；扩展修订未安装。

## NFC新线原生保存关闭重开验证通过；USB布局缺陷定位

原生CmdS后CmdQ明确Appquit，重新启动EDA，Recent明确repo主eprj3，取消非必要偏好，双击Mainboard PCB，原Claude Connect连接。fresh NFC_RXN仍有三段6miltrack（Top2679.1,1368.1→2706,1368.1 / Inner16→2810,1141.7 / Top→2846.5,1141.7），两20/12milvia都保持，nfc-local-rewire-application记录REOPEN_VERIFIED_POST_RELOAD_DRC_PENDING。最新epro320896已在上一轮导出，通过163/354关键pin检查；本轮只验证落盘，不称重载后DRC已通过。下一步仍需repour/freshstrictDRC，旧443是保存前有效计数，不假设重载后相同。

USB pad inventory记录四网实际pad坐标（来自先前native snapshot，下一轮移动前务必fresh确认）：串阻MCU侧DM836.5,1122距U1USB_DM856.3,895.3=227.56mil/5.78mm，DP836.5,1220.5距U1USB_DP856.3,945.3=275.91mil/7.01mm，间距与路径不对称。USB-C及ESD在x1700..1762,y289..388。需要按S3官方布局要求先将串阻挪到USBpins附近并核机械/pad/铜线，接再布差分对，不能用一般autorouter随意分别走。主bridge已重连，旧1aff846c失效；下一轮从list_instances读取新id。工程打开禁止离线修改活动epcb2。成本和生产文件继续未完成，不claim成品。


## USB官方布局约束和新鲜元件几何核对

重新读取native R2/R3/C4/C5/U1/D1/J2组件和全部553pad，USB坐标与前snapshot一致。Espressif官方最新PCB设计/原理图清单核实USB串联22/33Ω及可选对地电容靠近芯片，差分阻抗90Ω±10%、平行等长：https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html 与 schematic-checklist.html。绝不凭6mil线宽称阻抗达标，需嘉立创实际4层stackup。

R2/R3期望与U1 USBpin同y895.3/945.3，但U1右边已有两颗去耦电容：pad x937/992.1，y866.1/944.9，不能直挪近pin重叠。保持现两去耦位置，两个R0603水平6.25mil pad clearance共同最近候选centerx1060，MCU pad间距174.05mil/4.421mm、两路对称；相对现5.78/7.01mm缩短但仍需track/via/body/keepout和实际差分线空间审查。报告usb-series-placement-candidates，尚未移动；不能称已改善布线。原bridgecomponent.modify仍无done，下一轮优先原生UI位置提交或关闭工程安全离线按几何移动并重开，别用内存读回假保存。最新bridge0dbd7e7b/PCB2de8d5754015f9ac。

NFC.md同步删除已移除XL9535共享描述，澄清3V18随硬关机断电。NFC新线重开已验真，postreload repour/DRC仍待做，不称443fresh。完整成本报价和生产导出仍未完成。

## USB铜线候选被3V18支路占用；NFC重载DRC端点失败须优先修

fresh全部track/via核USB候选1060..1085两个电阻pad位置，均冲突3V18两31.496mil支路：e69c68113212c401从992.1,944.9→1029.9,944.9，ebfa6ccded51f484→1089.2,1004.1。不能只pad检查后搬器件。未移动USB元件，报告usb-series-placement-candidates更新PAD_AND_COPPER_CANDIDATES_NOT_APPLIED。需要调整局部电源支路和USB通道或更合理整体布局，勿拆掉去耦/缩细电源线硬放串阻。

完成NFC重载后repour+save+strictDRC，结果Connection444，无Clearance/Physical/Netlist。但对照保存前443，新增对象含NFC_RXP U8_16、NFC_RXN U8_15和C46_1；RXN错误2！不能把线仍在当作已经接通。报告nfc-local-rewire-reloaded-drc和application postReopenAddedConnectionDetails。上一轮只fresh内存DRC_RXN0，重载后端点精确坐标/原生保存连通关系有问题，优先解决此问题再继续USB。工具get_all pad坐标只有1位小数可能是序列化舍入，必须读原始Footprint PAD与组件原点旋转得到真实global坐标，不再用round过端点画线。modify旧SDK缺done，改端点应delete/recreate或原生UI，create数值layer可靠。工程打开，不能离线改活动epcb2；可只读源推导。最新repo epro320896是未经重载连接放行的工程点，生产仍STALE。明确用户说明接收线未最终修好，避免误报。bridge0dbd7e7b。

## 原始焊盘精确中心已修正，剩余RXN错误转到via

只读epcb2组件/ATTRFootprint和原始PAD：U8 origin2559.0551181102364,1377.9527559055118，fp5da9909cc515d9c5 pin15 e18 center120.08,-9.84（padAngle90，offsetY.001），pin16e19 +9.84；C46origin2874.015748031496,1141.732283464567，fpf11fd053052c204d pin1e15center-27.56,0(offsetX.005)。电气中心globalU8_15=2679.1351181102364,1368.112755905512，U8_16=2679.1351181102364,1387.7927559055117，C46_1=2846.455748031496,1141.732283464567。桥getallpad确实返回1位小数，不该用它画电气端点。

删除旧近pad3track6a0db3a1fd7ee33a/c90ec4fd70a2b6ca/79c72c965ac8d90f后先delete再create以免autosplit旧线，三条精确中心引出成功。报告nfc-exact-pad-endpoints包含exact与created。fresh严格DRC仅Connection444，NFC_RXN错误不再指U8/C46pad而是两Via e655/e656，说明端点问题部分解决但全网络仍未通过。fresh allNFC_RXN3track中心到via坐标一致；下一轮核viaType0、layerstack/孔连接及原生确切graph，不能只看几何宣称连通。需保存+重开再验；本轮未更新latest epro（仍320896旧round端点），工程打开，current0dbd7e7b。其他USB/成本进度未变，生产STALE。

## NFC内层重建内存通过，但重开再失败；保存坐标精度不一致新假设

SDK enumVia0明确普通通孔，source NORMAL；两via中心与三段line完全同坐标，已排除blind或无innerpad。删除/重建同几何Inner16后strict442且RXN0，保存原生退出再启动重开同repo，oldbridge0dbd断、新桥待读；fresh严格未repour843（不与442直接比较）。RXN错误又指U8_15/C46_1，说明尚未持久化通过，不能claim完成。新source证据：native保存LINE精确endpoint四位小数2679.1351,1368.1128/C462846.4557,1141.7323，COMPONENT仍保留origin长精度2559.0551181102364,1377.9527559055118以及2874.015748031496,1141.732283464567，PAD加和全精度差~0.00004mil。疑似严格连通内部要求一致节点，这是假设，不称物理断铜。报告nfc-exact-pad-endpoints和exact-reopen-drc。

下一步优先原生关闭并backup，仅将U8/C46COMPONENT origin四舍五入4dec（位移<0.00005mil）匹配LINE持久化网格，不改fp/meta/net/线宽/spacing，重开repour严格DRC及所有受影响NFCnet delta验证。如果不能解决，恢复实验并从原生pad-to-pad布线连接关系查，不继续反复delete/recreate无变化路径。工程现打开，禁止离线直接改；需先CmdS+CmdQ Appquit。仓库latest epro仍旧320896未覆盖exact修正，不当成production；报价/USB未完成。

## 两origin四位精度最小实验无效，已关闭EDA并完整恢复

原生CmdS+CmdQ确认Appquit，backup/tmp/ruri-before-nfc-origin-quantize.epcb2。仅U8/C46两COMPONENT x/y round4，逐行diff断言仅2行，其余含tombstone/pad/net/meta不动。重开repo主PCB、新ClaudeConnect、strict未repour843、RXN仍U8_15/C46_1两断连，说明简单origin/line精度假设不能解释（不能说已经定位根因）。原生再次savequit Appquit后完整恢复backup，字节相等true，报告nfc-origin-precision-experiment状态REJECTED_NO_RXN_IMPROVEMENT_RESTORED+experiment-drc。当前EDA已退出，所有旧bridge失效；下一轮启动repo主工程，不复用旧实例。

停止重复同坐标delete/create换内存DRC0；真正下一步用原生画线起止pad/过孔建立连接，或读取原生route构建的join graph与SDK primitive差异。当前几何3tracks/2via保存但RXN重载判不通，仍未完成。latestepro旧320896不代表最新exactpad修正，生产STALE/quote未完。不要再开展全板origin量化，也不要降strict规则迁就。可继续独立国内音频/电源成本工作避免全部陷在单网络。核心目标仍保持，不blocked（有其他工程动作）。

## 当前降本记录清理与TP4056弱USB输入预算

EDA保持已退出、原生桥断，不修改主原理图/PCB。读取domestic-cost文档发现仍写旧32连接/U2XL和U10保留，已重写为当前163件已删除U2/U5/U10、L1已国产、尚未合入NS4168/TP4056，并严格区分条件材料差额和正式两套总价。不再拿早期替换当当前节省成果。NS4168材料条件差额7.12、L1差额49.448、删除LTC旧料50.74须扣新增保持外围及送料差额，未相加宣称实现预算。核心报价仍未完成。

从拓品官方产品https://www.toppwr.com/product/view.php?id=478和官方PDF20241228/676f612b9f2dd.pdf核TP4056；这份17页REV2.3与此前REV2.4区分，不混用具体规格。单节4.2V、BAT侧终止、TEMP45..80%VCC和CE电平原厂确认。新增tp4056-input-power-budget报告，RPROG3k按1100系数名义366.7mA是条件算例，USB500mA只余133.3mA系统输入，5V/85%示例剩0.5667W≈3V18端178.2mA，并非设备已测功耗。不能直接用TP4056+USB拉gate关闭battery的简化powerpath替代BQ24074，必须补USB总输入限制/电池协助/终止与热设计，不能以便宜破坏原功能。未选择新的charging替代，未报价。下一轮可继续国内DPM充电候选或确立完整TP负载路径；NFC原生route连接问题仍需并行推进但禁止主动子agent。工程主epro仍320896旧checkpoint，Gerber生产STALE。

## SGM41562S 原生供货筛查完成：两型号均零库存，未合入

上一轮为用户状态答复，无工程进展；本轮执行下一可用选型动作。JLC search SGM41562S 初始共0且加载中不采用，加载结束共2：C55112397 SGM41562SXG/TR WLCSP9，显示0.125/扩展库/库存0；C55274234 SGM41562SAXTYH10G/TR TQFN10，显示0.243/海外代购扩展/库存0。无免换料费证据，零库存价格不是两套可采购报价，不能以超低显示价声称节省。原厂S型号powerpath及I2C确认，但SA型号另需spec不能混用。报告sgm41562s-sourcing。未改原理图/PCB，EDA保持退出。下一步优先已有货候选或完整离散输入限流，不再为零库存S系列展开逐脚工程；NFC原生连通问题及USB布线仍未解决，生产包STALE。

## ETA6003在库国产候选核对完成，外围费用可能吃掉节省

官方V2.7 PDF已下载11页，sha256与逐脚概要见eta6003-cost-spec-screen。JLC加载完成后C5455585 ETA6003Q3Q QFN3x3-16 stock10397，1+3.19/10+2.59；是否免换料费facet仅否，非免费。ISET1/2是batterycharge current；p6 IIN LIMIT=0.5A是典型波形，p3只有3.5A highside限流与4.5V典型Vhold，未找到总USB500mA可设置保证值，不能据描述输入限流叫可直接替BQ。CV最大4.24V也要电池规格确认。p9模拟GND与PGND布局区别需要图核，不全脚盲接地。历史BQ14.51vs3.19两颗条件材料差22.64；若新电感一种20fee+两0.425，其他外围前仅剩1.79节省，不能叫完成降本。未改主工程，EDA退出。下一步针对有货方案完整输入限流/外围报价或改稳压部分，勿重复零库存S筛查。

## 国产主升降压供货筛查：SGM62116/62110均无货

原生JLC加载完成后SGM62116YG/TR C5152035 WLCSP8显示6.93 stock0；SGM62110YG/TR C5152038显示7.8 stock0，S版C28314553 stock0，邮寄専用品也stock0，不采用超低预售价。SGM62116原厂18页p1/4为900mA典型输入限流，不能等同900mA输出，不能缩功率预算迁就便宜芯片。62110厂家3.3V预置输出，当前3V18必须重新核整机电压裕量，非直接换脚。广搜升降压3516项facet观察仅否，但关键词不能证明不存在所有免费器件。报告domestic-buckboost-stock-screen。没有新替换合入；下一步应按真实负载预算/供电架构找在库方案，勿不断检查零库存同系列。EDA保持退出，生产STALE。

## 供电选型预算建立，屏幕文档旧GPIO修正

新增design/POWER-BUDGET.md，明确500mA是Espressif电源预留建议不是实测，PN7160连续250mA仅TX非总电流。当前3V18共用功放/NFC/ESP；条件1W音频85%算例仅三项就1.12A，未包括屏幕逻辑/SD/MIC/静态电流。SGM62116典型900mA输入在3V→3.18/85%例只有0.7217A输出，且无全温保证，因此不是现架构可用低价替换。将功放移VSYS_RUN必须解决NS4168 VIH随VDD变化及新增料费，不能只改net或限制同时功能。文档有官方来源和缺项，未称最终功耗/续航。DISPLAY.md发现旧GPIO8SCK/16MOSI/扩展器RESET与当前PINOUT矛盾，修为共享SPI12SCK/11MOSI、16RESET、3V18，并同步屏幕33.95用户报价和PCB网络已同步但routing未完状态；POWER链接预算。未修改主EDA电路/铜线，EDA仍退出，最新epro仍旧checkpoint，生产STALE。下一步核真实屏幕/SD负载或推进原生NFC连接修复；不要再次用低功率零库存稳压器空转。

## 原生U8接收焊盘走线已保存，未通过整网连通

EDARecent打开报找不到eprj3，shell与原生文件选择器均证实文件存在；直接CmdO选精确repo文件成功，非缺失文件，不需恢复老epro。Claude重连4786d5e1主PCB。原生查找位号等于U8唯一项，放大实拍焊盘15和via位置，经菜单单路布线AltW从焊盘朝via接线。新LINE2cf2c906eeb7548b 10mil，原生自动移除回路删除旧9b8...6mil逃逸线，新endpoint2705.9872,1368.1128，保存。backup/tmp/ruri-before-native-rxn-join.epcb2。fresh严格未repour仍连接错误，RXN从U8_15/C46_1变成viae655/C46_1；说明原生焊盘连接影响图但未整网解决，不能称RXN已连通。完整报告nfc-native-pad-route。下一步继续C46端原生pad→via及内层via→via，必须确认native默认线宽/制造间距、repour/save/reopen完整验证。现EDA打开禁止离线改活动epcb，bridge4786d5e1有效；epro未更新仍旧checkpoint/生产STALE/报价未完。

## NFC两端原生pad及内层接线完成，repour严格442/RXN0；重开验收仍待

本轮原生DRC C46_1双击定位、实拍放大，AltW C46_1→via成功替换旧aaf059段，新d7a9fc3af051919b Top10mil。DRC_RXN仅两via。数值SDK删除旧innerf0da02e14215abfb后原生选择内层2，AltW C46via→U8via，第一次点击坐标止在2720,1380未接到via，source确认后原生再接真实过孔1012,455显示位置，RXN0。内层改为10mil45度路径，native remove loop生效；不得称最短模拟接收布局已验收。Tools铺铜管理器重建所有等待完成确认CmdS，fresh strict仅Connection442，RXN0，无Clearance/Physical/Netlist，详见nfc-native-repour-drc/nfc-native-pad-route。

为验证持久化原生CmdS+CmdQ明确Appquit，getApp已重启当前仍启动加载页，主repo尚未重新打开，所有旧bridge4786失效。下一步等启动完成，主Recent若再找不到文件用CmdO→CmdShiftG→setValue PathTextField精确repo eprj3，不能用paste（会超时）。取消偏好提示，再MainboardPCB打开ClaudeConnect，repour+strict验证RXN0。若重开再次失败不能claimrepair并须原生graph继续查。epro320896仍旧checkpoint未导出，生产STALE/quote未完。

## 用户起床状态核对：原生接线重开验收失败

核对最新已重开主PCB、重建全部地铜并保存后的严格DRC证据：仅Connection444，NFC_RXN仍U8_15/C46_1两个断连对象。保存前442/RXN0不能作为最终结果，nfc-native-pad-route改为REOPEN_FAILED_NOT_ACCEPTED，保存完整nfc-native-reopen-drc证据。原生画线也未解决重载连通，停止重复同一路径及坐标实验，下一步查焊盘/实例与持久化连接表示，并推进USB及真实整板成本核算。主EDA仍打开，禁止离线写活动epcb2。已有国产电感、删除U2/U5/U10、共享SPI等已合入，国内充电/功放替代尚未放行；完整两套报价未完成，旧Gerber/BOM/CPL不能投产。

## NFC焊盘原生属性排查

上一轮修正并保存重开失败证据属有效进展。本轮fresh list_instances确认主工程桥7b39d730仍在线，读两个RXN焊盘shape/specialPad/heatWelding/metallization：均Top1、正确NFC_RXN、RECT、specialPad空、metallization true、heatWelding null，没有显式禁止连接设置证据。报告nfc-live-pad-attributes。source原生10mil线起点落在焊盘矩形内部，不能将四位小数误差直接叫物理断铜；未改焊盘热连接、不用连接焊盘命令合并网络掩盖DRC。下一步在隔离副本核原生连接重建及导出重导入行为，避免继续重复同段坐标接线；未建立副本或完成实验。主工程仍打开，不离线写。总体444连接、USB未布、生产STALE、报价未完成。

## 最新工程点导出与隔离副本建立

fresh project_export_file显式epro成功321010bytes，ZIP113项CRC无损，更新仓库唯一latest epro（检查点非生产文件）。桥新项目导入JLCEDA Pro及EasyEDA Pro均明确Failed，不循环重试；原生File导入专业版对话框默认导入文档到当前项目，已取消，不向主工程追加。建立完整本地副本/private/tmp/ruri-connectivity-isolation-20260927，排除历史备份目录，仅复制未更改主源。下一步CmdO打开副本eprj3并验证窗口绝对路径，再做连接重建实验；尚未打开副本/实验未完成。报告nfc-isolation-export保存hash与失败证据。当前主工程仍打开、bridge7b39d730，禁止离线写主PCB。444连接/报价未完成，Gerber仍旧不能生产。

## 隔离项目已原生打开，重载基线重现RXN问题

CmdO精确副本eprj3打开，窗口路径明确/private/tmp/ruri-connectivity-isolation-20260927/Ruri-Passport-RevA，副本projectId98b7cc...；取消prefs，主PCB加载，ClaudeConnect bridge仍7b39d730但currentDocument切副本@98b7cc，不可沿用主项目ID。fresh strict verbose基线保存nfc-isolation-baseline，RXN两个pad断连重现；未repour总数不与主444比较。未变更副本或主工程铜线。下一步在此隔离副本验证连接重建/原生导出重导入或pad表示，修改后save/reopen才判断，勿只看内存。主epro321010检查点已保留，生产STALE/成本报价未完成。

## 隔离原生源码往返实验完成，未修复RXN

副本原生document_save导出1050619bytes3186行DOCHEAD/LINE竖线分隔。桥strict加载错误用单JSON解析全部3186invalid，属格式校验覆盖问题而非板子全部损坏。仅在@98b7cc隔离副本加载字节未修改原生源码validate off成功，自动backup4138a172；不关闭原生PCB规则。随后fresh严格DRC仍RXN两个pad断连，报告nfc-isolation-roundtrip，不能认为重新解析文档解决连接。未repour总数不与主444比较；未save/reopen，不向主工程合入此实验。下一步检查重载连接计算与instance footprint节点/原生导入格式，或推进独立USB及整板报价，停止同源码回载重试。当前EDA副本打开桥7b39d730/doc@98b7cc；主工程未改，latest epro321010工程点非生产，报价未完成。

**更正上述实验判读**：脚本实际输出259 Connection +1 Netlist，RXN0，上一段模板错误写仍两个断连，不采用。报告已更正ROUNDTRIP_CHANGED_DRC_RXN_ZERO_WITH_NEW_NETLIST_ERROR_NOT_ACCEPTED。全数大变且新网表错误，必须核163件553pad及track/pour/实例封装完整性，不得当连接修复；不要合入主工程。

## 隔离回载完整性首检：163件553焊盘保留

fresh原生查询component163/pad553/track1290/via223/pour2。与回载前原生导出源码逐ID对照COMPONENT/LINE/VIA/POUR，完整结果nfc-isolation-inventory；不能只凭数量证明网络/封装几何全同。DRC新增网表说明仅PCB与sch不同，须原生Import Changes预览具体差异；不应用重复器件。当前副本源COMPONENT原点四位小数，导出重载有坐标序列化，先前两origin实验无效，因此不可又宣称已定位精度根因。RXN0仍仅内存，尚未保存重开接受。主工程未改，副本打开@98b7cc桥7b39d730，生产STALE/报价未完。

## 副本网表差异具体定位为L1描述属性

原生AltI预览唯一L1删除描述属性，无新增元件或net变更；在隔离副本应用该属性同步，原生保存成功、全部重建地铜完成并确认保存。fresh严格结果见nfc-isolation-sync-repour，不再把此前1网表误称电气net新增丢失。下一步保存退出重开副本、repour严格检查，验证RXN及全板连接降低是否持久；尚未重开，禁止合入主工程。当前副本@98b7cc桥7b39d730，主工程未动，主epro321010工程点/生产STALE/quote未完成。

## 隔离副本保存重开验证完成

原生CmdS/CmdQ明确Appquit，重启Recent副本报找不到文件但确认后实际加载正确副本路径，取消prefs，PCB成功打开。Claude新桥95b48ff2，副本@98b7cc。全部repour完成确认保存，fresh严格结果见nfc-isolation-reopen-repour：{'Connection Error': 444, 'Netlist Error': 1} RXN=2。这才是重开结果，不沿用130旧计数。仍不能整板放行；下一步根据结果决定是否将原生文档规范化方案带回主工程，先做全部540pin-net/paste/geometry/source关联对照再合入，禁止直接替换整个项目掩盖问题。主工程未改/生产STALE/quote未完。

判定：重开444 Connection+1 Netlist、RXN2，原生source roundtrip仅改善内存连接图，未持久化解决。拒绝此方案，不向主工程合入；停止重复同一roundtrip。可在隔离副本做封装原生重建/小范围关联对照，或回主工程独立推进USB/成本，不能再称130是保存后成果。

## 用户明确暂停

用户“先停下吧”，已停止工程修改。最后只读对照：回载前与重开后的document source全部对象ID保持、只有DOCHEAD和两POURED变化，没有LINE/COMPONENT/PAD_NET变化，说明不能把DRC退化直接归因保存几何改写。项目epro封装32个相同无变化，部分symbolUUID及schematic引用重生成；报告source-roundtrip-diff/project-roundtrip-diff保留。最新副本重开严格444Connection+1Netlist/RXN2未解决，主未合入。EDA仍副本/private/tmp/ruri-connectivity-isolation-20260927打开、桥95b48ff2@98b7cc，恢复任务前先读此处，主生产包STALE/报价未完成。目标paused，自动任务也需保持暂停，不继续工程。

## 用户恢复工作（Astra）

用户明确“现在换astra继续这个工作”，恢复工程工作，不重建自动任务。已新鲜验证隔离副本桥95b48ff2严格444Connection+1Netlist，436是SMD Pad、RXN2。新增本地vendor ratline worker几何复现：精确提取保存文件RXN两pad、六track、两via，标准连通校准通过，实际几何全部同一连通分量；仅说明几何与冷载graph不一致，不代替原生DRC。报告nfc-worker-geometry-probe；脚本/tmp/ruri-worker-probe.cjs及ruri-nfc-probe-payload.py，bundled worker4.1.53与UI4.1.60差别需保留限定。正新建空白eprj2 `/private/tmp/Ruri-Passport-ImportCheck.eprj2`，原生创建成功并点“是”打开，下一步核currentProject再导入主latest321010 epro到此空白工程；不得导入主工程或老副本追加重复器件。

实时查询NS8002/C189960 SOP8，1+¥0.266/stock12787/扩展且非免换料费。不同于NS4168数字功放，需PDM→模拟RC重构及逐脚审核；未合入、不叫已省。音频功率放大器搜索3471条facet仅“否”，不据此断言全库不可能免费。报告ns8002-cost-candidate。主工程未改/制造STALE/fullquote未完。

## 原生新建 eprj2 导入与冷重开有实质进展

原生 File→Import 专业版将主 latest epro 导入空白 `/private/tmp/Ruri-Passport-ImportCheck.eprj2` 成功，项目 c13f6a2a7d191806ea36bc354f5491a7726a3efb92562565f730966f9fc54bbc，主PCB b684a953e71e082c；原生保存、CmdQ退出、重开后严格仍130Connection+1Netlist / NFC_RXN0，首次保持低计数，报告fresh-import-drc-20260927。当前桥d8e4ae1f，绝不能沿用旧副本文档ID。

完整性：163件/553焊盘网络多重集合一致，1290LINE/223VIA/POLY/FILL/REGION/POUR几何完全一致；163件封装所有PAD参数记录多重集合一致。12件坐标只有0.0001mil舍入差；原16规则无修改、导入新增2个铺铜spacing规则。报告fresh-import-integrity。此证据不能代替最终 ERC/DRC 或信号审核。

导入同步预览发现J3源device仍PH且sch Footprint=null，虽Name/C号和PCB为XH；初次同步取消。仅隔离副本Power页cffe9ed79c2ceada中J3=e344, Footprint属性e347明确绑定现PCB XH footprint fed51227b4d0c9e3，原生document_load备份6bfaa6e2。再次预览J3只新增空isSwitchClose+通道ID，未再回退封装，应用元数据同步并全部重建地铜保存。fresh严格130Connection/0Netlist。分布GND93,3V18 6,USB四网14,NFC_TVDD3,ANT_A/B各3,VSYS_RUN2,NFC晶振各2,I2C_SCL2（USB确切计数见原始JSON，不依此文字合计）。新属性修复尚未再次冷重开；工程最终检查点 `/private/tmp/ruri-importcheck-j3-fixed.epro`。主仓库原工程尚未替换，生产STALE/报价未完。下一步冷重开验证J3属性与0Netlist保持，转为正式工程之前比对全部schematic网络和保留源历史，避免两个工程并行编辑。

worker几何诊断补负对照，移除RXN中间329df9e860964488一段产生1条飞线，未删时0，校准有效。NS8002厂家Apr2023V1.3规格已读，仍只候选，未改音频。继续核TP4056+低价输入限流架构的总成本，不把充电限流当USB总输入限流。

第二次完整CmdQ/重开验证J3修正及同步保持：130Connection/0Netlist/RXN0，fresh-import-drc报告已补证据。当前桥ac4f42f9，文档仍b684...@c13...。354关键pin检查0错误。隔离恢复检查点复制至 hardware/eda/proposals/Ruri-Passport-Connectivity-Recovery.epro，仅工程恢复候选，不是制造文件，主文件尚未替换。

开始实际补GND：新只读planner plan_ground_stitches.py 读取553焊盘及现有铜线，保守避让各层铜/禁布区/焊盘和已有过孔，6.1mil余量、20/12mil过孔、10mil短线；六个C1/C3/C4/C6/C7/C30接地短线已原生写入，IDs见ground-stitch-applied-20260927，C5/C9/C34无短直出线未硬挤。此时正在原生全部重建地铜，需确认后strictDRC及保存重开，不将未通过的新增线合入主。源文件/ruri-fresh-import-reopened.epcb为新增前，继续规划前须新导出。

国产限流SGM2553YN6G/TR C699882查得3.58/1285库存/收费扩展，配TP4056条件两板芯片差额19.592元（BQ及TP旧价），未含外围/损耗，尚未合入。官方规格3-4页已视觉核对，68k限流可达610mA，不能声称最大500mA；100k公式typ379mA无直接max表，保留验证边界。报告sgm2553-cost-candidate。

## 接地第一批持久化结果与充电要求确认

六组短线/过孔已重铺铜保存，原生工程关闭重开后严格127 Connection / 0其他错误，GND93降至90；不是整板通过。C4/C30/C6仍被标记，局部铜皮几何探针显示六via均接同一内层地铜，但此探针不能覆盖原生DRC，停止盲加线。当前工程仍 /private/tmp/Ruri-Passport-ImportCheck.eprj2，桥ac4f42f9，PCB b684a953e71e082c@c13f6a2a7d191806ea36bc354f5491a7726a3efb92562565f730966f9fc54bbc。repo恢复epro须更新包含这六组短线；旧生产包STALE。

用户明确保留边用边充，不能改为关机才充电；继续比较有电源路径的国产方案完整成本。NS8002厂家Apr2023V1.3第一页视觉确认2号Bypass与3号INV相连，经1uF接地，绝不能直接接地；4号INN经输入电阻/隔直电容收音频，5号VO1反馈至4号，8号VO2与5号之间接扬声器。替换仍未实施，PDM滤波/静音/热设计待验证。

检查点已更新：原生导出 /private/tmp/ruri-ground-batch1.epro（350210bytes）复制至 hardware/eda/proposals/Ruri-Passport-Connectivity-Recovery.epro，包含六组地短线。此文件只供继续工程，不供投产；正式原工程未覆盖，127连接错误尚未解决。

## 优先打板阶段：接纳用户新增布线并修复局部短路

用户明确暂停自行编辑，允许接着修。当前同一eprj2已含其约614段新线/35via以及J2向内80mil位移；曾72clearance+42connection。完整先备份 /private/tmp/ruri-priority-live.epro。J2恢复原y195.7874（避免与D1/D2/D7重叠），保留其余新布线，删10条明确短路线及2个违规via，NFC_TVDD via24降20.1mil钻孔12.01不变；重铺后48Connection/0clearance。见priority-short-removal报告。再补15组地via/短线，其中USB B1/B12两via侵槽已删除，改相邻GND pad短接；目前新鲜结果见ruri-resume-drc。

独立只读release-schematic-review发现NFC内端实际7.874mil铜间隙，已新增15.748mil宽填充并用GUI查找填充ANT_A后启用官方桥接铜、加入ANT_B/ANT_A。该铜桥须Gerber连通及冷重开验证，不能先称NFC合格。手工源整体回载修改桥接属性曾被自动审批拒绝，未执行；改用原生GUI设置成功。另需落实R26/R27 53.6k/10k 0.1%实际采购号。

当前检查点 /private/tmp/ruri-current-resume.epro（362547bytes）和epcb，repo恢复候选尚需同步。用户中断后桥进程退出，已以EDA_BRIDGE_IDLE_EXIT_SEC=3600重启原有 /private/tmp/ruri-easyeda-mcp/dist/bridge-daemon/index.js，session65187；扩展ac4f42f9自动重连。未运行Freerouting，当前仅根agent，独立审核已结束。降本非必要改版暂停，仍须完成剩余网络/原生ERC/DRC/网表/生产文件一致性才可交付。

## 本轮继续：NFC 馈线与晶振实际补通（待本轮最终重铺/冷重开）

本轮从32 Connection/0其他起步。三条底层GND岛桥已读回保存，暂未降低计数，后续应核是否冗余，报告ground-island-bridges。补R67 ANT_B支路，C9接地fanout、C19短接既有5695b3dc06f33940 via；删除重复新增fd84279b85b4fb4d via。重铺后28 Connection/0其他。
ANT_A补外端馈线via(3430,995)，首次与新ANT_B支路交叉，已删除首次两条底层线，改绕(3250,1495)的下端路径，避开线圈区。报告antenna-a-feed-repair及correction。
NFC_XTAL2原先夹在NFC_VDD18顶层e966与3V18 e877/e878之间。删除e966，改VDD18用新(2429.1,1664.9)20/12via和底层短线接原e1996(2304.6,1464.6)；3V18主干e877保留31.496mil到y1610，y1610..1567.608局部及e878缩到11.418mil（约2mm局部），补7.874mil顶层晶振线。删除旧XTAL2内层支线db0af91ff1087665、6e96ab7416e21ca7、top fd8a3e63cb51f3a7、092136d0dfe4b9d6、5bbb08fb59f01374及换层via cd53482ab7740a8b，避免悬空线头。报告crystal-local-repair。最新未重铺DRC只剩24 Connection（GND12,I2C_SCL2,USB_DM_MCU2,DP_CONN4,DM_CONN4），其余全是待重铺Copper Region间距。正在原生铺铜管理器重建所有，须完成确认保存/严格DRC/冷重开；不能提前称0间距或成品。

GUI用户曾打开SMT匹配器，自动匹配将许多电容不同值全部错配C7432770、不同阻值全部错配C25803；返回编辑器时我选“否”，没有将错误匹配更新原理图/PCB。必须基于实际值逐行修复采购映射，自动匹配“60已匹配”不可当BOM验证。最新标准epro /private/tmp/ruri-progress-routing-standard.epro 362773bytes是在晶振修复之前；还需导出本轮最新并更新repo恢复候选。

本轮重铺后发现批量删除返回true但有两条旧内层晶振残线仍在源码，导致NFC_XTAL2又报2项；已逐条删除并读回确认两线不存在，再删5bbb短线。最终新鲜严格DRC为24 Connection/0其他（GND12,I2C2,USB10），证据routing-progress-drc-20260927.json。导出最新标准epro /private/tmp/ruri-latest-nfc-repaired.epro并覆盖repo恢复候选，仍明确不是生产版本。冷重开待执行；采购误配尚未修复，正式制造文件保持STALE。

随后I2C局部修复：e2050 IRQ过孔改至(2620,1170)，删e1454/e1455/e1446/e1447并重连IRQ顶层与Inner2；3V18支路e830局部宽度11.418mil；SCL从U8_7新(2593,1215)20/12via出线，经Bottom/Inner2/Top共4个中继via接既有e2056。报告i2c-local-repair。原生DRC无IRQ/I2C连接错误，剩22 Connection（GND12、USB10）；间距仅待重铺铜，正在重建所有。候选repo epro仍上一24项点，待当前重铺导出更新。临时模型快照需重新导出，不得拿ruri-route-current旧几何规划后续修改。

I2C重铺完成保存，原生GUI重新检查显示24 Connection/GND14（比重铺前新增C29_1与e2695孤岛），仍0其他；应采用重铺后24而不是22。已导出ruri-latest-i2c-repaired.epro 363691bytes并更新repo恢复候选。原生CmdS/CmdQ已实际退出，正在重新打开冷加载验证。不要宣称整板通过。

## 接地修复检查点：剩 USB 10 项

冷重开 I2C 修复保持24 Connection/0其他；当前桥9eede90d。随后补麦克风环形GND、SD卡6脚、C29、U7热焊盘、D5 ESD地和R5地，D5附近SD_DAT2局部避让，最新严格DRC为10 Connection（USB_DM_MCU2、USB_DP_CONN4、USB_DM_CONN4）/0其他。最新一批尚须重铺铜和冷重开。报告microphone-ground-repair、sd-nfc-ground-repair、sd-esd-ground-repair、lcd-reset-ground-repair。U7新via a560396e1360131f位于热焊盘内，需最终阻焊/焊膏验证。

检查点ruri-ground-complete-checkpoint.epro 363944bytes已更新repo恢复候选；正式制造包仍STALE。修正plan_ground_stitches.py自定义POLY焊盘双重平移问题，MIC环形地现按原始顶点定位。USB局部R2/R3/C4/C5移位仍只离线提案，未写入原生，避免误认为已换布局。后续先完整规划短差分线路与USB插座机械槽避让，随后原生变更、重铺、DRC、冷重开。采购自动误配问题仍未解决，不能据此报价。

## USB-C 插座局部补线：6 Connection / 0其他

原生增加14条线+2个20/12mil过孔，接通J2 A6/B6至D1_1、A7/B7至D1_2；两重复引脚交叉使用底层换层。全部重铺铜、CmdS后严格6 Connection/0其他，报告routing-progress-drc和usb-connector-local-applied。恢复候选更新为ruri-usb-connector-complete.epro 364062bytes。尚未冷重开。R2/R3/C4/C5仍未移动，USB MCU旧线仍保留。

主干正在离线规划共同走线通道：/private/tmp/ruri-usb-paired-45-plan.json已算出内层2共道候选，但参考平面距离与90Ω未落实，不能直接当合格USB线路。正在优先检查顶层共道可行性（脚本ruri-usb-pair-top-valid.py），以保持近地参考并减少换层。所有离线提案未写入PCB，正式包仍STALE。

## 首次严格 DRC 0/0，USB 完整重布和 3313 叠层

已原生实施91操作，报告usb-complete-routing-applied/proposal。删除旧USB_DM_MCU/DP_MCU全部LINE/VIA、e1834 I2S横线、e2541/e2542 GND支线及旧C4/C5四条GND支线。R2 e2547移1150,895.2774；R3 e172移1150,945.2774；C4 e36移1147.56,852并180°；C5 e40移1160,1000并180°。读回删除0残留。MCU侧短线与两可选电容重连；主干Bottom 6mil宽/8mil距并排，I2S_DIN在1660..1800,856.3局部换Top避让，保持麦克风功能。新增全板Inner2 GND_BOTTOM_REFERENCE地铜，沿用既有WiFi/NFC禁铜区，keepIsland=false。原生全部铺铜/CmdS后严格返回[]，首次0连接/0其他；冷重开仍待执行，不是投产放行。

原生物理层叠原来漏介电3，厚1.3758mm；经官方GUI物理堆叠选JLC04161H-3313预设，恢复上下0.0994mm介质、1.265mm芯板，总1.5642mm，已保存。官方JLCPCB计算器live确认90Ω、L4/L3、8mil线距、1oz外/0.5oz内、3313推荐6.05mil，现主干6mil。不要以主干参数宣称全部USB满足阻抗：仍须实际参考地覆盖/长短差/扇出/制造容差核验。浏览器阻抗结果tab1已打开，无任何订单。

最新ruri-usb-zero-drc-3313.epro 372066bytes已复制repo恢复候选。SHEET原始字节比较因原生导出重生图框UUID而不同；仅归一化带Company=嘉立创EDA图框的COMPONENT/Device/Symbol UUID后，其余全部一致，详usb-zero-drc-checkpoint。既有原生网表重跑354pin/0错，新鲜网表待冷重开后导出。当前桥9eede90d。继续先冷重开并重新连桥验证0DRC，然后导出供审核Gerber、做独立验证及采购绑定修复。正式生产包仍STALE，BOM错配未解决，报价未完成。

完整CmdQ退出、重开工程、重新连桥后strict DRC仍[]，0连接/0其他已冷加载保持。新桥d4573316。独立USB参考地审核和采购绑定审核正在只读导出副本，根任务独占EDA写入。354关键pin导出检查0错，553焊盘网络多重集合前后一致。制造放行仍待独立审核、Gerber/网表/ERC、采购号修复和实际报价。

## USB 独立审核修复与制造几何检查

只读ONE PASS完成：usb-reference-independent/review.md发现USB_DM_CONN旁VBUS e2016反焊盘造成约1.748mm无L3参考；已原生将e2016由1816.9,360.2移1780,420、外径24改20mil，e1171顶层短支线15.748mil并接新位置、e1172底层23.622mil保持。新增12个GND via后发现2个和原有GND via过近，已逐个删61693658f980c4f7/b8db5101762ee62b，净增10。重铺/CmdS/严格DRC再为[]，最新ruri-usb-return-repaired.epro372698bytes覆盖repo恢复候选，当前桥d4573316。usb-return-verification为根任务复用只读几何算法的修复验证，不是第二轮独立审核；实际L3未覆盖段只剩各USB信号via自身约0.609mm反焊盘，原VBUS连续缺口已消失。两个DP_MCU换层最近GND均0.711mm，未宣称全部换层都有紧贴成对via，连接器DM via最近仍1.631mm。DP额外2via/3D长度差约3.378mm仍保留，USB全速接口须样板实测。C4/R2丝印交叠为次要待处理。

修复前只供审核Gerber已原生导出/private/tmp/Ruri-Passport-USB-Zero-DRC-REVIEW-20260927.zip，不是当前最终铜版。check_fab_draft新增compact-88x85默认profile（保留legacy），安装孔从现有design/mounting-holes.json取，MIC孔55mm/D4(70,82)与紧凑工程核对；8项选定制造几何检查全过，USB NPTH0.1751mm铜间距仍待厂家DFM。正式制造包继续STALE。

采购独立报告bom-binding-independent/report.md已完成：144安装/19排除，100安装件Supplier/MPN空，R76 Value100k应10k，J3有效XH/C161860正确但私有device残PH元数据，C3/9/15/16 X5R与历史X7R要求待恢复或裁定。未修改BOM字段，报价尚未完成。后续集中修绑定、freshERC/netlist和最终制造导出。

R76已通过原生GUI在PCB与Power原理图同时改Value为10kΩ并恢复C25804；注意EDA修改Value会自动清空Supplier Part，必须最后恢复且读回！PCB还补±1% Tolerance，SCH Tolerance仍空（有效MPN本身1%），后续可补齐。最新ruri-r76-metadata-fixed.epro372841bytes已更新repo恢复候选。原生全Mainboard检查导出schematic-drc-current-20260927.txt：0致命/0错误/1警告（L1,U1,J1属性与C号不匹配）+J1机械MP1/MP2无符号pin信息，应逐项核实而不是盲目标准化替换封装。新鲜原生schematic-current-20260927.enet已替换repo schematic-current.enet，163/354/0错；R76 Name/Value10k、C25804已从新鲜网表读回确认。100颗空绑定尚未完成，J3底层device及X7R恢复未改。

采购补充：LCSC当前页面C17578242=GCM1885C2A751FA16J，0603/750pF/C0G/±1%/100V满足原RF标称约束，可据此推进绑定但未报价免换料费；C861467与C519489短链接本轮读取失败，搜索找到官方item.szlcsc.com/921805.html与LCSC完整型号页，尚未打开规格。不得称全部选型已经签核。

R76追加校正：PCB单独补Tolerance后严格DRC出现1 Netlist Error，原生差异预览确认仅R76容差±1%→空，非连线变化。已关闭“同时更新导线网络”并应用这唯一属性同步，恢复原理图/PCB一致，准确采购MPN仍0603WAF1002T5E(1%)。最新严格DRC[]，最新检查点/private/tmp/ruri-usb-r76-synced.epro372818bytes已更新repo恢复候选；上文单独±1%字段不再有效。新Gerber导出已取消（发现差异先处理），现留存Gerber仍是回流修复之前的审核包，不可当最新投产包。

## 采购绑定原生回读检查点 2026-09-27

143颗实例采购属性写入，L1继承已绑定器件C6331050，144安装件有效Supplier/MPN完整；19 DNP保持排除。51种原生库验证+MIC1/C844266两种官方页面核实；证据procurement-live-library-20260927.json。J3私有device残PH元数据改XH；C3/C9/C15/C16恢复C59782 X7R。原生GUI导入新工程hardware/eda/proposals/Ruri-Passport-Procurement-Bound.eprj2，UUID19b7f885524ec8859d343fa23df887dd52f0c523ab8f4726a58d956c93b8f359，Mainboard8ba8b91f8fadb6191a9df22976c275b6，桥d4573316。原ImportCheck工程保留不覆盖。

已重铺铜、关闭导线网络更新同步导入重编号通道ID、CmdS、native EPRO回读到同名proposals候选。163组件/354逐脚检查0错；有效采购字段SCH/PCB0差异；LINE/VIA/FILL/POUR/REGION/POLY几何忽略重编号ID后完全一致。报告procurement-native-readback/pin-check。严格DRC新导入工程有3 NFC ANT_A fill对ANT_B焊盘/via/hole间距错误，0网表错误；不能称DRC通过。新旧物理几何相同，须查原生导入/DRC忽略或端部几何原因，不得盲目屏蔽。原恢复候选仍上个0DRC检查点未覆盖，正式制造包继续STALE。

下一步先定位3 NFC端部错误并修复或有证据解释，再fresh ERC/netlist和制造导出。采购绑定不等于免换料费或现货验证：MIC1 C45337831官网只显示1个库存，两套供应不足待核；新报价和费用类别未确认。本轮没有下单付款或向第三方发消息。

## NFC端部桥接修复与新Gerber 2026-09-27

原生选择e3206 FILL，确认为内圈末端到ANT_B焊盘/via的0.4×0.7mm小矩形。改ANT_B后从3间距变1（与完整线圈ANT_A铜线e14接触），按官方桥接铜功能限定ANT_A/ANT_B端部跨网络连接。未加全局间距豁免，未改铜形。原生GUI141项完成0DRC(12:13:55)，MCP严格[]。native Gerber新导出review/Ruri-Passport-Procurement-NFC-REVIEW-20260927.zip，check_fab_draft8项通过；nfc-gerber-current-20260927.png独立解析局部Gerber显示完整四匝螺旋，未见跨匝短接，定量完整RF/匹配仍须样板。修正记录nfc-terminal-bridge-fix-20260927.json。

注意重大格式限制：旧epro导出只保存netName ANT_B，丢失isBridgingCopper/networkList，重导入会再出现端部间距。已另导出epro2并在内含epru中读回isBridgingCopper=true、networkList ANT_A/ANT_B。原生eprj2与proposals/Ruri-Passport-Procurement-Bound.epro2才是当前完整主工程；epro仅旧格式参考，不能当完整投产交换格式。下一步冷重开验证属性持久化和新鲜ERC/netlist、原生BOM/CPL、生产文件一致性及报价。正式latest仍STALE，不得发布为成品。

原生BOM导出57组/144数量/0空Supplier，L1有效继承C6331050确认；CPL原生163项，按BOM精确筛为144项/0缺失，19排除；导出分别review/procurement-native-bom/cpl(-all)-20260927.csv（原生UTF16 TSV无损转UTF8 CSV），未生产发布。新原生SCH DRC0致命/0错，但3个供应商属性警告组共许多元件，不能误称只L1/U1/J1：警告含新绑定电阻电容等，可能是Name/封装描述与库属性不一致，须器件标准化差异预览逐项判定，不能盲目替换封装。原始MCP汇总/procurement-sch-drc.json仅counts；sch_get_netlist再次长期不返回，停止等待，改GUI导出。后续先解决/解释警告、fresh GUI enet、冷加载epro2验证，再制造一致性检查和报价。

## 冷加载与四颗电容标准化 2026-09-27
冷重开新桥8997a117，严格DRC[]且桥接铜持久化；标准化旧列表缓存清除。C3/C9/C15/C16 GUI精确C59782改旧X5R底层身份，保留位号/唯一ID/符号/封装；PCB同步只四个器件身份，禁用导线网络更新。新严格DRC[]；EPRO2铜线/过孔/FILL/POUR/REGION/POLY/PAD完全一致，COMPONENT IDs因替换变化，需归一化验证，不能声称组件记录完全一致。主epro2已更新，报告procurement-standardization-four-20260927.json。其余属性警告、新鲜网表及完整报价待完成，正式制造latest仍STALE。

## 最终样板文件包 2026-09-27 12:50 后
已修复 Core 供电线/ESP_EN 误合并：e188 被拖为 490,190→490,210→410,210，删除合并线并恢复两条独立命名导线，清重复标签。新鲜 pilot-fixed-netlist-20260927.enet 163元件/354检查/0错；SCH0致命0错，3组供应商属性警告(有效144件属性differences[])，MP1/2机械脚信息。严格PCB[]；GUI141项0错12:48:52。最终源EPRO2 f95fa769...，PCB body与标准化四颗后的检查点完全一致。新Gerber caea1557...，8项几何通过；pilot-final-consistency再次NFC16/16、桥接只末端0.3mm相邻净空、144BOM/CPL匹配。已替换制造latest旧包，状态PILOT_PCB_DFM_READY/FULL_SMT_SUPPLY_NOT_READY，不可声称两套全贴片或实机成品。
当前JLC草稿实时371.86元现货物料+682.50加工=1054.36两套，EDA五片裸板参考50+屏幕67.9=1172.26已知项/两套，约586.13每套但仍缺MIC/USB/电池座供料、电池扬声器外壳等。MIC1自动配C2686054与最终C45337831不符；J2 C3020560/J3 C161860均平台邮寄供料，未闭环SMT库存与混合焊接DFM。禁止把预算达成/最低价或可全贴片支付说成完成。下步仅需供料/工厂DFM和样板验证，不重开无限降本重布线。
