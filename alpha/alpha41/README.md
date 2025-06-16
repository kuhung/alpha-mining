# Alpha#41: 价格几何平均与VWAP偏离度策略

## 描述

Alpha#41 的计算公式为：

```
Alpha#41 = ((high * low)^0.5) - vwap
```

这个 Alpha 策略旨在捕捉日内价格的一个"内在价值"与其"市场成交重心"之间的偏离。它由两个核心部分组成：

1.  **几何平均价**: `(high * low)^0.5`
    *   计算当日最高价 (`high`) 和最低价 (`low`) 的几何平均数。
    *   与算术平均数 `(high + low) / 2` 相比，几何平均数对极端价格的敏感度较低，能更稳健地代表当日价格范围的中心水平。可以将其视为当日价格的一个"内在价值中枢"。

2.  **成交量加权平均价**: `vwap`
    *   `vwap` (Volume-Weighted Average Price) 是当日的总成交额除以总成交量得到的平均价格。
    *   它代表了市场中大部分交易发生的平均成本，即当日的"市场成交重心"。

最终的 Alpha#41 值为这两者之差。一个正值表示内在价值中枢高于市场成交重心，可能暗示看涨情绪；一个负值则反之，可能暗示看跌情绪。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据 (确保包含 high, low, vwap)
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha41/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#41
│   ├── alpha41_results.csv    # 计算得到的 Alpha#41 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#41 策略简介
```

## 使用步骤

### 1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。

```bash
pip install pandas numpy
```

### 2. 检查模拟数据

本 Alpha 依赖于 `high`, `low`, 和 `vwap` 数据。请确保 `data/mock_data.csv` 文件存在且包含这些列。如果文件不存在或数据不完整，请运行或修改 `data/generate_mock_data.py`。

### 3. 计算 Alpha#41 因子

进入 `alpha/alpha41` 目录并运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#41，并将结果保存到当前目录下的 `alpha41_results.csv`。

## Alpha#41 策略解读与计算示例

为了更好地理解该因子的计算过程，我们以 `alpha41_results.csv` 中 `asset_1` 在 `2024-06-01` 的数据为例进行拆解。

**背景数据 (源自 `alpha41_results.csv`):**
-   `date`: 2024-06-01
-   `asset_id`: asset_1
-   `high`: 100.28
-   `low`: 99.08
-   `vwap`: 99.41

**计算步骤:**

1.  **计算几何平均价 (`geometric_mean_high_low`)**:
    ```
    geometric_mean = (high * low)^0.5
    geometric_mean = (100.28 * 99.08)^0.5
    geometric_mean = (9935.7824)^0.5
    geometric_mean = 99.678...
    ```
    四舍五入到两位小数后，得到 `99.68`。

2.  **计算 Alpha#41**:
    ```
    Alpha#41 = geometric_mean - vwap
    Alpha#41 = 99.68 - 99.41
    Alpha#41 = 0.27
    ```

此结果与 `alpha41_results.csv` 文件中对应行的 `alpha41` 值 `0.27` 相符。这表明，在 `2024-06-01` 这一天，`asset_1` 的价格内在价值中枢略高于其市场成交重心。

## 数据要求

-   `date`: 交易日期 (datetime)
-   `asset_id`: 资产ID (string/object)
-   `high`: 当日最高价 (float)
-   `low`: 当日最低价 (float)
-   `vwap`: 当日成交量加权平均价 (float)

## 输出格式

输出的 CSV 文件 (`alpha41_results.csv`) 将包含所有原始数据列以及以下新列，所有数值型 alpha 相关列均保留两位小数：

-   `geometric_mean_high_low`: `high` 和 `low` 的几何平均数，作为中间计算结果。
-   `alpha41`: 最终计算的 Alpha#41 值。

在保存到CSV之前，所有 `alpha41` 值为 NaN 的行都会被移除。

## 注意事项与风险提示

-   **数据完整性**: `alpha_calculator.py` 脚本会检查 `high`, `low`, `vwap` 等必需列是否存在。如果任一数据缺失，将导致该行的 `alpha41` 值为 NaN，并最终被从输出结果中剔除。
-   **因子解释**:
    *   **正值**: 表明价格内在价值高于市场成交重心。这可能是一个看涨信号，暗示市场有潜在的上涨动力，或者当日的买入力量主要集中在较高的价格区间。
    *   **负值**: 表明价格内在价值低于市场成交重心。这可能是一个看跌信号，暗示市场承受着下行压力，或者当日的主要成交量发生在比价格中枢更高的位置，形成了压力位。
-   **市场适用性**: 该因子是一个日内指标，其有效性可能在不同波动性、不同流动性的市场或资产上表现各异。建议进行充分的回测和验证。
-   **与其他因子结合**: Alpha#41 关注的是日内价格结构，可作为多元化投资组合中的一个因子，与其他基于趋势、动量或价值的因子结合使用。
-   **无未来保证**: 任何历史数据分析和因子构建都不保证未来的盈利能力。市场条件会不断变化。 