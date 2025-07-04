# Alpha#40: 波动率与相关性反转策略

## Formula

```
((-1 * rank(stddev(high, 10))) * correlation(high, volume, 10))
```

## Description

Alpha#40 是一个结合了市场波动性、成交量行为和资产间反转效应的量化策略。该策略的核心思想是识别并利用那些表现出低波动性但其价格（`high`）与成交量（`volume`）呈正相关的资产。策略预期这类资产在未来可能会表现不佳（即因子值为负）。

### Components:

1.  **`stddev(high, 10)`**: 计算过去10个周期的最高价（`high`）的标准差。这衡量了资产近期价格的波动性或不确定性。标准差越高，表明价格波动越剧烈。
2.  **`rank(stddev(high, 10))`**: 对计算出的10周期波动率进行横截面排名。波动性最高的资产获得最高的排名（接近1.0），而波动性最低的资产获得最低的排名（接近0.0）。
3.  **`-1 * rank(stddev(high, 10))`**: 将波动率排名取负。这一步意味着策略偏好（给予更高正值）那些近期波动性较低的资产，而惩罚（给予更低负值）那些波动性较高的资产。
4.  **`correlation(high, volume, 10)`**: 计算过去10个周期的最高价（`high`）与成交量（`volume`）之间的滚动相关性。
    *   **正相关** (接近 +1.0) 可能表示"价涨量增"，这通常被看作是趋势持续的健康信号，但也可能预示着趋势的顶部，因为大量交易可能在价格高点发生。
    *   **负相关** (接近 -1.0) 可能表示"价涨量缩"或"价跌量增"，这可能暗示趋势的强度不足或恐慌性抛售。
5.  **最终公式**: 将反转后的波动率排名（`-1 * rank(...)`）与价量相关性相乘。
    *   当一个资产**波动率低**（排名低，因此 `-1 * rank` 为一个接近于0的负数或小的正数）且**价量正相关**时，最终的 Alpha 值会趋向于一个较小的负数。
    *   当一个资产**波动率高**（排名高，因此 `-1 * rank` 为一个较大的负数）且**价量正相关**时，最终的 Alpha 值会是一个较大的负数，这是策略主要的做空信号。
    *   当**价量呈负相关**时，它会反转 `-1 * rank` 部分的符号，可能导致因子值为正，这可能被视为一个买入信号，特别是在高波动率的情况下（大负数乘以负数得到大正数）。

该策略旨在做空那些价格波动剧烈且交易量跟随价格上涨的资产，同时可能做多那些在高波动性下出现价量背离的资产。

## Calculation Steps

1.  **数据准备**: 加载 `high` 和 `volume` 数据。
2.  **计算波动率**: 对于每个资产，计算其过去10个周期的最高价 `high` 的滚动标准差 `stddev_high_10`。
3.  **波动率排名**: 在每个时间点上，对所有资产的 `stddev_high_10` 进行横截面排名，得到 `rank_stddev_high_10`。
4.  **计算相关性**: 对于每个资产，计算其过去10个周期的 `high` 和 `volume` 之间的滚动相关性，得到 `corr_high_volume_10`。
5.  **计算最终Alpha值**: 根据公式 `alpha40 = (-1 * rank_stddev_high_10) * corr_high_volume_10` 计算最终值。
6.  **结果处理**: 将计算出的所有中间列和最终 `alpha40` 列四舍五入至两位小数，并过滤掉 `alpha40` 为 `NaN` 的行后，保存到CSV文件。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py
│   └── mock_data.csv
├── alpha/alpha40/
│   ├── alpha_calculator.py    # 脚本：计算 Alpha#40
│   ├── alpha40_results.csv    # 计算结果
│   ├── README.md              # 本文档
│   └── cast.md                # 策略简介
```

## 使用步骤

### 1. 环境准备

确保已安装 `pandas` 和 `numpy`：

```bash
pip install pandas numpy
```

### 2. 检查数据

本 Alpha 依赖于 `high` 和 `volume` 数据。请确保 `data/mock_data.csv` 文件存在并包含所需列。

### 3. 计算 Alpha#40

在项目根目录下运行 `alpha_calculator.py` 脚本：

```bash
python alpha/alpha40/alpha_calculator.py
```

脚本将读取 `data/mock_data.csv`，计算 Alpha#40，并将结果保存到 `alpha/alpha40/alpha40_results.csv`。

## 数据输入

*   `high`: 每日最高价。
*   `volume`: 每日成交量。

数据从 `data/mock_data.csv` 文件中获取。

## 输出格式

输出的 CSV 文件 (`alpha40_results.csv`) 将包含以下列（除了原始数据列），所有数值型 alpha 相关列均保留两位小数：

-   `date`: 交易日期
-   `asset_id`: 资产ID
-   `open`, `high`, `low`, `close`, `volume`, `vwap`, `returns`: 原始数据
-   `stddev_high_10`: 10日最高价滚动标准差
-   `rank_stddev_high_10`: 10日最高价滚动标准差的横截面排名
-   `corr_high_volume_10`: 10日最高价与成交量的滚动相关性
-   `alpha40`: 最终计算的 Alpha#40 值

## 注意事项与风险提示

-   **NaN 值**: 在计算初期（前9个数据点），由于滚动窗口不足，结果将为 `NaN`。这些行在最终输出前被移除。
-   **数据质量**: 输入数据的准确性对波动率和相关性的计算至关重要。异常值可能会扭曲结果。
-   **市场适用性**: 此因子表现可能因市场环境（如牛市、熊市、高波动期）而异。
-   **相关性解读**: 价量相关性是一个复杂的指标，其解释可能需要结合其他市场信息。

## 策略解读与计算示例

我们将以 `asset_1` 在日期 `2024-06-10` 的数据为例，展示 Alpha#40 的计算。

**背景数据 (源自 `alpha40_results.csv` for `asset_1` on `2024-06-10`):**
- `stddev_high_10`: 1.85
- `rank_stddev_high_10`: 0.40
- `corr_high_volume_10`: 0.48
- `alpha40`: -0.19

**计算 Alpha#40:**

1.  **准备中间值**:
    *   首先，脚本已计算出 `asset_1` 在 `2024-06-10` 的10日最高价标准差为 `1.85`。
    *   然后，在当日所有资产中对该值进行排名，得到排名百分比 `rank_stddev_high_10` 为 `0.40`。
    *   同时，计算出 `asset_1` 在该日期的10日最高价与成交量的相关性 `corr_high_volume_10` 为 `0.48`。

2.  **代入公式**:
    *   `alpha40 = (-1 * rank_stddev_high_10) * corr_high_volume_10`
    *   `alpha40 = (-1 * 0.40) * 0.48`
    *   `alpha40 = -0.40 * 0.48`
    *   `alpha40 = -0.192`

3.  **结果取整**:
    *   保留两位有效数字后，最终值为 `-0.19`。

这个计算结果与 `alpha40_results.csv` 中 `asset_1` 在 `2024-06-10` 的 `alpha40` 值 `-0.19` 相符。这表明该资产当天具有中等偏低的波动率排名和中等程度的价量正相关性，因此产生了一个负的 Alpha 信号。 