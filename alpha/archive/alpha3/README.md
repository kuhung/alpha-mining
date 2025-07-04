# Alpha#3 策略模拟与计算

本项目演示了如何根据给定的 Alpha#3 公式生成模拟金融数据、计算 Alpha 因子，并对结果进行分析。

## Alpha#3 公式

Alpha#3 的计算公式如下：

```
(-1 * correlation(rank(open), rank(volume), 10))
```

其中：

* `open`: 资产的日开盘价。
* `volume`: 资产的日交易量。
* `rank(series)`: 计算 `series` 中每个值在当日所有资产间的排序百分比（0到1之间）。值越大，排名越高。
* `correlation(x, y, N)`: 计算时间序列 `x` 和 `y` 在过去 `N` 天的滚动相关系数。
* `(-1 *)`: 对相关系数取负值，使得负相关变为正的Alpha信号。

## 项目结构

```
alpha3/
├── alpha_calculator.py     # 脚本：根据公式计算 Alpha#3
├── alpha3_results.csv      # 计算得到的 Alpha#3 结果文件
├── cast.md                 # 策略简要说明
└── README.md               # 本说明文档
```

## 使用步骤

### 1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。如果未安装，可以通过 pip 安装：

```bash
pip install pandas numpy
```

### 2. 数据准备

确保在 `../../data/` 目录下有 `mock_data.csv` 文件，该文件应包含以下列：
- `date`: 交易日期
- `asset_id`: 资产标识符
- `open`: 开盘价
- `volume`: 交易量

### 3. 计算 Alpha#3 因子

运行 `alpha_calculator.py` 脚本来计算 Alpha#3 因子。该脚本会读取模拟数据，执行公式中的计算，并将结果保存到 `alpha3_results.csv`。

```bash
cd alpha/alpha3
python alpha_calculator.py
```

脚本执行完毕后，会在终端打印出结果文件的前5行、后5行以及 Alpha#3 值的描述性统计信息。

## Alpha#3 策略解读

该 Alpha 策略试图捕捉开盘价排名与交易量排名之间的相关关系模式。

### 实际计算结果统计

基于模拟数据的计算结果：

- **数据规模**: 5个资产，每个资产100天数据，共500条记录
- **Alpha#3值域**: -1.0000 到 1.0000
- **平均值**: -0.0341
- **标准差**: 0.3155
- **中位数**: 0.0000
- **非零值数量**: 391个（78.2%）

### 计算步骤详解

以实际数据中的2025-01-20为例：

| date       | asset_id | open    | volume   | alpha3  |
|------------|----------|---------|----------|---------|
| 2025-01-20 | asset_1  | 99.93   | 3507861  | -0.3081 |
| 2025-01-20 | asset_2  | 116.03  | 1274534  | -0.0000 |
| 2025-01-20 | asset_3  | 103.88  | 992619   | -0.1584 |
| 2025-01-20 | asset_4  | 96.97   | 736510   | -0.4062 |
| 2025-01-20 | asset_5  | 97.57   | 551061   | -0.1301 |

#### 1. **计算开盘价排名 (`rank(open)`)**

在2025-01-20这一天，各资产开盘价排名：
- asset_2 (116.03): 排名 1.0 (最高)
- asset_3 (103.88): 排名 0.8 (第2高)  
- asset_1 (99.93): 排名 0.6 (第3高)
- asset_5 (97.57): 排名 0.4 (第4高)
- asset_4 (96.97): 排名 0.2 (最低)

#### 2. **计算交易量排名 (`rank(volume)`)**

同日各资产交易量排名：
- asset_1 (3507861): 排名 1.0 (最高)
- asset_2 (1274534): 排名 0.8 (第2高)
- asset_3 (992619): 排名 0.6 (第3高)
- asset_4 (736510): 排名 0.4 (第4高)
- asset_5 (551061): 排名 0.2 (最低)

#### 3. **观察到的相关性模式**

从实际结果可以看出：
- **asset_1**: 中等开盘价但最高交易量，Alpha#3为-0.3081，表明其历史上开盘价排名与交易量排名呈正相关
- **asset_2**: 最高开盘价和第二高交易量，Alpha#3为0.0000，表明相关性接近中性
- **asset_4**: 最低开盘价和第四高交易量，Alpha#3为-0.4062，显示较强的正相关模式

### 策略含义分析

基于实际计算结果的观察：

#### **负值Alpha#3占主导**
在我们的结果中，大部分Alpha#3值为负数，这表明：
- 开盘价排名与交易量排名之间普遍存在**正相关关系**
- 开盘价较高的股票往往也有较高的交易量
- 这可能反映了市场对高价股票的关注度和活跃交易

#### **数值分布特征**
- **接近0的值**: 约22%的观测值为0，主要出现在早期数据（缺乏足够历史数据）或相关性很弱的时期
- **极端值**: 出现-1.0和1.0的极端值，通常在数据序列早期，当历史数据较少时相关系数容易出现极值
- **稳定期**: 随着历史数据积累，Alpha#3值趋于稳定，大多分布在-0.5到0.5之间

#### **时间演化模式**
从数据中可以观察到：
1. **初始阶段** (前几天): Alpha#3值为0，因为缺乏足够的历史数据
2. **波动阶段** (第5-15天): 出现较大波动，包括极端值
3. **稳定阶段** (第15天后): Alpha#3值趋于稳定，反映更可靠的相关性模式

### 投资逻辑与应用

基于实际结果的投资含义：

#### **流动性分析**
- **负Alpha#3**: 表明价格与成交量同向变动，可能暗示正常的市场流动性
- **正Alpha#3**: 表明价格与成交量反向变动，可能暗示流动性异常或特殊市场情况

#### **市场情绪识别**
- 持续的负Alpha#3可能表明市场处于正常的风险偏好状态
- Alpha#3值的突然转正可能预示市场情绪的转变

#### **交易策略应用**
1. **趋势跟踪**: 负Alpha#3较强时，可能适合跟踪高价高量的股票
2. **反转策略**: Alpha#3转正时，可能存在反转机会
3. **风险管理**: 极端Alpha#3值可能预示异常市场条件

## 注意事项

1. **数据要求**: 该因子需要至少10天的历史数据才能计算出稳定的相关系数
2. **早期偏差**: 前10天的Alpha#3值可能不够可靠，建议关注稳定期的数据
3. **极端值处理**: 算法已自动处理无穷大值，将其设置为0
4. **市场环境**: 相关系数的稳定性依赖于市场环境的一致性，在市场结构性变化时需要重新评估

## 实际表现总结

根据模拟数据的计算结果：
- Alpha#3成功捕捉了价格-成交量关系的动态变化
- 大部分时间显示正相关模式（负Alpha#3值）
- 提供了有意义的市场微观结构信息
- 可作为量化交易策略的有效因子之一

如需帮助或有建议，欢迎交流！ 