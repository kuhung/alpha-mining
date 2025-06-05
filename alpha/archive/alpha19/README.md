# Alpha#19: 趋势反转与长期回报的动态平衡

## 描述

Alpha#19 的计算公式为：

```
Alpha#19 = ((-1 * sign(((close - delay(close, 7)) + delta(close, 7)))) * (1 + rank((1 + sum(returns, 250)))))
```

这个 Alpha 策略结合了两个主要部分：
1.  **趋势反转信号**: `(-1 * sign(((close - delay(close, 7)) + delta(close, 7))))`
    *   `delay(close, 7)`: 7天前的收盘价。
    *   `close - delay(close, 7)`: 当前收盘价与7天前收盘价的差，代表过去7天的价格变化量。
    *   `delta(close, 7)`: 这通常也指 `close - delay(close, 7)`，即7日价格差。所以 `((close - delay(close, 7)) + delta(close, 7))` 实质上是 `2 * (close - delay(close, 7))`。
    *   `sign(...)`: 取上述表达式的符号（+1, -1, 或 0）。
    *   `-1 * sign(...)`: 对符号进行反转。如果过去7天价格显著上涨，`sign` 为 +1，乘以 -1 后为 -1。如果显著下跌，`sign` 为 -1，乘以 -1 后为 +1。
    *   这个部分旨在捕捉趋势反转：如果近期价格上涨，它给出一个负向信号；如果近期价格下跌，它给出一个正向信号，暗示一种潜在的短期反转机会。

2.  **长期回报增强**: `(1 + rank((1 + sum(returns, 250))))`
    *   `sum(returns, 250)`: 计算过去250天（约一年）的累计回报。
    *   `1 + sum(returns, 250)`: 将累计回报加1，避免负值影响。
    *   `rank(...)`: 对上述结果进行截面排名。
    *   `1 + rank(...)`: 将排名结果加1，确保最终乘数大于1。
    *   这个部分作为一个放大因子，基于资产的长期表现来调整信号强度。长期表现越好的资产，其信号会被放大得越多。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据 (需包含 close, returns)
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha19/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#19
│   ├── alpha19_results.csv    # 计算得到的 Alpha#19 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#19 策略简介
```

## 使用步骤

### 1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。如果未安装，可以通过 pip 安装：

```bash
pip install pandas numpy
```

### 2. 检查模拟数据

本 Alpha 依赖于 `close` 和 `returns` 数据。请确保 `data/mock_data.csv` 文件存在，并且包含了 `date`, `asset_id`, `close`, `returns` 列。 `returns` 应为日回报率（例如，0.01 代表 1%）。

```bash
# 检查或生成数据 (如果需要)
cd ../../data # 假设当前在 alpha/alpha19 目录
python generate_mock_data.py # 确保此脚本能生成 returns 列
cd ../alpha/alpha19
```

### 3. 计算 Alpha#19 因子

进入 `alpha/alpha19` 目录并运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#19，并将结果保存到 `alpha19_results.csv`。

## Alpha#19 策略解读与计算步骤概述

1.  **计算7日价格变动**:
    *   对每个资产，计算 `close - delay(close, 7)` 作为7日价格变动。
2.  **计算趋势反转信号**:
    *   对每个资产，计算 `trend_signal = -1 * sign(2 * price_change_7d)`。
3.  **计算250日累计回报**:
    *   对每个资产，计算 `sum_returns_250d = sum(returns, 250)`。
4.  **计算回报排名因子**:
    *   对每个资产，计算 `return_rank_factor = 1 + rank(1 + sum_returns_250d)`。
5.  **计算最终Alpha值**:
    *   `Alpha#19 = trend_signal * return_rank_factor`。

## Alpha#19 策略解读与计算示例

### 数据快照 (asset_1, 2025-01-24)

根据 `alpha19_results.csv` 的实际数据，我们选取 `asset_1` 在 `2025-01-24` 的数据作为示例：

| date       | asset_id | close | close_delay_7 | price_change_7d | trend_signal | sum_returns_250 | return_rank_factor | alpha19 |
|------------|----------|-------|---------------|-----------------|--------------|-----------------|-------------------|---------|
| 2025-01-24 | asset_1  | 97.20 | 95.80        | 1.40           | -1          | 0.156          | 1.850             | -1.850  |

### 计算步骤详解 (asset_1, 2025-01-24):

