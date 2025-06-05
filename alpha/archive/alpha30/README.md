# Alpha#30: 价格变动符号排名与成交量比率的乘积

本项目实现了 Alpha#30 因子的计算逻辑。

## 1. Alpha#30 公式

Alpha#30 的计算公式如下：

```
(((1.0 - rank(((sign((close - delay(close, 1))) + sign((delay(close, 1) - delay(close, 2)))) + sign((delay(close, 2) - delay(close, 3)))))) * sum(volume, 5)) / sum(volume, 20))
```

**公式各项说明**:

*   `close`: 资产的日收盘价。
*   `volume`: 资产的日成交量。
*   `delay(x, N)`: 将序列 `x` 的值向后推移 `N` 天，即取 `N` 天前的值 `x.shift(N)`。
*   `sign(x)`: 取 `x` 的符号。如果 `x > 0`，返回1；如果 `x < 0`，返回-1；如果 `x = 0`，返回0。
*   `rank(x)`: 对序列 `x` 在截面（特定日期所有资产）上进行百分位排名 (0到1之间)。
*   `sum(x, N)`: 计算序列 `x` 在过去 `N` 天窗口内的和。

## 2. 核心逻辑

计算 Alpha#30 的主要步骤如下：

1.  **计算价格变动符号之和 (`sign_sum`)**:
    *   `d1 = close - delay(close, 1)`: 计算当日收盘价与1日前收盘价的差值。
    *   `d2 = delay(close, 1) - delay(close, 2)`: 计算1日前收盘价与2日前收盘价的差值。
    *   `d3 = delay(close, 2) - delay(close, 3)`: 计算2日前收盘价与3日前收盘价的差值。
    *   `sign_sum = sign(d1) + sign(d2) + sign(d3)`: 将这三个差值的符号相加。该值范围为 `[-3, 3]`，反映了过去三天价格变动的总体方向和一致性。
        *   例如, `+3` 表示连续三日上涨, `-3` 表示连续三日下跌。

2.  **计算排名转换 (`rank_transformed`)**:
    *   `ranked_sign_sum = rank(sign_sum)`: 对每个交易日所有资产的 `sign_sum` 进行横截面百分位排名。
    *   `rank_transformed = 1.0 - ranked_sign_sum`: 用1.0减去排名。这意味着，如果一只股票的 `sign_sum` 较低（例如，持续下跌导致排名靠后），其 `rank_transformed` 值会较高。

3.  **计算成交量比率 (`volume_ratio`)**:
    *   `sum_volume_5 = sum(volume, 5)`: 计算过去5日的成交量总和。
    *   `sum_volume_20 = sum(volume, 20)`: 计算过去20日的成交量总和。
    *   `volume_ratio = sum_volume_5 / sum_volume_20`: 计算5日成交量总和与20日成交量总和的比率。此比率反映了近期成交量的相对活跃程度。
        *   (注意：需处理 `sum_volume_20` 为零的情况，脚本中已通过替换为 `np.nan` 来避免除零错误)。

4.  **计算最终 Alpha#30 值**:
    *   `alpha30 = rank_transformed * volume_ratio`。

## 3. 策略解读

Alpha#30 试图结合价格动量的短期一致性（经过特定排名转换）与成交量的相对活跃度。

*   **价格动量信号 (`rank_transformed`) 的含义**:
    *   `sign_sum` 捕捉了过去三天价格变动的连续性。值越高，表明上涨的一致性越强；值越低，表明下跌的一致性越强。
    *   `rank(sign_sum)` 对这种一致性在所有资产中进行排序。
    *   `1.0 - rank(...)` 操作将原始排名信号反转。因此，原始 `sign_sum` 值较低（如持续下跌，排名靠后）的资产，其 `rank_transformed` 会较高。这表明该部分因子倾向于关注那些近期价格表现疲软或呈下跌趋势的资产。

*   **成交量活跃度信号 (`volume_ratio`) 的含义**:
    *   `sum(volume, 5) / sum(volume, 20)` 衡量了短期（5日）成交量相对于中期（20日）成交量的放大或萎缩程度。
    *   比率大于1通常表示近期成交活跃度增加，小于1则表示活跃度下降。

*   **组合解读**:
    *   Alpha#30 将这两个信号相乘。一个较高的 Alpha#30 值可能来自于以下组合：
        1.  资产经历了持续下跌或上涨势头显著减弱（导致 `rank_transformed` 较高），**并且** 近期成交量显著放大（`volume_ratio` 较高）。这种情况可能指示"恐慌性抛售后的潜在反转点"或"下跌末期放量"。
        2.  资产经历了持续下跌或上涨势头显著减弱（`rank_transformed` 较高），**并且** 近期成交量显著萎缩（`volume_ratio` 较低）。这种情况可能指示"下跌中继的缩量整理"。
    *   由于 `rank_transformed` 的设计，该因子似乎更侧重于从价格表现较弱的股票中寻找机会，并通过成交量比率来进一步筛选。
    *   因子值的具体指向（看涨或看跌）最终需要通过因子与未来收益率的相关性回测来确定。

## 4. 项目结构

```text
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha30/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#30
│   ├── alpha30_results.csv    # 计算得到的 Alpha#30 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#30 策略总结与转换说明
```

## 5. 使用步骤

### 5.1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。

```bash
pip install pandas numpy
```

### 5.2. 数据准备

运行 `alpha_calculator.py` 脚本需要 `mock_data.csv` 文件位于项目根目录下的 `data/` 目录中。该 CSV 文件必须至少包含以下列：

*   `date` (日期)
*   `asset_id` (资产ID)
*   `close` (收盘价)
*   `volume` (成交量)

