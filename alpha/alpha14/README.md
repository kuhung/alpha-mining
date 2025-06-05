# Alpha#14: 收益率变动排名与开盘价成交量相关性的组合因子

## 描述

Alpha#14 的计算公式为：

```
((-1 * rank(delta(returns, 3))) * correlation(open, volume, 10))
```

该 Alpha 策略结合了两个主要部分：

1.  **近期收益率变动的负向排名**:
    *   `delta(returns, 3)`: 计算过去3天的日收益率 (`returns`) 的变化值（例如，今天的收益率减去3天前的收益率）。这反映了收益率变化的短期趋势或加速度。
    *   `rank(delta(returns, 3))`: 对上述收益率3日变化值在当日所有资产间进行横截面排名。排名越靠前（值小），表示收益率变化越小（或负向变化越大）。
    *   `-1 * rank(delta(returns, 3))`: 将排名取负。这意味着，如果一个资产的3日收益率变化在所有资产中排名较高（即变化较大，例如从大幅亏损变为小幅亏损，或从微小盈利变为大幅盈利），则这一部分的绝对值较大。如果原始排名靠前（收益率变化小或负向大），则乘以-1后变成一个较大的负数；如果原始排名靠后（收益率变化大或正向大），则乘以-1后变成一个较小的负数（或较大的正数，取决于排名是0-1还是1-N）。假设 `rank` 是百分比排名 (0-1)，值越大排名越靠后。那么 `-1 * rank` 会使得原来收益率变化最剧烈的（rank 接近1）变成接近 -1，原来收益率变化最平缓的（rank 接近0）变成接近 0。

2.  **开盘价与成交量的历史相关性**:
    *   `correlation(open, volume, 10)`: 计算过去10天内，每日开盘价 (`open`) 与每日成交量 (`volume`) 之间的滚动相关系数。
        *   正相关性高: 可能表示价涨量增或价跌量缩的同步性较强。
        *   负相关性高: 可能表示价涨量缩或价跌量增的反常情况。
        *   接近零: 表示开盘价与成交量之间没有明显的线性关系。

**综合信号逻辑**:

Alpha#14 将这两部分相乘。最终的 Alpha 值的大小和符号取决于：

*   **收益率变动排名的方向和大小**: `delta(returns, 3)` 的排名取负。
*   **开盘价与成交量的历史相关性**: `correlation(open, volume, 10)` 的符号和大小。

**解读**:

该因子试图捕捉这样一种模式：当一个资产的近期收益率变化（相对于其他资产）表现出某种特性（由 `-1 * rank(delta(returns,3))`衡量），并且其历史开盘价与成交量之间存在某种相关性时，可能会产生交易信号。

*   **示例场景 1 (因子值可能为较大的正)**:
    *   `delta(returns, 3)` 在截面上排名较低 (例如，收益率从大幅下跌变为小幅下跌，或者从微弱盈利变为小幅盈利，导致 `rank` 较低)。
    *   `-1 * rank(delta(returns, 3))` 因此是一个接近0或较小的负数。
    *   `correlation(open, volume, 10)` 是一个较大的负数 (例如，过去10天呈现价涨量缩或价跌量增)。
    *   此时，`(-1 * rank) * correlation` 可能得到一个较大的正值。

*   **示例场景 2 (因子值可能为较大的负)**:
    *   `delta(returns, 3)` 在截面上排名较高 (例如，收益率从微弱亏损变为大幅盈利，导致 `rank` 较高)。
    *   `-1 * rank(delta(returns, 3))` 因此是一个较大的负数 (接近-1，如果rank是0-1)。
    *   `correlation(open, volume, 10)` 是一个较大的正数 (例如，过去10天呈现价涨量增)。
    *   此时，`(-1 * rank) * correlation` 可能得到一个较大的负值。

