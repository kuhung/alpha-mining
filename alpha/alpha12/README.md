# Alpha#12: 成交量变动方向与价格反转因子

## 描述

Alpha#12 的计算公式为：

```
(sign(delta(volume, 1)) * (-1 * delta(close, 1)))
```

这个 Alpha 策略结合了成交量的变动方向和价格的反向变动。它旨在捕捉当成交量发生显著变化时，价格可能出现反转的信号。

**核心逻辑**:

1.  **`delta(volume, 1)`**: 当日成交量 (`volume`) 与昨日成交量的差值。这代表了成交量的短期变化。
2.  **`sign(delta(volume, 1))`**: 取上述成交量差值的符号：
    *   如果当日成交量 > 昨日成交量 (放量)，则为 `1`。
    *   如果当日成交量 < 昨日成交量 (缩量)，则为 `-1`。
    *   如果当日成交量 = 昨日成交量 (平量)，则为 `0`。
3.  **`delta(close, 1)`**: 当日收盘价 (`close`) 与昨日收盘价的差值，即当日价格变动。
4.  **`(-1 * delta(close, 1))`**: 当日价格变动的相反数。这代表了价格反转的潜在方向。

**计算步骤**:

*   计算当日成交量与昨日成交量的差值 `delta_volume_1`。
*   取 `delta_volume_1` 的符号 `sign_delta_volume_1`。
*   计算当日收盘价与昨日收盘价的差值 `delta_close_1`。
*   计算 `delta_close_1` 的相反数 `neg_delta_close_1`。
*   最终 Alpha#12 = `sign_delta_volume_1 * neg_delta_close_1`。

**解读**:

*   **放量上涨，因子看跌**: 如果成交量增加 (`sign_delta_volume_1 = 1`) 且价格上涨 (`delta_close_1 > 0`)，则因子值为负 (`1 * (-1 * 正数) = 负数`)。这可能意味着上涨动能可能衰竭，市场预期价格反转下跌。
*   **放量下跌，因子看涨**: 如果成交量增加 (`sign_delta_volume_1 = 1`) 且价格下跌 (`delta_close_1 < 0`)，则因子值为正 (`1 * (-1 * 负数) = 正数`)。这可能意味着恐慌抛售或下跌动能释放完毕，市场预期价格反转上涨。
*   **缩量上涨，因子看涨**: 如果成交量减少 (`sign_delta_volume_1 = -1`) 且价格上涨 (`delta_close_1 > 0`)，则因子值为正 (`-1 * (-1 * 正数) = 正数`)。因子逻辑认为，在缩量情况下，价格变动的反方向乘以成交量变动方向的负号，仍指向价格反转。
*   **缩量下跌，因子看跌**: 如果成交量减少 (`sign_delta_volume_1 = -1`) 且价格下跌 (`delta_close_1 < 0`)，则因子值为负 (`-1 * (-1 * 负数) = 负数`)。同上，因子逻辑指向价格反转。
*   **成交量不变**: 如果成交量不变 (`sign_delta_volume_1 = 0`)，则 Alpha#12 始终为 `0`，信号为中性。

