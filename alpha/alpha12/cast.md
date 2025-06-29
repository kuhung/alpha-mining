解读101个量化因子｜Alpha#12: 成交量价格反转

**公式**: `(sign(delta(volume, 1)) * (-1 * delta(close, 1)))`

**核心逻辑**: 

1.  **`sign(delta(volume, 1))`**: 获取昨日至今成交量的变动方向 (增加为1, 减少为-1, 不变为0)。
2.  **`(-1 * delta(close, 1))`**: 获取昨日至今价格变动的反方向。
3.  两者相乘：
    *   若成交量增加且价格上涨，因子为负 (预期反转下跌)。
    *   若成交量增加且价格下跌，因子为正 (预期反转上涨)。
    *   若成交量减少且价格上涨，因子为正。
    *   若成交量减少且价格下跌，因子为负。

**解读**: 当成交量放大时，因子预期价格反转。当成交量缩小时，因子的符号与价格反向变动的符号相同。

---

### 日本語訳

101の量的要因の解釈｜Alpha#12: 取引量価格反転

**数式**: `(sign(delta(volume, 1)) * (-1 * delta(close, 1)))`

**コアロジック**:

1.  **`sign(delta(volume, 1))`**: 昨日から今日までの取引量の変動方向を取得します（増加の場合は1、減少の場合は-1、変化なしの場合は0）。
2.  **`(-1 * delta(close, 1))`**: 昨日から今日までの価格変動の逆方向を取得します。
3.  両者を乗算します：
    *   取引量が増加し、価格が上昇した場合、ファクターは負になります（反転下落を期待）。
    *   取引量が増加し、価格が下落した場合、ファクターは正になります（反転上昇を期待）。
    *   取引量が減少し、価格が上昇した場合、ファクターは正になります。
    *   取引量が減少し、価格が下落した場合、ファクターは負になります。

**解釈**: 取引量が増加すると、ファクターは価格の反転を期待します。取引量が減少すると、ファクターの符号は価格の逆変動の符号と同じになります。 