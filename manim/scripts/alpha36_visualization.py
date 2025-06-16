#!/usr/bin/env python3
"""
Alpha#36 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -ql alpha36_visualization.py Alpha36Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha36Visualization.mp4
manim -qk alpha36_visualization.py Alpha36Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha36Visualization.mp4

3. 合并音频
PROCESS_PATH="/Users/kuhung/roy/alpha-mining/process"
FILE_PATH="/Users/kuhung/roy/alpha-mining/manim/outputs/"
${PROCESS_PATH}/process_videos.sh ${PROCESS_PATH}/origin.mov ${FILE_PATH}/Alpha36Visualization.mp4 ${FILE_PATH}/Alpha36Visualization.png
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

class Alpha36Visualization(Scene):
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
        
        # Alpha#36公式
        formula_title_text = "Alpha#36 多因子动量与价值策略"
        formula_title = Text(formula_title_text, font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#36} &= ((((2.21 \times \text{rank}(\text{corr}((\text{close} - \text{open}), \text{delay}(\text{volume}, 1), 15))) \\",
            r"&\quad + (0.7 \times \text{rank}((\text{open} - \text{close}))) \\",
            r"&\quad + (0.73 \times \text{rank}(\text{Ts\_Rank}(\text{delay}(-1 \times \text{returns}, 6), 5)))) \\",
            r"&\quad + \text{rank}(\text{abs}(\text{corr}(\text{vwap}, \text{adv20}, 6))) \\",
            r"&\quad + (0.6 \times \text{rank}(((\text{MA}_{200}(\text{close}) - \text{open}) \times (\text{close} - \text{open}))))))",
            font_size=24
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "结合价格动量、成交量、价值和波动性的综合因子",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
        self.show_summary_alpha36()
        self.end_scene()
    
    def create_data_table_alpha36(self):
        headers = ["分量", "原始值", "截面排名", "权重", "最终贡献"]
        # Data from README.md example
        data_values = [
            ["term1 (日内动量-成交量)", "0.50", "0.50", "2.21", "1.11"],
            ["term2 (日内反转)", "0.30", "0.30", "0.70", "0.21"],
            ["term3 (历史回报)", "0.70", "0.70", "0.73", "0.51"],
            ["term4 (VWAP-ADV20)", "0.80", "0.80", "1.00", "0.80"],
            ["term5 (价值-动量)", "0.60", "0.60", "0.60", "0.36"]
        ]
        
        header_mobjects = [Text(h, font_size=24, weight=BOLD) for h in headers]

        table = Table(
            data_values,
            col_labels=header_mobjects,
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": WHITE},
            element_to_mobject=Text, 
            element_to_mobject_config={"font_size": 20},
            h_buff=0.3, 
            v_buff=0.25
        )
        return table

    def show_calculation_steps(self):
        steps_title = Text("计算步骤演示 (Alpha#36)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (假设某交易日各项计算结果)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha36()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.75)
        self.play(Create(data_table))

        # Highlight data rows
        highlight_cells_group = VGroup()
        for row_idx in range(1, 6): # Rows for data values
            for col_idx in range(1, len(data_table.col_labels) + 1):
                highlight_cells_group.add(data_table.get_highlighted_cell((row_idx + 1, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title))
        
        # Store calculated values from README example
        calc_results = {
            'term1_raw': 0.50,
            'term1_weighted': 1.105,
            'term2_raw': 0.30,
            'term2_weighted': 0.21,
            'term3_raw': 0.70,
            'term3_weighted': 0.511,
            'term4_raw': 0.80,
            'term4_weighted': 0.80,
            'term5_raw': 0.60,
            'term5_weighted': 0.36,
            'alpha36_raw': 2.986,
            'alpha36_rounded': 2.99
        }

        self.show_step1_volume_price(steps_title, calc_results)
        self.show_step2_price_reversal(steps_title, calc_results)
        self.show_step3_returns_rank(steps_title, calc_results)
        self.show_step4_vwap_correlation(steps_title, calc_results)
        self.show_step5_value_momentum(steps_title, calc_results)
        self.show_final_result_alpha36(steps_title, calc_results)

    def show_step1_volume_price(self, title_obj, calc_results):
        step_title = Text("步骤1: 日内动量与成交量相关性", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{term1} = 2.21 \times \text{rank}(\text{corr}((\text{close} - \text{open}), \text{delay}(\text{volume}, 1), 15))",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        description = Text(
            "计算日内价格变动与昨日成交量的15天相关性，\n"
            "进行截面排名后乘以2.21的权重。",
            font_size=20, line_spacing=1.2
        )
        description.next_to(formula_text, DOWN, buff=0.3)

        result = MathTex(
            r"\text{term1} = 2.21 \times " + f"{calc_results['term1_raw']:.2f} = {calc_results['term1_weighted']:.3f}",
            font_size=24, color=YELLOW
        )
        result.next_to(description, DOWN, buff=0.2)
        
        self.play(Write(formula_text), Write(description))
        self.play(Write(result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description), FadeOut(result))

    def show_step2_price_reversal(self, title_obj, calc_results):
        step_title = Text("步骤2: 日内价格反转信号", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{term2} = 0.7 \times \text{rank}((\text{open} - \text{close}))",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        description = Text(
            "计算开盘价与收盘价的差值，进行截面排名后乘以0.7的权重。\n"
            "用于捕捉日内价格反转信号。",
            font_size=20, line_spacing=1.2
        )
        description.next_to(formula_text, DOWN, buff=0.3)

        result = MathTex(
            r"\text{term2} = 0.7 \times " + f"{calc_results['term2_raw']:.2f} = {calc_results['term2_weighted']:.3f}",
            font_size=24, color=YELLOW
        )
        result.next_to(description, DOWN, buff=0.2)
        
        self.play(Write(formula_text), Write(description))
        self.play(Write(result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description), FadeOut(result))

    def show_step3_returns_rank(self, title_obj, calc_results):
        step_title = Text("步骤3: 历史回报时间序列排名", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{term3} = 0.73 \times \text{rank}(\text{Ts\_Rank}(\text{delay}(-1 \times \text{returns}, 6), 5))",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        description = Text(
            "对6天前的负回报率在5天窗口内进行时间序列排名，\n"
            "再进行截面排名后乘以0.73的权重。",
            font_size=20, line_spacing=1.2
        )
        description.next_to(formula_text, DOWN, buff=0.3)

        result = MathTex(
            r"\text{term3} = 0.73 \times " + f"{calc_results['term3_raw']:.2f} = {calc_results['term3_weighted']:.3f}",
            font_size=24, color=YELLOW
        )
        result.next_to(description, DOWN, buff=0.2)
        
        self.play(Write(formula_text), Write(description))
        self.play(Write(result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description), FadeOut(result))

    def show_step4_vwap_correlation(self, title_obj, calc_results):
        step_title = Text("步骤4: VWAP与平均成交额相关性", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{term4} = \text{rank}(\text{abs}(\text{corr}(\text{vwap}, \text{adv20}, 6)))",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        description = Text(
            "计算VWAP与20日平均成交额在6天窗口的相关性绝对值，\n"
            "并进行截面排名。",
            font_size=20, line_spacing=1.2
        )
        description.next_to(formula_text, DOWN, buff=0.3)

        result = MathTex(
            r"\text{term4} = " + f"{calc_results['term4_raw']:.2f} = {calc_results['term4_weighted']:.3f}",
            font_size=24, color=YELLOW
        )
        result.next_to(description, DOWN, buff=0.2)
        
        self.play(Write(formula_text), Write(description))
        self.play(Write(result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description), FadeOut(result))

    def show_step5_value_momentum(self, title_obj, calc_results):
        step_title = Text("步骤5: 价值与动量交互项", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{term5} = 0.6 \times \text{rank}(((\text{MA}_{200}(\text{close}) - \text{open}) \times (\text{close} - \text{open})))",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        description = Text(
            "结合200日均线偏离度与日内动量的交互效应，\n"
            "进行截面排名后乘以0.6的权重。",
            font_size=20, line_spacing=1.2
        )
        description.next_to(formula_text, DOWN, buff=0.3)

        result = MathTex(
            r"\text{term5} = 0.6 \times " + f"{calc_results['term5_raw']:.2f} = {calc_results['term5_weighted']:.3f}",
            font_size=24, color=YELLOW
        )
        result.next_to(description, DOWN, buff=0.2)
        
        self.play(Write(formula_text), Write(description))
        self.play(Write(result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description), FadeOut(result))

    def show_final_result_alpha36(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=9.5, height=5, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(
            f"示例计算的 Alpha#36 值: {calc_results['alpha36_rounded']:.2f}", font_size=20, weight=BOLD
        )
        result_text_header.move_to(result_box.get_center() + UP * 1.8)

        result_text_body = Text(
            f"日内动量-成交量: {calc_results['term1_weighted']:.2f}\n" +
            f"日内反转: {calc_results['term2_weighted']:.2f}\n" +
            f"历史回报: {calc_results['term3_weighted']:.2f}\n" +
            f"VWAP相关性: {calc_results['term4_weighted']:.2f}\n" +
            f"价值-动量: {calc_results['term5_weighted']:.2f}",
            font_size=20, line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)
        
        summary_box = Rectangle(width=11, height=4, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "解读：Alpha#36 通过组合多个市场信号，包括日内动量、\n" +
            "成交量、价格反转、历史回报和价值因素，形成一个全面的\n" +
            "多因子策略。各分量权重的设计反映了不同信号的重要性。",
            font_size=24,
            line_spacing=1.3,
            color=WHITE
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

    def show_summary_alpha36(self):
        title = Text("策略总结 (Alpha#36)", font_size=36, color=BLUE)
        title.to_edge(UP, buff=1)
        self.play(Write(title))
        
        summary_box = RoundedRectangle(width=9, height=5, corner_radius=0.5, fill_color=BLUE_E, fill_opacity=0.1, stroke_color=BLUE).next_to(title, DOWN, buff=0.5)
        
        summary_points = VGroup(
            Text("✓ 结合多个市场信号的综合因子", font_size=22, color=GREEN),
            Text("✓ 通过权重设计突出重要信号", font_size=22, color=WHITE),
            Text("✗ 依赖多个数据源，计算复杂", font_size=22, color=RED),
            Text("✗ 窗口计算可能导致初始NaN值", font_size=22, color=RED),
            Text("★ 理论取值范围 [0, 5.24]", font_size=24, color=YELLOW),
            Text("★ 需要充分的回测和验证", font_size=22, color=YELLOW)
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
    # manim -pqh alpha36_visualization.py Alpha36Visualization
    pass 