**总结**:
该因子试图捕捉由成交量变化所指示的市场情绪，并结合价格的反向变动来产生交易信号。其核心思想是，当成交量放大时，价格有反转的倾向；当成交量缩小时，因子依然预期价格反转，因为`sign(delta(volume,1))`为-1，乘以`-1 * delta(close,1)`后，其逻辑与放量情况下的反转逻辑一致。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha12/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#12
│   ├── alpha12_results.csv    # 计算得到的 Alpha#12 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#12 策略总结
```

## 使用步骤

### 1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。如果未安装，可以通过 pip 安装：

```bash
pip install pandas numpy
```

### 2. 生成模拟数据 (如果需要)

本 Alpha 依赖于 `date`, `asset_id`, `close` 和 `volume` 数据。`data/generate_mock_data.py` 脚本可以生成这些数据。如果 `data/mock_data.csv` 不存在或需要更新：

```bash
cd ../../data  # 假设当前在 alpha/alpha12 目录
python generate_mock_data.py # 确保此脚本会生成 close 和 volume 列
cd ../alpha/alpha12 # 返回 alpha/alpha12 目录
```
请检查 `generate_mock_data.py` 以确保它生成了所需列。

### 3. 计算 Alpha#12 因子

在 `alpha/alpha12` 目录并运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#12，并将结果（包括中间计算列）保存到当前目录下的 `alpha12_results.csv`。同时会在终端打印部分结果和统计信息。

## Alpha#12 策略解读与计算示例

### 实际数据快照 (asset_1, 2025-01-04)

从 `alpha12_results.csv` 中提取的相关数据 (以 asset_1 在 2025-01-04 为例)：

| date       | asset_id | close | volume  | delta_close_1 | delta_volume_1 | sign_delta_volume_1 | alpha12 |
|------------|----------|-------|---------|---------------|----------------|---------------------|---------|
| 2025-01-03 | asset_1  | 100.20| 794092  | 0.10          | -442218.00     | -1.00               | 0.10    |
| **2025-01-04** | **asset_1**  | **99.40** | **1279416** | **-0.80**     | **485324.00**      | **1.00**            | **0.80**  |

*(注意：表格中为四舍五入后的结果，实际计算使用原始精度)*

### 计算步骤详解 (asset_1, 2025-01-04):

1.  **收集数据** (asset_1):
    *   `close` (当日, 2025-01-04): 99.40
    *   `volume` (当日, 2025-01-04): 1279416
    *   `close` (昨日, 2025-01-03): 100.20
    *   `volume` (昨日, 2025-01-03): 794092

2.  **计算 `delta_close_1`**:
    *   `delta_close_1` = `close (当日) - close (昨日)`
    *   `delta_close_1` = `99.40 - 100.20 = -0.80`

3.  **计算 `delta_volume_1`**:
    *   `delta_volume_1` = `volume (当日) - volume (昨日)`
    *   `delta_volume_1` = `1279416 - 794092 = 485324`

4.  **计算 `sign_delta_volume_1`**:
    *   `sign_delta_volume_1` = `sign(485324)` = `1.00`

5.  **计算 Alpha#12**:
    *   `alpha12` = `sign_delta_volume_1 * (-1 * delta_close_1)`
    *   `alpha12` = `1.00 * (-1 * -0.80)`
    *   `alpha12` = `1.00 * 0.80`
    *   `alpha12` = `0.80`

**解读 (asset_1, 2025-01-04)**:
在 `2025-01-04` 这一天，`asset_1` 的成交量较昨日增加 (`delta_volume_1 = 485324`, 因此 `sign_delta_volume_1 = 1`)，而收盘价较昨日下跌 (`delta_close_1 = -0.80`)。根据 Alpha#12 的逻辑（放量下跌，因子看涨），`alpha12` 值为 `0.80`，表示一个看涨信号，预期价格反转上涨。

## Alpha#12 实际数据统计 (基于 alpha12_results.csv)

运行 `alpha_calculator.py` 脚本后，会输出 Alpha#12 因子在所有资产上的统计信息。以下是本次运行的统计结果 (具体数值会根据您的 `mock_data.csv` 和计算脚本的精确运行而变化)：

```
--- General Information ---
Total rows in result: 500
Number of unique assets: 5
Number of NaN values in delta_close_1: 5 (expected for first day of each asset)
Number of NaN values in delta_volume_1: 5 (expected for first day of each asset)
Number of NaN values in sign_delta_volume_1: 5 (can happen if delta_volume_1 is NaN)
Number of NaN values in alpha12: 5 (expected due to deltas or if delta_volume_1 is zero then sign is zero)

Alpha12 column statistics (excluding NaNs):
count   495.00
mean     -0.03
std       1.53
min      -4.20
25%      -1.00
50%       0.00
75%       0.90
max       4.20
Name: alpha12, dtype: float64
```
这组统计数据显示了 Alpha#12 因子在模拟数据上的分布情况。均值接近0，标准差为1.53，表明 Alpha 值有一定的波动范围。最小值和最大值分别为 -4.20 和 4.20。这些统计数据有助于理解该因子的典型值域和离散程度。

## 数据需求
*   `date`: 交易日期 (YYYY-MM-DD 格式)
*   `asset_id`: 资产的唯一标识符
*   `close`: 当日收盘价 (浮点数)
*   `volume`: 当日成交量 (整数或浮点数)

## 输出格式
输出的 CSV 文件 (`alpha12_results.csv`) 将包含以下列，所有浮点数默认保留两位小数：
*   `date`: 交易日期
*   `asset_id`: 资产ID
*   `close`: 当日收盘价 (原始数据)
*   `volume`: 当日成交量 (原始数据)
*   `delta_close_1`: 当日价格与昨日价格的差 (计算中间值，保留两位小数)
*   `delta_volume_1`: 当日成交量与昨日成交量的差 (计算中间值，保留整数)
*   `sign_delta_volume_1`: 成交量差值的符号 (计算中间值，1.0, -1.0 或 0.0)
*   `alpha12`: 计算得到的 Alpha#12 值 (保留两位小数)。

## 注意事项与风险提示
*   **数据窗口**: `delta(close, 1)` 和 `delta(volume, 1)` 都需要至少1天的历史数据才能计算。因此，对于每个资产，在数据序列的开始，第一个 Alpha 值将为 NaN。
*   **成交量数据的质量**: 成交量数据的准确性和一致性对该因子的表现至关重要。异常的成交量数据（如股票分割、增发等未经调整的数据，或数据源错误）可能会产生误导性信号。
*   **零成交量变动**: 当 `delta(volume, 1)` 为零时，`sign(0)` 在 `numpy.sign` 中定义为 `0`，这将导致 Alpha#12 计算结果为 `0`。这种情况下，因子信号为中性。
*   **市场适用性**: 该 Alpha 结合了成交量和价格的反转逻辑。其有效性高度依赖于特定市场行为是否符合其核心假设（即成交量变化预示价格反转）。在趋势性强的市场中，反转信号可能表现不佳。
*   **回测与验证**: Alpha#12 是基于历史价格和成交量模式的统计策略，不保证未来表现。建议与其他因子结合使用，并在不同的市场环境和资产类别上进行充分的回测和验证，以评估其有效性和稳健性。
*   **交易成本**: 如果该因子产生的信号较为频繁，实际交易中需考虑交易成本对策略表现的影响。

如需帮助或有建议，欢迎交流！ 