#!/usr/bin/env python3
"""
Alpha#32 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -ql alpha32_visualization.py Alpha32Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha32Visualization.mp4
manim -qk alpha32_visualization.py Alpha32Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha32Visualization.mp4

3. 合并音频
PROCESS_PATH="/Users/kuhung/roy/alpha-mining/process"
FILE_PATH="/Users/kuhung/roy/alpha-mining/manim/outputs/"
${PROCESS_PATH}/process_videos.sh ${PROCESS_PATH}/origin.mov ${FILE_PATH}/Alpha32Visualization.mp4 ${FILE_PATH}/Alpha32Visualization.png
提示:
- `-pql` : 预览并使用低质量渲染 (加快速度). 可选: `-pqm` (中等), `-pqh` (高).
- `-o YOUR_ABSOLUTE_PATH_TO_PROJECT/manim/outputs/YourSceneName.mp4`: 指定输出文件的绝对路径和名称.
- `--flush_cache`: 移除缓存的片段电影文件.
- 查看您版本的所有可用选项: `manim render --help`
"""

from manim import *
import numpy as np

# 配置中文字体
config.font = "PingFang SC"

class Alpha32Visualization(Scene):
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

        # 风险警示
        risk_warning_text = "风险提示：本视频仅供科普，不构成投资建议。"
        self.risk_warning = Text(risk_warning_text, font_size=16, color=DARK_GRAY,weight=LIGHT)
        self.risk_warning.to_corner(DR, buff=0.3)
        self.add(self.risk_warning)

        # 标题
        title = Text("解读101个量化因子", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.add(title)
        
        # Alpha#32公式
        formula_title_text = "Alpha#32 趋势跟踪与量价相关性组合策略"
        formula_title = Text(formula_title_text, font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#32} = (\text{scale}(((\text{sum}(\text{close}, 7) / 7) - \text{close})) + (20 \times \text{scale}(\text{correlation}(\text{vwap}, \text{delay}(\text{close}, 5),\\ 230))))",
            font_size=28
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "结合短期价格趋势和长期量价相关性的综合因子",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
        self.show_summary_alpha32()
        self.end_scene()
    
    def create_data_table_alpha32(self):
        headers = ["日期", "收盘价 (C)", "VWAP", "Part A", "Part B", "Alpha#32"]
        # Data for asset_1 from 2025-04-08 to 2025-04-10 (based on README.md example)
        data_values = [
            ["2025-04-08", "89.60", "88.95", "-0.64", "0.00", "-0.64"],
            ["2025-04-09", "91.10", "90.70", "-0.74", "0.00", "-0.74"],
            ["2025-04-10", "93.10", "91.76", "-0.92", "0.00", "-0.92"]  # Target row
        ]
        
        header_mobjects = [Text(h, font_size=24, weight=BOLD) for h in headers]

        table = Table(
            data_values,
            col_labels=header_mobjects,
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": WHITE},
            element_to_mobject=Text, 
            element_to_mobject_config={"font_size": 20},
            h_buff=0.5, 
            v_buff=0.25
        )
        return table

    def show_calculation_steps(self):
        steps_title = Text("计算步骤演示 (Alpha#32)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-04-10 Alpha#32)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha32()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.85)
        self.play(Create(data_table))

        # Highlight the target row (2025-04-10)
        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((4, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title))
        
        # Store calculated values to pass between steps
        calc_results = {
            'close': 93.10,
            'vwap': 91.76,
            'part_A': -0.92,
            'part_B': 0.00,
            'alpha32': -0.92
        }

        self.show_step1_part_a(steps_title, calc_results)
        self.show_step2_part_b(steps_title, calc_results)
        self.show_step3_final_alpha(steps_title, calc_results)
        self.show_final_result_alpha32(steps_title, calc_results)

    def show_step1_part_a(self, title_obj, calc_results):
        step_title = Text("步骤1: 计算短期趋势部分 (Part A)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{Part A} = \text{scale}(((\text{sum}(\text{close}, 7) / 7) - \text{close}))",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        description = Text(
            "计算过去7日收盘价均值与当前收盘价的差值，并进行截面标准化。",
            font_size=20, line_spacing=1.2
        )
        description.next_to(formula_text, DOWN, buff=0.3)
        
        # Example calculation for Part A based on sample value
        # For more detailed breakdown, actual historical data would be needed.
        result = MathTex(
            r"\text{Part A} = " + f"{calc_results['part_A']:.2f}", font_size=24, color=YELLOW
        )
        result.next_to(description, DOWN, buff=0.2)
        
        self.play(Write(formula_text), Write(description))
        self.play(Write(result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description), FadeOut(result))

    def show_step2_part_b(self, title_obj, calc_results):
        step_title = Text("步骤2: 计算长期量价相关性部分 (Part B)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{Part B} = (20 \times \text{scale}(\text{correlation}(\text{vwap}, \text{delay}(\text{close}, 5), 230)))",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        description = Text(
            "计算VWAP与5天前收盘价在230日内的时序相关性，标准化后乘以20。",
            font_size=20, line_spacing=1.2
        )
        description.next_to(formula_text, DOWN, buff=0.3)
        
        result = MathTex(
            r"\text{Part B} = " + f"{calc_results['part_B']:.2f}", font_size=24, color=YELLOW
        )
        result.next_to(description, DOWN, buff=0.2)
        
        self.play(Write(formula_text), Write(description))
        self.play(Write(result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description), FadeOut(result))
        
    def show_step3_final_alpha(self, title_obj, calc_results):
        step_title = Text("步骤3: 计算最终 Alpha#32 值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_recap = MathTex(r"\text{Alpha\#32} = \text{Part A} + \text{Part B}", font_size=24)
        formula_recap.next_to(step_title, DOWN, buff=0.4)
        
        values_text = Text(
            f"Part A = {calc_results['part_A']:.2f}\n"+
            f"Part B = {calc_results['part_B']:.2f}",
            font_size=24
        )
        values_text.next_to(formula_recap, DOWN, buff=0.3)
        
        calculation_final = MathTex(
            r"\text{Alpha\#32} = " + f"{calc_results['part_A']:.2f} + {calc_results['part_B']:.2f} = {calc_results['alpha32']:.2f}",
            font_size=24, color=GREEN
        )
        calculation_final.next_to(values_text, DOWN, buff=0.2)
        
        self.play(Write(formula_recap), Write(values_text))
        self.play(Write(calculation_final))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_recap), FadeOut(values_text), FadeOut(calculation_final))

    def show_final_result_alpha32(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=9, height=4.5, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(
            f"asset_1 在 2025-04-10 的 Alpha#32 值: {calc_results['alpha32']:.2f}", font_size=20, weight=BOLD
        )
        result_text_header.move_to(result_box.get_center() + UP * 1.5)

        result_text_body = Text(
            f"短期趋势部分 (Part A) = {calc_results['part_A']:.2f}。\n" +
            f"长期量价相关性部分 (Part B) = {calc_results['part_B']:.2f} (此示例中可能为0)。\n" +
            f"最终 Alpha 值为 {calc_results['alpha32']:.2f}，综合判断短期趋势和长期量价关系。",
            font_size=20, line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)
        
        summary_box = Rectangle(width=11, height=4, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "解读：Alpha#32 综合利用短期价格均值偏离和长期量价相关性，\n"+
            "旨在捕捉市场中不同时间维度的信号。该因子结合了趋势跟踪和\n"+
            "量价关系的考量，以期提供更稳健的交易信号。",
            font_size=24,
            line_spacing=1.3,
            color=WHITE
        )
        summary.move_to(summary_box.get_center())
        
        self.play(Write(final_title))
        self.play(Create(result_box))
        self.play(Write(result_text_header), Write(result_text_body))
        self.wait(4) 
        
        self.play(FadeOut(result_box), FadeOut(result_text_header), FadeOut(result_text_body))
        self.play(Create(summary_box))
        self.play(Write(summary))
        self.wait(5)
        
        self.play(FadeOut(title_obj), FadeOut(final_title), FadeOut(summary_box), FadeOut(summary))

    def show_summary_alpha32(self):
        title = Text("策略总结 (Alpha#32)", font_size=36, color=BLUE)
        title.to_edge(UP, buff=1)
        self.play(Write(title))
        
        summary_box = RoundedRectangle(width=9, height=5, corner_radius=0.5, fill_color=BLUE_E, fill_opacity=0.1, stroke_color=BLUE).next_to(title, DOWN, buff=0.5)
        
        summary_points = VGroup(
            Text("✓ 结合短期趋势和长期量价关系", font_size=22, color=GREEN),
            Text("✓ 旨在捕捉多维度市场信号", font_size=22, color=WHITE),
            Text("✗ 因子组合复杂性可能导致解释性下降", font_size=22, color=RED),
            Text("✗ 数据质量和参数选择对因子表现影响大", font_size=22, color=RED),
            Text("★ 需进行充分回测和验证", font_size=24, color=YELLOW),
            Text("★ 可与其他因子结合使用以增强稳健性", font_size=22, color=YELLOW)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(summary_box)
        
        self.play(FadeIn(summary_box))
        self.play(Write(summary_points))
        self.wait(5)
        
        self.play(
            FadeOut(title), FadeOut(summary_box), FadeOut(summary_points)
        )

    def end_scene(self):
        self.play(FadeOut(self.reference_watermark), FadeOut(self.risk_warning), run_time=0.5)
        
        end_brand_text = self.brand_watermark 
        end_brand_text.set_color(BLUE_D).set_weight(BOLD)
        
        self.play(
            end_brand_text.animate.move_to([0, 1, 0]).scale(3),
            run_time=1.0
        )

        series_title = Text("101量化因子研究系列", font_size=36, color=BLUE_D, weight=BOLD)
        series_title.next_to(end_brand_text, DOWN, buff=0.5)
        self.play(Write(series_title))
        
        cta_text = Text("点赞👍 关注🔔 转发🚀", font_size=24, color=WHITE, font="Apple Color Emoji")
        cta_text.next_to(series_title, DOWN, buff=0.5)

        self.play(FadeIn(cta_text, shift=UP), run_time=1.5)
        self.wait(2)
        
        self.play(
            FadeOut(end_brand_text), FadeOut(series_title), FadeOut(cta_text)
        )

if __name__ == "__main__":
    # This script is intended to be run with Manim.
    # To render, use a command like:
    # manim -pqh alpha32_visualization.py Alpha32Visualization
    pass 