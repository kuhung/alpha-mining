#!/usr/bin/env python3
"""
Alpha#1 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha1_visualization.py Alpha1Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha1Visualization.mp4 --flush_cache

   (请将 YOUR_ABSOLUTE_PATH_TO_PROJECT 替换为您项目的实际绝对路径, 例如 /Users/username/my_project)

提示:
- `-pql` : 预览并使用低质量渲染 (加快速度). 可选: `-pqm` (中等), `-pqh` (高).
- `-o YOUR_ABSOLUTE_PATH_TO_PROJECT/manim/outputs/YourSceneName.mp4`: 指定输出文件的绝对路径和名称. 这是最可靠的方法。
- `--flush_cache`: 移除缓存的片段电影文件 (Manim v0.19.0 支持).
  (注意: 这可能不会删除所有类型的中间文件，例如 TeX 日志。
   对于更彻底的清理，您可能需要检查并手动删除 `manim/scripts/media/` 目录下的内容，
   特别是 `media/tex/` 和 `media/texts/` 等子目录，在渲染过程后。)
- 查看您版本的所有可用选项: `manim render --help`
"""

from manim import *
import numpy as np
import pandas as pd
# from pathlib import Path # Path不再需要，因为输出通过命令行控制

# # ---- 自定义输出目录配置 (已移除，改用命令行参数) ----
# # 获取当前脚本文件所在的目录
# current_script_dir = Path(__file__).parent
# # 设置输出目录为 manim/outputs/
# output_dir = current_script_dir.parent / "outputs"
# output_dir.mkdir(parents=True, exist_ok=True) # 确保目录存在
# 
# config.custom_folders = True
# config.video_output_dir = str(output_dir)
# # --------------------------

# 配置中文字体
config.font = "PingFang SC"

