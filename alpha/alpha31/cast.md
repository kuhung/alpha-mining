解读101个量化因子｜Alpha#31 多因子组合策略

**公式**: `((rank(rank(rank(decay_linear((-1 * rank(rank(delta(close, 10)))), 10)))) + rank((-1 * delta(close, 3)))) + sign(scale(correlation(adv20, low, 12))))`

**核心逻辑**:
Alpha#31 是一个复合因子，旨在通过整合市场价格趋势的持续性、短期反转机会以及量价关系的方向，生成一个综合性的交易信号。它主要由以下三个独立计算后相加的部分构成：

1. **趋势与动量部分**: `rank(rank(rank(decay_linear((-1 * rank(rank(delta(close, 10)))), 10))))`
   对收盘价10日变化的负向双重排名结果进行10日衰减线性加权，再进行三次排名，以捕捉平滑后的价格动量强度。
2. **短期反转部分**: `rank((-1 * delta(close, 3)))`
   对收盘价3日变化的负值进行排名，以捕捉短期价格反转信号。
3. **量价关系部分**: `sign(scale(correlation(adv20, low, 12)))`
   取20日平均成交量与每日最低价在12日内的时序相关性的截面标准化值的符号，以判断量价配合的方向。
