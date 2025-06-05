# Alpha#22: 相关性变化与波动率排序因子

## 描述

Alpha#22 的计算公式为：

```
Alpha#22 = -1 * (delta(correlation(high, volume, 5), 5) * rank(stddev(close, 20)))
```

该因子结合了高价与成交量的相关性变化和收盘价波动率的截面排序，旨在捕捉市场结构变化带来的交易机会。

**核心逻辑**：
1. 计算5日窗口内 high 与 volume 的相关性。
2. 计算该相关性5日变化（delta）。
3. 计算20日收盘价波动率，并在每个截面做排名。
4. 用相关性变化与波动率排名的乘积，取相反数，作为最终信号。

## 项目结构

```
alpha-mining/
├── data/
│   └── mock_data.csv
├── alpha/alpha22/
│   ├── alpha_calculator.py
│   ├── alpha22_results.csv
│   ├── README.md
│   └── cast.md
```

## 使用步骤

1. 确保已安装 pandas、numpy。
2. 数据文件 `data/mock_data.csv` 需包含 `date`, `asset_id`, `high`, `close`, `volume`。
3. 运行 `alpha/alpha22/alpha_calculator.py`，结果输出到 `alpha22_results.csv`。

```bash
cd alpha/alpha22
python alpha_calculator.py
```

## 数据需求
- `date`: 交易日期
- `asset_id`: 资产ID
- `high`: 最高价
- `close`: 收盘价
- `volume`: 成交量

## 输出格式
输出CSV包含：
- 原始数据列（如有）：`date`, `asset_id`, `open`, `high`, `low`, `close`, `volume`
- 计算列：
    - `corr_high_vol_5`：5日窗口 high 与 volume 的相关系数
    - `delta_corr_5`：5日相关性变化
    - `stddev_close_20`：20日收盘价标准差
    - `rank_stddev_close_20`：20日波动率的截面排名（百分比）
    - `alpha22`：最终信号，保留两位有效数字

| 字段名                | 含义                         | 备注           |
|-----------------------|------------------------------|----------------|
| corr_high_vol_5       | 5日窗口 high-volume 相关系数 |                |
| delta_corr_5          | 5日相关性变化                |                |
| stddev_close_20       | 20日收盘价标准差             |                |
| rank_stddev_close_20  | 20日波动率截面排名           | 0~1            |
| alpha22               | 最终信号                     | 两位有效数字   |

## 计算步骤示例

以某资产2025-01-25为例：

| date       | asset_id | high  | close | volume | corr_high_vol_5 | delta_corr_5 | stddev_close_20 | rank_stddev_close_20 | alpha22 |
|------------|----------|-------|-------|--------|-----------------|--------------|-----------------|---------------------|---------|
| 2025-01-25 | asset_1  | 101.2 | 99.8  | 12000  | 0.85            | 0.12         | 1.30            | 0.80                | -0.10   |

- `corr_high_vol_5` = 0.85
- `delta_corr_5` = 0.12
- `stddev_close_20` = 1.30
- `rank_stddev_close_20` = 0.80
- `alpha22 = -1 * (0.12 * 0.80) = -0.10`

## NaN与窗口期说明
- 需至少25天数据，前24天alpha22为NaN。
- 相关中间变量如`corr_high_vol_5`、`stddev_close_20`等，窗口不足时为NaN。
- 每个资产独立计算窗口。

## 信号解读
- alpha22>0：相关性上升且波动率高，预期回落/做空
- alpha22<0：相关性下降且波动率高，预期反弹/做多

## 注意事项
- 仅在数据缺失且无法由现有数据推导时，才修改data脚本。
- 相关性和波动率对极端值敏感，建议先行数据清洗。
- 本因子为示例，实际效果需回测验证。 