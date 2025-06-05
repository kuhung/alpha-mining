# Alpha#18: 波动、日内趋势与开收盘价相关性的综合排名

## 描述

Alpha#18 的计算公式为：

```
Alpha#18 = (-1 * rank(((stddev(abs((close - open)), 5) + (close - open)) + correlation(close, open, 10))))
```

这个 Alpha 策略综合了三个主要部分：
1.  **近期日内振幅的波动性**: `stddev(abs((close - open)), 5)`
    *   `abs((close - open))` 计算每日收盘价与开盘价差的绝对值，代表当日价格的实际振幅。
    *   `stddev(..., 5)` 计算这个日振幅在过去5天内的标准差，衡量近期振幅的稳定性或波动性。值越大，表明近期日内振幅波动越大。
2.  **当日价格变动方向与幅度**: `(close - open)`
    *   这直接反映了当日从开盘到收盘的价格净变化。正值表示上涨，负值表示下跌。
3.  **开盘价与收盘价的短期相关性**: `correlation(close, open, 10)`
    *   计算过去10天内，每日收盘价和开盘价之间的相关性。这可以揭示开盘价对收盘价的短期预测性或联动性。

这三部分加总后，形成一个综合指标。然后对这个综合指标进行截面排名（`rank(...)`），最后乘以 `-1`。这意味着，综合指标值较低（更负或更小正值）的资产，将获得较高的 Alpha#18 因子值。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据 (需包含 open, close)
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha18/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#18
│   ├── alpha18_results.csv    # 计算得到的 Alpha#18 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#18 策略简介
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
cd ../../data # 假设当前在 alpha/alpha18 目录
python generate_mock_data.py # 假设此脚本能生成所需字段
cd ../alpha/alpha18
```
默认的 `mock_data.csv` 应该已经包含了 `open` 和 `close` 字段。

### 3. 计算 Alpha#18 因子

进入 `alpha/alpha18` 目录并运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#18，并将结果保存到当前目录下的 `alpha18_results.csv`。

## Alpha#18 策略解读与计算步骤概述

1.  **计算日内振幅的绝对值**:
    *   对每个资产，计算每日 `abs(close - open)` 作为日内振幅的绝对值。
2.  **计算振幅标准差**:
    *   对每个资产，计算步骤1中日内振幅在过去5天的滚动标准差 `stddev_abs_co_5`。
3.  **计算日内价格变动**:
    *   对每个资产，计算每日 `close - open` 作为 `co_diff`。
4.  **计算开收盘价相关性**:
    *   对每个资产，计算过去10天 `close` 和 `open` 价格的滚动相关性 `corr_close_open_10`。
5.  **合并指标**:
    *   将上述三部分加总：`combined_value = stddev_abs_co_5 + co_diff + corr_close_open_10`。
6.  **截面排名与反转**:
    *   对每日所有资产的 `combined_value` 进行升序截面排名（百分比排名），然后乘以 -1 得到最终的 `Alpha#18` 值。

## Alpha#18 策略解读与计算示例

### 数据快照 (asset_1, 2025-01-24)

根据 `alpha18_results.csv` 的实际数据，我们选取 `asset_1` 在 `2025-01-24` 的数据作为示例：

| date       | asset_id | open  | close | abs_close_minus_open | stddev_abs_co_5 | co_diff | corr_close_open_10 | combined_value | rank_combined_value | alpha18 |
|------------|----------|-------|-------|---------------------|-----------------|---------|-------------------|----------------|-------------------|---------|
| 2025-01-24 | asset_1  | 97.00 | 97.20 | 0.200              | 1.550          | 0.200   | 0.072            | 1.822          | 0.800             | -0.800  |

### 计算步骤详解 (asset_1, 2025-01-24):

1.  **日内振幅的绝对值**:
    *   `abs_close_minus_open = abs(97.20 - 97.00) = 0.200`

2.  **振幅标准差**:
    *   过去5天的日内振幅标准差 `stddev_abs_co_5 = 1.550`

