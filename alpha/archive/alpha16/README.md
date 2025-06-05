# Alpha#16: 最高价与成交量排名的协方差因子

## 描述

Alpha#16 的计算公式为：

```
(-1 * rank(covariance(rank(high), rank(volume), 5)))
```

这个 Alpha 策略计算的是过去5天最高价排名和成交量排名的协方差，然后对这个协方差取截面排名，最后乘以-1。

**核心逻辑**:

1.  **数据排名**:
    *   `rank(high)`: 对每日的最高价 `high` 进行所有资产间的横截面排名 (百分位排名)。
    *   `rank(volume)`: 对每日的成交量 `volume` 进行所有资产间的横截面排名 (百分位排名)。
2.  **时间序列协方差**:
    *   `covariance(rank(high), rank(volume), 5)`: 对于每只资产，取其过去5天（包括当天）的 `rank(high)` 序列和 `rank(volume)` 序列，计算这两个时间序列的协方差。
3.  **协方差排名与最终 Alpha**:
    *   `rank(covariance(...))`: 对步骤2中计算得到的协方差值在所有资产的同一天进行横截面排名。
    *   `Alpha#16 = -1 * rank(covariance(...))`: 将上述排名取负得到最终的 Alpha 值。

**解读**:
该因子旨在识别那些"最高价市场排名"和"成交量市场排名"在近期（5日窗口）表现出特定相关性的股票。
*   计算得到的 `covariance(rank(high), rank(volume), 5)`：
    *   正值较大：表明股票的最高价排名和成交量排名倾向于同向变动（价涨量增排名同升，价跌量缩排名同降），意味着价量配合良好。
    *   负值较大（绝对值）：表明股票的最高价排名和成交量排名倾向于反向变动（价涨量缩排名背离，或价跌量增排名背离），意味着价量背离。
*   通过对这个协方差进行排名 (`rank_cov`)，我们得到一个相对强弱的指标。排名越高，意味着该股票的价量配合模式（无论是正相关还是负相关）在其协方差的具体数值上，相比其他股票更为突出。
*   最后乘以 `-1`，意味着原始协方差排名越高的股票（即协方差本身在所有股票中数值越大，通常代表更强的正相关性），其最终 Alpha 值越低（越负）。反之，如果原始协方差排名较低（协方差本身数值较小，甚至是负值），其最终 Alpha 值会较高（更接近0或为正）。
*   因此，Alpha#16倾向于给予那些"最高价与成交量排名协方差"在全体股票中不突出（协方差值较小或为负，导致协方差排名较低）的股票更高的 Alpha 值。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha16/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#16
│   ├── alpha16_results.csv    # 计算得到的 Alpha#16 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#16 策略总结
```

## 使用步骤

### 1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。如果未安装，可以通过 pip 安装：

```bash
pip install pandas numpy
```

### 2. 生成模拟数据 (如果需要)

本 Alpha 依赖于 `date`, `asset_id`, `high` 和 `volume` 数据。`data/generate_mock_data.py` 脚本可以生成这些数据。如果 `data/mock_data.csv` 不存在或需要更新，并且不包含 `high` 列:

```bash
cd ../../data  # 假设当前在 alpha/alpha16 目录
python generate_mock_data.py # **确保此脚本会生成 high, volume 列**
cd ../alpha/alpha16 # 返回 alpha/alpha16 目录
```
请检查 `generate_mock_data.py` 以确保它生成了所需列。如果 `high` 列缺失，您可能需要修改 `generate_mock_data.py` 来包含它。

### 3. 计算 Alpha#16 因子

在 `alpha/alpha16` 目录并运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#16，并将结果（包括原始数据和中间计算列）保存到当前目录下的 `alpha16_results.csv`。同时会在终端打印部分结果和统计信息。

## Alpha#16 策略解读与计算示例

### 数据快照 (asset_1, 2025-01-05)

根据 `alpha16_results.csv` 的实际数据，我们选取 `asset_1` 在 `2025-01-05` 的数据作为示例：

| date       | asset_id | open   | high   | low    | close  | volume  | returns | rank_high | rank_volume | cov_rank_high_rank_volume_5 | rank_cov | alpha16 |
|------------|----------|--------|--------|--------|--------|---------|---------|-----------|-------------|-----------------------------|----------|---------|
| 2025-01-05 | asset_1  | 98.99  | 100.58 | 98.69  | 100.50 | 1327947 | 0.0111  | 0.6000    | 0.8000      | 0.024000                    | 1.0000   | -1      |

*注: `cov_rank_high_rank_volume_5` 和 `alpha16` 的值直接来自生成的结果文件。`alpha16` 在CSV中通常已按两位有效数字的要求处理，但此处显示原始计算后的精确负值（如脚本内部的 `-1.0` 会显示为 `-1`）。其他浮点数列（如 `rank_high`, `rank_volume`, `rank_cov`）在CSV中会以特定小数位数保存。*

### 计算步骤详解 (asset_1, 2025-01-05):

1.  **收集 `asset_1` 从 `2025-01-01` 到 `2025-01-05` (共5天) 的 `rank_high` 和 `rank_volume` 数据**:
    *   `rank_high` 序列 (来自 `alpha16_results.csv`): `[0.6000, 1.0000, 0.6000, 0.8000, 0.6000]`
    *   `rank_volume` 序列 (来自 `alpha16_results.csv`): `[0.4000, 1.0000, 0.6000, 0.4000, 0.8000]`

2.  **计算 `covariance(rank_high_series, rank_volume_series, 5)`**:
    *   使用上述两个长度为5的序列，计算它们的样本协方差。
    *   根据 `alpha16_results.csv`，`asset_1` 在 `2025-01-05` 的值为 `0.024000`。

3.  **横截面排名 `rank_cov`**:
    *   在 `2025-01-05` 这一天，`asset_1` 计算得到的 `cov_rank_high_rank_volume_5` (`0.024000`) 与当日所有其他资产计算得到的协方差值进行比较排名。
    *   根据 `alpha16_results.csv`，`asset_1` 当日的 `rank_cov` 为 `1.0000` (即处于100%分位，表明其协方差是当天最高的)。

4.  **最终 Alpha#16 值**:
    *   `Alpha#16 = -1 * rank_cov`
    *   `Alpha#16 = -1 * 1.0000 = -1.0` (CSV中显示为 `-1`)

