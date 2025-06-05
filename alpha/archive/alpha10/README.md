# Alpha#10: 条件性趋势跟随与反转因子

## 描述

Alpha#10 的计算公式为：

```
rank(((0 < ts_min(delta(close, 1), 4)) ? delta(close, 1) : ((ts_max(delta(close, 1), 4) < 0) ? delta(close, 1) : (-1 * delta(close, 1)))))
```

这个 Alpha 策略是一个条件性的因子，它结合了近期的价格变动方向和幅度，并根据过去几日价格变动的极值情况来决定是跟随趋势还是反转趋势。

**核心逻辑**:

1.  **定义组件**:
    *   `delta(close, 1)`: 当日收盘价 (`close`) 与昨日收盘价的差值，即单日价格变动。我们将其简写为 `d_close_1`。
    *   `ts_min(delta(close, 1), 4)`: 过去4天（包括当天）的 `d_close_1` 的最小值。我们将其简写为 `min_d_close_4`。
    *   `ts_max(delta(close, 1), 4)`: 过去4天（包括当天）的 `d_close_1` 的最大值。我们将其简写为 `max_d_close_4`。
    *   `rank(...)`: 对括号内计算得到的中间值在所有资产的同一天进行横截面排名。

2.  **条件逻辑 (括号内的部分)**:
    *   `intermediate_value = `
        *   **条件1**: `0 < min_d_close_4` (即过去4天每日价格都在上涨)
            *   若为 **True**: `intermediate_value = d_close_1` (今日价格仍在上涨，则跟随趋势，取正的日价格变动)。
        *   **条件2**: (当条件1为 False 时评估) `max_d_close_4 < 0` (即过去4天每日价格都在下跌)
            *   若为 **True**: `intermediate_value = d_close_1` (今日价格仍在下跌，则跟随趋势，取负的日价格变动)。
        *   **条件3**: (当条件1和条件2都为 False 时评估)
            *   这意味着过去4天内，既有价格上涨的日子，也有价格下跌的日子（或者有些日子价格无变动）。
            *   `intermediate_value = -1 * d_close_1` (此时采取反转逻辑，如果今日价格上涨，则取其负值；如果今日价格下跌，则取其正值)。

3.  **最终 Alpha 值**:
    *   `Alpha#10 = rank(intermediate_value)`
    *   将计算得到的 `intermediate_value` 在当日所有资产间进行横截面排名，排名结果（通常处理为百分位或者归一化到特定范围）即为最终的 Alpha#10 值。