3.  **日内价格变动**:
    *   `co_diff = close - open = 97.20 - 97.00 = 0.200`

4.  **开收盘价相关性**:
    *   过去10天的开收盘价相关性 `corr_close_open_10 = 0.072`

5.  **合并指标**:
    *   `combined_value = 1.550 + 0.200 + 0.072 = 1.822`

6.  **最终 Alpha#18 值**:
    *   `rank_combined_value = 0.800` (表示在当日所有资产中，`combined_value` 排在第80%分位)
    *   `Alpha#18 = -1 * 0.800 = -0.800`

**解读 (asset_1, 2025-01-24)**:
在 `2025-01-24` 这一天，`asset_1`：
*   近期日内振幅波动性较大 (`stddev_abs_co_5 = 1.550`)
*   当日呈现小幅上涨 (`co_diff = 0.200`)
*   开收盘价几乎不相关 (`corr_close_open_10 = 0.072`)
综合这三个因素，`asset_1` 的综合指标值在市场中排名较高（第80%分位），最终得到一个较低的 Alpha#18 值 `-0.800`。

## 数据需求

-   `date`: 交易日期 (datetime)
-   `asset_id`: 资产ID (string/object)
-   `open`: 每日开盘价 (float)
-   `close`: 每日收盘价 (float)
-   (脚本可能包含 `high`, `low`, `volume`, `returns` 等在 `mock_data.csv` 中的其他列，以保持数据完整性，即使它们不直接用于此 Alpha 计算)

## 输出格式

输出的 CSV 文件 (`alpha18_results.csv`) 将包含以下列（除了原始数据列），所有数值型 alpha 相关列均保留一定小数位数，最终 Alpha#18 保留两位有效数字：

-   `date`: 交易日期
-   `asset_id`: 资产ID
-   `open`, `high`, `low`, `close`, `volume`, `returns`: 原始数据中的对应列（如果存在）
-   `abs_close_minus_open`: `abs(close - open)`
-   `stddev_abs_co_5`: `stddev(abs(close - open), 5)`，过去5日 `abs_close_minus_open` 的滚动标准差
-   `co_diff`: `close - open`，日内价格变动
-   `corr_close_open_10`: `correlation(close, open, 10)`，过去10日收盘价与开盘价的滚动相关性
-   `combined_value`: `stddev_abs_co_5 + co_diff + corr_close_open_10`
-   `rank_combined_value`: `combined_value` 的当日截面百分比排名
-   `alpha18`: 最终计算的 Alpha#18 值 (`-1 * rank_combined_value`)

## 注意事项与风险提示

-   **数据窗口期**:
    *   `stddev(abs((close - open)), 5)`: 计算标准差需要至少5天的数据。因此，每个资产的前4天该值为NaN。
    *   `correlation(close, open, 10)`: 计算相关性需要至少10天的数据。因此，每个资产的前9天该值为NaN。
    *   综合来看，`combined_value` 的第一个非NaN值取决于最长的窗口期，即10天。因此，每个资产数据序列的前9行其 `alpha18` 很可能为NaN。
-   **排名方法**: `pandas` 的 `rank(pct=True)` 方法用于所有截面排名，这意味着结果是百分比形式的排名。
-   **相关性与标准差计算**: `pandas` 的 `rolling().corr()` 和 `rolling().std()` 方法用于计算。确保窗口期内有足够非NaN数据点以避免结果全为NaN。如果窗口期内数据完全相同（例如 `abs(close-open)` 在5天内不变），标准差可能为0。
-   **小数位数**: 中间步骤建议保留足够精度，最终 Alpha#18 结果将按要求格式化为两位有效数字。
-   **市场适用性**: 此因子表现可能因市场环境、资产类别而异。需进行充分回测验证。
-   **数据质量**: 输入数据的准确性和完整性至关重要。

Alpha#18 是一个结合了波动性、趋势和价格关系的复合因子，不保证未来表现。建议与其他因子结合使用，并进行充分的回测验证。 