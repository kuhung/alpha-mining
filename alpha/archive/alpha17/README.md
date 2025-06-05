# Alpha#17: 多因子组合策略

## 描述

Alpha#17 的计算公式为：

```
Alpha#17 = (((-1 * rank(ts_rank(close, 10))) * rank(delta(delta(close, 1), 1))) * rank(ts_rank((volume / adv20), 5)))
```

这个 Alpha 策略是一个复合因子，结合了三个主要部分的乘积：
1.  **价格动量与趋势强度**: `(-1 * rank(ts_rank(close, 10)))`
    *   `ts_rank(close, 10)`: 计算每只资产过去10天收盘价的时间序列百分比排名。值越高表示当前收盘价在近期历史中越高。
    *   `rank(ts_rank(close, 10))`: 对上述时间序列排名进行截面百分比排名。这衡量了资产近期价格趋势强度在当前市场中的相对位置。
    *   乘以 `-1`: 反转信号，使得近期趋势越弱（`ts_rank` 越低）且在截面中排名越低（`rank(ts_rank)` 越低）的资产，这一部分的贡献越大（更正）。或者，如果趋势强（`ts_rank`高）且截面排名高（`rank(ts_rank)`高），则乘以-1后得到一个较大的负数。

2.  **价格加速度**: `rank(delta(delta(close, 1), 1))`
    *   `delta(close, 1)`: 计算每日收盘价的1日变化量（`close_t - close_{t-1}`）。
    *   `delta(delta(close, 1), 1)`: 计算上述1日变化量的1日变化量，即价格的二阶差分，衡量价格变化的加速度。
    *   `rank(delta(delta(close, 1), 1))`: 对价格加速度进行截面百分比排名。这捕捉了价格变化速度最快的资产。

3.  **成交量爆发强度**: `rank(ts_rank((volume / adv20), 5))`
    *   `adv20`: 计算每只资产过去20日的平均成交量。
    *   `volume / adv20`: 计算当日成交量相对于其20日平均成交量的比率。该比率衡量成交量的相对活跃程度。
    *   `ts_rank((volume / adv20), 5)`: 计算上述成交量比率在过去5天内的时间序列百分比排名。这捕捉了成交量近期是否持续活跃。
    *   `rank(ts_rank((volume / adv20), 5))`: 对成交量比率的5日时间序列排名进行截面百分比排名。这衡量了资产近期成交量爆发强度在当前市场的相对位置。

最终 Alpha#17 是这三个排名后（或处理后）的值的乘积。该因子试图捕捉那些近期价格趋势（反向）、价格加速以及成交量爆发综合表现显著的资产。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据 (需包含 close, volume)
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha17/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#17
│   ├── alpha17_results.csv    # 计算得到的 Alpha#17 结果文件 (脚本生成)
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#17 策略简介 (稍后创建)
```

## 使用步骤

### 1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。如果未安装，可以通过 pip 安装：

```bash
pip install pandas numpy
```

### 2. 检查模拟数据

本 Alpha 依赖于 `close` 和 `volume` 数据。请确保 `data/mock_data.csv` 文件存在，并且包含了 `date`, `asset_id`, `close`, `volume` 列。默认的 `mock_data.csv` 应该已包含这些字段。

```bash
# 假设当前在 alpha/alpha17 目录
# 若数据缺失，需先到 ../../data 目录运行或修改 generate_mock_data.py
# cd ../../data
# python generate_mock_data.py
# cd ../alpha/alpha17
```

### 3. 计算 Alpha#17 因子

进入 `alpha/alpha17` 目录并运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#17，并将结果保存到当前目录下的 `alpha17_results.csv`。

## Alpha#17 策略解读与计算步骤概述

1.  **计算 `adv20`**: 对每个资产，计算其过去20天的平均成交量 (`volume.rolling(window=20, min_periods=20).mean()`)。
2.  **计算 Component A**:
    a.  `ts_rank_close_10`: 对每个资产，计算其收盘价 (`close`) 在过去10天的时间序列百分比排名 (`rolling(window=10, min_periods=10).rank(pct=True)`)。
    b.  `rank_ts_rank_close_10`: 对每日的 `ts_rank_close_10` 进行截面百分比排名 (`groupby('date').rank(pct=True)`)。
    c.  `component_a = -1 * rank_ts_rank_close_10`。
3.  **计算 Component B**:
    a.  `delta_close_1`: 对每个资产，计算收盘价的1日差分 (`close.diff(1)`)。
    b.  `delta_delta_close_1_1`: 对每个资产，计算 `delta_close_1` 的1日差分 (`delta_close_1.diff(1)`)。
    c.  `rank_delta_delta_close_1_1`: 对每日的 `delta_delta_close_1_1` 进行截面百分比排名 (`groupby('date').rank(pct=True)`)。
    d.  `component_b = rank_delta_delta_close_1_1`。
4.  **计算 Component C**:
    a.  `volume_adv20_ratio`: 计算 `volume / adv20`。注意处理 `adv20` 可能为0或NaN的情况，产生的 `inf` 值需替换为 `NaN`。
    b.  `ts_rank_vol_adv20_5`: 对每个资产，计算 `volume_adv20_ratio` 在过去5天的时间序列百分比排名 (`rolling(window=5, min_periods=5).rank(pct=True)`)。
    c.  `rank_ts_rank_vol_adv20_5`: 对每日的 `ts_rank_vol_adv20_5` 进行截面百分比排名 (`groupby('date').rank(pct=True)`)。
    d.  `component_c = rank_ts_rank_vol_adv20_5`。
5.  **计算 `Alpha#17`**:
    `alpha17 = component_a * component_b * component_c`。
