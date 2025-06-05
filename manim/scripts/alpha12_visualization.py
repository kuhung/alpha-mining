#!/usr/bin/env python3
"""
Alpha#12 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha12_visualization.py Alpha12Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha12Visualization.mp4 --flush_cache
manim -qk alpha12_visualization.py Alpha12Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha12Visualization.mp4 --flush_cache

提示:
- `-pql` : 预览并使用低质量渲染 (加快速度). 可选: `-pqm` (中等), `-pqh` (高).
- `-o YOUR_ABSOLUTE_PATH_TO_PROJECT/manim/outputs/YourSceneName.mp4`: 指定输出文件的绝对路径和名称.
- `--flush_cache`: 移除缓存的片段电影文件.
- 查看您版本的所有可用选项: `manim render --help`
"""

from manim import *
import numpy as np
import pandas as pd

# 配置中文字体
config.font = "PingFang SC"

class Alpha12Visualization(Scene):
    def construct(self):
        # 品牌标识
        brand_name = "✨仓满量化✨"
        self.brand_watermark = Text(brand_name, font_size=22, color=GRAY, weight=NORMAL, font="Apple Color Emoji")
        self.brand_watermark.to_edge(UP, buff=0.7).to_edge(LEFT, buff=0.8)
        self.add(self.brand_watermark)

        # 参考来源
        reference_source_text = "Source: 101 Formulaic Alphas"
        self.reference_watermark = Text(reference_source_text, font_size=16, color=DARK_GRAY, weight=LIGHT)
        self.reference_watermark.to_corner(DL, buff=0.3)
        self.add(self.reference_watermark)

        # 标题
        title = Text("解读101个量化因子", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.add(title)
        
        # Alpha#12公式
        formula_title_text = "Alpha#12 成交量变动方向与价格反转因子"
        formula_title = Text(formula_title_text, font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#12} = \text{sign}(\text{delta}(\text{volume}, 1)) \times (-1 \times \text{delta}(\text{close}, 1))",
            font_size=28
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "结合成交量变动方向和价格反向变动的因子",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha12(self):
        headers = ["日期", "收盘价 (C)", "成交量 (V)"]
        data_values = [
            ["2025-01-03", "100.20", "794,092"],
            ["2025-01-04", "99.40", "1,279,416"]  # Target row for calculation
        ]
        
        header_mobjects = [Text(h, font_size=18, weight=BOLD) for h in headers]

        table = Table(
            data_values,
            col_labels=header_mobjects,
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": WHITE},
            element_to_mobject=Text, 
            element_to_mobject_config={"font_size": 16},
            h_buff=0.5, 
            v_buff=0.25
        )
        return table

    def show_calculation_steps(self):
        steps_title = Text("计算步骤演示 (Alpha#12)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-01-04 Alpha#12)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha12()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.85)
        self.play(Create(data_table))

        # Highlight the target row (2025-01-04), which is the 2nd data row, mobject table row 3.
        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((3, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title))
        
        # Store calculated values to pass between steps if needed
        calc_results = {}

        self.show_step1_delta_close(steps_title, calc_results)
        self.show_step2_delta_volume(steps_title, calc_results)
        self.show_step3_sign_delta_volume(steps_title, calc_results)
        self.show_step4_neg_delta_close(steps_title, calc_results)
        self.show_step5_final_alpha(steps_title, calc_results)
        self.show_final_result_alpha12(steps_title, calc_results)

    def show_step1_delta_close(self, title_obj, calc_results): 
        step_title = Text("步骤1: 计算 delta(close, 1)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(r"\text{delta}(\text{close}, 1)_t = \text{close}_t - \text{close}_{t-1}", font_size=24)
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        description = Text("计算 2025-01-04 的价格变动:", font_size=20)
        description.next_to(formula_text, DOWN, buff=0.3)
        
        calculation = Text(
            "delta_close_1 = close(2025-01-04) - close(2025-01-03)\n"
            "delta_close_1 = 99.40 - 100.20 = -0.80",
            font_size=18, color=GREEN, line_spacing=1.2
        )
        calculation.next_to(description, DOWN, buff=0.2)
        
        calc_results['delta_close_1'] = -0.80

        self.play(Write(formula_text), Write(description))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description), FadeOut(calculation))

    def show_step2_delta_volume(self, title_obj, calc_results): 
        step_title = Text("步骤2: 计算 delta(volume, 1)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(r"\text{delta}(\text{volume}, 1)_t = \text{volume}_t - \text{volume}_{t-1}", font_size=24)
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        description = Text("计算 2025-01-04 的成交量变动:", font_size=20)
        description.next_to(formula_text, DOWN, buff=0.3)
        
        calculation = Text(
            "delta_volume_1 = volume(2025-01-04) - volume(2025-01-03)\n"
            "delta_volume_1 = 1,279,416 - 794,092 = 485,324",
            font_size=18, color=GREEN, line_spacing=1.2
        )
        calculation.next_to(description, DOWN, buff=0.2)
        
        calc_results['delta_volume_1'] = 485324

        self.play(Write(formula_text), Write(description))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description), FadeOut(calculation))

    def show_step3_sign_delta_volume(self, title_obj, calc_results):
        step_title = Text("步骤3: 计算 sign(delta(volume, 1))", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(r"\text{sign}(x) = \begin{cases} 1 & x > 0 \\ 0 & x = 0 \\ -1 & x < 0 \end{cases}", font_size=24)
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        description = Text(f"delta_volume_1 = {calc_results['delta_volume_1']}", font_size=20)
        description.next_to(formula_text, DOWN, buff=0.3)
        
        calculation = MathTex(r"\text{sign}(485,324) = 1", font_size=24, color=YELLOW)
        calculation.next_to(description, DOWN, buff=0.2)
        
        calc_results['sign_delta_volume_1'] = 1

        self.play(Write(formula_text), Write(description))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description), FadeOut(calculation))

    def show_step4_neg_delta_close(self, title_obj, calc_results):
        step_title = Text("步骤4: 计算 -1 * delta(close, 1)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))
        
        description = Text(f"delta_close_1 = {calc_results['delta_close_1']}", font_size=20)
        description.next_to(step_title, DOWN, buff=0.4)
        
        calculation = MathTex(r"-1 \times (-0.80) = 0.80", font_size=24, color=YELLOW)
        calculation.next_to(description, DOWN, buff=0.2)
        
        calc_results['neg_delta_close_1'] = 0.80

        self.play(Write(description))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(description), FadeOut(calculation))
        
    def show_step5_final_alpha(self, title_obj, calc_results):
        step_title = Text("步骤5: 计算最终 Alpha#12 值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_recap = MathTex(
            r"\text{Alpha\#12} = \text{sign}(\text{delta\_volume\_1}) \times (-1 \times \text{delta\_close\_1})", 
            font_size=24
        )
        formula_recap.next_to(step_title, DOWN, buff=0.4)
        
        values_text = Text(
            f"sign_delta_volume_1 = {calc_results['sign_delta_volume_1']}\n"
            f"neg_delta_close_1 = {calc_results['neg_delta_close_1']}",
            font_size=20, line_spacing=1.2
        )
        values_text.next_to(formula_recap, DOWN, buff=0.3)
        
        calculation_final = MathTex(r"\text{Alpha\#12} = 1 \times 0.80 = 0.80", font_size=24, color=GREEN)
        calculation_final.next_to(values_text, DOWN, buff=0.2)
        
        calc_results['alpha12'] = 0.80

        self.play(Write(formula_recap), Write(values_text))
        self.play(Write(calculation_final))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_recap), FadeOut(values_text), FadeOut(calculation_final))

    def show_final_result_alpha12(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=8, height=4.5, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(f"asset_1 在 2025-01-04 的 Alpha#12 值: {calc_results['alpha12']:.2f}", font_size=20, weight=BOLD)
        result_text_header.move_to(result_box.get_center() + UP * 1.5)

        result_text_body = Text(
            f"解读: 当日成交量较昨日增加 (delta_volume = {calc_results['delta_volume_1']}),\n"
            f"sign(delta_volume) = {calc_results['sign_delta_volume_1']:.0f} (放量)。\n"
            f"当日收盘价较昨日下跌 (delta_close = {calc_results['delta_close_1']:.2f})。\n"
            f"因子值为正 ({calc_results['alpha12']:.2f})，表示看涨，预期价格反转上涨。",
            font_size=17, line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)
        
        summary_box = Rectangle(width=10, height=5, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#12 捕捉成交量变化方向与价格反转信号。\n"
            "放量上涨 => 看跌; 放量下跌 => 看涨。\n"
            "缩量上涨 => 看涨; 缩量下跌 => 看跌。\n"
            "核心思想是成交量放大预示当前趋势衰竭和价格反转，\n"
            "而缩量情况下的因子逻辑也指向价格反转。",
            font_size=18,
            line_spacing=1.3,
            color=RED
        )
        summary.move_to(summary_box.get_center())
        
        self.play(Write(final_title))
        self.play(Create(result_box))
        self.play(Write(result_text_header), Write(result_text_body))
        self.wait(6) 
        
        self.play(FadeOut(result_box), FadeOut(result_text_header), FadeOut(result_text_body))
        self.play(Create(summary_box))
        self.play(Write(summary))
        self.wait(7)
        
        self.play(FadeOut(title_obj), FadeOut(final_title), FadeOut(summary_box), FadeOut(summary))

        # 片尾动画序列
        self.play(FadeOut(self.reference_watermark), run_time=0.5)
        
        end_brand_text = self.brand_watermark 
        end_brand_text.set_color(BLUE_D).set_weight(BOLD)
        
        self.play(
            end_brand_text.animate.move_to([0, 1, 0]).scale(3),
            run_time=1.0
        )

        series_title = Text("101量化因子研究系列", font_size=36, color=BLUE_D, weight=BOLD)
        series_title.next_to(self.brand_watermark, DOWN, buff=0.5) # Use self.brand_watermark which is now animated
        self.play(Write(series_title))
        self.wait(0.2)

        cta_text = Text("点赞👍 关注🔔 转发🚀", font_size=20, color=WHITE, font="Apple Color Emoji")
        cta_text.next_to(series_title, DOWN, buff=0.8)

        self.play(Write(cta_text), run_time=1.5)
        self.wait(3)

if __name__ == "__main__":
    # This script is intended to be run with Manim.
    # To render, use a command like:
    # manim -pqh alpha12_visualization.py Alpha12Visualization
    pass
