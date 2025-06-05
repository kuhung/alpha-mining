#!/usr/bin/env python3
"""
Alpha#11 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha11_visualization.py Alpha11Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha11Visualization.mp4 --flush_cache
manim -qk alpha11_visualization.py Alpha11Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha11Visualization.mp4

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

class Alpha11Visualization(Scene):
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
        
        # Alpha#11公式
        formula_title_text = "Alpha#11 VWAP、收盘价差值与成交量变动的综合排名"
        formula_title = Text(formula_title_text, font_size=32, color=GREEN) # Adjusted font size
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#11} = ((\text{rank}(\text{ts\_max}((\text{vwap} - \text{close}), 3)) + \text{rank}(\text{ts\_min}((\text{vwap} - \text{close}), 3))) \times \text{rank}(\text{delta}(\text{volume}, 3)))",
            font_size=26 # Adjusted font size
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "结合价格偏离极值与成交量变动的综合排名因子",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0]) # Adjusted position
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha11(self):
        headers = ["日期", "收盘价 (C)", "VWAP", "成交量 (V)"]
        data_values = [
            ["2025-01-01", "100.00", "100.32", "690896"],
            ["2025-01-02", "100.10", "100.41", "1236310"],
            ["2025-01-03", "100.20", "100.39", "794092"],
            ["2025-01-04", "99.40", "100.42", "1279416"]  # Target row for calculation
        ]
        
        header_mobjects = [Text(h, font_size=18, weight=BOLD) for h in headers] # Adjusted font size

        table = Table(
            data_values,
            col_labels=header_mobjects,
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": WHITE},
            element_to_mobject=Text, 
            element_to_mobject_config={"font_size": 14}, # Adjusted font size
            h_buff=0.3, # Adjusted h_buff
            v_buff=0.2
        )
        return table

    def show_calculation_steps(self):
        steps_title = Text("计算步骤演示 (Alpha#11)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-01-04 Alpha#11)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha11()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.85) # Adjusted scale
        self.play(Create(data_table))

        # Highlight the target row for calculation (2025-01-04)
        # Data for 2025-01-04 is the 4th data row, mobject table row 5.
        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((5, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title))
        
        self.show_step1_vwap_close_diff(steps_title)
        self.show_step2_ts_max_min(steps_title)
        self.show_step3_delta_volume(steps_title)
        self.show_step4_ranks(steps_title)
        self.show_step5_final_alpha(steps_title)
        self.show_final_result_alpha11(steps_title)

    def show_step1_vwap_close_diff(self, title_obj): 
        step_title = Text("步骤1: 计算 vwap - close (vwap_close_diff)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(r"\text{vwap\_close\_diff}_t = \text{vwap}_t - \text{close}_t", font_size=24)
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        description = Text("计算截至 2025-01-04 的过去3日 vwap_close_diff:", font_size=20)
        description.next_to(formula_text, DOWN, buff=0.3)
        
        calcs = [
            "d(01-02) = 100.41 - 100.10 = 0.31",
            "d(01-03) = 100.39 - 100.20 = 0.19",
            "d(01-04) = 100.42 - 99.40 = 1.02 (目标日)",
        ]
        calc_text_group = VGroup(*[Text(c, font_size=18, color=GREEN, line_spacing=1.2) for c in calcs])
        calc_text_group.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        calc_text_group.next_to(description, DOWN, buff=0.2)
        
        self.play(Write(formula_text), Write(description))
        self.play(Write(calc_text_group))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description), FadeOut(calc_text_group))

    def show_step2_ts_max_min(self, title_obj): 
        step_title = Text("步骤2: 计算 ts_max 和 ts_min (窗口期=3)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        diff_series_intro = Text("使用步骤1中计算的 vwap_close_diff 序列 (for 2025-01-04):", font_size=20)
        diff_series_intro.next_to(step_title, DOWN, buff=0.4)
        diff_series_display = Text("[0.31, 0.19, 1.02]", font_size=18, color=GREEN)
        diff_series_display.next_to(diff_series_intro, DOWN, buff=0.2)

        ts_max_calc_text = MathTex(r"\text{ts\_max\_diff\_3} = \text{max}([0.31, 0.19, 1.02]) = 1.02", font_size=22)
        ts_max_calc_text.next_to(diff_series_display, DOWN, buff=0.3)
        
        ts_min_calc_text = MathTex(r"\text{ts\_min\_diff\_3} = \text{min}([0.31, 0.19, 1.02]) = 0.19", font_size=22)
        ts_min_calc_text.next_to(ts_max_calc_text, DOWN, buff=0.2)
        
        results_group = VGroup(ts_max_calc_text, ts_min_calc_text).set_color(YELLOW)

        self.play(Write(step_title))
        self.play(Write(diff_series_intro), Write(diff_series_display))
        self.play(Write(results_group))
        self.wait(4)
        
        self.play(FadeOut(step_title), FadeOut(diff_series_intro), FadeOut(diff_series_display), FadeOut(results_group))

    def show_step3_delta_volume(self, title_obj): 
        step_title = Text("步骤3: 计算 delta(volume, 3)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        formula_text = MathTex(r"\text{delta}(\text{volume}, 3)_t = \text{volume}_t - \text{volume}_{t-3}", font_size=24)
        formula_text.next_to(step_title, DOWN, buff=0.4)

        volume_data = Text(
            "Volume(2025-01-04) = 1,279,416\n"
            "Volume(2025-01-01) (3日前) = 690,896", 
            font_size=18, color=GREEN, line_spacing=1.2
        )
        volume_data.next_to(formula_text, DOWN, buff=0.3)
        
        delta_vol_calc = MathTex(r"\text{delta\_volume\_3} = 1,279,416 - 690,896 = 588,520", font_size=22, color=YELLOW)
        delta_vol_calc.next_to(volume_data, DOWN, buff=0.2)
        
        self.play(Write(step_title))
        self.play(Write(formula_text), Write(volume_data))
        self.play(Write(delta_vol_calc))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(volume_data), FadeOut(delta_vol_calc))

    def show_step4_ranks(self, title_obj): 
        step_title = Text("步骤4: 计算各项截面排名 (rank)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        rank_intro = Text(
            "对当日所有资产的 ts_max_diff_3, ts_min_diff_3, delta_volume_3 进行排名。\n"
            "排名方法为百分比排名 (0到1)，值越大排名越高 (ascending=True, pct=True)。",
            font_size=18, line_spacing=1.2
        )
        rank_intro.next_to(step_title, DOWN, buff=0.3)

        # Example intermediate values and ranks for asset_1 on 2025-01-04
        # These are from the provided alpha11_results.csv
        asset1_values = Text(
            "asset_1 (2025-01-04) 的计算值:\n"
            "ts_max_diff_3 = 1.02\n"
            "ts_min_diff_3 = 0.19\n"
            "delta_volume_3 = 588,520.00",
            font_size=16, line_spacing=1.2, color=GREEN
        )
        asset1_values.next_to(rank_intro, DOWN, buff=0.3, aligned_edge=LEFT)
        
        asset1_ranks = Text(
            "asset_1 (2025-01-04) 的示例排名:\n"
            "rank_ts_max_diff_3 = 0.80\n"
            "rank_ts_min_diff_3 = 1.00\n"
            "rank_delta_volume_3 = 1.00",
            font_size=16, line_spacing=1.2, color=YELLOW
        )
        asset1_ranks.next_to(asset1_values, RIGHT, buff=0.5, aligned_edge=UP)
        
        group = VGroup(asset1_values, asset1_ranks)

        self.play(Write(rank_intro))
        self.play(Write(group))
        self.wait(5)
        
        self.play(FadeOut(step_title), FadeOut(rank_intro), FadeOut(group))
        
    def show_step5_final_alpha(self, title_obj):
        step_title = Text("步骤5: 计算最终 Alpha#11 值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        formula_text = MathTex(
            r"\text{Alpha\#11} = (\text{rank\_ts\_max} + \text{rank\_ts\_min}) \times \text{rank\_delta\_vol}", 
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        calculation_sum = MathTex(r"\text{Sum of ranks} = 0.80 + 1.00 = 1.80", font_size=22)
        calculation_sum.next_to(formula_text, DOWN, buff=0.3)
        
        calculation_final = MathTex(r"\text{Alpha\#11} = 1.80 \times 1.00 = 1.80", font_size=24, color=GREEN)
        calculation_final.next_to(calculation_sum, DOWN, buff=0.2)
        
        self.play(Write(step_title))
        self.play(Write(formula_text))
        self.play(Write(calculation_sum))
        self.play(Write(calculation_final))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(calculation_sum), FadeOut(calculation_final))

    def show_final_result_alpha11(self, title_obj):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=8, height=4, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text("asset_1 在 2025-01-04 的 Alpha#11 值: 1.80", font_size=20, weight=BOLD)
        result_text_header.move_to(result_box.get_center() + UP * 1.3)

        result_text_body = Text(
            "解读: 该资产的VWAP与收盘价差值的短期极端表现\n"
            "(ts_max 和 ts_min 的排名之和高 = 1.80) \n"
            "与成交量的显著正向变化 (排名高 = 1.00) 相结合，\n"
            "产生了较高的Alpha值。",
            font_size=17, line_spacing=1.2 # Adjusted font size
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)
        
        summary_box = Rectangle(width=10, height=4.5, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#11 旨在捕捉那些近期价格偏离其VWAP达到极值，\n"
            "并且成交量也发生显著变化的资产。较高的Alpha值可能表明\n"
            "市场对该资产的关注度和价格波动性同时增强。具体投资含义\n"
            "需结合回测结果进行分析。该因子综合了价格短期波动的\n"
            "极端性和成交量变化的显著性。",
            font_size=18,
            line_spacing=1.3,
            color=RED
        )
        summary.move_to(summary_box.get_center())
        
        self.play(Write(final_title))
        self.play(Create(result_box))
        self.play(Write(result_text_header), Write(result_text_body))
        self.wait(5) # Increased wait time
        
        self.play(FadeOut(result_box), FadeOut(result_text_header), FadeOut(result_text_body))
        self.play(Create(summary_box))
        self.play(Write(summary))
        self.wait(7) # Increased wait time
        
        self.play(FadeOut(title_obj), FadeOut(final_title), FadeOut(summary_box), FadeOut(summary))

        # 片尾动画序列
        original_position = self.brand_watermark.get_center()
        # original_scale = self.brand_watermark.get_height() / 22 # original_scale not used directly
        
        self.play(FadeOut(self.reference_watermark))
        self.wait(0.2)
        
        end_brand_text = self.brand_watermark
        end_brand_text.set_color(BLUE_D).set_weight(BOLD)
        
        self.play(
            end_brand_text.animate.move_to([0, 1, 0]).scale(3), # Scale factor might need adjustment
            run_time=1.0
        )

        series_title = Text("101量化因子研究系列", font_size=36, color=BLUE_D, weight=BOLD)
        series_title.next_to(end_brand_text, DOWN, buff=0.5)
        self.play(Write(series_title))
        self.wait(0.2)

        cta_text = Text("点赞👍 关注🔔 转发🚀", font_size=20, color=WHITE, font="Apple Color Emoji")
        cta_text.next_to(series_title, DOWN, buff=0.8)

        self.play(Write(cta_text), run_time=1.5)
        self.wait(3)

if __name__ == "__main__":
    # This script is intended to be run with Manim.
    # To render, use a command like:
    # manim -pqh alpha11_visualization.py Alpha11Visualization
    pass 