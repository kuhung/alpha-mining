# Alpha#37: 截面合成因子

## 因子定义

```
(rank(correlation(delay((open - close), 1), close, 200)) + rank((open - close)))
```

## 计算逻辑

该因子结合了时间序列相关性分析和截面排名，旨在捕捉市场中开盘价与收盘价差异的动量效应。

1.  **`(open - close)`**:
    *   计算每日开盘价与收盘价的差值。这代表了当日的价格动量或反转信号，正值表示收涨，负值表示收跌。

2.  **`delay((open - close), 1)`**:
    *   获取前一日的 `(open - close)` 值。

3.  **`correlation(delay((open - close), 1), close, 200)`**:
    *   计算前一日的 `(open - close)` 值与当日 `close` 价格在过去200个交易日的时间序列相关性。
    *   此部分旨在衡量历史动量与当前收盘价之间的关系强度和方向。正相关性可能意味着前一日的动量与今日收盘价同向变动，反之亦然。

4.  **`rank(correlation(delay((open - close), 1), close, 200))`**:
    *   对上述200日时间序列相关性结果进行截面排名。排名越高，表示相关性在截面上越强（无论是正向还是负向），或者在所有资产中排名前列。

5.  **`rank((open - close))`**:
    *   对当日的 `(open - close)` 值进行截面排名。排名越高，表示当日开盘价与收盘价的差值越大（通常意味着当日表现更强劲或更弱势，取决于原始差值的方向）。

6.  **最终因子值**：
    *   将步骤4和步骤5的结果相加。
    *   该最终结果即为 Alpha#37 的值。高的因子值通常意味着：
        *   前一日动量与当前收盘价之间存在显著的时间序列相关性（经过排名）。
        *   当日的开盘价与收盘价的差异在截面上相对较大（经过排名）。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据 (确保包含 open, close 字段)
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha37/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#37
│   ├── alpha37_results.csv    # 计算得到的 Alpha#37 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#37 策略简介
```

## 使用步骤

### 1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。如果未安装，可以通过 pip 安装：

```bash
pip install pandas numpy
```

### 2. 检查模拟数据

本 Alpha 依赖于 `open` 和 `close` 数据。请确保 `data/mock_data.csv` 文件存在，并且包含了 `date`, `asset_id`, `open`, `close` 列。如果文件不存在或数据不完整，请运行或修改 `data/generate_mock_data.py` 脚本。

```bash
# 检查或生成数据 (如果需要)
cd ../../data # 假设当前在 alpha/alpha37 目录
python generate_mock_data.py # 假设此脚本能生成所需字段
cd ../alpha/alpha37
```

### 3. 计算 Alpha#37 因子

进入 `alpha/alpha37` 目录并运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#37，并将结果保存到当前目录下的 `alpha37_results.csv`。

## 数据输入

*   `open`: 每日开盘价数据。
*   `close`: 每日收盘价数据。

这些数据预计从 `../../data/mock_data.csv` 文件中获取。

## 输出格式

输出的 CSV 文件 (`alpha37_results.csv`) 将包含以下列（除了原始数据列），所有数值型 alpha 相关列均保留两位小数：

-   `date`: 交易日期
-   `asset_id`: 资产ID
-   `open`, `high`, `low`, `close`, `volume`, `vwap`, `returns`: 原始数据中的对应列
-   `oc_diff`: `(open - close)` 中间计算结果
-   `corr_oc_delay1_close_200`: `correlation(delay((open - close), 1), close, 200)` 中间计算结果
-   `ranked_corr`: `rank(correlation(delay((open - close), 1), close, 200))` 中间计算结果
-   `ranked_oc_diff`: `rank((open - close))` 中间计算结果
-   `alpha37`: 最终计算的 Alpha#37 值。

## 注意事项与风险提示

-   **NaN 值**: 如果输入数据缺失或计算中出现 `NaN`（例如，相关性计算需要足够的数据点），相应的 Alpha 值将为 `NaN`。请确保数据完整性。
-   **排名方法**: `pandas` 的 `rank(method='average', pct=True)` 通常用于截面排名，结果是百分比形式。
-   **小数位数**: 最终的 Alpha#37 值及中间结果按要求保留两位小数。
-   **市场适用性**: 此因子在不同市场环境或资产类别上表现可能迥异。务必进行充分的回测和验证。
-   **数据质量**: 输入数据的准确性和完整性至关重要。

Alpha#37 是一个基于多项指标合成的因子，不保证未来表现。建议与其他因子结合使用，并进行充分的回测验证。

## 策略解读与计算示例

我们将以 `asset_1` 在日期 `2025-01-05` 的数据为例，展示 Alpha#37 的计算。

**背景数据 (源自 `alpha37_results.csv` for `asset_1` on `2025-01-05`):**
- `open` (2025-01-05): 100.00
- `close` (2025-01-05): 99.50
- `open` (2025-01-04): 101.00
- `close` (2025-01-04): 100.00
- `oc_diff` (2025-01-05): 0.50
- `corr_oc_delay1_close_200` (intermediate for 2025-01-05): 0.15 (假设值)
- `ranked_corr` (intermediate for 2025-01-05): 0.70 (假设值)
- `ranked_oc_diff` (intermediate for 2025-01-05): 0.30 (假设值)
- `alpha37` (2025-01-05): 1.00 (假设值)

**计算 Alpha#37 (简化示例，使用中间结果):**

1.  **`(open - close)` (2025-01-05):**
    `100.00 - 99.50 = 0.50`

2.  **`delay((open - close), 1)` (2025-01-05 对应的 2025-01-04):**
    `open` (2025-01-04) - `close` (2025-01-04) = `101.00 - 100.00 = 1.00`

3.  **`correlation(delay((open - close), 1), close, 200)` (2025-01-05):**
    假设经过200日时间序列相关性计算，在 `2025-01-05` 得到 `0.15`。

4.  **`rank(correlation(delay((open - close), 1), close, 200))` (2025-01-05):**
    假设对所有资产在 `2025-01-05` 的相关性值进行截面排名，`asset_1` 得到 `0.70`。

5.  **`rank((open - close))` (2025-01-05):**
    假设对所有资产在 `2025-01-05` 的 `(open - close)` 值进行截面排名，`asset_1` 得到 `0.30`。

6.  **最终 Alpha#37 值**：
    `ranked_corr + ranked_oc_diff = 0.70 + 0.30 = 1.00`

因此，`Alpha#37` 对 `asset_1` 在 `2025-01-05` 的最终计算值为 `1.00`。
这个值应与 `alpha37_results.csv` 中 `asset_1` 在 `2025-01-05` 的 `alpha37` 列的值相符。 