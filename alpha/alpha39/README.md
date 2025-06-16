# Alpha#39: 复合因子策略

## Formula

```
((-1 * rank((delta(close, 7) * (1 - rank(decay_linear((volume / adv20), 9)))))) * (1 + rank(sum(returns, 250))))
```

## Description

Alpha#39 是一个多因子量化交易策略，结合了成交量调整后的价格动量、截面成交量分析和长期收益持续性。其核心思想是识别那些价格变化强劲（`delta(close, 7)`），但这种动量并非主要由线性衰减的高成交量（可能表示较弱的信念或潜在的短期噪音）所驱动的股票，然后将此信号与长期积极的收益趋势相结合。最终因子值是一个反向关系，这意味着当组合动量和成交量信号为负时，值越高越好，并且该值由长期积极收益趋势的强度进行加权。

### Components:

1.  **`delta(close, 7)`**: 计算7个周期内收盘价的变化。这捕捉了短期价格动量。
2.  **`volume / adv20`**: 将当前成交量除以20周期平均日成交量（`adv20`）。这提供了一个异常成交量的衡量标准。
3.  **`decay_linear((volume / adv20), 9)`**: 对 `volume / adv20` 应用9个周期内的线性衰减加权。近期异常成交量具有更高的权重。
4.  **`rank(decay_linear((volume / adv20), 9))`**: 对线性衰减后的异常成交量进行截面排名。衰减后异常成交量越高的股票，排名越高。
5.  **`1 - rank(decay_linear((volume / adv20), 9))`**: 反转衰减后异常成交量的排名。这意味着衰减后异常成交量*较低*的股票，在此组件中具有更高的值。
6.  **`delta(close, 7) * (1 - rank(decay_linear((volume / adv20), 9)))`**: 将短期价格动量乘以反转后的衰减异常成交量排名。这里的意图是倾向于那些价格动量*不*伴随过高或异常成交量的股票。
7.  **`rank((delta(close, 7) * (1 - rank(decay_linear((volume / adv20), 9)))))`**: 对组合后的价格动量和调整后成交量因子进行截面排名。
8.  **`-1 * rank(...)`**: 反转前一个组件的排名。这表明对于这个组合因子，较低（更负）的值是优选的，意味着该策略旨在做空或做空那些价格动量高但异常成交量也高（因此 `1 - rank(...)` 值低，使得乘积小或为负）的名称。
9.  **`sum(returns, 250)`**: 计算250周期（约一年）内日收益率的总和。这捕捉了长期收益的持续性。
10. **`rank(sum(returns, 250))`**: 对长期收益总和进行截面排名。长期正收益越强的股票，排名越高。
11. **`1 + rank(sum(returns, 250))`**: 在长期收益的排名上加1。这确保了正的缩放因子。
12. **最终公式**: 将反转后的动量-成交量因子乘以缩放后的长期收益持续性。该策略似乎奖励那些具有有利动量-成交量特征（可能是动量方面的均值回归，或没有过度成交量的动量），并由强劲的长期正收益放大。

## Calculation Steps

