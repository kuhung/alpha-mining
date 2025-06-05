# Alpha#20: 开盘价与昨日价格关键点位差异的综合排名

## 描述

Alpha#20 的计算公式为：

```
Alpha#20: (((-1 * rank((open - delay(high, 1)))) * rank((open - delay(close, 1)))) * rank((open - delay(low, 1))))
```

这个 Alpha 策略通过比较当日开盘价 (`open`) 与昨日（`delay(..., 1)`）的最高价 (`high`)、收盘价 (`close`) 和最低价 (`low`) 的差异，并对这些差异进行排名和组合，来生成交易信号。策略包含三个主要部分：

1.  **开盘价与昨日最高价的差异**: `(-1 * rank((open - delay(high, 1))))`
    *   `open - delay(high, 1)`: 当日开盘价减去昨日最高价。如果开盘价比昨日最高价还高（向上跳空），则为正。
    *   `rank(...)`: 对这个差异进行截面排名。
    *   `-1 * rank(...)`: 对排名取负。这意味着，如果开盘价远高于昨日最高价（差异值大，排名高），则此部分贡献一个较大的负值。

2.  **开盘价与昨日收盘价的差异**: `rank((open - delay(close, 1)))`
    *   `open - delay(close, 1)`: 当日开盘价减去昨日收盘价，即隔夜跳空幅度。
    *   `rank(...)`: 对这个差异进行截面排名。正值表示向上跳空，负值表示向下跳空。

3.  **开盘价与昨日最低价的差异**: `rank((open - delay(low, 1)))`
    *   `open - delay(low, 1)`: 当日开盘价减去昨日最低价。
    *   `rank(...)`: 对这个差异进行截面排名。值越大表示开盘价相对昨日最低价越高。

## 项目结构

```
alpha-mining/
├── data/
│   ├── generate_mock_data.py  # 脚本：生成模拟金融数据 (需包含 open, high, low, close)
│   └── mock_data.csv          # 生成的模拟数据文件
├── alpha/alpha20/
│   ├── alpha_calculator.py    # 脚本：根据公式计算 Alpha#20
│   ├── alpha20_results.csv    # 计算得到的 Alpha#20 结果文件
│   ├── README.md              # 本说明文档
│   └── cast.md                # Alpha#20 策略简介
```

## 使用步骤

### 1. 环境准备

确保您的 Python 环境中安装了 `pandas` 和 `numpy` 库。如果未安装，可以通过 pip 安装：

```bash
pip install pandas numpy
```

### 2. 检查模拟数据

本 Alpha 依赖于 `open`, `high`, `low`, `close` 数据。请确保 `data/mock_data.csv` 文件存在，并且包含了这些列。

```bash
cd ../../data # 假设当前在 alpha/alpha20 目录
python generate_mock_data.py # 确保生成所需字段
cd ../alpha/alpha20
```

### 3. 计算 Alpha#20 因子

进入 `alpha/alpha20` 目录并运行 `alpha_calculator.py` 脚本：

```bash
python alpha_calculator.py
```

脚本将读取 `../../data/mock_data.csv`，计算 Alpha#20，并将结果保存到 `alpha20_results.csv`。

## Alpha#20 策略解读与计算步骤概述

1.  **计算开盘价与昨日价格的差异**:
    *   对每个资产，计算 `diff_open_prev_high = open - delay(high, 1)`
    *   对每个资产，计算 `diff_open_prev_close = open - delay(close, 1)`
    *   对每个资产，计算 `diff_open_prev_low = open - delay(low, 1)`

2.  **计算差异的截面排名**:
    *   对每个资产，计算 `rank_diff_oph = rank(diff_open_prev_high)`
    *   对每个资产，计算 `rank_diff_opc = rank(diff_open_prev_close)`
    *   对每个资产，计算 `rank_diff_opl = rank(diff_open_prev_low)`

3.  **计算最终Alpha值**:
    *   `Alpha#20 = (-1 * rank_diff_oph) * rank_diff_opc * rank_diff_opl`

## Alpha#20 策略解读与计算示例

### 数据快照 (asset_1, 2025-01-24)

根据 `alpha20_results.csv` 的实际数据，我们选取 `asset_1` 在 `2025-01-24` 的数据作为示例：

| date       | asset_id | open  | prev_high | prev_close | prev_low | diff_oph | diff_opc | diff_opl | rank_oph | rank_opc | rank_opl | alpha20 |
|------------|----------|-------|-----------|------------|----------|----------|----------|----------|----------|----------|----------|---------|
| 2025-01-24 | asset_1  | 97.20 | 98.50     | 97.80     | 97.00    | -1.30    | -0.60    | 0.20     | 0.300    | 0.400    | 0.600    | -0.072  |

