# 最新硬件制造检查点

2026-09-26，J3 使用 JST S3B-XH-SM4-TB(LF)(SN) / C161860，XH 2.50 mm、3 A（22 AWG 功率线）。原理图和 PCB 已同步，严格 DRC 0 错误，350 项针脚网络核对和8项Gerber几何检查通过。

- Gerber ZIP：本目录唯一制板输出。
- bom.csv：当前客户端导出的 UTF-16 制表符 BOM。
- cpl.xlsx：当前客户端坐标，按 BOM 筛选装配器件，剔除 DNP、测试点和 PCB 天线；J3 的旧库器件标签按当前 MPN 更正为 XH，封装、坐标和旋转均来自客户端。
- netlist.enet：当前工程原生网表。
- manifest.json：文件校验和与状态。

工程 J3 的库器件别名仍沿用旧 PH 名称，实例采购型号和激活封装已改为 XH；请按 BOM 的 Manufacturer Part / Supplier Part 和实际封装核对，不能按旧别名采购。

该检查点尚未生产放行：屏幕排线装配、按键实体脚位、USB DFM、NFC调谐、电池温度门限和完整供料报价仍需确认。第二轮报价早于 J3 变更，不能当作当前准确价格。配套插头 XHP-3，针号1=正极、2=NTC、3=负极。