1.  **数据准备与预计算**: 加载`close`, `volume`, `returns`数据。为每个资产计算20周期平均成交量 `adv20`，作为后续计算的基础。
2.  **计算动量与成交量复合因子**: 首先分别计算价格动量 `delta(close, 7)` 和成交量调整项 `(1 - rank(decay_linear((volume / adv20), 9)))`。然后将两者相乘，得到动量与成交量复合因子 `momentum_volume_component`。
3.  **计算反转后的动量排名**: 对第二步得到的复合因子进行截面排名，并乘以-1，得到 `neg_ranked_momentum_volume_component`。这是公式的第一个主要部分。
4.  **计算长期收益因子**: 计算250日累计收益 `sum(returns, 250)`，然后对其结果进行截面排名并加1，得到 `scaled_long_term_returns`。这是公式的第二个主要部分。
5.  **计算最终Alpha值**: 将第三步和第四步的结果相乘，得到最终的 `alpha39` 值，并筛选掉NaN值后保存结果。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据 (确保包含 close, volume, returns 字段)
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha39/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#39
│   ├── alpha39_results.csv    # 计算得到的 Alpha#39 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#39 策略简介
```

## 使用步骤

### 1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。如果未安装，可以通过 pip 安装：

```bash
pip install pandas numpy
```

### 2. 检查模拟数据

本 Alpha 依赖于 `close`, `volume`, `returns` 数据。请确保 `data/mock_data.csv` 文件存在，并且包含了 `date`, `asset_id`, `close`, `volume`, `returns` 列。如果文件不存在或数据不完整，请运行或修改 `data/generate_mock_data.py` 脚本。

```bash
# 检查或生成数据 (如果需要)
cd ../../data # 假设当前在 alpha/alpha39 目录
python generate_mock_data.py # 假设此脚本能生成所需字段
cd ../alpha/alpha39
```

### 3. 计算 Alpha#39 因子

进入 `alpha/alpha39` 目录并运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#39，并将结果保存到当前目录下的 `alpha39_results.csv`。

## 数据输入

*   `close`: 每日收盘价数据。
*   `volume`: 每日成交量数据。
*   `returns`: 每日收益率数据。

这些数据预计从 `../../data/mock_data.csv` 文件中获取。

## 输出格式

输出的 CSV 文件 (`alpha39_results.csv`) 将包含以下列（除了原始数据列），所有数值型 alpha 相关列均保留两位小数：

-   `date`: 交易日期
-   `asset_id`: 资产ID
-   `open`, `high`, `low`, `close`, `volume`, `vwap`, `returns`: 原始数据中的对应列
-   `adv20`: 20日平均成交量
-   `delta_close_7`: 7日收盘价变化
-   `volume_div_adv20`: 成交量与20日平均成交量的比值
-   `decay_linear_volume_adv20_9`: 线性衰减后的成交量与20日平均成交量的比值
-   `ranked_decay_linear_volume_adv20`: 衰减后成交量与20日平均成交量比值的截面排名
-   `one_minus_ranked_decay_linear`: `1 - rank(decay_linear_volume_adv20_9)`
-   `momentum_volume_component`: `delta(close, 7) * (1 - rank(decay_linear((volume / adv20), 9)))`
-   `ranked_momentum_volume_component`: `momentum_volume_component` 的截面排名
-   `neg_ranked_momentum_volume_component`: `-1 * ranked_momentum_volume_component`
-   `sum_returns_250`: 250日收益率总和
-   `ranked_sum_returns_250`: 250日收益率总和的截面排名
-   `one_plus_ranked_sum_returns`: `1 + ranked_sum_returns_250`
-   `alpha39`: 最终计算的 Alpha#39 值。

## 注意事项与风险提示

-   **NaN 值**: 如果输入数据缺失或计算中出现 `NaN`（例如，排名或时间序列操作需要足够的数据点），相应的 Alpha 值将为 `NaN`。请确保数据完整性。计算结果中 `alpha39` 列为 `NaN` 的行将不会被写入最终的 CSV 文件。
-   **排名方法**: `pandas` 的 `rank(method='average', pct=True)` 通常用于截面排名，结果是百分比形式。
-   **小数位数**: 最终的 Alpha#39 值及中间结果按要求保留两位小数。
-   **市场适用性**: 此因子在不同市场环境或资产类别上表现可能迥异。务必进行充分的回测和验证。
-   **数据质量**: 输入数据的准确性和完整性至关重要。

Alpha#39 是一个基于多项指标合成的因子，不保证未来表现。建议与其他因子结合使用，并进行充分的回测验证。

## 策略解读与计算示例

我们将以 `asset_1` 在日期 `2025-02-05` 的数据为例，展示 Alpha#39 的计算。

**背景数据 (源自 `alpha39_results.csv` for `asset_1` on `2025-02-05`):**
- `delta_close_7`: -4.00
- `one_minus_ranked_decay_linear`: 0.40
- `momentum_volume_component`: -1.60
- `neg_ranked_momentum_volume_component`: -0.20
- `one_plus_ranked_sum_returns`: 1.20
- `alpha39`: -0.24

**计算 Alpha#39 (简化步骤):**

1.  **数据准备与预计算**:
    -   我们已经预先计算好 `adv20`，这对于计算成交量调整项是必要的。

2.  **计算动量与成交量复合因子**:
    -   `momentum_volume_component = delta_close_7 * one_minus_ranked_decay_linear`
    -   `= -4.00 * 0.40 = -1.60`

3.  **计算反转后的动量排名**:
    -   `neg_ranked_momentum_volume_component` 是对 `momentum_volume_component` 进行截面排名后乘以-1得到的结果。
    -   `= -0.20`

4.  **计算长期收益因子**:
    -   `one_plus_ranked_sum_returns` 是对250日累计收益进行排名后加1得到的结果。
    -   `= 1.20`

5.  **最终 Alpha#39 值**:
    -   `alpha39 = neg_ranked_momentum_volume_component * one_plus_ranked_sum_returns`
    -   `= -0.20 * 1.20 = -0.24`

因此，`Alpha#39` 对 `asset_1` 在 `2025-02-05` 的最终计算值为 `-0.24`。这个值与 `alpha39_results.csv` 中对应行的 `alpha39` 列的值相符。 