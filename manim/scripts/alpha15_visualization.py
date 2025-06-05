#!/usr/bin/env python3
"""
Alpha#15 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha15_visualization.py Alpha15Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha15Visualization.mp4 --flush_cache
manim -qk alpha15_visualization.py Alpha15Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha15Visualization.mp4

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

class Alpha15Visualization(Scene):
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
        
        # Alpha#15公式
        formula_title_text = "Alpha#15 最高价与成交量相关性的时序聚合"
        formula_title = Text(formula_title_text, font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#15} = (-1 \times \text{sum}(\text{rank}(\text{correlation}(\text{rank}(\text{high}), \text{rank}(\text{volume}), 3)), 3))",
            font_size=28
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "捕捉最高价与成交量排名相关性的市场排名变化趋势",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha15(self):
        headers = ["日期", "最高价 (H)", "成交量 (V)", "rank(H)", "rank(V)"]
        # Data for asset_1 from 2025-01-03 to 2025-01-05 (based on README.md example)
        data_values = [
            ["2025-01-03", "100.20", "794,092", "0.60", "0.60"],
            ["2025-01-04", "99.40", "1,279,416", "0.80", "0.40"],
            ["2025-01-05", "100.50", "1,327,947", "0.60", "0.80"]  # Target row
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
        steps_title = Text("计算步骤演示 (Alpha#15)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-01-05 Alpha#15)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha15()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.85)
        self.play(Create(data_table))

        # Highlight the target row (2025-01-05)
        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((4, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title))
        
        # Store calculated values to pass between steps
        calc_results = {
            'rank_high_series': [0.60, 0.80, 0.60],
            'rank_volume_series': [0.60, 0.40, 0.80],
            'correlation_high_volume_3': -0.87,
            'rank_correlation': 1.00,
            'rank_correlation_series': [1.00, 1.00, 1.00],
            'sum_rank_correlation_3': 3.00,
            'alpha15': -3.00
        }

        self.show_step1_rank_series(steps_title, calc_results)
        self.show_step2_correlation(steps_title, calc_results)
        self.show_step3_rank_correlation(steps_title, calc_results)
        self.show_step4_sum_rank_correlation(steps_title, calc_results)
        self.show_step5_final_alpha(steps_title, calc_results)
        self.show_final_result_alpha15(steps_title, calc_results)

    def show_step1_rank_series(self, title_obj, calc_results): 
        step_title = Text("步骤1: 计算 rank(high) 和 rank(volume) 序列", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        intro_text = Text(
            "对于 asset_1, 截至 2025-01-05 的过去3日数据:\n"
            "rank(high) 和 rank(volume) 是每日所有资产间的横截面百分位排名。",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        rank_high_text = MathTex(r"\text{rank(high) series: }", str(calc_results['rank_high_series']), font_size=22)
        rank_high_text.next_to(intro_text, DOWN, buff=0.3)
        
        rank_volume_text = MathTex(r"\text{rank(volume) series: }", str(calc_results['rank_volume_series']), font_size=22)
        rank_volume_text.next_to(rank_high_text, DOWN, buff=0.2)
        
        series_group = VGroup(rank_high_text, rank_volume_text).set_color(GREEN)

        self.play(Write(intro_text))
        self.play(Write(series_group))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(series_group))

    def show_step2_correlation(self, title_obj, calc_results): 
        step_title = Text("步骤2: 计算3日相关性 correlation", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        formula_text = MathTex(
            r"\text{correlation}(\text{rank(high)}, \text{rank(volume)}, 3)", 
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        series_display_rh = Text(f"rank(high) series = {calc_results['rank_high_series']}", font_size=18)
        series_display_rv = Text(f"rank(volume) series = {calc_results['rank_volume_series']}", font_size=18)
        series_display_rh.next_to(formula_text, DOWN, buff=0.3)
        series_display_rv.next_to(series_display_rh, DOWN, buff=0.15)
        
        corr_result_text = MathTex(
            r"\text{correlation\_high\_volume\_3} = " + f"{calc_results['correlation_high_volume_3']:.2f}", 
            font_size=24, color=YELLOW
        )
        corr_result_text.next_to(series_display_rv, DOWN, buff=0.3)
        
        self.play(Write(step_title))
        self.play(Write(formula_text))
        self.play(Write(series_display_rh), Write(series_display_rv))
        self.play(Write(corr_result_text))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(series_display_rh), 
                  FadeOut(series_display_rv), FadeOut(corr_result_text))

    def show_step3_rank_correlation(self, title_obj, calc_results):
        step_title = Text("步骤3: 计算相关性的排名 rank(correlation)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        intro_text = Text(
            f"将当日 asset_1 计算得到的相关性值 {calc_results['correlation_high_volume_3']:.2f}\n"
            "与其他所有资产当日的相关性值进行横截面百分位排名。",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        rank_corr_result = MathTex(
            r"\text{rank\_correlation} = " + f"{calc_results['rank_correlation']:.2f}", 
            font_size=24, color=YELLOW
        )
        rank_corr_result.next_to(intro_text, DOWN, buff=0.3)
        
        self.play(Write(intro_text))
        self.play(Write(rank_corr_result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(rank_corr_result))

    def show_step4_sum_rank_correlation(self, title_obj, calc_results):
        step_title = Text("步骤4: 计算排名的3日求和", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        intro_text = Text(
            "计算过去3日 rank_correlation 的总和:",
            font_size=18
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        series_text = Text(
            f"rank_correlation 序列: {calc_results['rank_correlation_series']}\n"
            f"sum_rank_correlation_3 = {' + '.join([str(x) for x in calc_results['rank_correlation_series']])} = {calc_results['sum_rank_correlation_3']:.2f}",
            font_size=18, line_spacing=1.2
        )
        series_text.next_to(intro_text, DOWN, buff=0.3)
        
        self.play(Write(intro_text))
        self.play(Write(series_text))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(series_text))
        
    def show_step5_final_alpha(self, title_obj, calc_results):
        step_title = Text("步骤5: 计算最终 Alpha#15 值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_recap = MathTex(r"\text{Alpha\#15} = -1 \times \text{sum\_rank\_correlation\_3}", font_size=24)
        formula_recap.next_to(step_title, DOWN, buff=0.4)
        
        values_text = Text(f"sum_rank_correlation_3 = {calc_results['sum_rank_correlation_3']:.2f}", font_size=20)
        values_text.next_to(formula_recap, DOWN, buff=0.3)
        
        calculation_final = MathTex(
            r"\text{Alpha\#15} = -1 \times " + f"{calc_results['sum_rank_correlation_3']:.2f} = {calc_results['alpha15']:.2f}", 
            font_size=24, color=GREEN
        )
        calculation_final.next_to(values_text, DOWN, buff=0.2)
        
        self.play(Write(formula_recap), Write(values_text))
        self.play(Write(calculation_final))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_recap), FadeOut(values_text), FadeOut(calculation_final))

    def show_final_result_alpha15(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=9, height=4.5, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(f"asset_1 在 2025-01-05 的 Alpha#15 值: {calc_results['alpha15']:.2f}", font_size=20, weight=BOLD)
        result_text_header.move_to(result_box.get_center() + UP * 1.5)

        result_text_body = Text(
            f"解读: asset_1 的3日价量排名相关性为 {calc_results['correlation_high_volume_3']:.2f}。\n"
            f"此相关性在当日所有资产中排名为 {calc_results['rank_correlation']:.2f} (100%分位)。\n"
            f"过去3日排名总和为 {calc_results['sum_rank_correlation_3']:.2f}。\n"
            f"最终 Alpha 值为 {calc_results['alpha15']:.2f}，表示价量关系较强且持续。",
            font_size=16, line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)
        
        summary_box = Rectangle(width=10, height=5, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#15 通过多层次的时序和截面计算，\n"
            "捕捉资产最高价与成交量排名之间的相关性模式。\n"
            "负的 Alpha 值表示该资产的价量排名相关性\n"
            "在市场中持续处于较高水平，这种模式的持续性\n"
            "可能预示着未来价格走势的变化。",
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
    # manim -pqh alpha15_visualization.py Alpha15Visualization
    pass 