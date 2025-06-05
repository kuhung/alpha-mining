#!/usr/bin/env python3
"""
Alpha#31 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha31_visualization.py Alpha31Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha31Visualization.mp4 --flush_cache
manim -qk alpha31_visualization.py Alpha31Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha31Visualization.mp4

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

class Alpha31Visualization(Scene):
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
        
        # Alpha#31公式
        formula_title_text = "Alpha#31 多因子组合策略"
        formula_title = Text(formula_title_text, font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\begin{aligned} \text{Alpha\#31} = {}& \text{rank}(\text{rank}(\text{rank}(\text{decay\_linear}((-1 \times \text{rank}(\text{rank}(\text{delta}(\text{close}, 10)))), 10)))) \\ & + \text{rank}((-1 \times \text{delta}(\text{close}, 3))) \\ & + \text{sign}(\text{scale}(\text{correlation}(\text{adv20}, \text{low}, 12))) \end{aligned}",
            font_size=24
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "结合市场价格趋势、短期反转和量价关系的综合因子",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha31(self):
        headers = ["日期", "收盘价 (C)", "最低价 (L)", "ADV20"]
        data_values = [
            ["2025-01-24", "101.00", "100.50", "1,359,053.75"],
            ["2025-01-25", "101.20", "100.80", "1,359,053.75"],
            ["2025-01-26", "101.50", "101.00", "1,359,053.75"]  # Target row
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
        steps_title = Text("计算步骤演示 (Alpha#31)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-01-26 Alpha#31)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha31()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.85)
        self.play(Create(data_table))

        # Highlight the target row (2025-01-26)
        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((4, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title))
        
        # Store calculated values to pass between steps
        calc_results = {
            'part_A': 0.80,
            'part_B': 0.80,
            'part_C': -1.00,
            'alpha31': 0.60
        }

        self.show_step1_part_a(steps_title, calc_results)
        self.show_step2_part_b(steps_title, calc_results)
        self.show_step3_part_c(steps_title, calc_results)
        self.show_step4_final_alpha(steps_title, calc_results)
        self.show_final_result_alpha31(steps_title, calc_results)

    def show_step1_part_a(self, title_obj, calc_results): 
        step_title = Text("步骤1: 计算趋势与动量部分 (Part A)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{Part A} = \text{rank}(\text{rank}(\text{rank}(\text{decay\_linear}((-1 \times \text{rank}(\text{rank}(\text{delta}(\text{close}, 10)))), 10))))",
            font_size=22
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        description = Text(
            "对收盘价10日变化的负向双重排名结果进行10日衰减线性加权，\n"
            "再进行三次排名，以捕捉平滑后的价格动量强度。",
            font_size=18, line_spacing=1.2
        )
        description.next_to(formula_text, DOWN, buff=0.3)
        
        result = MathTex(r"\text{Part A} = " + f"{calc_results['part_A']:.2f}", font_size=24, color=YELLOW)
        result.next_to(description, DOWN, buff=0.2)
        
        self.play(Write(formula_text), Write(description))
        self.play(Write(result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description), FadeOut(result))

    def show_step2_part_b(self, title_obj, calc_results): 
        step_title = Text("步骤2: 计算短期反转部分 (Part B)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        formula_text = MathTex(
            r"\text{Part B} = \text{rank}((-1 \times \text{delta}(\text{close}, 3)))",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        description = Text(
            "对收盘价3日变化的负值进行排名，\n"
            "以捕捉短期价格反转信号。",
            font_size=18, line_spacing=1.2
        )
        description.next_to(formula_text, DOWN, buff=0.3)
        
        result = MathTex(r"\text{Part B} = " + f"{calc_results['part_B']:.2f}", font_size=24, color=YELLOW)
        result.next_to(description, DOWN, buff=0.2)
        
        self.play(Write(step_title))
        self.play(Write(formula_text))
        self.play(Write(description))
        self.play(Write(result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description), FadeOut(result))

    def show_step3_part_c(self, title_obj, calc_results):
        step_title = Text("步骤3: 计算量价关系部分 (Part C)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{Part C} = \text{sign}(\text{scale}(\text{correlation}(\text{adv20}, \text{low}, 12)))",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        description = Text(
            "取20日平均成交量与每日最低价在12日内的时序相关性\n"
            "的截面标准化值的符号，以判断量价配合的方向。",
            font_size=18, line_spacing=1.2
        )
        description.next_to(formula_text, DOWN, buff=0.3)
        
        result = MathTex(r"\text{Part C} = " + f"{calc_results['part_C']:.2f}", font_size=24, color=YELLOW)
        result.next_to(description, DOWN, buff=0.2)
        
        self.play(Write(formula_text))
        self.play(Write(description))
        self.play(Write(result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description), FadeOut(result))
        
    def show_step4_final_alpha(self, title_obj, calc_results):
        step_title = Text("步骤4: 计算最终 Alpha#31 值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_recap = MathTex(r"\text{Alpha\#31} = \text{Part A} + \text{Part B} + \text{Part C}", font_size=24)
        formula_recap.next_to(step_title, DOWN, buff=0.4)
        
        values_text = Text(
            f"Part A = {calc_results['part_A']:.2f}\n"
            f"Part B = {calc_results['part_B']:.2f}\n"
            f"Part C = {calc_results['part_C']:.2f}",
            font_size=20, line_spacing=1.2
        )
        values_text.next_to(formula_recap, DOWN, buff=0.3)
        
        calculation_final = MathTex(
            r"\text{Alpha\#31} = " + f"{calc_results['part_A']:.2f} + {calc_results['part_B']:.2f} + ({calc_results['part_C']:.2f}) = {calc_results['alpha31']:.2f}",
            font_size=24, color=GREEN
        )
        calculation_final.next_to(values_text, DOWN, buff=0.2)
        
        self.play(Write(formula_recap), Write(values_text))
        self.play(Write(calculation_final))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_recap), FadeOut(values_text), FadeOut(calculation_final))

    def show_final_result_alpha31(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=9, height=4.5, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(f"asset_1 在 2025-01-26 的 Alpha#31 值: {calc_results['alpha31']:.2f}", font_size=20, weight=BOLD)
        result_text_header.move_to(result_box.get_center() + UP * 1.5)

        result_text_body = Text(
            f"解读: 趋势动量部分 (Part A) = {calc_results['part_A']:.2f}，表示价格动量较强。\n"
            f"短期反转部分 (Part B) = {calc_results['part_B']:.2f}，表示存在反转信号。\n"
            f"量价关系部分 (Part C) = {calc_results['part_C']:.2f}，表示量价负相关。\n"
            f"最终 Alpha 值为 {calc_results['alpha31']:.2f}，综合表现中等偏上。",
            font_size=16, line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)
        
        summary_box = Rectangle(width=10, height=5, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#31 是一个多因子组合策略，\n"
            "通过整合市场价格趋势的持续性、短期反转机会\n"
            "以及量价关系的方向，生成一个综合性的交易信号。\n"
            "该因子通过多层次的计算和组合，\n"
            "试图捕捉市场中更复杂和持久的价格模式。",
            font_size=17,
            line_spacing=1.3,
            color=RED
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

        # 片尾动画序列
        self.play(FadeOut(self.reference_watermark), run_time=0.5)
        
        end_brand_text = self.brand_watermark 
        end_brand_text.set_color(BLUE_D).set_weight(BOLD)
        
        self.play(
            end_brand_text.animate.move_to([0, 1, 0]).scale(3),
            run_time=1.0
        )

        series_title = Text("101量化因子研究系列", font_size=36, color=BLUE_D, weight=BOLD)
        series_title.next_to(self.brand_watermark, DOWN, buff=0.5)
        self.play(Write(series_title))
        self.wait(0.2)

        cta_text = Text("点赞👍 关注🔔 转发🚀", font_size=20, color=WHITE, font="Apple Color Emoji")
        cta_text.next_to(series_title, DOWN, buff=0.8)

        self.play(Write(cta_text), run_time=1.5)
        self.wait(3)

if __name__ == "__main__":
    # This script is intended to be run with Manim.
    # To render, use a command like:
    # manim -pqh alpha31_visualization.py Alpha31Visualization
    pass 