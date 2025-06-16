# Alpha#32: 趋势跟踪与量价相关性组合策略

## 描述

Alpha#32 的计算公式为：

```
Alpha#32: (scale(((sum(close, 7) / 7) - close)) + (20 * scale(correlation(vwap, delay(close, 5),
230))))
```

这个 Alpha 策略结合了短期价格趋势和长期量价相关性，旨在捕捉市场中不同时间维度的信号：

1. **部分 A**: `scale(((sum(close, 7) / 7) - close))`

   * `sum(close, 7) / 7`：计算过去7天的收盘价均值，代表短期均线。
   * `(sum(close, 7) / 7) - close`：计算短期均线与当前收盘价的差值，反映短期价格趋势。如果均线高于收盘价，表示下跌趋势；反之，上涨趋势。
   * `scale(...)`：对上述差值进行截面标准化。标准化有助于因子在不同资产间进行比较。
   * 这个部分旨在衡量短期价格相对于其近期均值的偏离程度，以捕捉短期趋势或反转。
2. **部分 B**: `(20 * scale(correlation(vwap, delay(close, 5), 230)))`

   * `delay(close, 5)`：获取5天前的收盘价，引入滞后性。
   * `correlation(vwap, delay(close, 5), 230)`：计算成交量加权平均价 (`vwap`) 与5天前收盘价在过去230天内的时序相关性。`vwap` 反映了交易的实际价格水平，与滞后收盘价的相关性可能揭示市场情绪或资金流向与价格走势的长期关系。
   * `scale(...)`：对计算出的相关性系数进行截面标准化。
   * `20 * ...`：将标准化后的相关性因子乘以20。这个乘数用于调整该部分在总 Alpha 值中的权重或影响力。
   * 这个部分旨在捕捉成交量和价格之间长期、滞后的关系，其强度可能预示趋势的持续性或反转。

最终的 Alpha#32 值为这两个部分的加权和。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据 (确保包含 close, vwap 字段)
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha32/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#32
│   ├── alpha32_results.csv    # 计算得到的 Alpha#32 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#32 策略简介
```

## 使用步骤

### 1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。如果未安装，可以通过 pip 安装：

```bash
pip install pandas numpy
```

### 2. 检查模拟数据

本 Alpha 依赖于 `close` 和 `vwap` 数据。请确保 `data/mock_data.csv` 文件存在，并且包含了 `date`, `asset_id`, `close`, `vwap` 列。如果文件不存在或数据不完整，请运行或修改 `data/generate_mock_data.py` 脚本。

```bash
# 检查或生成数据 (如果需要)
cd ../../data # 假设当前在 alpha/alpha32 目录
python generate_mock_data.py # 假设此脚本能生成所需字段
cd ../alpha/alpha32
```

### 3. 计算 Alpha#32 因子

进入 `alpha/alpha32` 目录并运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#32，并将结果保存到当前目录下的 `alpha32_results.csv`。

## 策略解读与计算示例

我们将以 `asset_1` 在日期 `2025-04-10` 的数据为例，展示 Alpha#32 的计算。

**背景数据 (源自 `alpha32_results.csv` for `asset_1` on `2025-04-10`):**
- `close`: 93.10
- `vwap`: 91.76
- `part_A`: -0.92
- `part_B`: 0.00 (注意：由于模拟数据长度限制，`correlation` 函数的 230 天窗口可能未被完全满足，导致 `part_B` 在此示例中为 0。在实际足够长的数据中，`part_B` 将会有非零值。)

**计算 Alpha#32:**
`Alpha#32 = part_A + part_B`
`Alpha#32 = -0.92 + 0.00 = -0.92`

此值与 `alpha32_results.csv` 中 `asset_1` 在 `2025-04-10` 的 `alpha32` 列的值 `-0.92` 相符。
各部分 (`part_A`, `part_B`) 的详细计算步骤可参考 `alpha_calculator.py` 脚本中的实现。

## 数据需求

- `date`: 交易日期 (datetime)
- `asset_id`: 资产ID (string/object)
- `close`: 每日收盘价 (float)
- `vwap`: 每日成交量加权平均价 (float)
- (脚本还会包含 `open`, `high`, `low`, `volume`, `returns` 等在 `mock_data.csv` 中的其他列，以保持数据完整性)

## 输出格式

输出的 CSV 文件 (`alpha32_results.csv`) 将包含以下列（除了原始数据列），所有数值型 alpha 相关列均保留两位小数：

- `date`: 交易日期
- `asset_id`: 资产ID
- `open`, `high`, `low`, `close`, `volume`, `vwap`, `returns`: 原始数据中的对应列
- `part_A`: Alpha#32 公式中第一部分的最终计算结果
- `part_B`: Alpha#32 公式中第二部分的最终计算结果
- `alpha32`: 最终计算的 Alpha#32 值。

## 注意事项与风险提示

- **数据窗口与NaN值**：
  - **`sum(close, 7)` 和 `delay(close, 5)`**: 计算会引入 NaN 值，例如 `sum(close, 7)` 需要7个数据点，前6个数据点会是 NaN。
  - **`correlation(vwap, delay(close, 5), 230)`**: 需要230个数据点来计算相关性。这意味着每个资产的前229个数据点将无法计算出有效的相关性值，导致 `part_B` 在这些日期为 NaN。
  - **`alpha32`**: 最终的 `alpha32` 值将受到各部分中最大窗口期的影响。因此，`alpha32` 的第一个非 NaN 值将出现在每个资产的第230个交易日。
- **标准化 (`scale`)**: 通常指减去均值后除以标准差。`scale(x)` 一般表示 `(x - mean(x)) / std(x)`，按截面计算。需要处理标准差为零的情况。
- **相关性计算**: `pandas` 的 `rolling().corr()`。注意窗口期内数据不足或标准差为零的情况。
- **小数位数**: 最终的 Alpha#32 值和所有中间计算的 Alpha 相关列均按要求保留两位小数。
- **因子组合的复杂性**: 复杂因子可能导致模型解释性下降，且各部分之间的相互作用可能复杂。
- **市场适用性**: 此复杂因子在不同市场环境或资产类别上表现可能迥异。务必进行充分的回测和验证。
- **数据质量**: 输入数据的准确性和完整性至关重要。

Alpha#32 是一个基于多种信号的复杂因子，不保证未来表现。建议与其他因子结合使用，并进行充分的回测验证。
