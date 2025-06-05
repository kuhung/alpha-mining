#!/usr/bin/env python3
"""
Alpha#29 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha29_visualization.py Alpha29Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha29Visualization.mp4 --flush_cache
manim -qk alpha29_visualization.py Alpha29Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha29Visualization.mp4

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

class Alpha29Visualization(Scene):
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
        
        # Alpha#29公式
        formula_title_text = "Alpha#29: 复杂价格变换与延迟负收益时序排名的加和"
        formula_title = Text(formula_title_text, font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#29} = \text{min}(\text{product}(\text{rank}(\text{rank}(\text{scale}(\text{log}(\text{sum}(\text{ts\_min}(\text{rank}(\text{rank}(-1 \times \text{rank}(\text{delta}(\text{close} - 1, 5))))), 2), 1))))), 1), 5) \\ + \text{ts\_rank}(\text{delay}(-1 \times \text{returns}, 6), 5)",
            font_size=24
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "结合价格变化的多重变换与延迟收益率的时序排名",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha29(self):
        headers = ["日期", "收盘价 (C)", "收益率 (R)", "delta_close_5"]
        # Data for asset_1, 2025-01-11 calculation
        data_values = [
            ["2025-01-09", "98.80", "-0.0119", "-1.70"],
            ["2025-01-10", "99.20", "0.0040", "-1.30"],
            ["2025-01-11", "99.50", "0.0030", "-0.90"]  # Target row
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
        steps_title = Text("计算步骤演示 (Alpha#29)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-01-11 Alpha#29)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha29()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.85)
        self.play(Create(data_table))

        # Highlight the target row (2025-01-11)
        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((4, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title))
        
        # Store calculated values to pass between steps
        calc_results = {
            'delta_close_5': -0.90,
            'rank_delta': 0.40,
            'neg_rank_delta': -0.40,
            'rank1': 0.60,
            'rank2': 0.80,
            'ts_min_2': 0.60,
            'sum_1': 0.60,
            'log_val': -0.51,
            'scaled_val': 0.20,
            'rank3': 0.70,
            'rank4': 0.90,
            'product_1': 0.90,
            'min_5': 0.70,
            'part1': 0.70,
            'neg_returns': 0.0030,
            'delayed_returns': -0.0119,
            'ts_rank_5': 0.20,
            'part2': 0.20,
            'alpha29': 0.90
        }

        self.show_step1_part1(steps_title, calc_results)
        self.show_step2_part2(steps_title, calc_results)
        self.show_step3_final_alpha(steps_title, calc_results)
        self.show_final_result_alpha29(steps_title, calc_results)

    def show_step1_part1(self, title_obj, calc_results): 
        step_title = Text("步骤1: 计算第一部分 (价格变化的多重变换)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        intro_text = Text(
            "计算价格变化的多重变换序列，包括差分、排名、\n"
            "取负、时序最小值、对数、标准化等操作。",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        calculations = VGroup(
            Text(f"1. delta(close-1, 5) = {calc_results['delta_close_5']:.2f}", font_size=16),
            Text(f"2. rank(delta) = {calc_results['rank_delta']:.2f}", font_size=16),
            Text(f"3. -1 × rank = {calc_results['neg_rank_delta']:.2f}", font_size=16),
            Text(f"4. rank(rank) = {calc_results['rank2']:.2f}", font_size=16),
            Text(f"5. ts_min(2) = {calc_results['ts_min_2']:.2f}", font_size=16),
            Text(f"6. log(sum) = {calc_results['log_val']:.2f}", font_size=16),
            Text(f"7. scale = {calc_results['scaled_val']:.2f}", font_size=16),
            Text(f"8. min(5) = {calc_results['min_5']:.2f}", font_size=16)
        ).arrange(DOWN, buff=0.15)
        calculations.next_to(intro_text, DOWN, buff=0.3)
        
        result = Text(f"part1 = {calc_results['part1']:.2f}", font_size=20, color=GREEN)
        result.next_to(calculations, DOWN, buff=0.3)

        self.play(Write(intro_text))
        self.play(Write(calculations))
        self.play(Write(result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(calculations), FadeOut(result))

    def show_step2_part2(self, title_obj, calc_results): 
        step_title = Text("步骤2: 计算第二部分 (延迟负收益的时序排名)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        intro_text = Text(
            "计算6日前的负收益率，并进行5日时序排名",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        calculations = VGroup(
            Text(f"1. -1 × returns = {calc_results['neg_returns']:.4f}", font_size=16),
            Text(f"2. delay(6) = {calc_results['delayed_returns']:.4f}", font_size=16),
            Text(f"3. ts_rank(5) = {calc_results['ts_rank_5']:.2f}", font_size=16)
        ).arrange(DOWN, buff=0.2)
        calculations.next_to(intro_text, DOWN, buff=0.3)
        
        result = Text(f"part2 = {calc_results['part2']:.2f}", font_size=20, color=GREEN)
        result.next_to(calculations, DOWN, buff=0.3)
        
        self.play(Write(step_title))
        self.play(Write(intro_text))
        self.play(Write(calculations))
        self.play(Write(result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(calculations), FadeOut(result))

    def show_step3_final_alpha(self, title_obj, calc_results):
        step_title = Text("步骤3: 计算最终 Alpha#29 值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{Alpha\#29} = \text{part1} + \text{part2}", 
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.3)
        
        calculation = MathTex(
            f"{calc_results['part1']:.2f} + {calc_results['part2']:.2f} = {calc_results['alpha29']:.2f}",
            font_size=24, color=YELLOW
        )
        calculation.next_to(formula_text, DOWN, buff=0.3)
        
        self.play(Write(formula_text))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(calculation))

    def show_final_result_alpha29(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=9, height=4.5, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(f"asset_1 在 2025-01-11 的 Alpha#29 值: {calc_results['alpha29']:.2f}", font_size=20, weight=BOLD)
        result_text_header.move_to(result_box.get_center() + UP * 1.5)

        result_text_body = Text(
            f"解读:\n"
            f"• 价格变化多重变换部分 (part1 = {calc_results['part1']:.2f})\n"
            f"• 延迟负收益时序排名部分 (part2 = {calc_results['part2']:.2f})\n"
            f"• 两部分综合得到 Alpha 值 = {calc_results['alpha29']:.2f}",
            font_size=16,
            line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)

        summary_box = Rectangle(width=10, height=5, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#29 通过复杂的多层次计算：\n"
            "1. 捕捉价格变化的深层模式\n"
            "2. 考虑历史收益率的时序特征\n"
            "3. 结合多重非线性变换\n"
            "正的 Alpha 值表示资产在多个维度上\n"
            "展现出潜在的积极信号。",
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
    # manim -pqh alpha29_visualization.py Alpha29Visualization
    pass 