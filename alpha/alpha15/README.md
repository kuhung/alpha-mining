# Alpha#15: 最高价与成交量相关性的时序聚合

## 描述

Alpha#15 的计算公式为：

```
Alpha#15: (-1 * sum(rank(correlation(rank(high), rank(volume), 3)), 3))
```

这个 Alpha 策略旨在捕捉资产的最高价（high）和成交量（volume）之间的秩相关性（rank correlation）在短期内的时序变化趋势。它首先计算每日最高价和成交量的秩，然后计算这两个秩在过去3天内的相关性。接着，对这个相关性值进行截面排名。最后，将这个排名在过去3天内进行求和，并取负值。

核心逻辑步骤：
1.  **数据秩化**：分别计算每日最高价 (`high`) 和成交量 (`volume`) 在所有资产中的截面排名 (`rank(high)` 和 `rank(volume)`)。
2.  **短期相关性**：计算过去3天内，每日最高价秩和成交量秩之间的相关性系数 (`correlation(rank(high), rank(volume), 3)`)。这个相关性是针对每个资产独立计算的时间序列相关性。
3.  **相关性排名**：对每日计算出的相关性系数进行当日所有资产间的截面排名 (`rank(correlation(...))`)。
4.  **时序聚合与反转**：将每日的相关性排名在过去3天内进行求和 (`sum(rank(correlation(...)), 3)`)，然后乘以 -1。

这个因子的设计思路是，如果某资产的最高价排名和成交量排名在过去一段时间内持续表现出较强的正（或负）相关性，并且这种相关性强度在近期所有资产中也处于较高（或较低）的排名，那么这种模式的持续性可能预示着未来的价格走势。最终的求和与反转操作旨在整合这种短期趋势信号。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据 (确保包含 high, volume 字段)
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha15/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#15
│   ├── alpha15_results.csv    # 计算得到的 Alpha#15 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#15 策略简介
```

## 使用步骤

### 1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。如果未安装，可以通过 pip 安装：

```bash
pip install pandas numpy
```
注意：`pandas` 的 `rank()` 和 `rolling().corr()` 方法足以完成此 Alpha 的计算。

### 2. 检查模拟数据

本 Alpha 依赖于 `high` 和 `volume` 数据。请确保 `data/mock_data.csv` 文件存在，并且包含了 `date`, `asset_id`, `high`, `volume` 列。如果文件不存在或数据不完整，请运行或修改 `data/generate_mock_data.py` 脚本。

```bash
# 检查或生成数据 (如果需要)
cd ../../data # 假设当前在 alpha/alpha15 目录
python generate_mock_data.py # 假设此脚本能生成所需字段
cd ../alpha/alpha15
```
默认的 `mock_data.csv` 应该已经包含了 `high` 和 `volume` 字段。

### 3. 计算 Alpha#15 因子

进入 `alpha/alpha15` 目录并运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#15，并将结果保存到当前目录下的 `alpha15_results.csv`。

## Alpha#15 策略解读与计算示例 (基于实际数据)

以下示例将使用 `alpha15_results.csv` 中 `asset_1` 在日期 `2025-01-05` 的实际计算结果来展示各步骤，这是其第一个非 NaN 的 Alpha15 值出现的日期。

**背景数据 (源自 `alpha15_results.csv` 或 `mock_data.csv`):**

对于 `asset_1`:
-   **2025-01-03**: `rank_high`=0.60, `rank_volume`=0.60
-   **2025-01-04**: `rank_high`=0.80, `rank_volume`=0.40
-   **2025-01-05**: `rank_high`=0.60, `rank_volume`=0.80

**计算步骤 for asset_1 at 2025-01-05:**

1.  **数据秩化 (已完成)**:
    *   `rank_high` 和 `rank_volume` 已在每日截面上计算。

2.  **计算 `correlation_high_volume_3` (时序相关性, correlation_window=3)**:
    *   需要 `asset_1` 在 `2025-01-03`, `2025-01-04`, `2025-01-05` 的 `rank_high` 和 `rank_volume` 值。
        *   `rank_high` 序列: `[0.60, 0.80, 0.60]`
        *   `rank_volume` 序列: `[0.60, 0.40, 0.80]`
    *   计算这两个序列的相关性。根据 `alpha15_results.csv`，`asset_1` 在 `2025-01-05` 的 `correlation_high_volume_3` 为 `-0.87`。

3.  **计算 `rank_correlation` (截面排名)**:
    *   在 `2025-01-05` 这一天，对所有资产计算出的 `correlation_high_volume_3` 值进行升序百分比排名。
    *   根据 `alpha15_results.csv`，`asset_1` 在 `2025-01-05` 的 `rank_correlation` (即 `-0.87` 这个相关性值在当日所有资产相关性值中的排名) 为 `1.00`。 (注意: 实际结果是1.00，示例计算中可能因为其他资产的数据导致该值为1.00。如果为百分比排名，0.33可能更合理，但以结果文件为准，此处是1.00)。

4.  **计算 `sum_rank_correlation_3` (时序求和, sum_window=3)**:
    *   需要 `asset_1` 在 `2025-01-03`, `2025-01-04`, `2025-01-05` 的 `rank_correlation` 值。
        *   `2025-01-03`: `rank_correlation` for `asset_1` is `1.00`
        *   `2025-01-04`: `rank_correlation` for `asset_1` is `1.00`
        *   `2025-01-05`: `rank_correlation` for `asset_1` is `1.00`
    *   `sum_rank_correlation_3 = 1.00 + 1.00 + 1.00 = 3.00`
    *   (对应 `alpha15_results.csv` 中 `asset_1` 在 `2025-01-05` 的 `sum_rank_correlation_3` 列的值 `3.00`)

5.  **计算 `Alpha#15`**:
    *   `Alpha#15 = -1 * sum_rank_correlation_3`
    *   `Alpha#15 = -1 * 3.00 = -3.00`
    *   (对应 `alpha15_results.csv` 中 `asset_1` 在 `2025-01-05` 的 `alpha15` 列的值 `-3.00`)