6.  **结果处理**: 将 `alpha17` 和所有中间数值列保留两位小数。

## Alpha#17 策略解读与计算示例

### 数据快照 (asset_1, 2025-01-24)

根据 `alpha17_results.csv` 的实际数据，我们选取 `asset_1` 在 `2025-01-24` 的数据作为示例：

| date       | asset_id | close | volume   | adv20      | ts_rank_close_10 | rank_ts_rank_close_10 | component_a | delta_close_1 | delta_delta_close_1_1 | rank_delta_delta_close_1_1 | component_b | volume_adv20_ratio | ts_rank_vol_adv20_5 | rank_ts_rank_vol_adv20_5 | component_c | alpha17 |
|------------|----------|-------|----------|------------|------------------|-----------------------|-------------|---------------|-----------------------|----------------------------|-------------|--------------------|---------------------|--------------------------|-------------|---------|
| 2025-01-24 | asset_1  | 97.20 | 3075917  | 1389671.40 | 0.20             | 0.50                  | -0.50       | -0.50         | 2.60                  | 1.00                       | 1.00        | 2.21               | 1.00                | 1.00                     | 1.00        | -0.50   |

*注: 上述数值直接取自 `alpha17_results.csv` 文件，并已按脚本中的要求保留了相应的小数位数。*

### 计算步骤详解 (asset_1, 2025-01-24):

1.  **Component A: `(-1 * rank(ts_rank(close, 10)))`**
    *   `ts_rank_close_10` for `asset_1` on `2025-01-24` is `0.20`. (收盘价在过去10天的百分位排名)
    *   `rank_ts_rank_close_10` for `asset_1` on `2025-01-24` (截面排名) is `0.50`.
    *   `component_a = -1 * 0.50 = -0.50`.

2.  **Component B: `rank(delta(delta(close, 1), 1))`**
    *   `delta_close_1` for `asset_1` on `2025-01-24` is `-0.50`. (前一日 `2025-01-23` 的 `delta_close_1` 为 `-3.10`)
    *   `delta_delta_close_1_1` for `asset_1` on `2025-01-24` is `-0.50 - (-3.10) = 2.60`. (价格加速度)
    *   `rank_delta_delta_close_1_1` for `asset_1` on `2025-01-24` (截面排名) is `1.00`.
    *   `component_b = 1.00`.

3.  **Component C: `rank(ts_rank((volume / adv20), 5))`**
    *   `adv20` for `asset_1` on `2025-01-24` is `1389671.40`.
    *   `volume_adv20_ratio` for `asset_1` on `2025-01-24` is `3075917 / 1389671.40 = 2.21`.
    *   `ts_rank_vol_adv20_5` for `asset_1` on `2025-01-24` is `1.00`. (成交量比率在过去5天的百分位排名)
    *   `rank_ts_rank_vol_adv20_5` for `asset_1` on `2025-01-24` (截面排名) is `1.00`.
    *   `component_c = 1.00`.