因子的具体交易含义和有效性依赖于 `-1 * rank(delta(returns,3))` 部分如何解读（是希望捕捉收益率变化的"改善"还是"恶化"，或者仅仅是变化的幅度），以及开盘价与成交量的相关性在特定市场条件下预示着什么。通常，价涨量增被视作健康的上涨，价跌量缩被视作正常的调整。价涨量缩可能预示上涨动能不足，价跌量增可能预示恐慌抛售。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha14/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#14
│   ├── alpha14_results.csv    # 计算得到的 Alpha#14 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#14 策略总结
...
```

## 使用步骤

### 1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。如果未安装，可以通过 pip 安装：

```bash
pip install pandas numpy
```

### 2. 模拟数据

本 Alpha 依赖于 `date`, `asset_id`, `returns`, `open`, 和 `volume` 数据。这些数据应存在于 `../../data/mock_data.csv` 文件中。
`returns` 列通常由 `close` 价格计算得到：`returns = close.pct_change()` 或 `returns = close / close.shift(1) - 1`。
`open`, `close`, `volume` 是基础行情数据。

如果 `../../data/mock_data.csv` 不存在或需要更新，可以运行 `data/generate_mock_data.py` 脚本。请确保该脚本能生成或已包含 `open`, `close` (用于计算returns), `volume` 列。

```bash
# 假设 generate_mock_data.py 会生成包含 open, close, volume 的 mock_data.csv
cd ../../data
python generate_mock_data.py
cd ../alpha/alpha14
```

### 3. 计算 Alpha#14 因子

进入 `alpha/alpha14` 目录并运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#14，并将结果（包含原始数据列和中间计算值）保存到当前目录下的 `alpha14_results.csv`。

## Alpha#14 策略解读与计算示例 (基于实际数据)

以下示例将使用 `alpha14_results.csv` 中 `asset_1` 在日期 `2025-01-10` 的实际计算结果来展示各步骤。

**背景数据 (来自 `alpha14_results.csv` 或源数据 `mock_data.csv`):**

- 日期: `2025-01-10`
- 资产ID: `asset_1`
- 当日收益率 (`returns_today`): `0.0060`
- 3日前收益率 (`returns_3_days_ago`, 即 `2025-01-07` 的收益率): `0.0139` (此值需要从源数据查找确认)
- 当日开盘价 (`open`): `99.4500`
- 当日成交量 (`volume`): `1548483`
- 过去10天 (含当日) 的 `open` 和 `volume` 数据序列用于计算相关性。

**计算步骤:**

1.  **计算 `delta_returns_3`**:
    *   `delta_returns_3 = returns_today - returns_3_days_ago`
    *   `delta_returns_3 = 0.0060 - 0.0139 = -0.0079`
    *   (对应 `alpha14_results.csv` 中 `delta_returns_3` 列的值)

2.  **计算 `rank_delta_returns_3`**:
    *   脚本会在 `2025-01-10` 这一天，对所有资产的 `delta_returns_3` 值 (-0.0079只是asset_1的值) 进行升序百分比排名。
    *   根据 `alpha14_results.csv`，`asset_1` 在 `2025-01-10` 的 `rank_delta_returns_3` 为 `0.8000`。
    *   这意味着 `asset_1` 当日的3日收益率变化值在所有资产中处于较高的位置（约80%分位，因为是升序排名，值越大排名越靠后）。

3.  **计算 `neg_rank_delta_returns_3`**:
    *   `neg_rank_delta_returns_3 = -1 * rank_delta_returns_3`
    *   `neg_rank_delta_returns_3 = -1 * 0.8000 = -0.8000`
    *   (对应 `alpha14_results.csv` 中 `neg_rank_delta_returns_3` 列的值)

4.  **计算 `corr_open_volume_10`**:
    *   脚本会取 `asset_1` 从 `2025-01-01` 至 `2025-01-10` (共10天) 的 `open` 和 `volume` 数据序列。
    *   计算这两个序列的皮尔逊相关系数。
    *   根据 `alpha14_results.csv`，`asset_1` 在 `2025-01-10` 的 `corr_open_volume_10` 为 `-0.0347`。
    *   这表示在过去10天，`asset_1` 的开盘价和成交量之间存在轻微的负相关关系。

5.  **计算 Alpha#14**:
    *   `Alpha#14 = neg_rank_delta_returns_3 * corr_open_volume_10`
    *   `Alpha#14 = -0.8000 * -0.0347 = 0.02776`
    *   脚本输出到 `alpha14_results.csv` 时，会将此值格式化为两位有效数字，即 `0.028`。

**解读示例**:

在此实际数据示例中 (`asset_1`, `2025-01-10`)：
- 该资产的3日收益率变化 (`-0.0079`) 在当天所有资产中排名靠后 (80%分位)，表明其收益率变化幅度相对较大或者说"表现"相对不佳（如果正向解读delta的话，这里是负向变化减小，但排名靠后说明其他资产可能有更大的正向变化或更小的负向变化）。
- `neg_rank_delta_returns_3` 为 `-0.8000`。
- 其过去10天的开盘价与成交量呈现轻微负相关 (`-0.0347`)。
- 最终 Alpha 值为 `0.028`。这个较小的正值信号的产生，是由于一个较大的负排名因子（接近-1）与一个较小的负相关性因子相乘得到的。

