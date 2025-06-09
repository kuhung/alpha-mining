# Alpha 策略研究与可视化项目

本项目通过 Alpha 策略计算、大语言模型 (LLM) 及 Manim 动画引擎，实现策略研发、评估至可视化的流程。

## 核心流程

1. **数据准备**: Alpha 策略原始数据位于 `data/` (mock 数据)。
2. **策略计算与文档**: 在各 `alpha/alpha_/` 目录下，其 `README` 文件包含或引用计算逻辑，执行后生成结果与说明。
3. **LLM 交互**: 提取策略 `README` 中的核心信息，交由 LLM 生成 Manim 动画脚本。
4. **Manim 脚本存储**: LLM 生成的 `.py` 脚本保存至 `manim/scripts/`。
5. **Manim 视频渲染**: 使用 Manim 渲染脚本，如 `manim -qk manim/scripts/script_name.py SceneName`。视频保存至 `manim/outputs/`。
6. **结果整合**: 完整产出包括策略源文件、计算结果、Manim 脚本和视频，可被 `doc/` 引用。

## 环境设置

1. 克隆仓库并进入目录。
2. 创建并激活 Python 虚拟环境 (推荐 Python 3.12):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. 安装依赖：

   - 推荐使用 [uv](https://github.com/astral-sh/uv)（更快的 Python 包管理器）：
     ```bash
     pip install uv
     uv pip install -r requirements.txt
     ```
   - 或使用传统 pip（若有 `requirements.txt`）:
     ```bash
     pip install -r requirements.txt
     ```

   (否则根据需要手动安装 `manim`, `pandas`, `numpy` 等)

## 流程最佳实践

1. 在doc/目录下，选取需要实现的alpha因子
   1. 进入对话框
   2. 选取任意两个已实现的alpha因子
   3. 输入提示词
2. 生成readme文件、python文件后，执行python文件，获得数据详情
3. 选择生产的数据，输入提示词更新readme文档
4. 根据readme文档，选择已经生成的可视化脚本，输入提示词
5. 微调可视化脚本，配音乐上传

## 目录结构

* `.venv/`: Python 虚拟环境。
* `alpha/`: Alpha 策略子目录。
  * `alpha_strategy_name/README.md`: 策略描述、计算逻辑、结果。
* `data/`: **Mock 数据**。
* `doc/`: 项目文档。
* `manim/`: Manim 相关。
  * `scripts/`: Manim Python 脚本。
  * `outputs/`: Manim 输出 (视频/图片)。
* `README.md`: 本项目说明。

## 注意

* **Mock 数据**: 所有计算和演示基于 mock 数据。

欢迎使用本项目！
