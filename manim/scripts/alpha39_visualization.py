#!/usr/bin/env python3
"""
Alpha#39 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -ql alpha39_visualization.py Alpha39Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha39Visualization.mp4
manim -qk alpha39_visualization.py Alpha39Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha39Visualization.mp4

3. 合并音频
PROCESS_PATH="/Users/kuhung/roy/alpha-mining/process"
FILE_PATH="/Users/kuhung/roy/alpha-mining/manim/outputs/"
${PROCESS_PATH}/process_videos.sh ${PROCESS_PATH}/origin.mov ${FILE_PATH}/Alpha39Visualization.mp4 ${FILE_PATH}/Alpha39Visualization.png
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

class Alpha39Visualization(Scene):
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
        
        # Alpha#39公式
        formula_title_text = "Alpha#39 复合因子策略"
        formula_title = Text(formula_title_text, font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"(-1 \times \text{rank}((\text{delta}(\text{close}, 7) \times (1 - \text{rank}(\text{decay\_linear}((\text{volume} / \text{adv20}), 9)))))) \times (1 + \text{rank}(\text{sum}(\text{returns}, 250)))",
            font_size=24
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "识别价格变化强劲但不受异常成交量过度影响，并由强劲长期正收益放大的股票",
            font_size=24,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(5)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps_alpha39()
        self.show_summary_alpha39()
        self.end_scene()
    
    def create_data_table_alpha39(self):
        headers = ["日期", "资产ID", "收盘价 (C)", "成交量 (V)", "收益 (R)"]
        # Data for asset_1 from 2025-02-05
        data_values = [
            ["2025-02-05", "asset_1", "82.40", "985290", "-0.01"],
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

    def show_calculation_steps_alpha39(self):
        steps_title = Text("计算步骤演示 (Alpha#39)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例输入数据 (asset_1, 2025-02-05)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha39()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.8)
        self.play(Create(data_table))

        # Highlight the target row
        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((2, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title)) 
        
        # Store calculated values for asset_1 from 2025-02-05
        calc_results = {
            'momentum_volume_component': -1.60,
            'neg_ranked_momentum_volume_component': -0.20,
            'one_plus_ranked_sum_returns': 1.20,
            'alpha39': -0.24
        }

        self.show_step_component(steps_title, "动量与成交量复合因子", r"\text{delta(C,7)} \times (1 - \text{rank}(\text{...}))", calc_results['momentum_volume_component'], "基于: delta(C,7), V/adv20 等")
        self.show_step_component(steps_title, "反转后的动量排名", r"-1 \times \text{rank}(\text{momentum\_volume\_component})", calc_results['neg_ranked_momentum_volume_component'], "基于: 动量与成交量复合因子")
        self.show_step_component(steps_title, "长期收益因子", r"1 + \text{rank}(\text{sum(R,250)})", calc_results['one_plus_ranked_sum_returns'], "基于: sum(R,250)")
        
        self.show_final_multiplication(steps_title, calc_results)
        self.show_final_result_alpha39(steps_title, calc_results)

    def show_step_component(self, title_obj, step_name, formula_str, calc_value, dependency_text_str):
        step_title = Text(f"步骤: 计算 {step_name}", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula = MathTex(formula_str, font_size=22)
        formula.next_to(step_title, DOWN, buff=0.4)
        
        dependency_text = Text(dependency_text_str, font_size=20, color=GRAY)
        dependency_text.next_to(formula, DOWN, buff=0.2)

        calc = MathTex(f"= {calc_value:.2f}", font_size=24, color=YELLOW)
        calc.next_to(dependency_text, DOWN, buff=0.2)

        self.play(Write(formula), Write(dependency_text), Write(calc))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula), FadeOut(dependency_text), FadeOut(calc))

    def show_final_multiplication(self, title_obj, calc_results):
        step_title = Text("最终步骤: 相乘得到 Alpha#39", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_multiply = MathTex(
            r"\text{Alpha\#39} = \text{momentum factor} \times \text{return factor}",
            font_size=22
        )
        formula_multiply.next_to(step_title, DOWN, buff=0.4)
        
        multiply_calc = MathTex(
            f"= {calc_results['neg_ranked_momentum_volume_component']:.2f} \times {calc_results['one_plus_ranked_sum_returns']:.2f} = {calc_results['alpha39']:.2f}",
            font_size=24, color=GREEN
        )
        multiply_calc.next_to(formula_multiply, DOWN, buff=0.2)
        
        self.play(Write(formula_multiply))
        self.play(Write(multiply_calc))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_multiply), FadeOut(multiply_calc))

    def show_final_result_alpha39(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=9.5, height=4, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(
            f"asset_1 在 2025-02-05 的 Alpha#39 值: {calc_results['alpha39']:.2f}", font_size=20, weight=BOLD
        )
        result_text_header.move_to(result_box.get_center() + UP * 1.5)

        result_text_body = Text(
            f"动量与成交量复合因子 = {calc_results['momentum_volume_component']:.2f}\n"
            f"反转后的动量排名 = {calc_results['neg_ranked_momentum_volume_component']:.2f}\n"
            f"长期收益因子 = {calc_results['one_plus_ranked_sum_returns']:.2f}\n"
            f"最终 Alpha = {calc_results['neg_ranked_momentum_volume_component']:.2f} × {calc_results['one_plus_ranked_sum_returns']:.2f} = {calc_results['alpha39']:.2f}",
            font_size=18, line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)
        
        self.play(Write(final_title))
        self.play(Create(result_box))
        self.play(Write(result_text_header), Write(result_text_body))
        self.wait(4) 
        
        self.play(FadeOut(result_box), FadeOut(result_text_header), FadeOut(result_text_body))
        
        summary_box = Rectangle(width=11, height=4, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "解读：Alpha#39 旨在识别价格变化强劲但不受异常成交量过度影响，\n"+
            "并由强劲长期正收益放大的股票。\n"+
            "通过结合动量与成交量调整，以及长期收益持续性，\n"+
            "寻找高质量的趋势跟踪或反转机会。",
            font_size=24,
            line_spacing=1.3,
            color=WHITE
        )
        summary.move_to(summary_box.get_center())

        self.play(Create(summary_box))
        self.play(Write(summary))
        self.wait(5)
        
        self.play(FadeOut(title_obj), FadeOut(final_title), FadeOut(summary_box), FadeOut(summary))

    def show_summary_alpha39(self):
        title = Text("策略总结 (Alpha#39)", font_size=36, color=BLUE)
        title.to_edge(UP, buff=1)
        self.play(Write(title))
        
        summary_box = RoundedRectangle(width=9, height=5, corner_radius=0.5, fill_color=BLUE_E, fill_opacity=0.1, stroke_color=BLUE).next_to(title, DOWN, buff=0.5)
        
        summary_points = VGroup(
            Text("✓ 识别价格变化强劲但不受异常成交量过度影响的股票", font_size=22, color=GREEN),
            Text("✓ 结合短期动量、成交量分析和长期收益持续性", font_size=22, color=WHITE),
            Text("✗ 对数据质量和时间序列长度有要求", font_size=22, color=RED),
            Text("✗ 对市场环境变化敏感", font_size=22, color=RED),
            Text("★ 需进行充分回测和验证", font_size=24, color=YELLOW),
            Text("★ 适用于寻找高质量的趋势跟踪或反转机会", font_size=22, color=YELLOW)
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
    # manim -pqh alpha39_visualization.py Alpha39Visualization
    pass 