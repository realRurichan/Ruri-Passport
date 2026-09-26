# 第二轮物料修正与降本审查

基线：`b17f67b`。只读审查现有报价导出及 `hardware/design/POWER.md`，没有修改 CAD、采购匹配或订单。终止条件：最多六项可执行建议后停止；本轮共五项。原报价为 2 套的自动匹配草稿，不能据此生产。

## 可执行结论

| 优先级 / 位号 | 证据与风险 | 最小修正及价格状态 |
| --- | --- | --- |
| SERIOUS — R22 | 原需求 1.78kΩ/1%，报价错误匹配 C2934253 / FRL0603FR500TS，即 0.5Ω。电流设定电阻不可用此替代。 | 改用 **C22849 / UNI-ROYAL 0603WAF1781T5E**，0603、1.78kΩ、1%、100mW。LCSC 页面核对料号及参数；100 起零售价显示 **US$0.0013/颗**，是零售参考，**嘉立创贴片价格/库存尚未建立**。删除 BOM Value 中的 `500mA`，把电流目标移到独立备注，避免再次误匹配。 |
| SERIOUS — C28 | 所需 1nF/50V/C0G 被匹配为 C1588 / CL10B102KB8NNNC（X7R）。 | 与现有 C46/C47 合并到 **C309468 / YAGEO CC0603FRNPO9BN102**：0603、1nF、50V、NP0、1%。原 JLC 草稿该 SKU 实读 **¥0.0966/颗，20 颗 ¥1.93**；合并后实际数量/换料费需重新报价。可减少一个不同 SKU，不能只比较电容单价。 |
| SERIOUS — C9、C3、C15、C16 | 这些位号需求 X7R；原匹配 C15849 / CL10A105KB8NNNC 为 X5R。C9 的最低耐压16V，另三颗10V。 | 统一 **C59782 / Samsung CL10B105KO8NNNC**，0603、1µF、16V、X7R、10%。厂家现行页面确认。LCSC 页面 50 起零售 **US$0.0211/颗**；**贴片人民币价待重新匹配**。不把美元零售价格冒充国内贴片价。C27/C32 可在核对实际偏压有效容量后加入同一 SKU，不能只按标称1µF一概替换。 |
| MINOR — L1 降本候选 | 当前 XFL4015-471MEC 的草稿实读 **¥25.85/颗，2 颗 ¥51.70**。国产候选 **顺络 MWSA0402S-R47MT / C6331050** 有可追溯型号和规格。 | 可进入布局替代评估；**不是现封装免改替换，也未确立价格便宜多少**。具体电气/机械条件见下节；本轮保留原 L1，不盲换。 |
| MINOR — 相同 SKU 重复行 | SW1–SW5 都是 C21262538，却按五行各采购5颗，共25颗、¥10.05；R1/R4/R5 与 R8/R15–R19/R56 同为 C25804；R53 与 R48/R54 同为 C21190。 | 报价 BOM 按“确定的料号＋封装”合并位号，按键功能文字移备注。同 SKU 合并能避免逐行 MOQ 重复；**换料费是否已按 SKU 去重须看新报价，不预先承诺五行省五次换料费**。R26/R27 的0.1%精密电阻不并入普通1%料。 |

## L1 候选的资格边界

顺络原厂规格书（分销商镜像）MWSA0402S-R47MT：0.47µH±20%，DCR最大14mΩ，饱和电流典型9.5A，温升电流典型7.5A；电流表另列7.6A/6.65A于其 `Max.` 栏，不将该含混栏解释成保证最小值。原厂把饱和条件定义为约30%电感下降，温升条件约40℃。尺寸为4.2±0.25 × 4.4±0.35 × 1.8±0.2mm，需按原厂推荐焊盘重建/核对封装及屏幕下方高度。[顺络规格书，第4、6、12页](https://www.alfatec.de/fileadmin/productfiles/datasheets/sunlord_mwsa_s_series.pdf)

TPS63802 规定有效电感0.37–0.57µH；其 Boost 限流最大5.75A。上述顺络典型电流说明值得评估，但只凭额定0.47µH及9.5A不能证明偏压、温度、公差下仍满足有效电感窗口。需核对 L-I 曲线与启动/过载工况，重新评估开关回路、损耗和温升后才能批准。14mΩ比现有 Coilcraft 更高；按3A RMS计算电感直流铜耗约0.126W，尚不含磁芯/交流损耗。[TI TPS63802，第5、6、19页](https://www.ti.com/lit/ds/symlink/tps63802.pdf)

LCSC 商品页确认 C6331050 与该顺络型号对应，标作扩展库，但本轮读取未得到实际单价和贴片库存。**价格状态 NOT ESTABLISHED，不给出虚构的“¥1内”替换价或已实现节约额。**[立创商品页](https://item.szlcsc.com/7279230.html)

## 已核实及来源

- R22 正确料号、阻值、公差、功率和封装对应：[LCSC C22849](https://www.lcsc.com/product-detail/Chip-Resistor-Surface-Mount_UNI-ROYAL-Uniroyal-Elec_C22849.html)。
- C28 可与既有 NFC 1nF NP0 的同型号合并，原厂规格确认：[YAGEO CC0603FRNPO9BN102](https://www.yageogroup.com/download/specsheet/CC0603FRNPO9BN102)、[LCSC C309468](https://www.lcsc.com/product-detail/Multilayer-Ceramic-Capacitors-MLCC-SMD-SMT_YAGEO-CC0603FRNPO9BN102_C309468.html)。
- C59782 额定16V X7R覆盖本轮列出的10V/16V标称要求：[Samsung 原厂产品页](https://product.samsungsem.com/mlcc/CL10B105KO8NNN.do)、[LCSC C59782](https://www.lcsc.com/product-detail/C59782.html)。尚未将其视为所有1µF用途的有效容量签核。
- 人民币原始草稿价格来自仓库 `jlc-quote-candidates-20260926.json`；新报价总价尚未建立。零售现货和贴片现货属不同渠道，不互相代替。

结论：先修 R22 及两类介质错配并合并同料号报价；L1 留为有原厂资料的替代候选，待尺寸、电感偏压和贴片价格核对。本轮只读审查结束。
