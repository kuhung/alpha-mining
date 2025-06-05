#!/usr/bin/env python3
"""
Alpha#30 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha30_visualization.py Alpha30Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha30Visualization.mp4 --flush_cache
manim -qk alpha30_visualization.py Alpha30Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha30Visualization.mp4

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

class Alpha30Visualization(Scene):
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
        
        # Alpha#30公式
        formula_title_text = "Alpha#30: 成交量加权的价格变化与收益率时序排名"
        formula_title = Text(formula_title_text, font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\begin{aligned} \text{Alpha\#30} = {}& \Big( \text{sign}(\text{close} - \text{delay}(\text{close}, 1)) \\ & + \text{sign}(\text{delay}(\text{close}, 1) - \text{delay}(\text{close}, 2)) \\ & + \text{sign}(\text{delay}(\text{close}, 2) - \text{delay}(\text{close}, 3)) \Big) \\ & \times \frac{\text{sum}(\text{volume}, 5)}{\text{sum}(\text{volume}, 20)} \end{aligned}",
            font_size=24
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "结合价格变化方向和成交量权重的综合指标",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha30(self):
        headers = ["日期", "收盘价 (C)", "成交量 (V)", "价格变化符号"]
        # Data for asset_1, 2025-01-20 calculation, from alpha30_results.csv
        # Close prices: C_16=97.7, C_17=98.0, C_18=100.1, C_19=97.9, C_20=98.8
        data_values = [
            ["2025-01-17", "98.0", "763,238", "+1"],   # sign(98.0 - 97.7)
            ["2025-01-18", "100.1", "1,487,560", "+1"], # sign(100.1 - 98.0)
            ["2025-01-19", "97.9", "2,061,421", "-1"],  # sign(97.9 - 100.1)
            ["2025-01-20", "98.8", "1,698,241", "+1"]   # sign(98.8 - 97.9) Target row
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
        steps_title = Text("计算步骤演示 (Alpha#30)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-01-11 Alpha#30)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha30()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.85)
        self.play(Create(data_table))

        # Highlight the target row (2025-01-11)
        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((5, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title))
        
        # Calculated values based on CSV data for asset_1 on 2025-01-20
        # C_20=98.8, C_19=97.9, C_18=100.1, C_17=98.0
        # V_20=1698241, V_19=2061421, V_18=1487560, V_17=763238, V_16=791336
        # sum_vol_5 = V_16+V_17+V_18+V_19+V_20 = 791336+763238+1487560+2061421+1698241 = 6801796
        # sum_vol_20 (01-01 to 01-20) = 23697712 (calculated from CSV)
        calc_results = {
            'sign_1': 1,  # sign(98.8 - 97.9)
            'sign_2': -1, # sign(97.9 - 100.1)
            'sign_3': 1,  # sign(100.1 - 98.0)
            'sign_sum': 1, # 1 + (-1) + 1
            'volume_5': 6801796,
            'volume_20': 23697712,
            'volume_ratio': 6801796 / 23697712, # approx 0.28702
            'alpha30': 1 * (6801796 / 23697712) # approx 0.28702
        }

        self.show_step1_signs(steps_title, calc_results)
        self.show_step2_volumes(steps_title, calc_results)
        self.show_step3_final_alpha(steps_title, calc_results)
        self.show_final_result_alpha30(steps_title, calc_results)

    def show_step1_signs(self, title_obj, calc_results): 
        step_title = Text("步骤1: 计算价格变化符号 (基于收盘价)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        intro_text = Text(
            "计算连续三个价格变化的符号 (C_t - C_t-1) 并求和:\n"
            "C(01/20)=98.8, C(01/19)=97.9, C(01/18)=100.1, C(01/17)=98.0",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        calculations = VGroup(
            Text(f"1. sign(C_20 - C_19) = sign(98.8 - 97.9) = {calc_results['sign_1']}", font_size=16),
            Text(f"2. sign(C_19 - C_18) = sign(97.9 - 100.1) = {calc_results['sign_2']}", font_size=16),
            Text(f"3. sign(C_18 - C_17) = sign(100.1 - 98.0) = {calc_results['sign_3']}", font_size=16),
            Text(f"4. 符号和 (sign_sum) = {calc_results['sign_1']} + ({calc_results['sign_2']}) + {calc_results['sign_3']} = {calc_results['sign_sum']}", font_size=16)
        ).arrange(DOWN, buff=0.2)
        calculations.next_to(intro_text, DOWN, buff=0.3)
        
        result = Text(f"sign_sum = {calc_results['sign_sum']}", font_size=20, color=GREEN)
        result.next_to(calculations, DOWN, buff=0.3)

        self.play(Write(intro_text))
        self.play(Write(calculations))
        self.play(Write(result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(calculations), FadeOut(result))

    def show_step2_volumes(self, title_obj, calc_results): 
        step_title = Text("步骤2: 计算成交量比率", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        intro_text = Text(
            "计算5日和20日成交量之和的比值 (截至2025-01-20)",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        calculations = VGroup(
            Text(f"1. sum(volume, 5 days) = {calc_results['volume_5']:,}", font_size=16),
            Text(f"2. sum(volume, 20 days) = {calc_results['volume_20']:,}", font_size=16),
            Text(f"3. volume_ratio = {calc_results['volume_5']:,} / {calc_results['volume_20']:,} = {calc_results['volume_ratio']:.3f}", font_size=16)
        ).arrange(DOWN, buff=0.2)
        calculations.next_to(intro_text, DOWN, buff=0.3)
        
        result = Text(f"volume_ratio = {calc_results['volume_ratio']:.3f}", font_size=20, color=GREEN)
        result.next_to(calculations, DOWN, buff=0.3)
        
        self.play(Write(step_title))
        self.play(Write(intro_text))
        self.play(Write(calculations))
        self.play(Write(result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(calculations), FadeOut(result))

    def show_step3_final_alpha(self, title_obj, calc_results):
        step_title = Text("步骤3: 计算最终 Alpha#30 值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{Alpha\#30} = \text{sign\_sum} \times \text{volume\_ratio}", 
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.3)
        
        calculation = MathTex(
            f"{calc_results['sign_sum']} \times {calc_results['volume_ratio']:.2f} = {calc_results['alpha30']:.2f}",
            font_size=24, color=YELLOW
        )
        calculation.next_to(formula_text, DOWN, buff=0.3)
        
        self.play(Write(formula_text))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(calculation))

    def show_final_result_alpha30(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=9, height=4.5, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(f"asset_1 在 2025-01-20 的 Alpha#30 (演示值): {calc_results['alpha30']:.3f}", font_size=20, weight=BOLD)
        result_text_header.move_to(result_box.get_center() + UP * 1.8) # Adjusted position

        result_text_body = Text(
            f"基于Manim脚本中演示的简化公式:\n"
            f"• 价格变化符号和 (sign_sum) = {calc_results['sign_sum']}\n"
            f"• 成交量比率 (volume_ratio) = {calc_results['volume_ratio']:.3f}\n"
            f"• Alpha#30 (演示值) = {calc_results['sign_sum']} × {calc_results['volume_ratio']:.3f} = {calc_results['alpha30']:.3f}\n"
            f"(注: CSV中该日实际Alpha#30值为0.06, 基于完整公式计算)", # Clarification
            font_size=16,
            line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)

        summary_box = Rectangle(width=10, height=5, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4) # This will overlap, will hide previous first

        summary = Text(
            "总结：Alpha#30 通过以下方式捕捉市场信号：\n"
            "1. 识别连续的价格变化方向\n"
            "2. 考虑不同时间窗口的成交量比例\n"
            "3. 结合价格趋势和成交量变化\n"
            "正的 Alpha 值表示价格上涨趋势\n"
            "得到成交量的支撑。",
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
    # manim -pqh alpha30_visualization.py Alpha30Visualization
    pass 