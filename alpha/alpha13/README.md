# Alpha#13: 收盘价与成交量排名的协方差因子

## 描述

Alpha#13 的计算公式为：

```
(-1 * rank(covariance(rank(close), rank(volume), 5)))
```

这个 Alpha 策略计算的是过去5天收盘价排名和成交量排名的协方差，然后对这个协方差取截面排名，最后乘以-1。

**核心逻辑**:

1.  **数据排名**:
    *   `rank(close)`: 对每日的收盘价 `close` 进行所有资产间的横截面排名 (百分位排名)。
    *   `rank(volume)`: 对每日的成交量 `volume` 进行所有资产间的横截面排名 (百分位排名)。
2.  **时间序列协方差**:
    *   `covariance(rank(close), rank(volume), 5)`: 对于每只资产，取其过去5天（包括当天）的 `rank(close)` 序列和 `rank(volume)` 序列，计算这两个时间序列的协方差。
3.  **协方差排名与最终 Alpha**:
    *   `rank(covariance(...))`: 对步骤2中计算得到的协方差值在所有资产的同一天进行横截面排名。
    *   `Alpha#13 = -1 * rank(covariance(...))`: 将上述排名取负得到最终的 Alpha 值。

**解读**:
该因子旨在识别那些"收盘价市场排名"和"成交量市场排名"在近期（5日窗口）表现出特定相关性的股票。
*   计算得到的 `covariance(rank(close), rank(volume), 5)`：
    *   正值较大：表明股票的价格排名和成交量排名倾向于同向变动（价涨量增排名同升，价跌量缩排名同降），意味着价量配合良好。
    *   负值较大（绝对值）：表明股票的价格排名和成交量排名倾向于反向变动（价涨量缩排名背离，或价跌量增排名背离），意味着价量背离。
*   通过对这个协方差进行排名 (`rank_cov`)，我们得到一个相对强弱的指标。排名越高，意味着该股票的价量配合模式（无论是正相关还是负相关）在其协方差的具体数值上，相比其他股票更为突出。
*   最后乘以 `-1`，意味着原始协方差排名越高的股票（即协方差本身在所有股票中数值越大，通常代表更强的正相关性），其最终 Alpha 值越低（越负）。反之，如果原始协方差排名较低（协方差本身数值较小，甚至是负值），其最终 Alpha 值会较高（更接近0或为正）。
*   因此，Alpha#13倾向于给予那些"价量排名协方差"在全体股票中不突出（协方差值较小或为负，导致协方差排名较低）的股票更高的 Alpha 值。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha13/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#13
│   ├── alpha13_results.csv    # 计算得到的 Alpha#13 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#13 策略总结
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
cd ../../data  # 假设当前在 alpha/alpha13 目录
python generate_mock_data.py # 确保此脚本会生成 close 和 volume 列
cd ../alpha/alpha13 # 返回 alpha/alpha13 目录
```
请检查 `generate_mock_data.py` 以确保它生成了所需列。

### 3. 计算 Alpha#13 因子

在 `alpha/alpha13` 目录并运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#13，并将结果（包括原始数据和中间计算列）保存到当前目录下的 `alpha13_results.csv`。同时会在终端打印部分结果和统计信息。

## Alpha#13 策略解读与计算示例

### 实际数据快照 (asset_1, 2025-01-05)

从 `alpha13_results.csv` 中提取 `asset_1` 在 `2025-01-05` 的数据：

| date       | asset_id | close | volume  | rank_close | rank_volume | cov_rank_close_rank_volume_5 | rank_cov | alpha13 |
|------------|----------|-------|---------|------------|-------------|------------------------------|----------|---------|
| 2025-01-05 | asset_1  | 100.5 | 1327947 | 0.8        | 0.8         | 0.0120                       | 0.6      | -0.6    |

*注：为清晰起见，协方差值显示为0.0120，实际计算时精度可能更高。*

### 计算步骤详解 (asset_1, 2025-01-05):

1.  **收集 `asset_1` 过去5天 (含2025-01-05) 的 `rank_close` 和 `rank_volume` 数据**:
    *   `rank_close` 序列: `[0.6, 0.8, 0.8, 0.8, 0.8]` (日期从 2025-01-01 到 2025-01-05)
    *   `rank_volume` 序列: `[0.4, 1.0, 0.6, 0.4, 0.8]` (日期从 2025-01-01 到 2025-01-05)

2.  **计算 `covariance(rank_close_series, rank_volume_series, 5)`**:
    *   使用上述两个长度为5的序列，计算它们的样本协方差。
    *   根据脚本的输出，这个值为 `0.0120` (此处显示为4位小数，脚本内部会先计算完整精度再进行最终的alpha输出)。

3.  **横截面排名 `rank_cov`**:
    *   在 `2025-01-05` 这一天，`asset_1` 计算得到的 `cov_rank_close_rank_volume_5` (0.0120) 与当日所有其他资产计算得到的协方差值进行比较排名。
    *   从结果文件看，`asset_1` 当日的 `rank_cov` 为 `0.6`。

4.  **最终 Alpha#13 值**:
    *   `Alpha#13 = -1 * rank_cov`
    *   `Alpha#13 = -1 * 0.6 = -0.6`

