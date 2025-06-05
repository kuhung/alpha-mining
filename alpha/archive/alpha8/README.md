# Alpha#8: 开盘价与回报率的短期相关性变化

## 描述

Alpha#8 的计算公式为：

```
Alpha#8: (-1 * rank(((sum(open, 5) * sum(returns, 5)) - delay((sum(open, 5) * sum(returns, 5)), 10))))
```

这个 Alpha 策略旨在捕捉开盘价（open）和回报率（returns）在短期内的相关性变化。它通过计算过去5天的开盘价总和与回报率总和的乘积，并与10天前的相同乘积进行比较，最后对差值进行排名并取负值。这种设计可以捕捉到价格与回报率之间相关性的动态变化，从而产生潜在的交易信号。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据（包含open, returns字段）
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha8/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#8
│   ├── alpha8_results.csv     # 计算得到的 Alpha#8 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md               # Alpha#8 策略总结
```

## 使用步骤

### 1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。如果未安装，可以通过 pip 安装：

```bash
pip install pandas numpy
```

### 2. 生成模拟数据 (如果需要)

本 Alpha 依赖于 `open` 和 `returns` 数据。`data/generate_mock_data.py` 脚本可以生成这些数据。如果 `data/mock_data.csv` 不存在或需要更新：

```bash
cd data
python generate_mock_data.py
cd ..
```

该脚本默认生成5只资产100天的数据。

### 3. 计算 Alpha#8 因子

进入 `alpha/alpha8` 目录并运行 `alpha_calculator.py` 脚本：

```bash
cd alpha/alpha8
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#8，并将结果保存到当前目录下的 `alpha8_results.csv`。同时会在终端打印部分结果和统计信息。

## Alpha#8 策略解读与计算示例

Alpha#8 是一个**开盘价与回报率短期相关性变化因子**。它通过以下步骤捕捉价格与回报率之间的动态关系：

1. **短期累积（5天窗口）**：

   - 计算过去5天开盘价的总和 `sum(open, 5)`
   - 计算过去5天回报率的总和 `sum(returns, 5)`
   - 将两个总和相乘，得到短期相关性指标
2. **相关性变化（10天对比）**：

   - 计算当前的相关性指标与10天前的差值
   - 这个差值反映了短期相关性的变化程度
3. **信号生成**：

   - 对差值进行排名 `rank(...)`
   - 取排名的负值 `-1 * rank(...)`
   - 较大的负值表示相关性增强，较大的正值表示相关性减弱

### 实际数据示例 (asset_1 from alpha8_results.csv)

以下为 `asset_1` 在 `alpha8_results.csv` 中部分日期的计算结果：

| date       | asset_id | open   | returns | sum_open_5 | sum_returns_5 | open_returns_product | delayed_product | product_diff | rank_diff | alpha8 |
| ---------- | -------- | ------ | ------- | ---------- | ------------- | -------------------- | --------------- | ------------ | --------- | ------ |
| 2025-01-11 | asset_1  | 99.58  | -0.0119 | 501.21     | -0.01         | -5.01                | NaN             | NaN          | NaN       | NaN    |
| 2025-01-12 | asset_1  | 100.42 | -0.003  | 500.95     | -0.03         | -15.03               | NaN             | NaN          | NaN       | NaN    |
| 2025-01-13 | asset_1  | 98.46  | -0.002  | 498.62     | -0.01         | -4.99                | NaN             | NaN          | NaN       | NaN    |
| 2025-01-14 | asset_1  | 98.54  | 0.002   | 496.45     | -0.01         | -4.96                | NaN             | NaN          | NaN       | NaN    |
| 2025-01-15 | asset_1  | 99.38  | -0.0232 | 496.38     | -0.04         | -19.86               | 20.07           | -39.93       | 0.4       | -0.4   |

### 计算步骤详解

以 `asset_1` 在 `2025-01-15` 的数据为例 (数据来源于 `alpha8_results.csv`)：

1. **计算5天总和**：

   * `sum_open_5` = 496.38 (过去5天开盘价总和)
   * `sum_returns_5` = -0.04 (过去5天回报率总和)
2. **计算乘积**：

   * 当前乘积 (`open_returns_product`) = 496.38 * (-0.04) = -19.86
   * 10天前乘积 (`delayed_product`) = 20.07 (10个交易日前的 `open_returns_product` 值)
3. **计算差值**：

   * 差值 (`product_diff`) = -19.86 - 20.07 = -39.93
4. **排名并取负**：

   * 该差值在当日所有资产的 `product_diff` 值中的排名 (`rank_diff`) 为 0.4 (具体排名方法见 `alpha_calculator.py`，此处为示例)
   * `alpha8` = -1 * 0.4 = -0.4

### 策略逻辑与解读

- **正向信号（alpha8 > 0）**：

  - 表示相关性变化较弱或为负
  - 可能暗示价格与回报率的关系不稳定，存在套利机会
- **负向信号（alpha8 < 0）**：

  - 表示相关性变化较强或为正
  - 可能暗示价格与回报率的关系趋于稳定

## 数据需求

- `date`: 交易日期
- `asset_id`: 资产ID
- `open`: 每日开盘价
- `returns`: 每日回报率

## 输出格式

输出的 CSV 文件 (`alpha8_results.csv`) 包含以下列：

- `date`: 交易日期
- `asset_id`: 资产ID
- `open`: 当日开盘价（原始数据）
- `returns`: 当日回报率（原始数据）
- `sum_open_5`: 5天开盘价总和（中间计算值）
- `sum_returns_5`: 5天回报率总和（中间计算值）
- `open_returns_product`: `sum_open_5` 和 `sum_returns_5` 的乘积（中间计算值）
- `delayed_product`: 10天前的 `open_returns_product` 值（中间计算值）
- `product_diff`: `open_returns_product` 和 `delayed_product` 的差值（中间计算值）
- `rank_diff`: `product_diff` 在当日所有资产中的排名（中间计算值）
- `alpha8`: 计算得到的 Alpha#8 值，保留两位小数

## 注意事项与风险提示

- **数据窗口**：

  - 需要至少5天数据计算总和
  - 需要至少10天数据计算延迟差值
  - 窗口期不足时会产生 NaN 值
- **精度控制**：

  - 所有中间计算结果（除排名外）和最终 Alpha 值均保留两位小数
  - 排名方法可能影响因子表现，`alpha_calculator.py` 中使用的是 `method='average'`
- **市场环境**：

  - 价格与回报率的关系可能随市场环境变化
  - 建议结合其他因子使用
  - 需要进行充分的回测验证
- **数据质量**：

  - 确保输入数据中 `open` 和 `returns` 的质量
  - 处理异常值和缺失值
  - 注意数据更新的及时性

Alpha#8 是基于历史价格和回报率模式的统计策略，不保证未来表现。建议与其他因子结合使用，并进行充分的回测验证。

如需帮助或有建议，欢迎交流！
