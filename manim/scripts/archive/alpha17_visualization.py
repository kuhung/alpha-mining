#!/usr/bin/env python3
"""
Alpha#17 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha17_visualization.py Alpha17Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha17Visualization.mp4 --flush_cache
manim -qk alpha17_visualization.py Alpha17Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha17Visualization.mp4

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

class Alpha17Visualization(Scene):
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
        
        # Alpha#17公式
        formula_title_text = "Alpha#17: 价格动量、加速度与成交量的多因子组合"
        formula_title = Text(formula_title_text, font_size=28, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#17} = (((-1 \times \text{rank}(\text{ts\_rank}(\text{close}, 10))) \times \text{rank}(\text{delta}(\text{delta}(\text{close}, 1), 1))) \times \text{rank}(\text{ts\_rank}(\text{volume} / \text{adv20}, 5)))",
            font_size=24
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "结合价格趋势、加速度和成交量爆发的复合因子",
            font_size=26,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha17(self):
        headers = ["日期", "收盘价 (C)", "成交量 (V)", "adv20", "delta_close_1"]
        # Data for asset_1, 2025-01-24 calculation
        data_values = [
            ["2025-01-22", "100.80", "1,236,310", "1,389,671.40", "-"],
            ["2025-01-23", "97.70", "794,092", "1,389,671.40", "-3.10"],
            ["2025-01-24", "97.20", "3,075,917", "1,389,671.40", "-0.50"]  # Target row
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
        steps_title = Text("计算步骤演示 (Alpha#17)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-01-24 Alpha#17)", font_size=26, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha17()
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
            "注: ts_rank(close, 10) 使用 asset_1 从 2025-01-15 至 2025-01-24 的数据。",
            font_size=16, color=GRAY
        )
        note.next_to(data_table, DOWN, buff=0.3)
        self.play(Write(note))
        self.wait(2.5)

        self.play(FadeOut(data_table), FadeOut(data_title), FadeOut(note), FadeOut(highlight_cells_group))
        
        calc_results = {
            'ts_rank_close_10': 0.20,
            'rank_ts_rank_close_10': 0.50,
            'component_a': -0.50,
            'delta_close_1': -0.50,
            'delta_delta_close_1_1': 2.60,
            'rank_delta_delta_close_1_1': 1.00,
            'component_b': 1.00,
            'volume_adv20_ratio': 2.21,
            'ts_rank_vol_adv20_5': 1.00,
            'rank_ts_rank_vol_adv20_5': 1.00,
            'component_c': 1.00,
            'alpha17': -0.50
        }

        self.show_step1_component_a(steps_title, calc_results)
        self.show_step2_component_b(steps_title, calc_results)
        self.show_step3_component_c(steps_title, calc_results)
        self.show_step4_final_alpha(steps_title, calc_results)
        self.show_final_result_alpha17(steps_title, calc_results)

    def show_step1_component_a(self, title_obj, calc_results): 
        step_title = Text("步骤1: 计算 Component A (-1 * rank(ts_rank(close, 10)))", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        intro_text = Text(
            "计算收盘价在过去10天的时间序列排名，\n"
            "然后对该排名进行截面排名并取负。",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        calculation = VGroup(
            Text(f"ts_rank(close, 10) = {calc_results['ts_rank_close_10']:.2f}", font_size=18),
            Text(f"rank(ts_rank(close, 10)) = {calc_results['rank_ts_rank_close_10']:.2f}", font_size=18),
            Text(f"component_a = -1 * {calc_results['rank_ts_rank_close_10']:.2f} = {calc_results['component_a']:.2f}", 
                 font_size=18, color=GREEN)
        ).arrange(DOWN, buff=0.2)
        calculation.next_to(intro_text, DOWN, buff=0.3)
        
        self.play(Write(intro_text))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(calculation))

    def show_step2_component_b(self, title_obj, calc_results): 
        step_title = Text("步骤2: 计算 Component B (rank(delta(delta(close, 1), 1)))", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        intro_text = Text(
            "计算收盘价的二阶差分（加速度），\n"
            "然后对该加速度进行截面排名。",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        calculation = VGroup(
            Text(f"delta(close, 1) = {calc_results['delta_close_1']:.2f}", font_size=18),
            Text(f"delta(delta(close, 1), 1) = {calc_results['delta_delta_close_1_1']:.2f}", font_size=18),
            Text(f"component_b = rank(delta(delta(close, 1), 1)) = {calc_results['component_b']:.2f}", 
                 font_size=18, color=GREEN)
        ).arrange(DOWN, buff=0.2)
        calculation.next_to(intro_text, DOWN, buff=0.3)
        
        self.play(Write(step_title))
        self.play(Write(intro_text))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(calculation))

    def show_step3_component_c(self, title_obj, calc_results):
        step_title = Text("步骤3: 计算 Component C (rank(ts_rank(volume/adv20, 5)))", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        intro_text = Text(
            "计算成交量相对于20日均量的比率，\n"
            "对该比率进行5日时间序列排名，\n"
            "然后对排名进行截面排名。",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        calculation = VGroup(
            Text(f"volume/adv20 = {calc_results['volume_adv20_ratio']:.2f}", font_size=18),
            Text(f"ts_rank(volume/adv20, 5) = {calc_results['ts_rank_vol_adv20_5']:.2f}", font_size=18),
            Text(f"component_c = rank(ts_rank(volume/adv20, 5)) = {calc_results['component_c']:.2f}", 
                 font_size=18, color=GREEN)
        ).arrange(DOWN, buff=0.2)
        calculation.next_to(intro_text, DOWN, buff=0.3)
        
        self.play(Write(intro_text))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(calculation))
        
    def show_step4_final_alpha(self, title_obj, calc_results):
        step_title = Text("步骤4: 计算最终 Alpha#17 值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_recap = MathTex(r"\text{Alpha\#17} = \text{component\_a} \times \text{component\_b} \times \text{component\_c}", font_size=24)
        formula_recap.next_to(step_title, DOWN, buff=0.4)
        
        values_text = Text(
            f"component_a = {calc_results['component_a']:.2f}\n"
            f"component_b = {calc_results['component_b']:.2f}\n"
            f"component_c = {calc_results['component_c']:.2f}",
            font_size=20, line_spacing=1.2
        )
        values_text.next_to(formula_recap, DOWN, buff=0.3)
        
        calculation_final = MathTex(
            f"\\text{{Alpha\#17}} = {calc_results['component_a']:.2f} \\times {calc_results['component_b']:.2f} \\times {calc_results['component_c']:.2f} = {calc_results['alpha17']:.2f}", 
            font_size=24, color=GREEN
        )
        calculation_final.next_to(values_text, DOWN, buff=0.2)
        
        self.play(Write(formula_recap), Write(values_text))
        self.play(Write(calculation_final))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_recap), FadeOut(values_text), FadeOut(calculation_final))

    def show_final_result_alpha17(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=9, height=4.5, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(f"asset_1 在 2025-01-24 的 Alpha#17 值: {calc_results['alpha17']:.2f}", font_size=20, weight=BOLD)
        result_text_header.move_to(result_box.get_center() + UP * 1.5)

        result_text_body = Text(
            f"解读 (asset_1, 2025-01-24):\n"
            f"• 近期价格趋势相对较弱，市场排名中等 (component_a = {calc_results['component_a']:.2f})\n"
            f"• 价格加速度显著，市场排名最高 (component_b = {calc_results['component_b']:.2f})\n"
            f"• 成交量爆发强度显著，市场排名最高 (component_c = {calc_results['component_c']:.2f})\n"
            f"• Alpha 值 = {calc_results['component_a']:.2f} * {calc_results['component_b']:.2f} * {calc_results['component_c']:.2f} = {calc_results['alpha17']:.2f}",
            font_size=16,
            line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)

        summary_box = Rectangle(width=10, height=5, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#17 通过组合三个不同维度的市场信号：\n"
            "1. 价格趋势的反转信号\n"
            "2. 价格变化的加速度\n"
            "3. 成交量的爆发强度\n"
            "负的 Alpha 值表示资产可能处于价格趋势转折点，\n"
            "同时具有显著的价格加速和成交量特征。",
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
    # manim -pqh alpha17_visualization.py Alpha17Visualization
    pass 