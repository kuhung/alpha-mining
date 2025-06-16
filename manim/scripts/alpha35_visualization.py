#!/usr/bin/env python3
"""
Alpha#35 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -ql alpha35_visualization.py Alpha35Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha35Visualization.mp4
manim -qk alpha35_visualization.py Alpha35Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha35Visualization.mp4

3. 合并音频
PROCESS_PATH="/Users/kuhung/roy/alpha-mining/process"
FILE_PATH="/Users/kuhung/roy/alpha-mining/manim/outputs/"
${PROCESS_PATH}/process_videos.sh ${PROCESS_PATH}/origin.mov ${FILE_PATH}/Alpha35Visualization.mp4 ${FILE_PATH}/Alpha35Visualization.png
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

class Alpha35Visualization(Scene):
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

        # Alpha#35公式
        formula_title_text = "Alpha#35 交易量与价格综合因子"
        formula_title = Text(formula_title_text, font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])

        formula = MathTex(
            r"\text{Alpha\#35} = (\text{Ts\_Rank}(\text{volume}, 32) \times (1 - \text{Ts\_Rank}((\text{close} + \text{high} - \text{low}), 16))) \times (1 - \text{Ts\_Rank}(\text{returns}, 32))",
            font_size=28
        )
        formula.move_to([0, 0.5, 0])

        explanation = Text(
            "结合交易量、价格波动和回报率时间序列排名的综合因子",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])

        self.add(formula_title, formula, explanation)
        self.wait(4)

        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))

        self.show_calculation_steps()
        self.show_summary_alpha35()
        self.end_scene()

    def create_data_table_alpha35(self):
        headers = ["分量", "时间序列排名 (Ts_Rank)", "转换后数值"]
        # Data from README.md example
        data_values = [
            ["volume", "0.80", "-"],
            ["(close + high - low)", "0.20", "1 - 0.20 = 0.80"],
            ["returns", "0.10", "1 - 0.10 = 0.90"]
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
        steps_title = Text("计算步骤演示 (Alpha#35)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))

        data_title = Text("示例数据 (假设某交易日各项排名)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)

        self.play(Write(data_title))

        data_table = self.create_data_table_alpha35()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.75)
        self.play(Create(data_table))

        # Highlight data rows
        highlight_cells_group = VGroup()
        for row_idx in range(1, 4): # Rows for data values
            for col_idx in range(1, len(data_table.col_labels) + 1):
                highlight_cells_group.add(data_table.get_highlighted_cell((row_idx + 1, col_idx), color=YELLOW))

        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title))

        # Store calculated values for visualization
        calc_results = {
            'volume_rank': 0.80,
            'price_term_rank': 0.20,
            'returns_rank': 0.10,
            'price_term_converted': 0.80, # 1 - 0.20
            'returns_converted': 0.90,   # 1 - 0.10
            'alpha35_raw': 0.80 * 0.80 * 0.90,
            'alpha35_rounded': 0.58
        }

        self.show_step1_volume_rank(steps_title, calc_results)
        self.show_step2_price_term(steps_title, calc_results)
        self.show_step3_returns_term(steps_title, calc_results)
        self.show_step4_final_multiplication(steps_title, calc_results)
        self.show_final_result_alpha35(steps_title, calc_results)

    def show_step1_volume_rank(self, title_obj, calc_results):
        step_title = Text("步骤1: 交易量时间序列排名", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{Ts\_Rank}(\text{volume}, 32)",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)

        description = Text(
            "计算过去32天交易量的时间序列排名，表示市场活跃度。",
            font_size=20, line_spacing=1.2
        )
        description.next_to(formula_text, DOWN, buff=0.3)

        result = MathTex(
            r"\text{Ts\_Rank}(\text{volume}, 32) = " + f"{calc_results['volume_rank']:.2f}", font_size=24, color=YELLOW
        )
        result.next_to(description, DOWN, buff=0.2)

        self.play(Write(formula_text), Write(description))
        self.play(Write(result))
        self.wait(3)

        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description), FadeOut(result))

    def show_step2_price_term(self, title_obj, calc_results):
        step_title = Text("步骤2: 价格动量与波动排名", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"1 - \text{Ts\_Rank}((\text{close} + \text{high} - \text{low}), 16)",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)

        description = Text(
            "计算过去16天 (收盘价 + 最高价 - 最低价) 的时间序列排名，并取1减去其值。\n"
            "排名越低（动量波动越小），贡献越大。",
            font_size=20, line_spacing=1.2
        )
        description.next_to(formula_text, DOWN, buff=0.3)

        rank_val = MathTex(
            r"\text{Ts\_Rank}((\text{close} + \text{high} - \text{low}), 16) = " + f"{calc_results['price_term_rank']:.2f}", font_size=24, color=YELLOW
        )
        rank_val.next_to(description, DOWN, buff=0.2)

        result = MathTex(
            r"1 - " + f"{calc_results['price_term_rank']:.2f} = " + f"{calc_results['price_term_converted']:.2f}", font_size=24, color=YELLOW
        )
        result.next_to(rank_val, DOWN, buff=0.2)

        self.play(Write(formula_text), Write(description))
        self.play(Write(rank_val))
        self.play(Write(result))
        self.wait(3)

        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description), FadeOut(rank_val), FadeOut(result))

    def show_step3_returns_term(self, title_obj, calc_results):
        step_title = Text("步骤3: 回报率时间序列排名", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"1 - \text{Ts\_Rank}(\text{returns}, 32)",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)

        description = Text(
            "计算过去32天每日回报率的时间序列排名，并取1减去其值。\n"
            "回报率排名越低（近期回报越差），贡献越大。",
            font_size=20, line_spacing=1.2
        )
        description.next_to(formula_text, DOWN, buff=0.3)

        rank_val = MathTex(
            r"\text{Ts\_Rank}(\text{returns}, 32) = " + f"{calc_results['returns_rank']:.2f}", font_size=24, color=YELLOW
        )
        rank_val.next_to(description, DOWN, buff=0.2)

        result = MathTex(
            r"1 - " + f"{calc_results['returns_rank']:.2f} = " + f"{calc_results['returns_converted']:.2f}", font_size=24, color=YELLOW
        )
        result.next_to(rank_val, DOWN, buff=0.2)

        self.play(Write(formula_text), Write(description))
        self.play(Write(rank_val))
        self.play(Write(result))
        self.wait(3)

        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description), FadeOut(rank_val), FadeOut(result))

    def show_step4_final_multiplication(self, title_obj, calc_results):
        step_title = Text("步骤4: 三个分量相乘", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{Alpha\#35} = (\text{Ts\_Rank}(\text{volume}, 32) \times (1 - \text{Ts\_Rank}((\text{close} + \text{high} - \text{low}), 16))) \times (1 - \text{Ts\_Rank}(\text{returns}, 32))",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)

        multiplication_step = MathTex(
            f"{calc_results['volume_rank']:.2f} \\times {calc_results['price_term_converted']:.2f} \\times {calc_results['returns_converted']:.2f}",
            font_size=24, color=YELLOW
        )
        multiplication_step.next_to(formula_text, DOWN, buff=0.3)

        result = MathTex(
            r"\text{Alpha\#35} = " + f"{calc_results['alpha35_raw']:.3f}", font_size=28, color=GREEN
        )
        result.next_to(multiplication_step, DOWN, buff=0.2)

        rounded_result = Text(f"四舍五入到两位小数: {calc_results['alpha35_rounded']:.2f}", font_size=24, color=YELLOW)
        rounded_result.next_to(result, DOWN, buff=0.2)

        self.play(Write(formula_text))
        self.play(Write(multiplication_step))
        self.play(Write(result))
        self.play(Write(rounded_result))
        self.wait(4)

        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(multiplication_step), FadeOut(result), FadeOut(rounded_result))


    def show_final_result_alpha35(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)

        result_box = Rectangle(width=9.5, height=5, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)

        result_text_header = Text(
            f"示例计算的 Alpha#35 值: {calc_results['alpha35_rounded']:.2f}", font_size=20, weight=BOLD
        )
        result_text_header.move_to(result_box.get_center() + UP * 1.8)

        result_text_body = Text(
            f"交易量排名 = {calc_results['volume_rank']:.2f}。\n" +
            f"价格动量/波动（转换后）= {calc_results['price_term_converted']:.2f}。\n" +
            f"回报率（转换后）= {calc_results['returns_converted']:.2f}。\n" +
            f"最终 Alpha 值为 {calc_results['alpha35_rounded']:.2f}，"
            f"表示交易量较大的市场模式，\n"
            f"同时价格动量和回报率较低。",
            font_size=20, line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)

        summary_box = Rectangle(width=11, height=4, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "解读：Alpha#35 倾向于在交易量较大、价格动量或波动相对较小、\n" +
            "且近期回报率相对较低的市场条件下产生较高的值。\n" +
            "该因子旨在捕捉由这些基本指标共同驱动的潜在机会。",
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

    def show_summary_alpha35(self):
        title = Text("策略总结 (Alpha#35)", font_size=36, color=BLUE)
        title.to_edge(UP, buff=1)
        self.play(Write(title))

        summary_box = RoundedRectangle(width=9, height=5, corner_radius=0.5, fill_color=BLUE_E, fill_opacity=0.1, stroke_color=BLUE).next_to(title, DOWN, buff=0.5)

        summary_points = VGroup(
            Text("✓ 结合交易量、价格波动和回报率", font_size=22, color=GREEN),
            Text("✓ 倾向于在特定市场条件下产生高值", font_size=22, color=WHITE),
            Text("✗ 对数据质量和完整性要求高 (NaN值)", font_size=22, color=RED),
            Text("✗ 时间序列排名在数据开头可能出现NaN值", font_size=22, color=RED),
            Text("★ 需进行充分回测和验证，不保证未来表现", font_size=24, color=YELLOW),
            Text("★ 建议与其他因子结合使用以增强稳健性", font_size=22, color=YELLOW)
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
    # manim -pqh alpha35_visualization.py Alpha35Visualization
    pass 