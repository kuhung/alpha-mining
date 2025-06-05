#!/usr/bin/env python3
"""
Alpha#22 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha22_visualization.py Alpha22Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha22Visualization.mp4 --flush_cache
manim -qk alpha22_visualization.py Alpha22Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha22Visualization.mp4

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

class Alpha22Visualization(Scene):
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
        
        # Alpha#22公式
        formula_title_text = "Alpha#22: 相关性变化与波动率排序因子"
        formula_title = Text(formula_title_text, font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#22} = -1 \times (\Delta\text{corr}(high, volume, 5, 5) \times \text{rank}(\text{stddev}(close, 20)))",
            font_size=24
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "捕捉高价与量相关性变化，结合波动率排序的信号",
            font_size=26,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha22(self):
        headers = ["日期", "最高价 (H)", "收盘价 (C)", "成交量 (V)", "corr_high_vol_5", "delta_corr_5", "stddev_close_20", "rank_stddev_close_20", "alpha22"]
        # 示例数据，参考README
        data_values = [
            ["2025-01-25", "101.2", "99.8", "12000", "0.85", "0.12", "1.30", "0.80", "-0.10"]
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
        steps_title = Text("计算步骤演示 (Alpha#22)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-01-25 Alpha#22)", font_size=26, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha22()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.80)
        self.play(Create(data_table))

        # 高亮目标行
        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((2, col_idx), color=YELLOW))
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title), FadeOut(highlight_cells_group))

        calc_results = {
            'corr_high_vol_5': 0.85,
            'delta_corr_5': 0.12,
            'stddev_close_20': 1.30,
            'rank_stddev_close_20': 0.80,
            'alpha22': -0.10
        }

        self.show_step1_corr(calc_results, steps_title)
        self.show_step2_std_rank(calc_results, steps_title)
        self.show_step3_final_signal(calc_results, steps_title)
        self.show_final_result_alpha22(calc_results, steps_title)

    def show_step1_corr(self, calc_results, title_obj):
        step_title = Text("步骤1: 计算5日相关性及其变化", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        intro_text = Text(
            "计算5日窗口内 high 与 volume 的相关性，再计算5日相关性变化（delta）",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        calculation = VGroup(
            Text(f"corr_high_vol_5 = {calc_results['corr_high_vol_5']:.2f}", font_size=18),
            Text(f"delta_corr_5 = {calc_results['delta_corr_5']:.2f}", font_size=18)
        ).arrange(DOWN, buff=0.2)
        calculation.next_to(intro_text, DOWN, buff=0.3)
        
        self.play(Write(intro_text))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(calculation))

    def show_step2_std_rank(self, calc_results, title_obj):
        step_title = Text("步骤2: 计算波动率及其截面排名", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        intro_text = Text(
            "计算20日收盘价标准差，并在当日所有资产中做排名（百分比）",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        calculation = VGroup(
            Text(f"stddev_close_20 = {calc_results['stddev_close_20']:.2f}", font_size=18),
            Text(f"rank_stddev_close_20 = {calc_results['rank_stddev_close_20']:.2f}", font_size=18)
        ).arrange(DOWN, buff=0.2)
        calculation.next_to(intro_text, DOWN, buff=0.3)
        
        self.play(Write(intro_text))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(calculation))

    def show_step3_final_signal(self, calc_results, title_obj):
        step_title = Text("步骤3: 得出最终信号", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_recap = MathTex(r"\text{Alpha\#22} = -1 \times (\Delta\text{corr} \times \text{rank})", font_size=24)
        formula_recap.next_to(step_title, DOWN, buff=0.4)
        
        values_text = Text(
            f"最终信号: alpha22 = {calc_results['alpha22']}",
            font_size=20, line_spacing=1.2
        )
        values_text.next_to(formula_recap, DOWN, buff=0.3)
        
        self.play(Write(formula_recap), Write(values_text))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_recap), FadeOut(values_text))

    def show_final_result_alpha22(self, calc_results, title_obj):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=9, height=3.5, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(f"asset_1 在 2025-01-25 的 Alpha#22 值: {calc_results['alpha22']}", font_size=20, weight=BOLD)
        result_text_header.move_to(result_box.get_center() + UP * 1.0)

        result_text_body = Text(
            f"解读 (asset_1, 2025-01-25):\n"
            f"• 5日相关性变化为正，波动率排名较高\n"
            f"• alpha22为负，预示短期回调或结构转折",
            font_size=16,
            line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)

        summary_box = Rectangle(width=10, height=3.5, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#22 通过捕捉价格与量能相关性的结构性变化，\n"
            "结合波动率排序，反映市场情绪突变或结构转折。",
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
    # manim -pqh alpha22_visualization.py Alpha22Visualization
    pass 