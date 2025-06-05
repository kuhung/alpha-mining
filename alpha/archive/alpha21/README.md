# Alpha#21: 均值与波动率条件反转因子

## 描述

Alpha#21 的计算公式为：

```
Alpha#21 = ((((sum(close, 8) / 8) + stddev(close, 8)) < (sum(close, 2) / 2)) ? (-1) : (((sum(close, 2) / 2) < ((sum(close, 8) / 8) - stddev(close, 8))) ? 1 : (((1 < (volume / adv20)) || ((volume / adv20) == 1)) ? 1 : -1)))
```

该因子通过均值、波动率和成交量的多重条件，捕捉价格短期反转与量能驱动信号。

**核心逻辑**：
1. 计算8日均价 `sum(close, 8) / 8` 和8日波动率 `stddev(close, 8)`。
2. 计算2日均价 `sum(close, 2) / 2`。
3. 若"8日均价+8日波动率"小于2日均价，给出-1信号（短期价格偏高，预期回落）。
4. 若2日均价小于"8日均价-8日波动率"，给出+1信号（短期价格偏低，预期反弹）。
5. 否则，若成交量大于等于20日均量，给出+1信号（量能驱动上涨）；否则给出-1信号。

## 项目结构

```
alpha-mining/
├── data/
│   └── mock_data.csv
├── alpha/alpha21/
│   ├── alpha_calculator.py
│   ├── alpha21_results.csv
│   ├── README.md
│   └── cast.md
```

## 使用步骤

1. 确保已安装 pandas、numpy。
2. 数据文件 `data/mock_data.csv` 需包含 `date`, `asset_id`, `close`, `volume`。
3. 运行 `alpha/alpha21/alpha_calculator.py`，结果输出到 `alpha21_results.csv`。

```bash
cd alpha/alpha21
python alpha_calculator.py
```

## 数据需求
- `date`: 交易日期
- `asset_id`: 资产ID
- `close`: 收盘价
- `volume`: 成交量

## 输出格式
输出CSV包含：
- 原始数据列（如有）：`date`, `asset_id`, `open`, `high`, `low`, `close`, `volume`
- 计算列：
    - `close_mean_8`：8日均价
    - `close_std_8`：8日收盘价标准差
    - `close_mean_2`：2日均价
    - `adv20`：20日均量
    - `volume_over_adv20`：成交量/20日均量
    - `cond1`：条件1（8日均价+8日波动率 < 2日均价）
    - `cond2`：条件2（2日均价 < 8日均价-8日波动率）
    - `cond3`：条件3（成交量大于等于20日均量）
    - `alpha21`：最终信号，取值为1或-1，保留两位有效数字

| 字段名              | 含义                         | 备注           |
|---------------------|------------------------------|----------------|
| close_mean_8        | 8日均价                      |                |
| close_std_8         | 8日收盘价标准差              |                |
| close_mean_2        | 2日均价                      |                |
| adv20               | 20日均量                     |                |
| volume_over_adv20   | 成交量/20日均量              |                |
| cond1               | 条件1                        | 布尔值         |
| cond2               | 条件2                        | 布尔值         |
| cond3               | 条件3                        | 布尔值         |
| alpha21             | 最终信号                     | 1或-1，两位有效数字 |

## 计算步骤示例

以某资产2025-01-21为例：

| date       | asset_id | close | volume | close_mean_8 | close_std_8 | close_mean_2 | adv20 | volume_over_adv20 | cond1 | cond2 | cond3 | alpha21 |
|------------|----------|-------|--------|--------------|-------------|--------------|-------|-------------------|-------|-------|-------|---------|
| 2025-01-21 | asset_1  | 98.20 | 12000  | 97.50        | 1.20        | 98.00        | 11000 | 1.09              | False | True  | True  | 1       |

- `close_mean_8` = 97.50
- `close_std_8` = 1.20
- `close_mean_2` = 98.00
- `adv20` = 11000
- `volume_over_adv20` = 1.09
- `cond1` = False
- `cond2` = True
- `cond3` = True
- 满足cond2，alpha21=1

## NaN与窗口期说明
- 需至少20天数据，前19天alpha21为NaN。
- 相关中间变量如`close_mean_8`、`adv20`等，窗口不足时为NaN。
- 每个资产独立计算窗口。

## 信号解读
- alpha21=1：短期价格偏低或量能放大，预期反弹/上涨
- alpha21=-1：短期价格偏高或量能不足，预期回落/下跌

## 注意事项
- 仅在数据缺失且无法由现有数据推导时，才修改data脚本。
- 量价数据异常会影响因子表现，建议先行数据清洗。
- 本因子为示例，实际效果需回测验证。 