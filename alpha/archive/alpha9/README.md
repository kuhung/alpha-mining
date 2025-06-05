# Alpha#9: 条件性趋势跟随/反转因子

## 描述

Alpha#9 的计算公式为：

```
((0 < ts_min(delta(close, 1), 5)) ? delta(close, 1) : ((ts_max(delta(close, 1), 5) < 0) ? delta(close, 1) : (-1 * delta(close, 1))))
```

这个 Alpha 策略是一个条件性的因子，它根据过去5天每日价格变动（`delta(close, 1)`）的最小值和最大值来决定是跟随当日趋势还是反转当日趋势。

**核心逻辑**:

1. **`delta(close, 1)`**: 当日收盘价 (`close`) 与昨日收盘价的差值，即当日价格变动。
2. **`ts_min(delta(close, 1), 5)`**: 过去5天中，每日价格变动的最小值。
3. **`ts_max(delta(close, 1), 5)`**: 过去5天中，每日价格变动的最大值。

**条件判断**:

* **条件1: `0 < ts_min(delta(close, 1), 5)`**

  * 如果过去5天每日价格变动的最小值大于0，意味着过去5天每天都在上涨（或者至少没有下跌）。
  * **策略**: 跟随趋势，Alpha#9 = `delta(close, 1)` (当日价格变动)。即如果今天继续涨，Alpha为正；如果今天跌了（虽然过去5天都涨），Alpha为负。
* **条件2: `ts_max(delta(close, 1), 5) < 0` (当条件1不成立时判断)**

  * 如果过去5天每日价格变动的最大值小于0，意味着过去5天每天都在下跌（或者至少没有上涨）。
  * **策略**: 跟随趋势，Alpha#9 = `delta(close, 1)` (当日价格变动)。即如果今天继续跌，Alpha为负；如果今天涨了（虽然过去5天都跌），Alpha为正。
* **条件3: (当条件1和条件2都不成立时)**

  * 这意味着过去5天内既有上涨也有下跌，不存在明确的单边持续趋势。
  * **策略**: 反转趋势，Alpha#9 = `-1 * delta(close, 1)`。即如果今天上涨，Alpha为负；如果今天下跌，Alpha为正。

**总结**:

* 如果过去5天持续上涨，则跟随当日价格变动。
* 如果过去5天持续下跌，则跟随当日价格变动。
* 如果过去5天内价格有涨有跌（震荡），则反转当日价格变动。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha9/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#9
│   ├── alpha9_results.csv     # 计算得到的 Alpha#9 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#9 策略总结
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
cd data
python generate_mock_data.py
cd ..
```

该脚本默认生成5只资产100天的数据。请确保生成的数据包含 `close` 列。

### 3. 计算 Alpha#9 因子

进入 `alpha/alpha9` 目录并运行 `alpha_calculator.py` 脚本：

```bash
cd alpha/alpha9
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#9，并将结果保存到当前目录下的 `alpha9_results.csv`。同时会在终端打印部分结果和统计信息。

## Alpha#9 策略解读与计算示例

Alpha#9 是一个基于过去短期趋势持续性的条件交易策略。

### 实际数据示例 (asset_1 from alpha9_results.csv)

以下为 `asset_1` 在 `alpha9_results.csv` 中部分日期的计算结果：

| date       | asset_id | close  | delta_close_1 | ts_min_delta_close_1_5 | ts_max_delta_close_1_5 | alpha9 |
|------------|----------|--------|---------------|------------------------|------------------------|--------|
| 2025-01-01 | asset_1  | 100.00 | NaN           | NaN                    | NaN                    | NaN    |
| 2025-01-02 | asset_1  | 100.10 | 0.10          | NaN                    | NaN                    | -0.10  |
| 2025-01-03 | asset_1  | 100.20 | 0.10          | NaN                    | NaN                    | -0.10  |
| 2025-01-04 | asset_1  | 99.40  | -0.80         | NaN                    | NaN                    | 0.80   |
| 2025-01-05 | asset_1  | 100.50 | 1.10          | NaN                    | NaN                    | -1.10  |
| 2025-01-06 | asset_1  | 100.70 | 0.20          | -0.80                  | 1.10                   | -0.20  |
| 2025-01-07 | asset_1  | 102.10 | 1.40          | -0.80                  | 1.40                   | -1.40  |
| 2025-01-08 | asset_1  | 100.00 | -2.10         | -2.10                  | 1.40                   | 2.10   |
| 2025-01-09 | asset_1  | 100.10 | 0.10          | -2.10                  | 1.40                   | -0.10  |
| 2025-01-10 | asset_1  | 100.70 | 0.60          | -2.10                  | 1.40                   | -0.60  |


### 计算步骤详解 (以 asset_1 在 2025-01-06 为例)

我们要计算 `asset_1` 在 `2025-01-06` 的 Alpha#9 值。