**解读 (asset_1, 2025-01-05)**:
在 `2025-01-05` 这一天，`asset_1` 的最高价排名和成交量排名的5日协方差为 `0.024000`，这是一个正值，表明过去5天其最高价排名和成交量排名之间存在一定的正相关性。这个协方差值在当日所有资产中进行排名后得到 `rank_cov = 1.0000` (即处于最高分位)。最终Alpha值为 `-1`。这意味着，根据该因子的设计，在这一天，`asset_1` 获得了最低的Alpha评分。

## 数据需求
*   `date`: 交易日期 (YYYY-MM-DD 格式)
*   `asset_id`: 资产的唯一标识符
*   `open`: 当日开盘价 (浮点数) - *实际计算未使用，但通常包含在数据中并输出*
*   `high`: 当日最高价 (浮点数) - **核心计算列**
*   `low`: 当日最低价 (浮点数) - *实际计算未使用，但通常包含在数据中并输出*
*   `close`: 当日收盘价 (浮点数) - *实际计算未使用，但通常包含在数据中并输出*
*   `volume`: 当日成交量 (整数或浮点数) - **核心计算列**
*   `returns`: 当日回报率 (浮点数) - *实际计算未使用，但通常包含在数据中并输出*
*   *(脚本会保留输入数据中的 `open`, `low`, `close`, `returns` 等列到输出文件，以保持数据完整性)*

## 输出格式
输出的 CSV 文件 (`alpha16_results.csv`) 将包含以下列 (根据 `alpha16_results.csv` 的实际列序和内容):
*   `date`: 交易日期
*   `asset_id`: 资产ID
*   `open`: 当日开盘价 (原始数据)
*   `high`: 当日最高价 (原始数据)
*   `low`: 当日最低价 (原始数据)
*   `close`: 当日收盘价 (原始数据)
*   `volume`: 当日成交量 (原始数据)
*   `returns`: 当日回报率 (原始数据)
*   `rank_high`: 当日最高价的横截面百分位排名 (例如 `0.6000`)
*   `rank_volume`: 当日成交量的横截面百分位排名 (例如 `0.4000`)
*   `cov_rank_high_rank_volume_5`: `rank_high` 和 `rank_volume` 在过去5日窗口的协方差 (例如 `0.024000`)
*   `rank_cov`: `cov_rank_high_rank_volume_5` 的横截面百分位排名 (例如 `1.0000`)
*   `alpha16`: 计算得到的 Alpha#16 值 (`-1 * rank_cov`)，CSV中将以两位有效数字格式存储 (例如 `-1`, `0.00` 或 `-0.8`)。空值表示无法计算（如初始窗口期）。

## 注意事项与风险提示
*   **数据窗口**: `covariance` 函数窗口期为5，这意味着需要至少5天的 `rank_high` 和 `rank_volume` 数据。整体上需要至少5天的 `high` 和 `volume` 数据才能计算出第一个有效的协方差值。
*   **`high` 数据列**: 此 Alpha 明确依赖 `high` 列。如果源数据 `mock_data.csv` 中不存在此列，脚本将无法执行，您需要确保数据生成脚本 `data/generate_mock_data.py` 能够提供此列。
*   **Rank 实现**: 横截面 `rank` 的具体实现（通常是百分位排名 `pct=True`，返回0-1的值）会影响协方差的计算和最终 Alpha 值的范围。
*   **协方差计算**: 协方差的计算需要两个长度至少为2的序列。如果窗口期内数据点不足，协方差可能为 NaN。脚本中会设置 `min_periods` 为 `max(2, window)`。
*   **-1 的影响**: 乘以 -1 会反转因子的排序。
*   Alpha#16 是一个基于历史价量关系统计的因子，不保证未来表现。建议与其他因子结合使用，并进行充分的回测验证。

如需帮助或有建议，欢迎交流！ 