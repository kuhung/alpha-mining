# Alpha#33: 价格反转因子

## 描述

Alpha#33 的计算公式为：

```
Alpha#33: rank((-1 * ((1 - (open / close))^1)))
```

这个 Alpha 策略旨在捕捉基于开盘价和收盘价关系的价格反转信号。公式可以简化为 `rank(-1 * (1 - (open / close)))`。

1.  **开盘价与收盘价的比率**: `(open / close)`
    *   计算每日开盘价与收盘价的比率。
2.  **1 减去比率**: `(1 - (open / close))`
    *   这个值反映了当日价格变化的幅度。如果收盘价高于开盘价（上涨），则此值小于1，`1 - (open / close)` 为负数；如果收盘价低于开盘价（下跌），则此值大于1，`1 - (open / close)` 为正数。
3.  **取负值**: `-1 * (1 - (open / close))`
    *   对上述结果取负。这意味着如果当日上涨，结果为正；如果当日下跌，结果为负。这将其转换为一个"反转"信号：上涨越多，这个值越正；下跌越多，这个值越负。
4.  **截面排名**: `rank(...)`
    *   对每日所有资产的计算结果进行截面排名。排名越高，表示该资产当日的反转信号越强（即，下跌越多，或上涨越少，相对而言更可能是反转的候选）。

最终的 Alpha#33 值是上述计算结果的截面排名。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据 (确保包含 open, close 字段)
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha33/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#33
│   ├── alpha33_results.csv    # 计算得到的 Alpha#33 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#33 策略简介
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
cd ../../data # 假设当前在 alpha/alpha33 目录
python generate_mock_data.py # 假设此脚本能生成所需字段
cd ../alpha/alpha33
```

### 3. 计算 Alpha#33 因子

进入 `alpha/alpha33` 目录并运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#33，并将结果保存到当前目录下的 `alpha33_results.csv`。

## 数据需求

-   `date`: 交易日期 (datetime)
-   `asset_id`: 资产ID (string/object)
-   `open`: 每日开盘价 (float)
-   `close`: 每日收盘价 (float)
-   (脚本还会包含 `high`, `low`, `volume`, `vwap`, `returns` 等在 `mock_data.csv` 中的其他列，以保持数据完整性)

## 输出格式

输出的 CSV 文件 (`alpha33_results.csv`) 将包含以下列（除了原始数据列），所有数值型 alpha 相关列均保留两位小数：

-   `date`: 交易日期
-   `asset_id`: 资产ID
-   `open`, `high`, `low`, `close`, `volume`, `vwap`, `returns`: 原始数据中的对应列
-   `alpha33`: 最终计算的 Alpha#33 值。

## 注意事项与风险提示

-   **NaN 值**: 如果 `open` 或 `close` 数据缺失，相应的 Alpha 值将为 NaN。
-   **排名方法**: `pandas` 的 `rank(method='average', pct=True)` 通常用于截面排名，结果是百分比形式。
-   **小数位数**: 最终的 Alpha#33 值按要求保留两位小数。
-   **市场适用性**: 此因子在不同市场环境或资产类别上表现可能迥异。务必进行充分的回测和验证。
-   **数据质量**: 输入数据的准确性和完整性至关重要。

Alpha#33 是一个基于价格关系的因子，不保证未来表现。建议与其他因子结合使用，并进行充分的回测验证。

## 策略解读与计算示例

我们将以 `asset_1` 在日期 `2025-01-01` 的数据为例，展示 Alpha#33 的计算。

**背景数据 (源自 `alpha33_results.csv` for `asset_1` on `2025-01-01`):**
- `open`: 100.30
- `close`: 100.00
- `alpha33`: 0.80

**计算 Alpha#33:**
1.  计算 `(1 - (open / close))`：
    `1 - (100.30 / 100.00) = 1 - 1.003 = -0.003`
2.  乘以 `-1`：
    `-1 * (-0.003) = 0.003`
3.  对所有资产在 `2025-01-01` 的此中间结果进行截面排名：
    *   `asset_1`: 0.003
    *   `asset_2`: 0.0053
    *   `asset_3`: -0.0008
    *   `asset_4`: -0.0034
    *   `asset_5`: -0.001

    按照数值从小到大排序，并进行百分比排名：
    -   `asset_4` (-0.0034) -> 排名 0.20
    -   `asset_5` (-0.001) -> 排名 0.40
    -   `asset_3` (-0.0008) -> 排名 0.60
    -   `asset_1` (0.003) -> 排名 0.80
    -   `asset_2` (0.0053) -> 排名 1.00

因此，`Alpha#33` 对 `asset_1` 在 `2025-01-01` 的最终计算值为 `0.80`。

此值与 `alpha33_results.csv` 中 `asset_1` 在 `2025-01-01` 的 `alpha33` 列的值 `0.80` 相符。 