如果数据文件不存在或需要更新，您可以运行 `data/generate_mock_data.py` (请确保该脚本会生成上述所有必需列)。

### 5.3. 计算 Alpha#30 因子

在 `alpha/alpha30/` 目录下，通过命令行运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将：
1.  读取 `../../data/mock_data.csv` 文件。
2.  计算 Alpha#30 因子。
3.  将结果（包括部分原始数据列和计算得到的 `alpha30` 列）保存到当前目录下的 `alpha30_results.csv` 文件中。
4.  在终端打印输出文件的前5行、后5行以及 `alpha30` 列的描述性统计信息。

## 6. Alpha#30 计算示例 (基于实际输出)

### 6.1. 数据快照

根据 `alpha30_results.csv` 的实际输出数据，我们选取 `asset_1` 在 `2025-01-20` 的数据作为示例：

| date       | asset_id | close | volume  | alpha30 |
|:-----------|:---------|:------|:--------|:--------|
| 2025-01-20 | asset_1  | 98.8  | 1698241 | 0.06    |

*(注: `alpha30` 的值直接来自生成的结果文件。空值表示因计算窗口期不足等原因无法计算)*

### 6.2. 计算步骤详解 (以 asset_1, 2025-01-20 为例)

为计算 `asset_1` 在 `2025-01-20` 的 `alpha30` 值，`alpha_calculator.py` 脚本会执行以下操作：

1.  **获取价格和成交量数据**：获取 `asset_1` 在 `2025-01-20` 及之前3个交易日的 `close` 数据，以及之前20个交易日的 `volume` 数据。
2.  **计算 `sign_sum`**:
    *   `close` (01-20): 98.8; `close` (01-19): 97.9; `close` (01-18): 100.1; `close` (01-17): 98.0.
    *   `sign(98.8 - 97.9) = sign(0.9) = 1`
    *   `sign(97.9 - 100.1) = sign(-2.2) = -1`
    *   `sign(100.1 - 98.0) = sign(2.1) = 1`
    *   `sign_sum = 1 + (-1) + 1 = 1`
3.  **计算 `rank_transformed`**:
    *   假设在 `2025-01-20` 这一天，`asset_1` 的 `sign_sum` (值为1) 在当日所有资产中进行横截面排名后，得到的百分位排名 `rank(sign_sum)` 为 `0.6` (此为示例值，实际值取决于当日其他资产的 `sign_sum` 分布)。
    *   `rank_transformed = 1.0 - 0.6 = 0.4`。
4.  **计算 `volume_ratio`**:
    *   计算 `asset_1` 截至 `2025-01-20` 的过去5日成交量总和 `sum_volume_5` (例如，`6,801,796`)。
    *   计算 `asset_1` 截至 `2025-01-20` 的过去20日成交量总和 `sum_volume_20` (例如，`45,000,000`)。
    *   `volume_ratio = sum_volume_5 / sum_volume_20 = 6801796 / 45000000 pprox 0.151` (此为示例值)。
5.  **计算最终 `alpha30`**:
    *   `alpha30 = rank_transformed * volume_ratio = 0.4 * 0.151 = 0.0604`。
    *   保留两位小数后，最终存储为 `0.06`。

**对 `alpha30 = 0.06` 的解读**: 
在 `2025-01-20` 这一天，`asset_1` 的 `alpha30` 值为 `0.06`。这个较小的正值表明，该资产近期价格趋势信号（经反转排名）与成交量相对强度信号的乘积，略微偏向正向，但信号强度不大。

## 7. 数据列说明

### 7.1. 输入数据 (`mock_data.csv`)

*   `date`: 交易日期 (例如 `YYYY-MM-DD` 格式)。
*   `asset_id`: 资产的唯一标识符。
*   `close`: 当日收盘价 (数值型) - **核心计算列**。
*   `volume`: 当日成交量 (数值型) - **核心计算列**。
*   *(脚本会保留输入数据中的其他列到输出文件，但它们不直接参与 Alpha#30 的核心计算)*

### 7.2. 输出数据 (`alpha30_results.csv`)

输出的 CSV 文件将包含原始数据中的所有相关列，并附加一列 `alpha30`：

*   `date`, `asset_id`, `close`, `volume` (及其他原始列，如脚本中所包含的)
*   `alpha30`: 计算得到的 Alpha#30 因子值 (浮点数，保留两位小数)。空值（NaN）表示无法计算。

## 8. 注意事项与风险提示

*   **数据窗口期**: 公式中包含 `delay(close, 3)` 和 `sum(volume, 20)`。因此，计算 `alpha30` 需要至少20个交易日的历史数据（主要受 `sum(volume, 20)` 影响，尽管 `delay` 最多3天）。输出结果中，前19个左右有效交易日的 `alpha30` 值可能为空。根据 `alpha30_results.csv` 示例，第一个非空值出现在 `2025-01-20`。
*   **成交量为零**: 如果 `sum(volume, 20)` 在某个计算点为零（例如，长期停牌后刚复牌的股票，累积成交量不足），会导致除以零的错误。`alpha_calculator.py` 脚本中通过将 `volume_ratio` 在此情况下设为 `np.nan` 来处理。
*   **可解释性**: 虽然公式的每个组成部分都有其直观含义，但 `1.0 - rank` 的反向操作使得最终因子的多空信号解释需要特别注意，并强烈建议结合严格的回测结果来最终判断其预测方向和有效性。
*   **因子有效性**: Alpha#30 是一个基于历史价量数据统计构建的因子，其历史表现不代表未来收益。在实际应用前，建议进行充分的回测验证。

---

如需帮助或对本文档及代码有任何建议，欢迎随时交流！ 