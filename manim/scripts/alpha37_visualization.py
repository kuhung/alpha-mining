#!/usr/bin/env python3
"""
Alpha#37 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -ql alpha37_visualization.py Alpha37Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha37Visualization.mp4
manim -qk alpha37_visualization.py Alpha37Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha37Visualization.mp4

3. 合并音频
PROCESS_PATH="/Users/kuhung/roy/alpha-mining/process"
FILE_PATH="/Users/kuhung/roy/alpha-mining/manim/outputs/"
${PROCESS_PATH}/process_videos.sh ${PROCESS_PATH}/origin.mov ${FILE_PATH}/Alpha37Visualization.mp4 ${FILE_PATH}/Alpha37Visualization.png
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

class Alpha37Visualization(Scene):
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
        
        # Alpha#37公式
        formula_title_text = "Alpha#37 截面合成因子"
        formula_title = Text(formula_title_text, font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#37} = (\text{rank}(\text{correlation}(\text{delay}((\text{open} - \text{close}), 1), \text{close}, 200)) + \text{rank}((\text{open} - \text{close})))",
            font_size=28
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "结合短期价格动量与历史相关性的综合因子",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
        self.show_summary_alpha37()
        self.end_scene()
    
    def create_data_table_alpha37(self):
        headers = ["日期", "资产ID", "开盘价 (O)", "收盘价 (C)", "O-C", "延迟O-C", "相关性", "Ranked Corr", "Ranked O-C", "Alpha#37"]
        # Data for asset_1 from 2025-01-04 to 2025-01-06 (to show context for delay and correlation)
        # The example in README uses 2025-01-05 for calculation.
        data_values = [
            ["2025-01-04", "asset_1", "101.00", "100.00", "1.00", "NaN", "NaN", "NaN", "NaN", "NaN"], # Delay 1 will be NaN
            ["2025-01-05", "asset_1", "100.00", "99.50", "0.50", "1.00", "0.15", "0.70", "0.30", "1.00"], # Target row
            ["2025-01-06", "asset_1", "99.00", "98.80", "0.20", "0.50", "0.10", "0.60", "0.50", "1.10"],
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

    def show_calculation_steps(self):
        steps_title = Text("计算步骤演示 (Alpha#37)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-01-05 Alpha#37)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha37() # Changed to alpha37
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.7)
        self.play(Create(data_table))

        # Highlight the target row (2025-01-05)
        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((3, col_idx), color=YELLOW)) # Row 3 is 2025-01-05
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title)) # Ensure data_title is faded out
        
        # Store calculated values for asset_1 from 2025-01-05 (from README.md example)
        calc_results = {
            'open_t': 100.00,
            'close_t': 99.50,
            'open_t_minus_1': 101.00,
            'close_t_minus_1': 100.00,
            'oc_diff': 0.50,
            'oc_diff_delay1': 1.00,
            'corr_oc_delay1_close_200': 0.15,
            'ranked_corr': 0.70,
            'ranked_oc_diff': 0.30,
            'alpha37': 1.00
        }

        self.show_step1_oc_diff_delay(steps_title, calc_results)
        self.show_step2_correlation(steps_title, calc_results)
        self.show_step3_rank_oc_diff(steps_title, calc_results)
        self.show_step4_sum_ranks(steps_title, calc_results)
        self.show_final_result_alpha37(steps_title, calc_results)

    def show_step1_oc_diff_delay(self, title_obj, calc_results):
        step_title = Text("步骤1: 计算 (开盘价 - 收盘价) 及延迟值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        oc_diff_formula = MathTex(
            r"\text{oc\_diff} = \text{open} - \text{close}",
            font_size=24
        )
        oc_diff_formula.next_to(step_title, DOWN, buff=0.4)
        
        oc_diff_calc = MathTex(
            f"\text{{oc\_diff}} = {calc_results['open_t']:.2f} - {calc_results['close_t']:.2f} = {calc_results['oc_diff']:.2f}",
            font_size=24, color=YELLOW
        )
        oc_diff_calc.next_to(oc_diff_formula, DOWN, buff=0.2)

        delay_formula = MathTex(
            r"\text{oc\_diff\_delay1} = \text{delay}(\text{oc\_diff}, 1)",
            font_size=24
        )
        delay_formula.next_to(oc_diff_calc, DOWN, buff=0.4)

        delay_calc = MathTex(
            f"\text{{oc\_diff\_delay1}} = (\text{{open}}_{{-1}} - \text{{close}}_{{-1}}) = {calc_results['open_t_minus_1']:.2f} - {calc_results['close_t_minus_1']:.2f} = {calc_results['oc_diff_delay1']:.2f}",
            font_size=24, color=YELLOW
        )
        delay_calc.next_to(delay_formula, DOWN, buff=0.2)
        
        self.play(Write(oc_diff_formula), Write(oc_diff_calc))
        self.wait(2)
        self.play(Write(delay_formula), Write(delay_calc))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(oc_diff_formula), FadeOut(oc_diff_calc), FadeOut(delay_formula), FadeOut(delay_calc))

    def show_step2_correlation(self, title_obj, calc_results):
        step_title = Text("步骤2: 计算相关性并排名", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        corr_formula = MathTex(
            r"\text{corr\_oc\_delay1\_close\_200} = \text{correlation}(\text{oc\_diff\_delay1}, \text{close}, 200)",
            font_size=22
        )
        corr_formula.next_to(step_title, DOWN, buff=0.4)
        
        corr_calc = MathTex(
            f"\text{{corr\_oc\_delay1\_close\_200}} = {calc_results['corr_oc_delay1_close_200']:.2f}",
            font_size=24, color=YELLOW
        )
        corr_calc.next_to(corr_formula, DOWN, buff=0.2)

        ranked_corr_formula = MathTex(
            r"\text{ranked\_corr} = \text{rank}(\text{corr\_oc\_delay1\_close\_200})",
            font_size=24
        )
        ranked_corr_formula.next_to(corr_calc, DOWN, buff=0.4)
        
        ranked_corr_result = MathTex(
            f"\text{{Ranked Corr}} = {calc_results['ranked_corr']:.2f}",
            font_size=24, color=YELLOW
        )
        ranked_corr_result.next_to(ranked_corr_formula, DOWN, buff=0.2)
        
        self.play(Write(corr_formula), Write(corr_calc))
        self.wait(2)
        self.play(Write(ranked_corr_formula), Write(ranked_corr_result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(corr_formula), FadeOut(corr_calc), FadeOut(ranked_corr_formula), FadeOut(ranked_corr_result))
        
    def show_step3_rank_oc_diff(self, title_obj, calc_results):
        step_title = Text("步骤3: 计算 (开盘价 - 收盘价) 的排名", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        ranked_oc_diff_formula = MathTex(
            r"\text{ranked\_oc\_diff} = \text{rank}((\text{open} - \text{close}))",
            font_size=24
        )
        ranked_oc_diff_formula.next_to(step_title, DOWN, buff=0.4)
        
        ranked_oc_diff_result = MathTex(
            f"\text{{Ranked O-C}} = {calc_results['ranked_oc_diff']:.2f}",
            font_size=24, color=YELLOW
        )
        ranked_oc_diff_result.next_to(ranked_oc_diff_formula, DOWN, buff=0.2)
        
        self.play(Write(ranked_oc_diff_formula), Write(ranked_oc_diff_result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(ranked_oc_diff_formula), FadeOut(ranked_oc_diff_result))

    def show_step4_sum_ranks(self, title_obj, calc_results):
        step_title = Text("步骤4: 求和得到最终 Alpha#37", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_sum = MathTex(
            r"\text{Alpha\#37} = \text{ranked\_corr} + \text{ranked\_oc\_diff}",
            font_size=24
        )
        formula_sum.next_to(step_title, DOWN, buff=0.4)
        
        sum_calc = MathTex(
            f"\text{{Alpha\#37}} = {calc_results['ranked_corr']:.2f} + {calc_results['ranked_oc_diff']:.2f} = {calc_results['alpha37']:.2f}",
            font_size=24, color=GREEN
        )
        sum_calc.next_to(formula_sum, DOWN, buff=0.2)
        
        self.play(Write(formula_sum))
        self.play(Write(sum_calc))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_sum), FadeOut(sum_calc))

    def show_final_result_alpha37(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=9.5, height=5, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(
            f"asset_1 在 2025-01-05 的 Alpha#37 值: {calc_results['alpha37']:.2f}", font_size=20, weight=BOLD
        )
        result_text_header.move_to(result_box.get_center() + UP * 1.8)

        result_text_body = Text(
            f"开盘-收盘差值 (oc_diff) = {calc_results['oc_diff']:.2f}。\n" +
            f"延迟开盘-收盘差值 (oc_diff_delay1) = {calc_results['oc_diff_delay1']:.2f}。\n" +
            f"相关性 (corr_oc_delay1_close_200) = {calc_results['corr_oc_delay1_close_200']:.2f}。\n" +
            f"排名相关性 (ranked_corr) = {calc_results['ranked_corr']:.2f}。\n" +
            f"排名开盘-收盘差值 (ranked_oc_diff) = {calc_results['ranked_oc_diff']:.2f}。\n" +
            f"最终 Alpha 值为 {calc_results['alpha37']:.2f}，综合判断短期价格动量和历史相关性。",
            font_size=18, line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)
        
        summary_box = Rectangle(width=11, height=4, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "解读：Alpha#37 综合利用短期价格动量和历史相关性，\n"+
            "旨在捕捉市场中开盘价与收盘价差异的动量效应。\n"+
            "该因子结合了当前价格行为与历史相关性，\n"+
            "以期提供更稳健的交易信号。",
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

    def show_summary_alpha37(self):
        title = Text("策略总结 (Alpha#37)", font_size=36, color=BLUE)
        title.to_edge(UP, buff=1)
        self.play(Write(title))
        
        summary_box = RoundedRectangle(width=9, height=5, corner_radius=0.5, fill_color=BLUE_E, fill_opacity=0.1, stroke_color=BLUE).next_to(title, DOWN, buff=0.5)
        
        summary_points = VGroup(
            Text("✓ 结合短期价格动量与历史相关性", font_size=22, color=GREEN),
            Text("✓ 旨在捕捉开盘价与收盘价差异的动量效应", font_size=22, color=WHITE),
            Text("✗ 相关性计算对数据量要求高，可能导致早期 NaN", font_size=22, color=RED),
            Text("✗ 因子组合复杂，解释性可能受限", font_size=22, color=RED),
            Text("★ 需进行充分回测和验证", font_size=24, color=YELLOW),
            Text("★ 可与其他因子结合使用以增强稳健性", font_size=22, color=YELLOW)
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
    # manim -pqh alpha37_visualization.py Alpha37Visualization
    pass 