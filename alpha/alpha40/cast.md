# 解读101个量化因子｜Alpha#40 波动率与相关性反转策略

**因子公式:** `((-1 * rank(stddev(high, 10))) * correlation(high, volume, 10))`

Alpha#40 是一个旨在利用资产波动性与价量关系进行反转交易的因子。其核心思想是，高波动性与高价量正相关性同时出现，可能预示着趋势的衰竭或反转，因此构成一个负面（做空）信号。

1. 反转的波动率排名 (`-1 * rank(stddev(high, 10))`): 此部分对资产的短期（10日）价格波动率进行排名，然后取负。这意味着策略偏好低波动率的资产（给予更高分），而惩罚高波动率的资产（给予更低分）。
2. 价量相关性 (`correlation(high, volume, 10)`): 此部分衡量资产的最高价与成交量在短期（10日）内的相关性。正相关（价涨量增）通常被视为趋势健康的标志，但在此策略中与其他部分结合，可能被解读为过热信号。
3. 乘积: 将上述两个部分相乘。当一个资产波动率高（`-1 * rank` 为大的负数）且价量正相关时，最终的 Alpha 值会是一个较大的负数，构成一个强烈的卖出或做空信号。反之，当价量为负相关时，可能会产生正的 Alpha 值，尤其是在高波动率的情况下。

预期效果: 识别出那些价格波动剧烈且成交量跟随价格上涨（可能预示着非理性繁荣或趋势末端）的资产，并将其作为潜在的做空目标。

## 数据要求

* `high`: 每日最高价。
* `volume`: 每日成交量。

## 输出

生成 `alpha40_results.csv` 文件，其中包含计算出的 `alpha40` 值及其中间列（如 `stddev_high_10`, `rank_stddev_high_10`, `corr_high_volume_10`），所有数值均保留两位小数。`alpha40` 列为 `NaN` 的行将被剔除。