这个基于实际数据的示例更清晰地展示了 `alpha_calculator.py` 脚本如何处理数据并生成最终的 Alpha 值。

## 数据需求

- `date`: 交易日期 (YYYY-MM-DD)
- `asset_id`: 资产ID
- `open`: 每日开盘价
- `volume`: 每日成交量
- `returns`: 每日收益率 (如果源数据中没有，需要从 `close` 计算得到)
  (如果需要从 `close` 计算 `returns`:
- `close`: 每日收盘价)

## 输出格式

输出的 CSV 文件 (`alpha14_results.csv`) 包含以下列：

- `date`: 交易日期
- `asset_id`: 资产ID
- `open`: 当日开盘价（原始数据）
- `volume`: 当日成交量（原始数据）
- `returns`: 当日收益率（原始或计算数据）
- `close`: 当日收盘价 (如果用于计算收益率，则包含)
- `delta_returns_3`: 过去3日收益率的变化 (中间计算值，保留四位小数)
- `rank_delta_returns_3`: `delta_returns_3` 的截面百分比排名 (中间计算值，保留四位小数)
- `neg_rank_delta_returns_3`: `-1 * rank_delta_returns_3` (中间计算值，保留四位小数)
- `corr_open_volume_10`: 过去10日开盘价与成交量的相关系数 (中间计算值，保留四位小数)
- `alpha14`: 计算得到的 Alpha#14 值，保留两位有效数字

## 注意事项与风险提示

- **数据窗口期**:
    - `delta(returns, 3)` 需要至少4个历史收益率数据点（即每个资产序列的前3个 `delta_returns_3` 值为NaN）。对于5个资产，总共会有15个NaN值。
    - `correlation(open, volume, 10)` 使用10天的滚动窗口且 `min_periods=10`，因此需要至少10个数据点。每个资产序列的前9个 `corr_open_volume_10` 值为NaN。对于5个资产，总共会有45个NaN值。
    - 最终的 `alpha14` 值同样会因为上述原因，在每个资产序列的前9行出现NaN，总计45个NaN值。
- **排名方法 (`rank`)**:
    - 脚本中默认使用升序百分比排名 (`method='average', ascending=True, pct=True`)。这意味着 `delta_returns_3` 最小的值（例如，收益率改善最大或恶化最小）得到接近0的排名，最大的值得到接近1的排名。
    - `na_option='keep'` 会在排名时保留NaN。
- **相关性计算 (`correlation`)**:
    - 相关性系数的取值范围是 `[-1, 1]`。
    - 计算相关性时，如果窗口期内数据标准差为零（例如，开盘价或成交量在10天内完全不变），则相关性可能为NaN。
- **收益率计算 (`returns`)**:
    - 如果 `returns` 列不是原始数据的一部分，通常由 `close` 价格计算。第一个日期的收益率无法计算 (NaN)。
    - `delta(returns, 3)` 会进一步引入NaN。
- **数据质量**:
    - 输入数据的准确性至关重要。异常值、缺失值会影响 `delta`, `rank`, `correlation` 的计算。
    - 确保 `open`, `volume`, `returns` (或 `close`) 数据是经过清洗和调整的（如复权处理）。
- **解释性与回测**:
    - Alpha#14是一个复合因子，其经济学含义可能不直观，需要结合因子值的分布和实际市场回测来验证其有效性。
    - `-1 * rank(delta(returns,3))` 部分的解释：
        - 当 `delta(returns,3)` 值较小（例如，近期收益率变化平缓，或者从大幅亏损变为小幅亏损/盈利），`rank` 值接近0 (因为是升序百分比排名)。此时 `-1 * rank` 也接近0。
        - 当 `delta(returns,3)` 值较大（例如，近期收益率变化剧烈，比如从微亏/盈变为大幅盈利，或者从微亏/盈变为大幅亏损），`rank` 值接近1。此时 `-1 * rank` 接近-1。
        - 因此，`-1 * rank(delta(returns,3))` 这一项的取值范围大致在 `[-1, 0]` 区间（忽略NaN）。它将收益率变化最剧烈（无论是正向还是负向，只要绝对变化大且排名靠后）的情况映射到接近-1的值，将收益率变化最平缓的情况映射到接近0的值。
- **共线性和过拟合**:
    - 多个基础指标组合的复杂因子有过度拟合历史数据的风险。应在样本外数据上进行严格测试。

建议将 Alpha#14 与其他因子分析结合，并进行充分的回测和风险评估。 