### 计算步骤详解 (asset_1, 2025-01-24):

1.  **开盘价与昨日价格的差异**:
    *   `diff_open_prev_high = 97.20 - 98.50 = -1.30`
    *   `diff_open_prev_close = 97.20 - 97.80 = -0.60`
    *   `diff_open_prev_low = 97.20 - 97.00 = 0.20`

2.  **差异的截面排名**:
    *   `rank_diff_oph = 0.300` (表示在当日所有资产中排在第30%分位)
    *   `rank_diff_opc = 0.400` (表示在当日所有资产中排在第40%分位)
    *   `rank_diff_opl = 0.600` (表示在当日所有资产中排在第60%分位)

3.  **最终 Alpha#20 值**:
    *   `alpha20 = (-1 * 0.300) * 0.400 * 0.600 = -0.072`

**解读 (asset_1, 2025-01-24)**:
在 `2025-01-24` 这一天，`asset_1`：
*   开盘价低于昨日最高价（`diff_oph = -1.30`）
*   开盘价低于昨日收盘价（`diff_opc = -0.60`），表示向下跳空
*   开盘价高于昨日最低价（`diff_opl = 0.20`）
*   三个排名值分别为30%、40%和60%分位，相乘后得到一个较小的负Alpha值（-0.072）
*   这个较小的负值表明该资产在当日的开盘价格模式相对不太显著

## 数据需求

-   `date`: 交易日期 (datetime)
-   `asset_id`: 资产ID (string/object)
-   `open`: 当日开盘价 (float)
-   `high`: 当日最高价 (float) (用于计算 `delay(high,1)`)
-   `low`: 当日最低价 (float) (用于计算 `delay(low,1)`)
-   `close`: 当日收盘价 (float) (用于计算 `delay(close,1)`)
-   (脚本可能包含 `volume`, `returns` 等其他列以保持数据完整性)

## 输出格式

输出的 CSV 文件 (`alpha20_results.csv`) 将包含以下列（除了原始数据列），所有数值型 alpha 相关列均保留一定小数位数，最终 Alpha#20 保留两位有效数字：

-   `date`: 交易日期
-   `asset_id`: 资产ID
-   `open`, `high`, `low`, `close`, `volume`, `returns`: 原始数据中的对应列（如果存在）
-   `prev_high`: 昨日最高价 (`delay(high, 1)`)
-   `prev_close`: 昨日收盘价 (`delay(close, 1)`)
-   `prev_low`: 昨日最低价 (`delay(low, 1)`)
-   `diff_open_prev_high`: `open - prev_high`
-   `diff_open_prev_close`: `open - prev_close`
-   `diff_open_prev_low`: `open - prev_low`
-   `rank_diff_oph`: `rank(diff_open_prev_high)` (截面百分比排名)
-   `rank_diff_opc`: `rank(diff_open_prev_close)` (截面百分比排名)
-   `rank_diff_opl`: `rank(diff_open_prev_low)` (截面百分比排名)
-   `alpha20`: 最终计算的 Alpha#20 值

## 注意事项与风险提示

-   **数据窗口期**:
    *   所有 `delay` 操作都是 `delay(..., 1)`，因此每个资产的第一天无法计算这些延迟值。
    *   每个资产数据序列的第1行其 `alpha20` 将为 NaN。
-   **排名方法**: `pandas` 的 `rank(pct=True)` 方法用于所有截面排名，这意味着结果是百分比形式的排名。
-   **乘法组合**: 由于 Alpha 值是三个排名（其中一个取负）的乘积，其值的范围和分布可能比较特殊，需要通过回测仔细分析其特性。
-   **小数位数**: 中间步骤建议保留足够精度，最终 Alpha#20 结果将按要求格式化为两位有效数字。
-   **市场跳空行为**: 此因子高度依赖开盘价和昨日价格的关系，对市场开盘跳空行为敏感。
-   **市场适用性**: 此因子表现可能因市场环境、资产类别而异。需进行充分回测验证。
-   **数据质量**: 输入数据的准确性和完整性至关重要，特别是开盘价和前一日的各项价格数据。
-   **极端情况处理**: 当市场出现剧烈波动或异常交易时，价格跳空幅度可能较大，可能导致因子值出现极值。

Alpha#20 是一个基于开盘价相对位置的复合因子，不保证未来表现。建议与其他因子结合使用，并进行充分的回测验证。 