1.  **收集当日及历史数据**:
    *   当日 `close` (`2025-01-06`): 100.70
    *   当日 `delta_close_1` (`delta_today`): 0.20 (即 100.70 - 100.50)
    *   用于计算 `ts_min` 和 `ts_max` 的过去5日 `delta_close_1` 序列 (包括当日的 `delta_close_1`)：
        *   `delta(close,1)` on 2025-01-02: 0.10
        *   `delta(close,1)` on 2025-01-03: 0.10
        *   `delta(close,1)` on 2025-01-04: -0.80
        *   `delta(close,1)` on 2025-01-05: 1.10
        *   `delta(close,1)` on 2025-01-06: 0.20
    *   此5日 `delta_close_1` 序列为: `[0.10, 0.10, -0.80, 1.10, 0.20]`

2.  **计算 `ts_min(delta(close, 1), 5)`**:
    *   `min_delta_last_5` = `min([0.10, 0.10, -0.80, 1.10, 0.20])` = `-0.80`.

3.  **计算 `ts_max(delta(close, 1), 5)`**:
    *   `max_delta_last_5` = `max([0.10, 0.10, -0.80, 1.10, 0.20])` = `1.10`.

4.  **条件判断**:
    *   **条件1: `0 < min_delta_last_5`?** (Is `0 < -0.80`?)
        *   False.
    *   **条件2: `max_delta_last_5 < 0`?** (Is `1.10 < 0`?)
        *   False.
    *   **条件3 (Else case)**: 两个条件都不满足，因此 Alpha#9 = `-1 * delta_today`.

5.  **最终 Alpha 值**:
    *   `Alpha#9` = `-1 * 0.20` = `-0.20`.

**解读 (asset_1, 2025-01-06)**:
在 `2025-01-06` 这一天，`asset_1` 的当日价格变动 (`delta_close_1`) 为 `0.20`。在过去5天（包括当日）的每日价格变动中，最小值为 `-0.80`，最大值为 `1.10`。由于最小值不大于0，且最大值不小于0，表明市场在过去5天内处于震荡状态（既有上涨也有下跌）。因此，策略采用反转逻辑，Alpha#9 计算为当日价格变动的相反数，即 `-0.20`。

### Alpha#9 实际数据统计 (基于 alpha9_results.csv)

运行 `alpha/alpha9/alpha_calculator.py` 脚本后，终端会输出实际的统计数据。以下是某次运行的示例输出（您的具体数值可能会因输入数据而异）：

```
--- General Information ---
Total rows in result: 500
Number of unique assets: 5
Number of NaN values in delta_close_1: 5
Number of NaN values in ts_min_delta_close_1_5: 20
Number of NaN values in ts_max_delta_close_1_5: 20
Number of NaN values in alpha9: 5

Alpha9 column statistics (excluding NaNs):
count   495.00
mean      0.03
std       1.53
min      -4.20
25%      -0.90
50%       0.00
75%       1.00
max       4.20
Name: alpha9, dtype: float64
```

这些统计数据显示了 Alpha#9 因子在模拟数据上的分布情况。例如，`alpha9` 列的均值为 `0.03`，标准差为 `1.53`，值域从 `-4.20` 到 `4.20`。这可以帮助理解该因子的分布和潜在信号强度。

## 数据需求

* `date`: 交易日期
* `asset_id`: 资产ID
* `close`: 当日收盘价 (用于计算 `delta(close, 1)`)

## 输出格式

输出的 CSV 文件 (`alpha9_results.csv`) 将包含以下列：

* `date`: 交易日期
* `asset_id`: 资产ID
* `close`: 当日收盘价 (原始数据)
* `delta_close_1`: 当日价格变动 `close - prev_close` (计算中间值)
* `ts_min_delta_close_1_5`: 过去5日 `delta(close,1)` 的最小值 (计算中间值)
* `ts_max_delta_close_1_5`: 过去5日 `delta(close,1)` 的最大值 (计算中间值)
* `alpha9`: 计算得到的 Alpha#9 值，保留两位小数。

## 注意事项与风险提示

* **数据窗口**: `delta(close, 1)` 需要至少1天历史数据。`ts_min` 和 `ts_max` 在5日窗口上操作，因此有效计算 Alpha#9 需要至少5个 `delta(close, 1)` 值，即对应资产至少有6条连续的 `close` 数据。对于每个资产，在数据序列的早期（前5天），`alpha9` 的计算会因 `ts_min/ts_max` 的 NaN 值而使用默认逻辑 (`-1 * delta_close_1`)，首日的 `alpha9` 会因 `delta_close_1` 为 NaN 而是 NaN。
* **交易成本**: 该策略可能产生频繁的交易信号，实际应用中需考虑交易成本的影响。
* **趋势定义**: "趋势持续"的定义依赖于固定的5天窗口，可能不适用于所有市场状况或资产特性。
* Alpha#9 是基于历史价格模式的统计策略，不保证未来表现。建议与其他因子结合使用，并进行充分的回测验证。

如需帮助或有建议，欢迎交流！