class Alpha1Visualization(Scene):
    def construct(self):
        # 品牌标识
        brand_name = "✨仓满量化✨"
        # 使用稍小字号、深灰色、细体作为水印
        self.brand_watermark = Text(brand_name, font_size=22, color=GRAY, weight=NORMAL, font="Apple Color Emoji")
        self.brand_watermark.to_edge(UP, buff=0.7).to_edge(LEFT, buff=0.8) # 保持左侧，但垂直位置与标题对齐
        self.add(self.brand_watermark) # 将水印添加到场景中，使其持久显示

        # 参考来源
        reference_source_text = "Source: 101 Formulaic Alphas"
        self.reference_watermark = Text(reference_source_text, font_size=16, color=DARK_GRAY, weight=LIGHT) # 比品牌字号略小
        self.reference_watermark.to_corner(DL, buff=0.3) # DR 代表 DOWN + RIGHT，放置在右下角
        self.add(self.reference_watermark)

        # 标题
        title = Text("解读101个量化因子", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.add(title)
        
        # Alpha#1公式
        formula_title = Text("Alpha#1 筛选近期强势资产", font_size=36, color=GREEN)
        formula_title.move_to([0, 2, 0])  # 居中显示，y坐标设为2
        
        formula = MathTex(
            r"\text{Alpha\#1} = \text{rank}(\text{Ts\_ArgMax}(\text{SignedPower}(X, 2), 5)) - 0.5",
            font_size=32
        )
        formula.move_to([0, 0.5, 0])  # 居中显示，y坐标设为0.5
        
        condition_formula = MathTex(
            r"X = \begin{cases} \text{stddev}(\text{returns}, 20) & \text{if returns} < 0 \\ \text{close} & \text{if returns} \geq 0 \end{cases}",
            font_size=28
        )
        condition_formula.move_to([0, -1, 0])  # 居中显示，y坐标设为-1
        
        self.add(formula_title)
        self.add(formula)
        self.add(condition_formula)
        self.wait(3)
        
        # 清除屏幕
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(condition_formula))
        
        # 开始计算步骤演示
        self.show_calculation_steps()
    
    def show_calculation_steps(self):
        # 步骤标题
        steps_title = Text("计算步骤演示", font_size=42, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        # 示例数据
        data_title = Text("示例数据 (asset_1)", font_size=32, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        # 创建数据表格
        data_table = self.create_data_table()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.8)
        
        self.play(Write(data_title))
        self.play(Create(data_table))
        self.wait(2)
        
        # 清除数据表格
        self.play(FadeOut(data_table), FadeOut(data_title))
        
        # 步骤1: 条件价值计算
        self.show_step1(steps_title)
        
        # 步骤2: 符号幂计算
        self.show_step2(steps_title)
        
        # 步骤3: 时间序列最大值
        self.show_step3(steps_title)
        
        # 步骤4: 排名计算
        self.show_step4(steps_title)
        
        # 步骤5: 中心化
        self.show_step5(steps_title)
        
        # 最终结果
        self.show_final_result(steps_title)
    
    def create_data_table(self):
        # 创建表格数据
        headers = ["日期", "收盘价", "回报率"]
        data_values = [
            ["2025-01-21", "102.4", "0.0"],
            ["2025-01-22", "103.8", "0.0137"], # 此行应高亮显示
            ["2025-01-23", "101.8", "-0.0193"],
            ["2025-01-24", "101.9", "0.001"],
            ["2025-01-25", "101.3", "-0.0059"]
        ]
        
        # 为表头创建Text Mobjects
        header_mobjects = [Text(h, font_size=28, weight=BOLD) for h in headers]

        table = Table(
            data_values,
            col_labels=header_mobjects,
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": WHITE},
            # 为数据条目使用Text并设置字体大小
            element_to_mobject=Text, 
            element_to_mobject_config={"font_size": 24},
            h_buff=0.5, # 调整水平缓冲区
            v_buff=0.3  # 调整垂直缓冲区
        )
        
        # 设置表格样式：高亮第二行数据 (行索引2, 因为表头后的数据行从1开始计数)
        # 这对应于截图中 "2023-01-22" 这一行
        table.add_highlighted_cell((2,1), color=YELLOW)
        table.add_highlighted_cell((2,2), color=YELLOW)
        table.add_highlighted_cell((2,3), color=YELLOW)
        
        return table
    
    def show_step1(self, title):
        step1_title = Text("步骤1: 条件价值计算", font_size=32, color=ORANGE)
        step1_title.next_to(title, DOWN, buff=0.5)
        
        condition_text = Text(
            "如果 returns < 0: 使用 stddev(returns, 20)\n如果 returns ≥ 0: 使用 close",
            font_size=24,
            line_spacing=1.2
        )
        condition_text.next_to(step1_title, DOWN, buff=0.3)
        
        example1 = Text("2025-01-25: returns = -0.0059 < 0", font_size=20, color=RED)
        example1.next_to(condition_text, DOWN, buff=0.3)
        
        example1_result = Text("→ 使用 stddev = 0.015 (假设值)", font_size=20, color=RED)
        example1_result.next_to(example1, DOWN, buff=0.1)
        
        example2 = Text("2025-01-24: returns = 0.001 ≥ 0", font_size=20, color=GREEN)
        example2.next_to(example1_result, DOWN, buff=0.2)
        
        example2_result = Text("→ 使用 close = 101.9", font_size=20, color=GREEN)
        example2_result.next_to(example2, DOWN, buff=0.1)
        
        self.play(Write(step1_title))
        self.play(Write(condition_text))
        self.play(Write(example1))
        self.play(Write(example1_result))
        self.play(Write(example2))
        self.play(Write(example2_result))
        self.wait(3)
        
        self.play(FadeOut(step1_title), FadeOut(condition_text), 
                 FadeOut(example1), FadeOut(example1_result),
                 FadeOut(example2), FadeOut(example2_result))
    
    def show_step2(self, title):
        step2_title = Text("步骤2: 符号幂计算", font_size=32, color=ORANGE)
        step2_title.next_to(title, DOWN, buff=0.5)
        
        formula_text = MathTex(
            r"\text{SignedPower}(x, 2) = \text{sign}(x) \times |x|^2",
            font_size=28
        )
        formula_text.next_to(step2_title, DOWN, buff=0.3)
        
        example1 = Text("2025-01-25: SignedPower(0.015, 2)", font_size=20, color=RED)
        example1.next_to(formula_text, DOWN, buff=0.3)
        
        calc1 = MathTex(r"= 1 \times (0.015)^2 = 0.000225", font_size=20, color=RED)
        calc1.next_to(example1, DOWN, buff=0.1)
        
        example2 = Text("2025-01-24: SignedPower(101.9, 2)", font_size=20, color=GREEN)
        example2.next_to(calc1, DOWN, buff=0.2)
        
        calc2 = MathTex(r"= 1 \times (101.9)^2 = 10383.61", font_size=20, color=GREEN)
        calc2.next_to(example2, DOWN, buff=0.1)
        
        self.play(Write(step2_title))
        self.play(Write(formula_text))
        self.play(Write(example1))
        self.play(Write(calc1))
        self.play(Write(example2))
        self.play(Write(calc2))
        self.wait(3)
        
        self.play(FadeOut(step2_title), FadeOut(formula_text),
                 FadeOut(example1), FadeOut(calc1),
                 FadeOut(example2), FadeOut(calc2))
    
    def show_step3(self, title):
        step3_title = Text("步骤3: 时间序列最大值 (Ts_ArgMax)", font_size=32, color=ORANGE)
        step3_title.next_to(title, DOWN, buff=0.5)
        
        description = Text("找出过去5天SignedPower值中的最大值", font_size=24)
        description.next_to(step3_title, DOWN, buff=0.3)
        
        # 创建时间序列图表
        values_text = Text("过去5天的SignedPower值 (asset_1):", font_size=20)
        values_text.next_to(description, DOWN, buff=0.3)
        
        values = Text(
            "01-21: 10000 (示例)\n01-22: 10100 (示例)\n01-23: 10200 (示例)\n01-24: 10383.61\n01-25: 0.000225",
            font_size=18,
            line_spacing=1.2
        )
        values.next_to(values_text, DOWN, buff=0.2)
        
        result_text = Text("Ts_ArgMax = 10383.61 (最大值)", font_size=20, color=YELLOW)
        result_text.next_to(values, DOWN, buff=0.3)
        
        self.play(Write(step3_title))
        self.play(Write(description))
        self.play(Write(values_text))
        self.play(Write(values))
        self.play(Write(result_text))
        self.wait(3)
        
        self.play(FadeOut(step3_title), FadeOut(description),
                 FadeOut(values_text), FadeOut(values), FadeOut(result_text))
    
    def show_step4(self, title):
        step4_title = Text("步骤4: 排名计算", font_size=32, color=ORANGE)
        step4_title.next_to(title, DOWN, buff=0.5)
        
        description = Text("对所有资产的Ts_ArgMax值进行排名 (百分位)", font_size=24)
        description.next_to(step4_title, DOWN, buff=0.3)
        
        ranking_data = Text(
            "asset_1: 10383.61 → rank = 0.8\n" +
            "asset_2: 12000.0  → rank = 1.0 (示例)\n" +
            "asset_3: 10000.0  → rank = 0.2 (示例)\n" +
            "asset_4: 10100.0  → rank = 0.4 (示例)\n" +
            "asset_5: 10200.0  → rank = 0.6 (示例)",
            font_size=18,
            line_spacing=1.2
        )
        ranking_data.next_to(description, DOWN, buff=0.3)
        
        highlight = Text("asset_1的rank值: 0.8", font_size=20, color=YELLOW)
        highlight.next_to(ranking_data, DOWN, buff=0.3)
        
        self.play(Write(step4_title))
        self.play(Write(description))
        self.play(Write(ranking_data))
        self.play(Write(highlight))
        self.wait(3)
        
        self.play(FadeOut(step4_title), FadeOut(description),
                 FadeOut(ranking_data), FadeOut(highlight))
    
    def show_step5(self, title):
        step5_title = Text("步骤5: 中心化", font_size=32, color=ORANGE)
        step5_title.next_to(title, DOWN, buff=0.5)
        
        description = Text("将排名值减去0.5进行中心化", font_size=24)
        description.next_to(step5_title, DOWN, buff=0.3)
        
        calculation = MathTex(
            r"\text{Alpha\#1} = \text{rank} - 0.5 = 0.8 - 0.5 = 0.3",
            font_size=28
        )
        calculation.next_to(description, DOWN, buff=0.3)
        
        interpretation = Text(
            "正值表示高于平均水平\n负值表示低于平均水平",
            font_size=20,
            line_spacing=1.2
        )
        interpretation.next_to(calculation, DOWN, buff=0.3)
        
        self.play(Write(step5_title))
        self.play(Write(description))
        self.play(Write(calculation))
        self.play(Write(interpretation))
        self.wait(3)
        
        self.play(FadeOut(step5_title), FadeOut(description),
                 FadeOut(calculation), FadeOut(interpretation))
    
    def show_final_result(self, title):
        final_title = Text("最终结果", font_size=36, color=BLUE)
        final_title.next_to(title, DOWN, buff=0.5)
        
        result_box = Rectangle(width=8, height=3, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.3)
        
        result_text = Text(
            "asset_1 在 2025-01-25 的 Alpha#1 值: 0.3\n" +
            "这表明该资产在当日的表现\n高于所有资产的平均水平",
            font_size=20,
            line_spacing=1.2
        )
        result_text.move_to(result_box.get_center())
        
        summary = Text(
            "总结：Alpha#1 策略通过结合近期（5日）的\n"
            "动量效应和截面相对强度，筛选出那些在\n"
            "特定条件下（下跌看波动率，上涨看价格水平）\n"
            "表现出强劲信号的资产。",
            font_size=24,
            line_spacing=1.4,
            color=RED
        )
        summary.move_to(result_box.get_center())
        
        # 先显示标题和结果框
        self.play(Write(final_title))
        self.play(Create(result_box))
        self.play(Write(result_text))
        self.wait(2)
        
        # 淡出结果框，为总结腾出空间
        self.play(FadeOut(result_box), FadeOut(result_text))
        
        # 显示总结
        self.play(Write(summary))
        self.wait(4)
        
        # 结束动画
        self.play(FadeOut(title), FadeOut(final_title), FadeOut(summary))
        # self.wait(0.1) # 可以在此添加一个短暂的停顿

        # --- 新的片尾动画序列 ---
        # 1. 将左上角的水印移动到中心并放大
        # 保存原始水印的位置和样式
        original_position = self.brand_watermark.get_center()
        original_scale = self.brand_watermark.get_height() / 22  # 原始字号是22
        
        # 淡出参考来源水印
        self.play(FadeOut(self.reference_watermark))
        self.wait(0.2)  # 短暂等待
        
        # 2. 将品牌水印移动到中心并放大
        end_brand_text = self.brand_watermark  # 重用现有的水印对象
        end_brand_text.set_color(BLUE_D).set_weight(BOLD)  # 更新样式
        
        # 创建移动和缩放的动画
        self.play(
            end_brand_text.animate
            .move_to([0, 1, 0])  # 移动到中间偏上的位置
            .scale(3),  # 直接放大到合适大小
            run_time=1.0
        )
        self.wait(0.2)  # 短暂停留

        # 3. 创建并动画引导三连文本
        cta_text = Text(
            "点赞👍 关注🔔 转发🚀",
            font_size=30, # 设置合适的字号
            color=WHITE,   # 使用白色，确保可见
            font="Apple Color Emoji" # 添加字体指定
        )
        # 定位在放大的品牌文字下方
        cta_text.next_to(end_brand_text, DOWN, buff=0.8)

        self.play(Write(cta_text), run_time=1.5) # 文字书写动画
        self.wait(3) # 最后停留3秒展示
        # --- 片尾动画序列结束 ---


# 运行脚本的主函数
if __name__ == "__main__":
    # Manim通过命令行参数处理场景渲染，此处无需额外代码
    pass 