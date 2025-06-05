# Alpha#31: 多因子组合策略

## 描述

Alpha#31 的计算公式为：

```
Alpha#31: ((rank(rank(rank(decay_linear((-1 * rank(rank(delta(close, 10)))), 10)))) + rank((-1 * delta(close, 3)))) + sign(scale(correlation(adv20, low, 12))))
```

这个 Alpha 策略是一个多因子组合模型，结合了市场价格的趋势、短期反转以及量价关系特征。它由三个主要部分构成：

1. **部分 A**: `rank(rank(rank(decay_linear((-1 * rank(rank(delta(close, 10)))), 10))))`

   * 计算收盘价在过去10天的变化 (`delta(close, 10)`)。
   * 对这个变化值进行两次截面排名 (`rank(rank(delta(close, 10)))`)。
   * 取其负值 (`-1 * ...`)。
   * 对上述结果应用10天的衰减线性加权 (`decay_linear(..., 10)`)。
   * 最后再进行三次截面排名。
   * 这个部分旨在捕捉价格动量的持续性和相对强度，经过多次排名和衰减加权平滑处理。
2. **部分 B**: `rank((-1 * delta(close, 3)))`

   * 计算收盘价在过去3天的变化 (`delta(close, 3)`)。
   * 取其负值，表示短期价格变化的反向。
   * 对该反向变化值进行截面排名。
   * 这个部分旨在捕捉短期价格反转的信号。
3. **部分 C**: `sign(scale(correlation(adv20, low, 12)))`

   * 计算20日平均成交量 (`adv20`) 和每日最低价 (`low`) 在过去12天内的时序相关性 (`correlation(adv20, low, 12)`)。
   * 对计算出的相关性系数进行截面标准化 (`scale(...)`)。
   * 取标准化后相关性系数的符号 (`sign(...)`)。
   * 这个部分旨在捕捉成交量与价格之间的关系方向。例如，价跌量增（负相关）或价跌量缩（正相关）等模式。

最终的 Alpha#31 值为这三个部分的总和。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据 (确保包含 close, adv20, low 字段)
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha31/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#31
│   ├── alpha31_results.csv    # 计算得到的 Alpha#31 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#31 策略简介
```

## 使用步骤

### 1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。如果未安装，可以通过 pip 安装：

```bash
pip install pandas numpy scipy
# scipy 可能用于 decay_linear 的实现，如果 pandas 内置函数不足够
```

### 2. 检查模拟数据

本 Alpha 依赖于 `close`, `adv20` (假设为20日平均成交量), 和 `low` 数据。请确保 `data/mock_data.csv` 文件存在，并且包含了 `date`, `asset_id`, `close`, `adv20`, `low` 列。如果文件不存在或数据不完整，请运行或修改 `data/generate_mock_data.py` 脚本。

```bash
# 检查或生成数据 (如果需要)
cd ../../data # 假设当前在 alpha/alpha31 目录
python generate_mock_data.py # 假设此脚本能生成所需字段
cd ../alpha/alpha31
```

### 3. 计算 Alpha#31 因子

进入 `alpha/alpha31` 目录并运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#31，并将结果保存到当前目录下的 `alpha31_results.csv`。

## Alpha#31 策略解读与计算示例

由于公式较为复杂，此处提供一个基于实际输出 `alpha31_results.csv` 的概念性拆解。
我们将以 `asset_1` 在日期 `2025-01-26` 的数据为例。这是 `part_C` 开始对 `alpha31` 产生非零贡献的日期。

**背景数据 (源自 `alpha31_results.csv` for `asset_1` on `2025-01-26`):**
- `adv20`: 1359053.75 (假设由脚本根据 `volume` 计算得出，或从原始数据读取)
- `part_A`: 0.80
- `part_B`: 0.80
- `part_C`: -1.00

**计算 Alpha#31:**
`Alpha#31 = part_A + part_B + part_C`
`Alpha#31 = 0.80 + 0.80 + (-1.00) = 0.60`

此值与 `alpha31_results.csv` 中 `asset_1` 在 `2025-01-26` 的 `alpha31` 列的值 `0.60` 相符。
各部分 (`part_A`, `part_B`, `part_C`) 的详细计算步骤涉及多次排名、差分、衰减加权、相关性、标准化和符号提取，具体可参考 `alpha_calculator.py` 脚本中的实现。

## 数据需求

