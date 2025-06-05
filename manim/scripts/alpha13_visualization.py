#!/usr/bin/env python3
"""
Alpha#13 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha13_visualization.py Alpha13Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha13Visualization.mp4 --flush_cache
manim -qk alpha13_visualization.py Alpha13Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha13Visualization.mp4

提示:
- `-pql` : 预览并使用低质量渲染 (加快速度). 可选: `-pqm` (中等), `-pqh` (高).
- `-o YOUR_ABSOLUTE_PATH_TO_PROJECT/manim/outputs/YourSceneName.mp4`: 指定输出文件的绝对路径和名称.
- `--flush_cache`: 移除缓存的片段电影文件.
- 查看您版本的所有可用选项: `manim render --help`
"""

from manim import *
import numpy as np
# import pandas as pd # Not strictly needed for this script's logic, data is hardcoded

# 配置中文字体
config.font = "PingFang SC"

class Alpha13Visualization(Scene):
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
        
        # Alpha#13公式
        formula_title_text = "Alpha#13 价量排名协方差反转因子"
        formula_title = Text(formula_title_text, font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#13} = -1 \times \text{rank}(\text{covariance}(\text{rank}(\text{close}), \text{rank}(\text{volume}), 5))",
            font_size=28
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "寻找价量排名协方差在市场中不突出的股票",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha13(self):
        headers = ["日期", "Close", "Volume", "rank(Close)", "rank(Volume)"]
        # Data for asset_1 from 2025-01-01 to 2025-01-05
        data_values = [
            ["2025-01-01", "100.0", "690,896", "0.6", "0.4"],
            ["2025-01-02", "100.1", "1,236,310", "0.8", "1.0"],
            ["2025-01-03", "100.2", "794,092", "0.8", "0.6"],
            ["2025-01-04", "99.4", "1,279,416", "0.8", "0.4"],
            ["2025-01-05", "100.5", "1,327,947", "0.8", "0.8"] # Target row
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
        steps_title = Text("计算步骤演示 (Alpha#13)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-01-05 Alpha#13)", font_size=26, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha13()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.80)
        self.play(Create(data_table))

        # Highlight the target row (2025-01-05), which is the 5th data row, mobject table row 6.
        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((6, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title))
        
        # Store calculated values to pass between steps if needed
        calc_results = {
            'rank_close_series': [0.6, 0.8, 0.8, 0.8, 0.8],
            'rank_volume_series': [0.4, 1.0, 0.6, 0.4, 0.8],
            'cov_rank_close_rank_volume_5': 0.012, # From alpha13_results.csv
            'rank_cov': 0.6, # From alpha13_results.csv
            'alpha13': -0.6 # From alpha13_results.csv
        }

        self.show_step1_input_ranks(steps_title, calc_results)
        self.show_step2_covariance(steps_title, calc_results)
        self.show_step3_rank_covariance(steps_title, calc_results)
        self.show_step4_final_alpha(steps_title, calc_results)
        self.show_final_result_alpha13(steps_title, calc_results)

    def show_step1_input_ranks(self, title_obj, calc_results): 
        step_title = Text("步骤1: 获取 rank(close) 和 rank(volume) 序列 (5日)", font_size=26, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        intro_text = Text(
            "对于 asset_1, 截至 2025-01-05 的过去5日数据:\n"
            "rank(close) 和 rank(volume) 是每日所有资产间的横截面百分位排名。",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        rank_close_text = MathTex(r"\text{rank(close) series: }", str(calc_results['rank_close_series']), font_size=22)
        rank_close_text.next_to(intro_text, DOWN, buff=0.3)
        
        rank_volume_text = MathTex(r"\text{rank(volume) series: }", str(calc_results['rank_volume_series']), font_size=22)
        rank_volume_text.next_to(rank_close_text, DOWN, buff=0.2)
        
        series_group = VGroup(rank_close_text, rank_volume_text).set_color(GREEN)

        self.play(Write(intro_text))
        self.play(Write(series_group))
        self.wait(4)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(series_group))

    def show_step2_covariance(self, title_obj, calc_results): 
        step_title = Text("步骤2: 计算5日协方差 covariance", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        formula_text = MathTex(
            r"\text{cov} = \text{covariance}(\text{rank(close\_series)}, \text{rank(volume\_series)}, 5)", 
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        series_display_rc = Text(f"rank(close) series = {calc_results['rank_close_series']}", font_size=18)
        series_display_rv = Text(f"rank(volume) series = {calc_results['rank_volume_series']}", font_size=18)
        series_display_rc.next_to(formula_text, DOWN, buff=0.3, aligned_edge=LEFT)
        series_display_rv.next_to(series_display_rc, DOWN, buff=0.15, aligned_edge=LEFT)
        
        cov_result_text = MathTex(
            r"\text{cov\_rank\_close\_rank\_volume\_5} = " + f"{calc_results['cov_rank_close_rank_volume_5']:.3f}", 
            font_size=24, color=YELLOW
        )
        cov_result_text.next_to(series_display_rv, DOWN, buff=0.3)
        
        self.play(Write(step_title))
        self.play(Write(formula_text))
        self.play(Write(series_display_rc), Write(series_display_rv))
        self.play(Write(cov_result_text))
        self.wait(4)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(series_display_rc), 
                  FadeOut(series_display_rv), FadeOut(cov_result_text))

    def show_step3_rank_covariance(self, title_obj, calc_results):
        step_title = Text("步骤3: 计算协方差的排名 rank(covariance)", font_size=26, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        intro_text = Text(
            f"将当日 asset_1 计算得到的 cov = {calc_results['cov_rank_close_rank_volume_5']:.3f}\n"
            "与其他所有资产当日的协方差值进行横截面百分位排名。",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        rank_cov_result = MathTex(
            r"\text{rank\_cov} = " + f"{calc_results['rank_cov']:.1f}", 
            font_size=24, color=YELLOW
        )
        rank_cov_result.next_to(intro_text, DOWN, buff=0.3)
        
        self.play(Write(intro_text))
        self.play(Write(rank_cov_result))
        self.wait(4)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(rank_cov_result))
        
    def show_step4_final_alpha(self, title_obj, calc_results):
        step_title = Text("步骤4: 计算最终 Alpha#13 值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_recap = MathTex(r"\text{Alpha\#13} = -1 \times \text{rank\_cov}", font_size=24)
        formula_recap.next_to(step_title, DOWN, buff=0.4)
        
        values_text = Text(f"rank_cov = {calc_results['rank_cov']:.1f}", font_size=20)
        values_text.next_to(formula_recap, DOWN, buff=0.3)
        
        calculation_final = MathTex(
            r"\text{Alpha\#13} = -1 \times " + f"{calc_results['rank_cov']:.1f} = {calc_results['alpha13']:.1f}", 
            font_size=24, color=GREEN
        )
        calculation_final.next_to(values_text, DOWN, buff=0.2)
        
        self.play(Write(formula_recap), Write(values_text))
        self.play(Write(calculation_final))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_recap), FadeOut(values_text), FadeOut(calculation_final))

    def show_final_result_alpha13(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=9, height=4.5, color=BLUE, fill_opacity=0.1) # Adjusted size
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(f"asset_1 在 2025-01-05 的 Alpha#13 值: {calc_results['alpha13']:.1f}", font_size=20, weight=BOLD)
        result_text_header.move_to(result_box.get_center() + UP * 1.5)

        result_text_body = Text(
            f"解读: asset_1 的5日价量排名协方差为 {calc_results['cov_rank_close_rank_volume_5']:.3f}。\n"
            f"此协方差在当日所有资产中排名为 {calc_results['rank_cov']:.1f} (60%分位)。\n"
            f"最终 Alpha 值为 -1 * {calc_results['rank_cov']:.1f} = {calc_results['alpha13']:.1f}。\n"
            "该因子倾向于选择价量关系在市场中排名不突出的股票。",
            font_size=16, line_spacing=1.2 # Adjusted font size
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)
        
        summary_box = Rectangle(width=10, height=5, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#13 衡量价量排名的5日协方差，\n"
            "并对该协方差进行排名后取反。\n"
            "它关注的是价量关系（协方差）在横截面上的相对位置。\n"
            "因子值较高（接近0）表示原始协方差排名较低，\n"
            "即价量配合不显著或呈负相关，且这种关系在市场中不突出。",
            font_size=17, # Adjusted font size
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
    # manim -pqh alpha13_visualization.py Alpha13Visualization
    pass 