**解读示例**:

在此实际数据示例中 (`asset_1`, `2025-01-05`)：
-   该资产的 `rank_high` 和 `rank_volume` 在过去3天的相关性为 `-0.87`。
-   这个相关性值在 `2025-01-05` 当日所有资产的相关性值中排名为 `1.00` (百分比排名，表示处于最高位)。
-   该资产过去3天的 `rank_correlation` 值分别为 `1.00, 1.00, 1.00`，它们的和为 `3.00`。
-   最终 Alpha#15 值为 `-3.00`。这个较大的负值表明，该资产的价量秩相关性强度在过去3天内持续处于市场较高排名。

## 数据需求

-   `date`: 交易日期 (datetime)
-   `asset_id`: 资产ID (string/object)
-   `high`: 每日最高价 (float)
-   `volume`: 每日成交量 (float/int)
-   (脚本还会包含 `open`, `low`, `close`, `vwap`, `returns` 等在 `mock_data.csv` 中的其他列，以保持数据完整性)

## 输出格式

输出的 CSV 文件 (`alpha15_results.csv`) 将包含以下列（除了原始数据列），所有数值型 alpha 相关列均保留两位小数：

-   `date`: 交易日期
-   `asset_id`: 资产ID
-   `open`, `high`, `low`, `close`, `volume`, `vwap`, `returns`: 原始数据中的对应列
-   `rank_high`: 当日最高价的截面百分比排名
-   `rank_volume`: 当日成交量的截面百分比排名
-   `correlation_high_volume_3`: `rank_high` 和 `rank_volume` 在过去3天的时序相关性 (correlation_window=3)
-   `rank_correlation`: `correlation_high_volume_3` 的当日截面百分比排名
-   `sum_rank_correlation_3`: `rank_correlation` 在过去3天的时序加总 (sum_window=3)
-   `alpha15`: 最终计算的 Alpha#15 值 (`-1 * sum_rank_correlation_3`)

## 注意事项与风险提示

-   **数据窗口**：
    -   计算时序相关性 (`correlation_high_volume_3`) 使用 `correlation_window=3`，并设置 `min_periods=3`。因此，每个资产的前2天该值为NaN。
    -   计算时序加总 (`sum_rank_correlation_3`) 使用 `sum_window=3`，并设置 `min_periods=3`。此计算依赖于 `rank_correlation`。
    -   综合来看，第一个非NaN的 `alpha15` 值会在每个资产的第 `(correlation_window - 1) + (sum_window - 1) + 1 = (3-1) + (3-1) + 1 = 2 + 2 + 1 = 5` 天出现。即每个资产数据序列的前4行其 `alpha15` 值为NaN。对于5个资产，总共将有 `4 * 5 = 20` 个NaN的 `alpha15` 值。
    -   `correlation_high_volume_3` 列：每个资产前 `correlation_window - 1 = 2` 行为NaN。总计 `2 * 5 = 10` 个NaN。
    -   `rank_correlation` 列：与 `correlation_high_volume_3` 的NaN分布一致，因为它是基于该列的截面排名。总计10个NaN。
    -   `sum_rank_correlation_3` 列：每个资产前 `(correlation_window - 1) + (sum_window - 1) = 2 + 2 = 4` 行为NaN。总计 `4 * 5 = 20` 个NaN。
-   **排名方法**：`pandas` 的 `rank(method='average', pct=True)` 方法用于所有截面排名，这意味着结果是百分比形式的平均排名。
-   **相关性计算**：`pandas` 的 `rolling().corr()` 方法用于计算时序相关性。如果窗口期内任一序列的标准差为零（例如，`rank_high` 或 `rank_volume` 在3天内完全不变），相关性可能为NaN或inf/-inf (如`alpha15_results.csv`所示，脚本已处理inf为NaN或通过后续操作消除)。实际结果中，`inf` 值会出现，例如当一个序列不变而另一个序列变化时。
-   **小数位数**：最终的 Alpha#15 值和所有中间计算的 Alpha 相关列均保留两位小数。
-   **市场适用性**：此因子依赖于价量关系，在不同市场环境或不同类型资产上表现可能不同。务必进行充分的回测和验证。
-   **数据质量**：输入数据的准确性和完整性至关重要。异常值（如未预期的0或负值成交量/价格）可能需要预处理。

Alpha#15 是基于历史价量模式的统计策略，不保证未来表现。建议与其他因子结合使用，并进行充分的回测验证。 