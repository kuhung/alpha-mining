# Alpha#34: 截面合成因子

## 因子定义

```
rank(((1 - rank((stddev(returns, 2) / stddev(returns, 5)))) + (1 - rank(delta(close, 1)))))
```

## 计算逻辑

该因子结合了多项技术分析指标，旨在从不同的时间尺度和视角捕捉市场动量和趋势反转。

1.  **`stddev(returns, 2)` / `stddev(returns, 5)`**:
    *   计算过去2天和过去5天回报率的标准差。标准差衡量价格波动的幅度。
    *   两者之比可以反映短期波动性与长期波动性之间的关系。如果短期波动性相对于长期波动性较低，可能预示着趋势的稳定或潜在的反转。

2.  **`1 - rank((stddev(returns, 2) / stddev(returns, 5)))`**:
    *   对上述比率进行截面排序，并用1减去排序结果。
    *   这意味着比率越小（短期波动性相对于长期波动性越低），该部分的因子值越大。

3.  **`delta(close, 1)`**:
    *   计算今日收盘价与昨日收盘价的差值（即一日涨跌幅）。
    *   这是衡量短期价格变动最直接的指标。

4.  **`1 - rank(delta(close, 1))`**:
    *   对昨日收盘价差进行截面排序，并用1减去排序结果。
    *   这意味着价格跌幅越大（`delta(close, 1)`越小，排序值越小），该部分的因子值越大；反之，价格涨幅越大，该部分的因子值越小。

5.  **最终因子值**:
    *   将步骤2和步骤4的结果相加，并对总和进行最终的截面排序。
    *   该最终排序值即为 Alpha#34 的输出。高的因子值通常意味着：
        *   短期波动性相对于长期波动性较低（可能预示稳定或反转）。
        *   近一日价格下跌（可能预示超卖或反弹机会）。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据 (确保包含 returns, close 字段)
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha34/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#34
│   ├── alpha34_results.csv    # 计算得到的 Alpha#34 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#34 策略简介
```

## 使用步骤

### 1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。如果未安装，可以通过 pip 安装：

```bash
pip install pandas numpy
```

### 2. 检查模拟数据

本 Alpha 依赖于 `returns` 和 `close` 数据。请确保 `data/mock_data.csv` 文件存在，并且包含了 `date`, `asset_id`, `returns`, `close` 列。如果文件不存在或数据不完整，请运行或修改 `data/generate_mock_data.py` 脚本。

```bash
# 检查或生成数据 (如果需要)
cd ../../data # 假设当前在 alpha/alpha34 目录
python generate_mock_data.py # 假设此脚本能生成所需字段
cd ../alpha/alpha34
```

### 3. 计算 Alpha#34 因子

进入 `alpha/alpha34` 目录并运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#34，并将结果保存到当前目录下的 `alpha34_results.csv`。

## 数据输入

*   `returns`: 每日收盘价到收盘价的回报。
*   `close`: 每日收盘价数据。

这些数据预计从 `../../data/mock_data.csv` 文件中获取。

## 输出格式

输出的 CSV 文件 (`alpha34_results.csv`) 将包含以下列（除了原始数据列），所有数值型 alpha 相关列均保留两位小数：

-   `date`: 交易日期
-   `asset_id`: 资产ID
-   `open`, `high`, `low`, `close`, `volume`, `vwap`, `returns`: 原始数据中的对应列
-   `part_A`: 中间计算结果 `1 - rank((stddev(returns, 2) / stddev(returns, 5)))`
-   `part_B`: 中间计算结果 `1 - rank(delta(close, 1))`
-   `sum_parts_AB`: `part_A` 和 `part_B` 的总和
-   `alpha34`: 最终计算的 Alpha#34 值。

## 注意事项与风险提示

-   **NaN 值**: 如果输入数据缺失，相应的 Alpha 值将为 NaN。请确保数据完整性。
-   **排名方法**: `pandas` 的 `rank(method='average', pct=True)` 通常用于截面排名，结果是百分比形式。
-   **小数位数**: 最终的 Alpha#34 值及中间结果按要求保留两位小数。
-   **市场适用性**: 此因子在不同市场环境或资产类别上表现可能迥异。务必进行充分的回测和验证。
-   **数据质量**: 输入数据的准确性和完整性至关重要。

Alpha#34 是一个基于多项指标合成的因子，不保证未来表现。建议与其他因子结合使用，并进行充分的回测验证。

## 策略解读与计算示例

我们将以 `asset_1` 在日期 `2025-01-05` 的数据为例，展示 Alpha#34 的计算。

**背景数据 (源自 `alpha34_results.csv` for `asset_1` on `2025-01-05`):**
- `returns` (2025-01-05): 0.01
- `close` (2025-01-05): 100.50
- `close` (2025-01-04): 99.40
- `part_A` (intermediate): 0.20
- `part_B` (intermediate): 0.40
- `sum_parts_AB` (intermediate): 0.60
- `alpha34`: 0.40

**计算 Alpha#34 (简化示例，使用中间结果):**

1.  **`delta(close, 1)`**:
    `close` (2025-01-05) - `close` (2025-01-04) = `100.50 - 99.40 = 1.10`

2.  **`1 - rank((stddev(returns, 2) / stddev(returns, 5)))` (Part A):**
    此部分经过内部计算和截面排序，对于 `asset_1` 在 `2025-01-05` 的结果为 `part_A = 0.20`。

3.  **`1 - rank(delta(close, 1))` (Part B):**
    `delta(close, 1)` 的值（`1.10`）经过截面排序并用1减去排名后，对于 `asset_1` 在 `2025-01-05` 的结果为 `part_B = 0.40`。

4.  **求和**:
    `part_A + part_B = 0.20 + 0.40 = 0.60`

5.  **最终排名**:
    对所有资产在 `2025-01-05` 的 `sum_parts_AB` 值进行截面排名。
    假设在 `2025-01-05`，所有资产的 `sum_parts_AB` 值经过排序后，`asset_1` 的排名对应百分比为 `0.40`。

因此，`Alpha#34` 对 `asset_1` 在 `2025-01-05` 的最终计算值为 `0.40`。

此值与 `alpha34_results.csv` 中 `asset_1` 在 `2025-01-05` 的 `alpha34` 列的值 `0.40` 相符。 