# Alpha#38: 反向时间序列排名与日内波动排名

## 因子定义

```
((-1 * rank(Ts_Rank(close, 10))) * rank((close / open)))
```

## 计算逻辑

该因子结合了收盘价在短期时间序列中的反向排名与日内价格波动（开盘价与收盘价之比）的截面排名，旨在识别那些近期表现相对较弱，但日内波动较大的资产。它可能捕捉到短期超卖且具有潜在反转动力的股票。

1.  **`(close / open)`**:
    *   计算每日收盘价与开盘价的比值。这代表了当日的价格变化。如果比值大于1，表示收涨；小于1则表示收跌。

2.  **`rank((close / open))`**:
    *   对每日 `(close / open)` 的结果进行截面排名。排名越高，表示当日收盘价相对于开盘价的涨幅越大，或跌幅越小（如果排序是升序）。

3.  **`Ts_Rank(close, 10)`**:
    *   计算当前 `close` 价格在过去10个交易日中的时间序列排名。这反映了当前收盘价在近期历史中的相对位置。例如，如果 `Ts_Rank` 接近1，表示当前收盘价是过去10天中的最高点之一；如果接近0，则表示最低点之一。

4.  **`rank(Ts_Rank(close, 10))`**:
    *   对上述 `Ts_Rank(close, 10)` 的结果进行截面排名。排名越高，表示该资产的近期收盘价在所有资产中处于近期历史高位。

5.  **`(-1 * rank(Ts_Rank(close, 10)))`**:
    *   将步骤4的结果乘以-1。这意味着，如果一个资产的近期收盘价在截面上处于历史高位（`rank(Ts_Rank(close, 10))` 值高），那么这一部分的值会是负数且绝对值大。反之，如果近期收盘价在截面上处于历史低位，则这一部分的值会是正数且绝对值大。这旨在筛选出近期表现相对较弱的资产。

6.  **最终因子值**：
    *   将步骤5（反向时间序列排名）和步骤2（日内波动排名）的结果相乘。
    *   高的因子值通常意味着：
        *   资产近期收盘价在截面上处于历史低位（即 `Ts_Rank` 值小，乘以-1后变大）。
        *   当日的收盘价与开盘价的比值在截面上相对较大（收盘价相对于开盘价涨幅大或跌幅小）。
    *   此组合旨在寻找那些近期下跌但当日出现企稳或反弹迹象的资产。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据 (确保包含 open, close 字段)
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha38/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#38
│   ├── alpha38_results.csv    # 计算得到的 Alpha#38 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#38 策略简介
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
cd ../../data # 假设当前在 alpha/alpha38 目录
python generate_mock_data.py # 假设此脚本能生成所需字段
cd ../alpha/alpha38
```

### 3. 计算 Alpha#38 因子

进入 `alpha/alpha38` 目录并运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#38，并将结果保存到当前目录下的 `alpha38_results.csv`。

## 数据输入

*   `open`: 每日开盘价数据。
*   `close`: 每日收盘价数据。

这些数据预计从 `../../data/mock_data.csv` 文件中获取。

## 输出格式

输出的 CSV 文件 (`alpha38_results.csv`) 将包含以下列（除了原始数据列），所有数值型 alpha 相关列均保留两位小数：

-   `date`: 交易日期
-   `asset_id`: 资产ID
-   `open`, `high`, `low`, `close`, `volume`, `vwap`, `returns`: 原始数据中的对应列
-   `close_over_open`: `(close / open)` 中间计算结果
-   `ranked_close_over_open`: `rank((close / open))` 中间计算结果
-   `ts_rank_close_10`: `Ts_Rank(close, 10)` 中间计算结果
-   `ranked_ts_rank_close_10`: `rank(Ts_Rank(close, 10))` 中间计算结果
-   `neg_ranked_ts_rank`: `(-1 * rank(Ts_Rank(close, 10)))` 中间计算结果
-   `alpha38`: 最终计算的 Alpha#38 值。

## 注意事项与风险提示

-   **NaN 值**: 如果输入数据缺失或计算中出现 `NaN`（例如，排名或时间序列操作需要足够的数据点），相应的 Alpha 值将为 `NaN`。请确保数据完整性。
-   **排名方法**: `pandas` 的 `rank(method='average', pct=True)` 通常用于截面排名，结果是百分比形式。
-   **小数位数**: 最终的 Alpha#38 值及中间结果按要求保留两位小数。
-   **市场适用性**: 此因子在不同市场环境或资产类别上表现可能迥异。务必进行充分的回测和验证。
-   **数据质量**: 输入数据的准确性和完整性至关重要。

Alpha#38 是一个基于多项指标合成的因子，不保证未来表现。建议与其他因子结合使用，并进行充分的回测验证。

## 策略解读与计算示例

我们将以 `asset_1` 在日期 `2024-06-10` 的数据为例，展示 Alpha#38 的计算。

**背景数据 (源自 `alpha38_results.csv` for `asset_1` on `2024-06-10`):**
- `open` (2024-06-10): 104.28
- `close` (2024-06-10): 105.80
- `ts_rank_close_10` (2024-06-10): 1.00

**计算 Alpha#38 (简化示例，使用中间结果):**

1.  **`(close / open)` (2024-06-10):**
    `105.80 / 104.28 = 1.01` (保留两位小数)

2.  **`rank((close / open))` (2024-06-10):**
    假设对所有资产在 `2024-06-10` 的 `(close / open)` 值进行截面排名，`asset_1` 得到 `0.80`。

3.  **`Ts_Rank(close, 10)` (2024-06-10):**
    在 `2024-06-10`，`asset_1` 的 `close` 价格在过去10天的 `Ts_Rank` 为 `1.00`。

4.  **`rank(Ts_Rank(close, 10))` (2024-06-10):**
    假设对所有资产在 `2024-06-10` 的 `Ts_Rank(close, 10)` 值进行截面排名，`asset_1` 得到 `0.90`。

5.  **`(-1 * rank(Ts_Rank(close, 10)))` (2024-06-10):**
    `-1 * 0.90 = -0.90`

6.  **最终 Alpha#38 值**：
    `neg_ranked_ts_rank * ranked_close_over_open = -0.90 * 0.80 = -0.72`

因此，`Alpha#38` 对 `asset_1` 在 `2024-06-10` 的最终计算值为 `-0.72`。
这个值应与 `alpha38_results.csv` 中 `asset_1` 在 `2024-06-10` 的 `alpha38` 列的值相符。 