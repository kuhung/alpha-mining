# Alpha 策略研究与可视化项目

本项目通过 Alpha 策略计算、大语言模型 (LLM) 及 Manim 动画引擎，实现策略研发、评估至可视化的流程 (使用 **mock 数据**)。

## 核心流程

1. **数据准备**: Alpha 策略原始数据位于 `data/Mokita/` (mock 数据)。
2. **策略计算与文档**: 在各 `alpha/alpha_strategy_name/` 目录下，其 `README` 文件包含或引用计算逻辑，执行后生成结果与说明。
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
3. 安装依赖 (若有 `requirements.txt`):
   ```bash
   pip install -r requirements.txt
   ```

   (否则根据需要手动安装 `manim`, `pandas`, `numpy` 等)

## 目录结构

* `.venv/`: Python 虚拟环境。
* `alpha/`: Alpha 策略子目录。
  * `alpha_strategy_name/README.md`: 策略描述、计算逻辑、结果。
* `data/Mokita/`: **Mock 数据**。
* `doc/`: 项目文档。
* `manim/`: Manim 相关。
  * `scripts/`: Manim Python 脚本。
  * `outputs/`: Manim 输出 (视频/图片)。
* `README.md`: 本项目说明。

## 注意

* **Mock 数据**: 所有计算和演示基于 mock 数据。
* **LLM 集成**: LLM API 调用等需具体实现。
* **自动化**: 流程自动化程度可按需实现。
* **错误处理**: 建议添加错误处理和日志。

欢迎使用本项目！