- `date`: 交易日期 (datetime)
- `asset_id`: 资产ID (string/object)
- `close`: 每日收盘价 (float)
- `low`: 每日最低价 (float)
- `adv20`: 过去20日平均成交量 (float) - *假设 `adv20` 是已经预计算好或可以直接从数据源获取的字段。如果不是，`alpha_calculator.py` 中可能需要先计算它 (例如，基于 `volume` 列)。*
- (脚本还会包含 `open`, `high`, `volume`, `vwap`, `returns` 等在 `mock_data.csv` 中的其他列，以保持数据完整性)

## 输出格式

输出的 CSV 文件 (`alpha31_results.csv`) 将包含以下列（除了原始数据列），所有数值型 alpha 相关列均保留两位小数：

- `date`: 交易日期
- `asset_id`: 资产ID
- `open`, `high`, `low`, `close`, `volume`, `vwap`, `returns`: 原始数据中的对应列
- `adv20`: 20日平均成交量 (如果从 `volume` 计算得出，则会包含此列；如果是原始输入，则保留原始输入)
- `part_A`: Alpha#31 公式中第一部分的最终计算结果 (经过多次排名和衰减加权)
- `part_B`: Alpha#31 公式中第二部分的最终计算结果 (短期反转信号)
- `part_C`: Alpha#31 公式中第三部分的最终计算结果 (量价关系符号)
- `alpha31`: 最终计算的 Alpha#31 值。

## 注意事项与风险提示

- **数据窗口与NaN值** (基于 `alpha31_results.csv` 观察)：
  - **`adv20`**: 如果基于 `volume` 列计算 (默认20日窗口，`min_periods=15`)，每个资产的前14个交易日其值为NaN。在示例数据中，`adv20` 从第15个交易日 (`2025-01-15`) 开始有值。
  - **`part_A`**: (`delta(close,10)`, `decay_linear(...,10)`) 每个资产的前19个交易日其值为NaN。在示例数据中，`part_A` 从第20个交易日 (`2025-01-20`) 开始有值。
  - **`part_B`**: (`delta(close,3)`) 每个资产的前3个交易日其值为NaN。在示例数据中，`part_B` 从第4个交易日 (`2025-01-04`) 开始有值。
  - **`part_C`**: (`correlation(adv20,low,12)`) 依赖于 `adv20`。若 `adv20` 有14个NaN，加上12日相关性窗口（需要12个 `adv20` 的值，即 `adv20` 的第 `14+11=25` 个非NaN值之后），`corr_adv20_low_12` 会有约25个NaN。`cs_scale` 在其输入序列没有足够多非NaN值时返回0，因此 `part_C` (即 `sign(scale(...))`) 在早期可能为 `0.0`。在示例数据中，`part_C` 从第26个交易日 (`2025-01-26`) 开始出现非零值。
  - **`alpha31`**: `alpha31 = part_A + part_B + part_C`。其第一个非NaN值取决于 `part_A` (最早出现在第20天)。在第20至25天，`alpha31` 的计算中 `part_C` 的贡献为0。从第26天开始，`part_C` 开始贡献非零值。因此，每个资产时间序列的前19个交易日 `alpha31` 值为NaN。
- **排名方法**：`pandas` 的 `rank(method='average', pct=True)` 通常用于截面排名，结果是百分比形式。
- **衰减线性加权 (`decay_linear`)**: 具体实现方式会影响结果。通常是指对最近的数据赋予更高的权重，权重随时间线性递减。可以使用 `numpy.average` 配合自定义权重数组，或寻找现有的金融库函数。
- **标准化 (`scale`)**: 通常指减去均值后除以标准差。`scale(x)` 一般表示 `(x - mean(x)) / std(x)`，按截面计算。
- **相关性计算**: `pandas` 的 `rolling().corr()`。注意窗口期内数据不足或标准差为零的情况。
- **`adv20`的来源**: 需要明确 `adv20` 是直接提供还是需要基于原始 `volume` 计算。如果是后者，其计算本身也会引入窗口期（通常是20天）。
- **小数位数**: 最终的 Alpha#31 值和所有中间计算的 Alpha 相关列均按要求保留两位小数。
- **因子组合的复杂性**: 多因子组合可能导致模型解释性下降，且各部分之间的相互作用可能复杂。
- **市场适用性**: 此复杂因子在不同市场环境或资产类别上表现可能迥异。务必进行充分的回测和验证。
- **数据质量**: 输入数据的准确性和完整性至关重要。

Alpha#31 是一个基于多种信号的复杂因子，不保证未来表现。建议与其他因子结合使用，并进行充分的回测验证。
