# Alpha#24: 价格变化率与历史最小值的条件选择策略

## 描述

Alpha#24 的计算公式为：

```
((((delta((sum(close, 100) / 100), 100) / delay(close, 100)) < 0.05) ||
((delta((sum(close, 100) / 100), 100) / delay(close, 100)) == 0.05)) ? (-1 * (close - ts_min(close,
100))) : (-1 * delta(close, 3)))
```

该 Alpha 策略包含两个主要部分：

1. **条件判断部分**:
   * `delta((sum(close, 100) / 100), 100) / delay(close, 100)`: 计算100日移动平均的变化率
   * `< 0.05 || == 0.05`: 判断变化率是否小于等于5%

2. **信号生成部分**:
   * 当变化率≤5%时：`-1 * (close - ts_min(close, 100))` (当前价格与100日最低价之差的负值)
   * 当变化率>5%时：`-1 * delta(close, 3)` (3日价格差分的负值)

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha24/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#24
│   ├── alpha24_results.csv    # 计算得到的 Alpha#24 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#24 策略总结
```

## 使用步骤

### 1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。如果未安装，可以通过 pip 安装：

```bash
pip install pandas numpy
```

### 2. 数据准备

本 Alpha 策略依赖于 `close` 数据。请确保 `../../data/mock_data.csv` 文件存在并包含以下必要字段：
- `date`: 交易日期
- `asset_id`: 资产标识
- `close`: 收盘价

### 3. 计算 Alpha#24 因子

进入 `alpha/alpha24` 目录并运行 `alpha_calculator.py` 脚本：

```bash
cd alpha/alpha24
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#24，并将结果保存到当前目录下的 `alpha24_results.csv`。同时会在终端打印部分结果和统计信息。

## Alpha#24 策略解读与计算示例

以下示例使用 `alpha24_results.csv` 中的实际数据来展示计算过程。我们以 `asset_5` 在 `2025-02-02` 的数据为例：

**背景数据**:
- 日期: `2025-02-02`
- 资产ID: `asset_5`
- 当日收盘价 (`close`): `115.6`
- 3日价格差分 (`delta_close_3`): `9.6`
- 最终Alpha值 (`alpha24`): `-9.6`

**计算步骤**:

1. **计算100日移动平均的变化率**:
   * 由于数据量不足100天，我们暂时无法计算这个值
   * 在实际应用中，这个值用于判断市场环境

2. **条件判断**:
   * 在数据量不足的情况下，默认使用3日差分策略
   * 即 `-1 * delta(close, 3)`

3. **计算3日价格差分**:
   * `delta_close_3 = close_today - close_3_days_ago`
   * `delta_close_3 = 115.6 - 106.0 = 9.6`

4. **生成Alpha信号**:
   * 计算 `-1 * delta_close_3`
   * `alpha24 = -1 * 9.6 = -9.6`

这个示例展示了一个典型的信号生成过程：
- 在3日内价格大幅上涨（`delta_close_3`为正且较大）
- 生成了一个较大的负向信号（`-9.6`）
- 这表明策略预期价格可能会回落

## 数据需求

- `date`: 交易日期 (YYYY-MM-DD)
- `asset_id`: 资产ID
- `close`: 每日收盘价

## 输出格式

输出的 CSV 文件 (`alpha24_results.csv`) 包含以下列：

- `date`: 交易日期
- `asset_id`: 资产ID
- `close`: 当日收盘价（原始数据）
- `ma_100`: 100日移动平均（中间计算值，保留四位小数）
- `delta_ma_100`: 100日移动平均的变化值（中间计算值）
- `change_rate`: 变化率（中间计算值）
- `min_close_100`: 100日最低价（中间计算值）
- `delta_close_3`: 3日价格差分（中间计算值）
- `alpha24`: 计算得到的 Alpha#24 值，保留两位有效数字

## 注意事项与风险提示

1. **数据窗口要求**:
   - 需要至少100天的历史数据来计算移动平均和最低价
   - 需要至少3天的历史数据来计算差分
   - 每个资产序列的前99个Alpha值将为NaN

2. **信号特点**:
   - 根据市场环境自动切换策略
   - 在低波动环境下关注价格与历史最低点的距离
   - 在高波动环境下关注短期价格变化

3. **潜在风险**:
   - 在市场环境转换点可能产生错误信号
   - 对历史数据依赖性较强
   - 需要较长的数据积累期

4. **实践建议**:
   - 可以调整变化率阈值（5%）以适应不同市场
   - 考虑添加其他市场环境判断指标
   - 建议进行充分的回测验证 