**总结**:
*   如果过去4天价格持续上涨，且今天价格也上涨，则认为上涨趋势会持续，`intermediate_value` 为正。
*   如果过去4天价格持续下跌，且今天价格也下跌，则认为下跌趋势会持续，`intermediate_value` 为负。
*   如果过去4天价格波动（有涨有跌），则对今天的价格变动采取反转操作：今天涨则 `intermediate_value` 为负，今天跌则 `intermediate_value` 为正。
*   最后对这个 `intermediate_value` 进行横截面排名得到 Alpha 值。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha10/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#10
│   ├── alpha10_results.csv    # 计算得到的 Alpha#10 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#10 策略总结
```

## 使用步骤

### 1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。如果未安装，可以通过 pip 安装：

```bash
pip install pandas numpy
```

### 2. 生成模拟数据 (如果需要)

本 Alpha 依赖于 `close` 数据。`data/generate_mock_data.py` 脚本可以生成这些数据。如果 `data/mock_data.csv` 不存在或需要更新：

```bash
cd ../../data  # 假设当前在 alpha/alpha10 目录
python generate_mock_data.py
cd ../alpha/alpha10 # 返回 alpha/alpha10 目录
```
该脚本默认生成5只资产100天的数据。请确保生成的数据包含 `close` 列。

### 3. 计算 Alpha#10 因子

在 `alpha/alpha10` 目录并运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#10，并将结果保存到当前目录下的 `alpha10_results.csv`。同时会在终端打印部分结果和统计信息。

## Alpha#10 策略解读与计算示例

为了更好地理解计算过程，我们以 `alpha10_results.csv` 中 `asset_1` 在 `2025-01-08` 的数据为例进行分析。

### 实际数据快照 (asset_1, 2025-01-08)

从 `alpha10_results.csv` 中提取的相关数据：

| date       | asset_id | close  | delta_close_1 | ts_min_delta_close_1_4 | ts_max_delta_close_1_4 | intermediate_value | alpha10 |
|------------|----------|--------|---------------|------------------------|------------------------|--------------------|---------|
| 2025-01-05 | asset_1  | 100.50 | 1.10          | -0.80                  | 1.10                   | -1.10              | 0.60    |
| 2025-01-06 | asset_1  | 100.70 | 0.20          | -0.80                  | 1.10                   | -0.20              | 0.60    |
| 2025-01-07 | asset_1  | 102.10 | 1.40          | -0.80                  | 1.40                   | -1.40              | 0.30    |
| **2025-01-08** | **asset_1**  | **100.00** | **-2.10**         | **-2.10**                | **1.40**                 | **2.10**             | **1.00**  |

*(注意：表格中为四舍五入后的结果)*

### 计算步骤详解 (asset_1, 2025-01-08):

1.  **收集数据** (截至 2025-01-08):
    *   `close` (当日收盘价): 100.00
    *   `delta_close_1` (当日价格变动): -2.10 (100.00 - 102.10)
    *   过去4日 `delta_close_1` 序列 (包括当日):
        *   2025-01-05: 1.10
        *   2025-01-06: 0.20
        *   2025-01-07: 1.40
        *   2025-01-08: -2.10
    *   此4日 `delta_close_1` 序列为: `[1.10, 0.20, 1.40, -2.10]`

2.  **计算 `ts_min(delta(close, 1), 4)`**:
    *   `min_d_close_4` = `min([1.10, 0.20, 1.40, -2.10])` = -2.10.

3.  **计算 `ts_max(delta(close, 1), 4)`**:
    *   `max_d_close_4` = `max([1.10, 0.20, 1.40, -2.10])` = 1.40.

4.  **条件逻辑判断 `intermediate_value`**:
    *   **条件1**: `0 < min_d_close_4` (0 < -2.10) -> **False**.
    *   **条件2**: (当条件1为 False 时评估) `max_d_close_4 < 0` (1.40 < 0) -> **False**.
    *   **条件3**: (当条件1和条件2都为 False 时评估) -> **True**.
        *   `intermediate_value = -1 * delta_close_1 = -1 * (-2.10) = 2.10`.

5.  **横截面排名 (rank)**:
    *   `intermediate_value` 为 2.10。在2025-01-08这一天，asset_1的这个值与其他资产的相应值进行比较排名。
    *   从结果文件看，`alpha10` 为 1.00，这意味着 asset_1 当日的 `intermediate_value` (2.10) 在所有资产中是最高的（或并列最高）。

**解读 (asset_1, 2025-01-08)**:
在 `2025-01-08` 这一天，`asset_1` 的当日价格变动 (`delta_close_1`) 为 `-2.10`。在过去4天（包括当日）的每日价格变动中，最小值为 `-2.10`，最大值为 `1.40`。由于最小值不大于0，且最大值不小于0，表明市场在过去4天内处于震荡状态（既有上涨也有下跌）。因此，策略采用反转逻辑，`intermediate_value` 计算为当日价格变动的相反数，即 `2.10`。这个 `intermediate_value` 在当天所有资产中排名最高，因此最终 `alpha10` 值为 `1.00`。

### Alpha#10 实际数据统计 (基于 alpha10_results.csv)

对 `alpha10_results.csv` 中 `alpha10` 列（排除了因窗口期不足产生的NaN值）进行描述性统计，可以得到如下结果 (具体数值会根据您的 `mock_data.csv` 和计算脚本的精确运行而变化)：

```
count   495.00
mean      0.60
std       0.28
min       0.20
25%       0.40
50%       0.60
75%       0.80
max       1.00
Name: alpha10, dtype: float64
```
*(请运行 `alpha_calculator.py` 脚本以获取您数据对应的确切统计信息，以上为一次运行示例)*

这组统计数据显示了 Alpha#10 因子在模拟数据上的分布情况。均值为0.60，标准差为0.28，表明大部分Alpha值分布在较高的水平。最小值0.20和最大值1.00也符合百分位排名的预期。

## 数据需求
*   `date`: 交易日期
*   `asset_id`: 资产ID
*   `close`: 当日收盘价

## 输出格式
输出的 CSV 文件 (`alpha10_results.csv`) 将包含以下列：
*   `date`: 交易日期
*   `asset_id`: 资产ID
*   `close`: 当日收盘价 (原始数据)
*   `delta_close_1`: 当日价格与昨日价格的差 (计算中间值)
*   `ts_min_delta_close_1_4`: 过去4日 `delta_close_1` 的最小值 (计算中间值)
*   `ts_max_delta_close_1_4`: 过去4日 `delta_close_1` 的最大值 (计算中间值)
*   `intermediate_value`: 根据条件逻辑计算的中间值 (计算中间值)
*   `alpha10`: 计算得到的 Alpha#10 值 (横截面排名后的结果)，保留两位小数。

## 注意事项与风险提示
*   **数据窗口**: `delta(close, 1)` 需要至少1天历史数据。`ts_min` 和 `ts_max` 在窗口期为4时，需要至少4天的 `delta(close, 1)` 数据，这意味着从整体数据开始算，需要至少 `1 (for first delta) + 3 (for window) = 4` 天的 `close` 数据才能计算出第一个有效的 `ts_min` 和 `ts_max`。因此，在数据序列的早期，Alpha 值可能为 NaN。
*   **Rank 实现**: 横截面 `rank` 的具体实现（例如，是返回0-1的百分比排名，还是其他归一化方式）会影响最终 Alpha 值的范围和解释。
*   **条件判断的精确性**: `0 < ts_min` 和 `ts_max < 0` 的判断对于价格无变动 (delta=0) 的情况需要明确。按当前公式，如果 `ts_min` 为0，则 `0 < 0` 为 False。如果 `ts_max` 为0，则 `0 < 0` 为 False。
*   该 Alpha 结合了趋势跟随和反转逻辑，其有效性依赖于市场状态的正确判断。
*   Alpha#10 是基于历史价格模式的统计策略，不保证未来表现。建议与其他因子结合使用，并进行充分的回测验证。

## Alpha#10 与 Alpha#9 的比较

Alpha#10 和 Alpha#9 在核心逻辑上非常相似，都属于条件性趋势跟随/反转策略。它们都依赖于近期价格变动的历史极值来判断市场状态，并据此决定是跟随当日价格变动还是反转当日价格变动。

主要区别点：

1.  **历史窗口期 (Lookback Period)**:
    *   **Alpha#9**: 使用过去 **5天** 的 `delta(close, 1)` 来计算 `ts_min` 和 `ts_max`。
    *   **Alpha#10**: 使用过去 **4天** 的 `delta(close, 1)` 来计算 `ts_min` 和 `ts_max`。
    *   *影响*: Alpha#10 对市场状态的判断更为敏感，因为它依赖于一个更短的历史窗口。这可能使其对短期趋势变化反应更快，但也可能更容易受到短期市场噪音的影响。Alpha#9 则相对平滑一些。

2.  **最终输出 (Final Output)**:
    *   **Alpha#9**: 其直接输出是条件判断后的 `delta(close, 1)` 或 `-1 * delta(close, 1)`。这个值的量纲与价格变动相同。
    *   **Alpha#10**: 在计算出 `intermediate_value` (逻辑与 Alpha#9 的输出类似) 之后，还进行了一个额外的 **横截面排名 (`rank`)** 操作。
    *   *影响*: Alpha#10 的最终输出是一个经过排序的值（例如百分位），这使得不同资产之间的 Alpha 值具有可比性，并且其值域通常被归一化（例如，0到1之间或-1到1之间，具体取决于 `rank` 的实现）。而 Alpha#9 的原始输出值可能因资产价格和波动率的不同而差异很大。`rank` 操作通常用于构建多资产投资组合，因为它提供了相对强弱的信号。

3.  **公式结构**:
    *   Alpha#9 公式: `((0 < ts_min(delta(close, 1), 5)) ? delta(close, 1) : ((ts_max(delta(close, 1), 5) < 0) ? delta(close, 1) : (-1 * delta(close, 1))))`
    *   Alpha#10 公式: `rank(((0 < ts_min(delta(close, 1), 4)) ? delta(close, 1) : ((ts_max(delta(close, 1), 4) < 0) ? delta(close, 1) : (-1 * delta(close, 1)))))`

**总结相似性**:

*   两者都试图识别短期内的持续上涨、持续下跌或震荡行情。
*   在判断为持续上涨或持续下跌时，两者都采取趋势跟随策略（使用 `delta(close, 1)`）。
*   在判断为震荡行情时，两者都采取反转策略（使用 `-1 * delta(close, 1)`）。

**总结差异性**:

*   **敏感度**: Alpha#10 (4天窗口) 比 Alpha#9 (5天窗口) 更敏感。
*   **信号类型**: Alpha#9产生的是原始因子值，Alpha#10产生的是排名后的相对信号。这使得Alpha#10更适合直接用于跨资产比较和组合构建。

在实际应用中，选择哪个 Alpha 或如何结合使用它们，可能需要通过回测来评估它们在特定市场环境和资产类别上的表现。Alpha#10因为包含了`rank`操作，其信号的解释和使用方式与Alpha#9会有所不同。

如需帮助或有建议，欢迎交流！ 