**解读 (asset_1, 2025-01-05)**:
在 `2025-01-05` 这一天，`asset_1` 的收盘价排名和成交量排名的5日协方差为 `0.0120`，这是一个较小的正值，表明过去5天其价格排名和成交量排名之间存在轻微的正相关。这个协方差值在当日所有资产中进行排名后得到 `rank_cov = 0.6` (即处于60%分位)。最终Alpha值为 `-0.6`。

### Alpha#13 实际数据统计 (基于 alpha13_results.csv)

运行 `alpha_calculator.py` 脚本后，会输出 Alpha#13 因子在所有资产上的统计信息。以下是本次运行的统计结果：

```
count   480.00
mean     -0.60
std       0.24
min      -1.00
25%      -0.80
50%      -0.60
75%      -0.40
max      -0.20
Name: alpha13, dtype: float64
```
*(NaN 值数量: 20 (总计 500 行), 预期由初始计算窗口期和协方差/排名计算时组内数量不足导致)*

这组统计数据显示了 Alpha#13 因子在模拟数据上的分布情况。均值为-0.60，标准差为0.24。因子值主要分布在-1.00到-0.20之间。

## 数据需求
*   `date`: 交易日期 (YYYY-MM-DD 格式)
*   `asset_id`: 资产的唯一标识符
*   `close`: 当日收盘价 (浮点数)
*   `volume`: 当日成交量 (整数或浮点数)

## 输出格式
输出的 CSV 文件 (`alpha13_results.csv`) 将包含以下列：
*   `date`: 交易日期
*   `asset_id`: 资产ID
*   `close`: 当日收盘价 (原始数据)
*   `volume`: 当日成交量 (原始数据)
*   `rank_close`: 当日收盘价的横截面百分位排名 (计算中间值，DataFrame中保留较高精度，CSV中按需存储)
*   `rank_volume`: 当日成交量的横截面百分位排名 (计算中间值，DataFrame中保留较高精度，CSV中按需存储)
*   `cov_rank_close_rank_volume_5`: `rank_close` 和 `rank_volume` 在过去5日窗口的协方差 (计算中间值，DataFrame中保留4位小数，CSV中按需存储)
*   `rank_cov`: `cov_rank_close_rank_volume_5` 的横截面百分位排名 (计算中间值，DataFrame中保留较高精度，CSV中按需存储)
*   `alpha13`: 计算得到的 Alpha#13 值 (`-1 * rank_cov`)，在CSV中以较高精度存储，控制台预览时显示两位小数。

## 注意事项与风险提示
*   **数据窗口**: `covariance` 函数窗口期为5，这意味着需要至少5天的 `rank_close` 和 `rank_volume` 数据。由于 `rank` 是截面计算，理论上只要当天有数据就能计算当天的 `rank`。因此，整体上需要至少5天的 `close` 和 `volume` 数据才能计算出第一个有效的协方差值，并进而计算 Alpha。在数据序列的早期，Alpha 值可能为 NaN。
*   **Rank 实现**: 横截面 `rank` 的具体实现（通常是百分位排名 `pct=True`，返回0-1的值）会影响协方差的计算和最终 Alpha 值的范围。
*   **协方差计算**: 协方差的计算需要两个长度至少为2的序列（pandas默认 `min_periods=window`，脚本中已修改为 `min_periods=max(2, window)`）。如果窗口期内数据点不足，协方差可能为 NaN。
*   **-1 的影响**: 乘以 -1 会反转因子的排序。原本协方差越大（价量配合越好）的股票，排名越高，乘以 -1 后 Alpha 值越小。
*   Alpha#13 是一个基于历史价量关系统计的因子，不保证未来表现。建议与其他因子结合使用，并进行充分的回测验证。
*   成交量数据的质量和处理（例如，是否调整、是否包含异常值）对因子表现有重要影响。

如需帮助或有建议，欢迎交流！ 