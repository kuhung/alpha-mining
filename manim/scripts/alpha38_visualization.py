#!/usr/bin/env python3
"""
Alpha#38 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -ql alpha38_visualization.py Alpha38Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha38Visualization.mp4
manim -qk alpha38_visualization.py Alpha38Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha38Visualization.mp4

3. 合并音频
PROCESS_PATH="/Users/kuhung/roy/alpha-mining/process"
FILE_PATH="/Users/kuhung/roy/alpha-mining/manim/outputs/"
${PROCESS_PATH}/process_videos.sh ${PROCESS_PATH}/origin.mov ${FILE_PATH}/Alpha38Visualization.mp4 ${FILE_PATH}/Alpha38Visualization.png
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

class Alpha38Visualization(Scene):
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
        
        # Alpha#38公式
        formula_title_text = "Alpha#38 反向时间序列排名与日内波动排名"
        formula_title = Text(formula_title_text, font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#38} = (-1 \times \text{rank}(\text{Ts\_Rank}(\text{close}, 10))) \times \text{rank}((\text{close} / \text{open}))",
            font_size=28
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "识别短期超卖且日内波动大的资产",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps_alpha38()
        self.show_summary_alpha38()
        self.end_scene()
    
    def create_data_table_alpha38(self):
        headers = ["日期", "资产ID", "开盘价 (O)", "收盘价 (C)", "C/O", "Ts_Rank(C,10)", "Ranked Ts_Rank", "-1*Ranked Ts_Rank", "Ranked C/O", "Alpha#38"]
        # Data for asset_1 from 2024-06-10 (from README.md example)
        data_values = [
            ["2024-06-10", "asset_1", "104.28", "105.80", "1.01", "1.00", "0.90", "-0.90", "0.80", "-0.72"],
        ]
        
        header_mobjects = [Text(h, font_size=20, weight=BOLD) for h in headers]

        table = Table(
            data_values,
            col_labels=header_mobjects,
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": WHITE},
            element_to_mobject=Text, 
            element_to_mobject_config={"font_size": 18},
            h_buff=0.1, 
            v_buff=0.25
        )
        return table

    def show_calculation_steps_alpha38(self):
        steps_title = Text("计算步骤演示 (Alpha#38)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2024-06-10 Alpha#38)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha38()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.7)
        self.play(Create(data_table))

        # Highlight the target row (2024-06-10)
        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((2, col_idx), color=YELLOW)) # Row 2 is 2024-06-10
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title)) 
        
        # Store calculated values for asset_1 from 2024-06-10 (from README.md example)
        calc_results = {
            'open_t': 104.28,
            'close_t': 105.80,
            'close_over_open': 1.01,
            'ts_rank_close_10': 1.00,
            'ranked_ts_rank_close_10': 0.90,
            'neg_ranked_ts_rank': -0.90,
            'ranked_close_over_open': 0.80,
            'alpha38': -0.72
        }

        self.show_step1_close_over_open(steps_title, calc_results)
        self.show_step2_ts_rank_close(steps_title, calc_results)
        self.show_step3_neg_ranked_ts_rank(steps_title, calc_results)
        self.show_step4_ranked_close_over_open(steps_title, calc_results)
        self.show_step5_final_multiplication(steps_title, calc_results)
        self.show_final_result_alpha38(steps_title, calc_results)

    def show_step1_close_over_open(self, title_obj, calc_results):
        step_title = Text("步骤1: 计算 (收盘价 / 开盘价)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        close_over_open_formula = MathTex(
            r"\text{C/O} = \text{close} / \text{open}",
            font_size=24
        )
        close_over_open_formula.next_to(step_title, DOWN, buff=0.4)
        
        close_over_open_calc = MathTex(
            f"\text{{C/O}} = {calc_results['close_t']:.2f} / {calc_results['open_t']:.2f} = {calc_results['close_over_open']:.2f}",
            font_size=24, color=YELLOW
        )
        close_over_open_calc.next_to(close_over_open_formula, DOWN, buff=0.2)

        self.play(Write(close_over_open_formula), Write(close_over_open_calc))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(close_over_open_formula), FadeOut(close_over_open_calc))

    def show_step2_ts_rank_close(self, title_obj, calc_results):
        step_title = Text("步骤2: 计算 Ts_Rank(close, 10)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        ts_rank_formula = MathTex(
            r"\text{Ts\_Rank}(\text{close}, 10)",
            font_size=24
        )
        ts_rank_formula.next_to(step_title, DOWN, buff=0.4)
        
        ts_rank_calc = MathTex(
            f"\text{{Ts\_Rank(C,10)}} = {calc_results['ts_rank_close_10']:.2f}",
            font_size=24, color=YELLOW
        )
        ts_rank_calc.next_to(ts_rank_formula, DOWN, buff=0.2)
        
        self.play(Write(ts_rank_formula), Write(ts_rank_calc))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(ts_rank_formula), FadeOut(ts_rank_calc))

    def show_step3_neg_ranked_ts_rank(self, title_obj, calc_results):
        step_title = Text("步骤3: 计算 -1 * rank(Ts_Rank(close, 10))", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        ranked_ts_rank_formula = MathTex(
            r"\text{ranked\_Ts\_Rank} = \text{rank}(\text{Ts\_Rank}(\text{close}, 10))",
            font_size=22
        )
        ranked_ts_rank_formula.next_to(step_title, DOWN, buff=0.4)
        
        ranked_ts_rank_calc = MathTex(
            f"\text{{Ranked Ts\_Rank}} = {calc_results['ranked_ts_rank_close_10']:.2f}",
            font_size=24, color=YELLOW
        )
        ranked_ts_rank_calc.next_to(ranked_ts_rank_formula, DOWN, buff=0.2)

        neg_ranked_ts_rank_formula = MathTex(
            r"\text{neg\_ranked\_Ts\_Rank} = -1 * \text{ranked\_Ts\_Rank}",
            font_size=24
        )
        neg_ranked_ts_rank_formula.next_to(ranked_ts_rank_calc, DOWN, buff=0.4)

        neg_ranked_ts_rank_calc = MathTex(
            f"\text{{-1*Ranked Ts\_Rank}} = -1 * {calc_results['ranked_ts_rank_close_10']:.2f} = {calc_results['neg_ranked_ts_rank']:.2f}",
            font_size=24, color=YELLOW
        )
        neg_ranked_ts_rank_calc.next_to(neg_ranked_ts_rank_formula, DOWN, buff=0.2)
        
        self.play(Write(ranked_ts_rank_formula), Write(ranked_ts_rank_calc))
        self.wait(2)
        self.play(Write(neg_ranked_ts_rank_formula), Write(neg_ranked_ts_rank_calc))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(ranked_ts_rank_formula), FadeOut(ranked_ts_rank_calc), FadeOut(neg_ranked_ts_rank_formula), FadeOut(neg_ranked_ts_rank_calc))

    def show_step4_ranked_close_over_open(self, title_obj, calc_results):
        step_title = Text("步骤4: 计算 rank(close / open)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        ranked_close_over_open_formula = MathTex(
            r"\text{ranked\_C/O} = \text{rank}((\text{close} / \text{open}))",
            font_size=24
        )
        ranked_close_over_open_formula.next_to(step_title, DOWN, buff=0.4)
        
        ranked_close_over_open_calc = MathTex(
            f"\text{{Ranked C/O}} = {calc_results['ranked_close_over_open']:.2f}",
            font_size=24, color=YELLOW
        )
        ranked_close_over_open_calc.next_to(ranked_close_over_open_formula, DOWN, buff=0.2)
        
        self.play(Write(ranked_close_over_open_formula), Write(ranked_close_over_open_calc))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(ranked_close_over_open_formula), FadeOut(ranked_close_over_open_calc))

    def show_step5_final_multiplication(self, title_obj, calc_results):
        step_title = Text("步骤5: 相乘得到最终 Alpha#38", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_multiply = MathTex(
            r"\text{Alpha\#38} = \text{neg\_ranked\_Ts\_Rank} * \text{ranked\_C/O}",
            font_size=24
        )
        formula_multiply.next_to(step_title, DOWN, buff=0.4)
        
        multiply_calc = MathTex(
            f"\text{{Alpha\#38}} = {calc_results['neg_ranked_ts_rank']:.2f} * {calc_results['ranked_close_over_open']:.2f} = {calc_results['alpha38']:.2f}",
            font_size=24, color=GREEN
        )
        multiply_calc.next_to(formula_multiply, DOWN, buff=0.2)
        
        self.play(Write(formula_multiply))
        self.play(Write(multiply_calc))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_multiply), FadeOut(multiply_calc))

    def show_final_result_alpha38(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=9.5, height=5, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(
            f"asset_1 在 2024-06-10 的 Alpha#38 值: {calc_results['alpha38']:.2f}", font_size=20, weight=BOLD
        )
        result_text_header.move_to(result_box.get_center() + UP * 1.8)

        result_text_body = Text(
            f"收盘价/开盘价 (C/O) = {calc_results['close_over_open']:.2f}。\n" +
            f"Ts_Rank(close, 10) = {calc_results['ts_rank_close_10']:.2f}。\n" +
            f"排名后的 Ts_Rank (ranked_ts_rank_close_10) = {calc_results['ranked_ts_rank_close_10']:.2f}。\n" +
            f"反向排名后的 Ts_Rank (-1*ranked_ts_rank) = {calc_results['neg_ranked_ts_rank']:.2f}。\n" +
            f"排名后的 C/O (ranked_close_over_open) = {calc_results['ranked_close_over_open']:.2f}。\n" +
            f"最终 Alpha 值为 {calc_results['alpha38']:.2f}，综合判断短期超卖与日内波动。",
            font_size=18, line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)
        
        summary_box = Rectangle(width=11, height=4, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "解读：Alpha#38 旨在识别短期内相对弱势的资产。\n"+
            "这些资产在日内表现出一定反弹或企稳迹象。\n"+
            "通过结合反向时间序列排名和日内波动排名，\n"+
            "寻找可能处于短期底部并开始反弹的资产。",
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

    def show_summary_alpha38(self):
        title = Text("策略总结 (Alpha#38)", font_size=36, color=BLUE)
        title.to_edge(UP, buff=1)
        self.play(Write(title))
        
        summary_box = RoundedRectangle(width=9, height=5, corner_radius=0.5, fill_color=BLUE_E, fill_opacity=0.1, stroke_color=BLUE).next_to(title, DOWN, buff=0.5)
        
        summary_points = VGroup(
            Text("✓ 识别短期超卖且日内波动大的资产", font_size=22, color=GREEN),
            Text("✓ 结合反向时间序列排名与日内波动排名", font_size=22, color=WHITE),
            Text("✗ 对数据质量和时间序列长度有要求", font_size=22, color=RED),
            Text("✗ 可能对市场情绪变化敏感", font_size=22, color=RED),
            Text("★ 需进行充分回测和验证", font_size=24, color=YELLOW),
            Text("★ 适用于短线交易或反转策略", font_size=22, color=YELLOW)
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
    # manim -pqh alpha38_visualization.py Alpha38Visualization
    pass