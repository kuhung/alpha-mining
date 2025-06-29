# 解读101个量化因子｜Alpha#28: 成交量最低价相关性与价格中枢偏离的标准化

**原始公式**:

```
scale(((correlation(adv20, low, 5) + ((high + low) / 2)) - close))
```

**核心逻辑**:
该因子首先计算20日平均成交量 (`adv20`) 和当日的中间价 (`(high + low) / 2`)。然后，计算 `adv20` 与最低价 `low` 在过去5日的相关系数。将此相关系数与中间价相加，再减去当日收盘价 `close`。最后，对得到的结果进行横截面标准化 (`scale`)。

**解读**:

Alpha#28 结合了成交量动态（20日平均成交量与最低价的5日相关性）、价格日内位置（中间价与收盘价的差值），旨在寻找那些综合表现（经过横截面标准化后）偏离市场均值的股票。因子值为正，通常表示该股票在特定模式下表现相对较强；为负则表示相对较弱。

---

### 日本語訳

# 101の量的要因の解釈｜Alpha#28: 出来高・安値相関と価格中心からの乖離の標準化

**数式**:

```
scale(((correlation(adv20, low, 5) + ((high + low) / 2)) - close))
```

**コアロジック**:
このファクターは、まず20日平均出来高（`adv20`）と当日の中心価格（`(高値 + 安値) / 2`）を計算します。次に、`adv20`と安値（`low`）の過去5日間の相関係数を計算します。この相関係数を中心価格に加算し、そこから当日の終値（`close`）を減算します。最後に、得られた結果をクロスセクションで標準化（`scale`）します。

**解釈**:
Alpha#28は、出来高の動態（20日平均出来高と安値の5日間相関）、日中の価格位置（中心価格と終値の差）を組み合わせ、その総合的なパフォーマンス（クロスセクション標準化後）が市場平均から乖離している銘柄を探すことを目的としています。ファクター値が正の場合、通常、その銘柄が特定のパターンにおいて相対的に強いパフォーマンスを示していることを意味し、負の場合は相対的に弱いことを示します。
