#!/usr/bin/env python3
"""
Alpha#18 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha18_visualization.py Alpha18Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha18Visualization.mp4 --flush_cache
manim -qk alpha18_visualization.py Alpha18Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha18Visualization.mp4

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

class Alpha18Visualization(Scene):
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
        
        # Alpha#18公式
        formula_title_text = "Alpha#18: 波动、日内趋势与开收盘价相关性的综合排名"
        formula_title = Text(formula_title_text, font_size=28, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#18} = (-1 \times \text{rank}((\text{stddev}(\text{abs}(\text{close} - \text{open}), 5) + (\text{close} - \text{open}) + \text{correlation}(\text{close}, \text{open}, 10))))",
            font_size=24
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "结合波动性、趋势和价格关系的复合因子",
            font_size=26,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha18(self):
        headers = ["日期", "开盘价 (O)", "收盘价 (C)", "abs(C-O)", "stddev_5"]
        # Data for asset_1, 2025-01-24 calculation
        data_values = [
            ["2025-01-22", "100.80", "97.70", "3.10", "-"],
            ["2025-01-23", "97.00", "97.20", "0.20", "-"],
            ["2025-01-24", "97.00", "97.20", "0.20", "1.550"]  # Target row
        ]
        
        header_mobjects = [Text(h, font_size=16, weight=BOLD) for h in headers]

        table = Table(
            data_values,
            col_labels=header_mobjects,
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": WHITE},
            element_to_mobject=Text, 
            element_to_mobject_config={"font_size": 14},
            h_buff=0.4, 
            v_buff=0.2
        )
        return table

    def show_calculation_steps(self):
        steps_title = Text("计算步骤演示 (Alpha#18)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-01-24 Alpha#18)", font_size=26, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha18()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.80)
        self.play(Create(data_table))

        # Highlight the target row (2025-01-24)
        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((4, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        
        note = Text(
            "注: correlation(close, open, 10) 使用 asset_1 从 2025-01-15 至 2025-01-24 的数据。",
            font_size=16, color=GRAY
        )
        note.next_to(data_table, DOWN, buff=0.3)
        self.play(Write(note))
        self.wait(2.5)

        self.play(FadeOut(data_table), FadeOut(data_title), FadeOut(note), FadeOut(highlight_cells_group))
        
        calc_results = {
            'abs_close_minus_open': 0.200,
            'stddev_abs_co_5': 1.550,
            'co_diff': 0.200,
            'corr_close_open_10': 0.072,
            'combined_value': 1.822,
            'rank_combined_value': 0.800,
            'alpha18': -0.800
        }

        self.show_step1_volatility(steps_title, calc_results)
        self.show_step2_trend(steps_title, calc_results)
        self.show_step3_correlation(steps_title, calc_results)
        self.show_step4_combined_value(steps_title, calc_results)
        self.show_step5_final_alpha(steps_title, calc_results)
        self.show_final_result_alpha18(steps_title, calc_results)

    def show_step1_volatility(self, title_obj, calc_results): 
        step_title = Text("步骤1: 计算波动性指标 stddev(abs(close - open), 5)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        intro_text = Text(
            "计算每日收盘价与开盘价差的绝对值，\n"
            "然后计算过去5天的标准差。",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        calculation = VGroup(
            Text(f"abs(close - open) = {calc_results['abs_close_minus_open']:.3f}", font_size=18),
            Text(f"stddev_abs_co_5 = {calc_results['stddev_abs_co_5']:.3f}", font_size=18, color=GREEN)
        ).arrange(DOWN, buff=0.2)
        calculation.next_to(intro_text, DOWN, buff=0.3)
        
        self.play(Write(intro_text))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(calculation))

    def show_step2_trend(self, title_obj, calc_results): 
        step_title = Text("步骤2: 计算日内趋势 (close - open)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        intro_text = Text(
            "计算当日收盘价与开盘价的差值，\n"
            "反映日内价格变动的方向和幅度。",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        calculation = Text(
            f"co_diff = close - open = {calc_results['co_diff']:.3f}",
            font_size=18, color=GREEN
        )
        calculation.next_to(intro_text, DOWN, buff=0.3)
        
        self.play(Write(step_title))
        self.play(Write(intro_text))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(calculation))

    def show_step3_correlation(self, title_obj, calc_results):
        step_title = Text("步骤3: 计算开收盘价相关性 correlation(close, open, 10)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        intro_text = Text(
            "计算过去10天内开盘价与收盘价的相关性，\n"
            "反映开盘价对收盘价的短期预测能力。",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        calculation = Text(
            f"corr_close_open_10 = {calc_results['corr_close_open_10']:.3f}",
            font_size=18, color=GREEN
        )
        calculation.next_to(intro_text, DOWN, buff=0.3)
        
        self.play(Write(intro_text))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(calculation))

    def show_step4_combined_value(self, title_obj, calc_results):
        step_title = Text("步骤4: 计算综合指标值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula = MathTex(
            r"\text{combined\_value} = \text{stddev\_abs\_co\_5} + \text{co\_diff} + \text{corr\_close\_open\_10}",
            font_size=24
        )
        formula.next_to(step_title, DOWN, buff=0.4)
        
        values_text = VGroup(
            Text(f"stddev_abs_co_5 = {calc_results['stddev_abs_co_5']:.3f}", font_size=18),
            Text(f"co_diff = {calc_results['co_diff']:.3f}", font_size=18),
            Text(f"corr_close_open_10 = {calc_results['corr_close_open_10']:.3f}", font_size=18)
        ).arrange(DOWN, buff=0.2)
        values_text.next_to(formula, DOWN, buff=0.3)
        
        result = Text(
            f"combined_value = {calc_results['combined_value']:.3f}",
            font_size=18, color=GREEN
        )
        result.next_to(values_text, DOWN, buff=0.3)
        
        self.play(Write(formula))
        self.play(Write(values_text))
        self.play(Write(result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula), FadeOut(values_text), FadeOut(result))
        
    def show_step5_final_alpha(self, title_obj, calc_results):
        step_title = Text("步骤5: 计算最终 Alpha#18 值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_recap = MathTex(r"\text{Alpha\#18} = -1 \times \text{rank}(\text{combined\_value})", font_size=24)
        formula_recap.next_to(step_title, DOWN, buff=0.4)
        
        values_text = Text(
            f"combined_value = {calc_results['combined_value']:.3f}\n"
            f"rank(combined_value) = {calc_results['rank_combined_value']:.3f}",
            font_size=20, line_spacing=1.2
        )
        values_text.next_to(formula_recap, DOWN, buff=0.3)
        
        calculation_final = MathTex(
            f"\\text{{Alpha\#18}} = -1 \\times {calc_results['rank_combined_value']:.3f} = {calc_results['alpha18']:.3f}", 
            font_size=24, color=GREEN
        )
        calculation_final.next_to(values_text, DOWN, buff=0.2)
        
        self.play(Write(formula_recap), Write(values_text))
        self.play(Write(calculation_final))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_recap), FadeOut(values_text), FadeOut(calculation_final))

    def show_final_result_alpha18(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=9, height=4.5, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(f"asset_1 在 2025-01-24 的 Alpha#18 值: {calc_results['alpha18']:.3f}", font_size=20, weight=BOLD)
        result_text_header.move_to(result_box.get_center() + UP * 1.5)

        result_text_body = Text(
            f"解读 (asset_1, 2025-01-24):\n"
            f"• 近期日内振幅波动性较大 (stddev_abs_co_5 = {calc_results['stddev_abs_co_5']:.3f})\n"
            f"• 当日呈现小幅上涨 (co_diff = {calc_results['co_diff']:.3f})\n"
            f"• 开收盘价几乎不相关 (corr_close_open_10 = {calc_results['corr_close_open_10']:.3f})\n"
            f"• 综合指标值在市场中排名第 {calc_results['rank_combined_value']*100:.0f}% 分位",
            font_size=16,
            line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)

        summary_box = Rectangle(width=10, height=5, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#18 通过组合三个不同维度的市场信号：\n"
            "1. 日内振幅的波动性\n"
            "2. 日内价格变动趋势\n"
            "3. 开收盘价的短期相关性\n"
            "负的 Alpha 值表示资产的综合指标值较高，\n"
            "可能预示着市场波动加剧或趋势转折。",
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
    # manim -pqh alpha18_visualization.py Alpha18Visualization
    pass 