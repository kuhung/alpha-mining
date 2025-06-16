# Alpha#35: 交易量与价格综合因子

## 因子定义

```
((Ts_Rank(volume, 32) * (1 - Ts_Rank(((close + high) - low), 16))) * (1 - Ts_Rank(returns, 32)))
```

## 计算逻辑

Alpha#35 是一个结合了交易量、价格波动和回报率时间序列排名的综合因子。其旨在捕捉市场中由这些基本指标共同驱动的潜在机会。

1. **`Ts_Rank(volume, 32)`**: 计算过去32天交易量的时间序列排名。较高的排名表示近期交易量相对较大，可能反映市场活跃度。
2. **`Ts_Rank(((close + high) - low), 16)`**: 计算过去16天 `(收盘价 + 最高价 - 最低价)` 这个价格项的时间序列排名。这个价格项可以看作是衡量每日价格动量和波动范围的指标。`1 - Ts_Rank(...)` 意味着当该价格项的排名较低时（例如，价格动量或波动相对较小），对Alpha值贡献越大。
3. **`Ts_Rank(returns, 32)`**: 计算过去32天每日回报率的时间序列排名。`1 - Ts_Rank(...)` 意味着当回报率的排名较低时（例如，近期回报率相对较差），对Alpha值贡献越大，可能暗示某种反转或超跌机会。

最终的 Alpha#35 值通过将这三个组件（经过适当的转换和排名）相乘得到。该因子倾向于在交易量较大、价格动量或波动相对较小、且近期回报率相对较低的市场条件下产生较高的值。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据 (确保包含 close, high, low, volume, returns 字段)
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha35/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#35
│   ├── alpha35_results.csv    # 计算得到的 Alpha#35 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#35 策略简介
```

## 使用步骤

### 1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。如果未安装，可以通过 pip 安装：

```bash
pip install pandas numpy
```

### 2. 检查模拟数据

本 Alpha 依赖于 `close`, `high`, `low`, `volume`, `returns` 数据。请确保 `data/mock_data.csv` 文件存在，并且包含了所有必需的列。如果文件不存在或数据不完整，请运行或修改 `data/generate_mock_data.py` 脚本。

```bash
# 检查或生成数据 (如果需要)
cd ../../data # 假设当前在 alpha/alpha35 目录
python generate_mock_data.py # 假设此脚本能生成所需字段
cd ../alpha/alpha35
```

### 3. 计算 Alpha#35 因子

进入 `alpha/alpha35` 目录并运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#35，并将结果保存到当前目录下的 `alpha35_results.csv`。

## 数据输入

* `volume`: 每日成交量。
* `close`: 每日收盘价。
* `high`: 每日最高价。
* `low`: 每日最低价。
* `returns`: 每日收盘价到收盘价的回报。

这些数据预计从 `../../data/mock_data.csv` 文件中获取。

## 输出格式

输出的 CSV 文件 (`alpha35_results.csv`) 将包含所有原始数据列以及计算得到的 `Alpha#35` 值。所有数值型 Alpha 相关列均保留两位小数。

## 因子数值范围

`Alpha#35` 的理论数值区间为 `[0, 1]`。

这主要归因于 `ts_rank` 函数的实现。在 `alpha_calculator.py` 中，`ts_rank` 函数返回的是时间序列在指定窗口内的百分位排名，其值域被归一化到 `[0, 1]` 之间。

* `Ts_Rank(volume, 32)`: 返回 `[0, 1]` 范围内的值。
* `1 - Ts_Rank(((close + high) - low), 16)`: `Ts_Rank` 返回 `[0, 1]`，因此 `1 - Ts_Rank` 也返回 `[0, 1]`。
* `1 - Ts_Rank(returns, 32)`: `Ts_Rank` 返回 `[0, 1]`，因此 `1 - Ts_Rank` 也返回 `[0, 1]`。

最终的 `Alpha#35` 是这三个 `[0, 1]` 范围内的值的乘积，因此其结果也自然落在 `[0, 1]` 的区间内。

## 策略解读与计算示例

为了更好地理解Alpha#35的计算逻辑和数值特性，我们假设在某个交易日，对于某个资产，各分量的时间序列排名（归一化至[0,1]区间）如下：

* `Ts_Rank(volume, 32)` = 0.80 (表示当前交易量在过去32天中相对较高)
* `Ts_Rank(((close + high) - low), 16)` = 0.20 (表示价格动量/波动在过去16天中相对较低)
* `Ts_Rank(returns, 32)` = 0.10 (表示回报率在过去32天中相对较低)

根据公式：
`Alpha#35 = (Ts_Rank(volume, 32) * (1 - Ts_Rank(((close + high) - low), 16))) * (1 - Ts_Rank(returns, 32))`

代入假设值进行计算：

* `1 - Ts_Rank(((close + high) - low), 16)` = `1 - 0.20 = 0.80`
* `1 - Ts_Rank(returns, 32)` = `1 - 0.10 = 0.90`

因此：
`Alpha#35 = 0.80 * 0.80 * 0.90 = 0.64 * 0.90 = 0.576`

四舍五入到两位小数后，结果为 `0.58`。

这个例子说明，当交易量排名较高，同时价格动量和回报率排名较低时，Alpha#35 因子将产生较高的值，这符合因子旨在捕捉特定市场模式的预期。

## 注意事项与风险提示

* **NaN 值**: 如果输入数据缺失，相应的 Alpha 值将为 NaN。请确保数据完整性。
* **时间序列排名**: `Ts_Rank` 函数的计算基于过去指定天数的数据。在数据序列的开头，由于历史数据不足，可能会出现 NaN 值。
* **小数位数**: 最终的 Alpha#35 值按要求保留两位小数。
* **市场适用性**: 此因子在不同市场环境或资产类别上表现可能迥异。务必进行充分的回测和验证。
* **数据质量**: 输入数据的准确性和完整性至关重要。

Alpha#35 因子不保证未来表现。建议与其他因子结合使用，并进行充分的回测验证。