4.  **最终 Alpha#17 值**:
    *   `Alpha#17 = component_a * component_b * component_c`
    *   `Alpha#17 = -0.50 * 1.00 * 1.00 = -0.50`.

**解读 (asset_1, 2025-01-24)**:
在 `2025-01-24` 这一天，`asset_1`：
*   近期价格趋势相对较弱，但在市场中处于中间水平 (`component_a = -0.50`，原始 `ts_rank_close_10` 较低，`rank_ts_rank_close_10` 处于50%分位，乘以-1)。
*   价格变化加速度非常显著，在市场中排名最高 (`component_b = 1.00`)。
*   成交量爆发强度非常显著，在市场中排名最高 (`component_c = 1.00`)。
综合这三个因素，`asset_1` 当日的 Alpha#17 值为 `-0.50`。

## 数据需求

-   `date`: 交易日期 (datetime)
-   `asset_id`: 资产ID (string/object)
-   `close`: 每日收盘价 (float)
-   `volume`: 每日成交量 (float/int)
-   (脚本会包含 `mock_data.csv` 中的其他列，如 `open`, `high`, `low`, `vwap`, `returns` 以保持数据完整性)

## 输出格式

输出的 CSV 文件 (`alpha17_results.csv`) 将包含以下列（除了原始数据列），所有数值型 alpha 相关列均保留两位小数：

-   `date`: 交易日期
-   `asset_id`: 资产ID
-   `open`, `high`, `low`, `close`, `volume`, `vwap`, `returns`: 原始数据中的对应列 (若存在)
-   `adv20`: 20日平均成交量
-   `ts_rank_close_10`: 收盘价10日时间序列排名
-   `rank_ts_rank_close_10`: `ts_rank_close_10` 的截面排名
-   `component_a`: Alpha#17 的组成部分 A
-   `delta_close_1`: 收盘价1日差分
-   `delta_delta_close_1_1`: 收盘价二阶差分（加速度）
-   `rank_delta_delta_close_1_1`: `delta_delta_close_1_1` 的截面排名
-   `component_b`: Alpha#17 的组成部分 B
-   `volume_adv20_ratio`: 成交量与20日均量之比
-   `ts_rank_vol_adv20_5`: `volume_adv20_ratio` 的5日时间序列排名
-   `rank_ts_rank_vol_adv20_5`: `ts_rank_vol_adv20_5` 的截面排名
-   `component_c`: Alpha#17 的组成部分 C
-   `alpha17`: 最终计算的 Alpha#17 值

## 注意事项与风险提示

-   **数据窗口与NaN值**:
    -   `adv20`: 每个资产前19个数据点为NaN。
    -   `ts_rank_close_10`: 每个资产前9个数据点为NaN。
    -   `delta_delta_close_1_1`: 每个资产前2个数据点为NaN。
    -   `volume_adv20_ratio`: 依赖 `adv20`，因此至少前19个点为NaN。
    -   `ts_rank_vol_adv20_5`: 依赖 `volume_adv20_ratio`，在其基础上再加4个NaN点。因此，Component C 相关计算会导致每个资产序列前 `19 (adv20) + 4 (ts_rank) = 23` 个数据点为NaN。
    -   最终 `alpha17` 值的NaN情况取决于其三个组成部分中产生NaN最多的那个，即至少每个资产的前23个数据点为NaN。
-   **排名方法**: 所有排名（截面`rank`和时间序列`ts_rank`）均使用百分比排名 (`pct=True`) 和 `method='average'`。
-   **除零处理**: `volume / adv20` 计算中，如果 `adv20` 为零，可能产生 `inf`。脚本中应将其替换为 `NaN`。
-   **小数位数**: 最终的 Alpha#17 值和所有中间计算的 Alpha 相关数值列均保留两位小数。
-   **市场适用性**: 此因子表现可能因市场环境或资产类型而异。务必进行充分的回测和验证。
-   **数据质量**: 输入数据的准确性和完整性至关重要。

Alpha#17 是基于历史价量模式的统计策略，不保证未来表现。建议与其他因子结合使用，并进行充分的回测验证。 