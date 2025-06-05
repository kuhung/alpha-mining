# Alpha#2 策略模拟与计算

本项目演示了如何根据给定的 Alpha#2 公式生成模拟金融数据、计算 Alpha 因子，并对结果进行分析。

## Alpha#2 公式

Alpha#2 的计算公式如下：

```
(-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))
```

其中：

* `volume`: 资产的日成交量。
* `close`: 资产的日收盘价。
* `open`: 资产的日开盘价。
* `log(volume)`: 成交量的自然对数。
* `delta(series, N)`: 计算时间序列 `series` 的 N 期差分，即 `series[t] - series[t-N]`。
* `rank(series)`: 计算 `series` 中每个值在当日所有资产间的排序百分比（0到1之间）。值越大，排名越高。
* `correlation(x, y, N)`: 计算时间序列 `x` 和 `y` 在过去 `N` 天的滚动相关系数。
* `((close - open) / open)`: 日内收益率，即开盘到收盘的价格变化率。

## 项目结构

```
alpha-mining/
├── alpha/
│   └── alpha2/
│       ├── alpha_calculator.py     # 脚本：根据公式计算 Alpha#2
│       ├── alpha2_results.csv      # 计算得到的 Alpha#2 结果文件
│       ├── cast.md                 # Alpha#2 策略简要说明
│       └── README.md               # 本说明文档
├── data/
│   └── mock_data.csv               # 模拟数据文件（包含volume和open字段）
└── ...
```

## 使用步骤

### 1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。如果未安装，可以通过 pip 安装：

```bash
pip install pandas numpy
```

### 2. 数据准备

确保 `data/mock_data.csv` 文件包含以下必要字段：

- `date`: 交易日期
- `asset_id`: 资产标识
- `close`: 收盘价
- `open`: 开盘价
- `volume`: 成交量

### 3. 计算 Alpha#2 因子

运行 `alpha_calculator.py` 脚本来计算 Alpha#2 因子。该脚本会读取 `data/mock_data.csv`，执行公式中的计算，并将结果保存到 `alpha2_results.csv`。

```bash
cd alpha/alpha2
python alpha_calculator.py
```

脚本执行完毕后，会在终端打印出结果文件的前5行、后5行以及 Alpha#2 值的描述性统计信息。

## Alpha#2 策略解读

该 Alpha 策略试图捕捉成交量变化与日内收益率之间的负相关关系。

为了更好地理解计算过程，我们假设有以下模拟数据片段：

| date       | asset_id | open   | close  | volume  |
| ---------- | -------- | ------ | ------ | ------- |
| 2025-01-20 | asset_1  | 99.93  | 100.5  | 3507861 |
| 2025-01-21 | asset_1  | 100.79 | 99.6   | 1016495 |
| 2025-01-22 | asset_1  | 98.92  | 101.6  | 825693  |
| 2025-01-23 | asset_1  | 103.09 | 102.5  | 1496721 |
| 2025-01-24 | asset_1  | 102.22 | 100.9  | 1692425 |
| 2025-01-25 | asset_1  | 98.64  | 102.4  | 1677999 |

下面是 Alpha#2 计算的详细步骤：

1. **成交量对数差分 (`delta(log(volume), 2)`)**:

   * 首先计算成交量的自然对数：`log(volume)`
   * 然后计算2期差分：`log(volume)[t] - log(volume)[t-2]`

   *示例 (asset_1, 2025-01-22)*:
   ` ` = `13.624 - 15.070` = `-1.446`
2. **日内收益率 (`(close - open) / open`)**:

   * 计算每日的开盘到收盘收益率

   *示例 (asset_1, 2025-01-22)*:
   `(101.6 - 98.92) / 98.92` = `0.0271`
3. **排名计算 (`rank(...)`)**:

   * 分别对成交量对数差分和日内收益率进行当日横截面排名
   * 排名结果为0到1之间的百分位数
4. **滚动相关系数 (`correlation(..., 6)`)**:

   * 计算两个排名序列在过去6天的滚动相关系数
   * 相关系数范围在-1到1之间
5. **取负值 (`-1 * ...`)**:

   * 将相关系数取负值，使得负相关变为正的Alpha值
   * 这意味着当成交量变化与日内收益率呈负相关时，Alpha值为正

## 策略逻辑

Alpha#2 的核心逻辑是：

1. **成交量动量**: 通过 `delta(log(volume), 2)` 捕捉成交量的变化趋势
2. **日内表现**: 通过 `(close - open) / open` 衡量日内价格表现
3. **负相关信号**: 当成交量增加而日内表现较差时（或成交量减少而日内表现较好时），产生正的Alpha信号

这种策略可能反映了以下市场现象：

- 恐慌性抛售：成交量放大但价格下跌
- 理性回调：成交量萎缩但价格稳定或小幅上涨

如需帮助或有建议，欢迎交流！