1.  **7日价格变动**:
    *   `price_change_7d = close - close_delay_7 = 97.20 - 95.80 = 1.40`

2.  **趋势反转信号**:
    *   `double_price_change = 2 * 1.40 = 2.80`
    *   `sign(2.80) = 1`
    *   `trend_signal = -1 * 1 = -1`

3.  **250日累计回报**:
    *   过去250天的累计回报 `sum_returns_250 = 0.156` (15.6%)

4.  **回报排名因子**:
    *   `1 + sum_returns_250 = 1.156`
    *   `rank(1.156) = 0.850` (表示在当日所有资产中排在第85%分位)
    *   `return_rank_factor = 1 + 0.850 = 1.850`

5.  **最终 Alpha#19 值**:
    *   `alpha19 = trend_signal * return_rank_factor = -1 * 1.850 = -1.850`

**解读 (asset_1, 2025-01-24)**:
在 `2025-01-24` 这一天，`asset_1`：
*   过去7天价格上涨（`price_change_7d = 1.40`），导致趋势反转信号为负
*   过去250天累计回报较好（15.6%），在市场中排名靠前（85%分位）
*   由于长期表现好（回报排名因子为1.850），放大了负向的趋势反转信号
*   最终得到一个较大的负向Alpha值（-1.850），暗示可能即将出现回调

## 数据需求

-   `date`: 交易日期 (datetime)
-   `asset_id`: 资产ID (string/object)
-   `close`: 每日收盘价 (float)
-   `returns`: 每日回报率 (float, e.g., 0.01 for 1%)
-   (脚本可能包含 `open`, `high`, `low`, `volume` 等其他列以保持数据完整性)

## 输出格式

输出的 CSV 文件 (`alpha19_results.csv`) 将包含以下列（除了原始数据列），所有数值型 alpha 相关列均保留一定小数位数，最终 Alpha#19 保留两位有效数字：

-   `date`: 交易日期
-   `asset_id`: 资产ID
-   `open`, `high`, `low`, `close`, `volume`, `returns`: 原始数据中的对应列（如果存在）
-   `close_delay_7`: 7天前的收盘价
-   `price_change_7d`: 7天价格变化 (close - delay(close, 7))
-   `double_price_change_7d`: 双倍7天价格变化
-   `sign_double_price_change`: 价格变化的符号
-   `trend_signal`: 趋势反转信号 (-1 * sign)
-   `sum_returns_250`: 250天累计回报
-   `one_plus_sum_returns`: 累计回报加1
-   `rank_sum_returns`: 累计回报的排名
-   `return_rank_factor`: 回报排名因子 (1 + rank)
-   `alpha19`: 最终计算的 Alpha#19 值

## 注意事项与风险提示

-   **数据窗口期**:
    *   `delay(close, 7)` 和 `delta(close, 7)`: 需要至少7天前的收盘价数据。每个资产的前7天相关计算值为NaN。
    *   `sum(returns, 250)`: 计算累计回报需要至少250天的数据。每个资产的前249天该值为NaN。
    *   综合来看，`alpha19` 的第一个非NaN值将取决于最长的窗口期（250天）。因此，每个资产数据序列的前249行其 `alpha19` 很可能为NaN。
-   **`delta(close, 7)`的理解**: 在WorldQuant的公式中，`delta(X, d)` 通常指 `X - delay(X, d)`。因此 `(close - delay(close, 7)) + delta(close, 7)` 等价于 `2 * (close - delay(close, 7))`。代码实现将基于此理解。
-   **`sign` 函数**: 如果 `(close - delay(close, 7)) + delta(close, 7)` 为0，`sign` 函数返回0，导致 Alpha#19 为0。
-   **排名方法**: `pandas` 的 `rank(pct=True)` 方法用于所有截面排名，这意味着结果是百分比形式的排名。
-   **回报率 `returns`**: 确保 `returns` 列是日回报率（小数形式）。累计回报 `sum(returns, 250)` 是算术求和，不是几何累计。
-   **小数位数**: 中间步骤建议保留足够精度，最终 Alpha#19 结果将按要求格式化为两位有效数字。
-   **市场适用性**: 此因子表现可能因市场环境、资产类别而异。需进行充分回测验证。
-   **数据质量**: 输入数据的准确性和完整性至关重要。

Alpha#19 是一个结合了趋势反转信号和长期回报表现的复合因子，不保证未来表现。建议与其他因子结合使用，并进行充分的回测验证。