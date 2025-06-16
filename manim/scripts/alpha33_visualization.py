#!/usr/bin/env python3
"""
Alpha#33 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -ql alpha33_visualization.py Alpha33Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha33Visualization.mp4
manim -qk alpha33_visualization.py Alpha33Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha33Visualization.mp4

3. 合并音频
PROCESS_PATH="/Users/kuhung/roy/alpha-mining/process"
FILE_PATH="/Users/kuhung/roy/alpha-mining/manim/outputs/"
${PROCESS_PATH}/process_videos.sh ${PROCESS_PATH}/origin.mov ${FILE_PATH}/Alpha33Visualization.mp4 ${FILE_PATH}/Alpha33Visualization.png
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

class Alpha33Visualization(Scene):
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
        
        # Alpha#33公式
        formula_title_text = "Alpha#33 价格反转因子"
        formula_title = Text(formula_title_text, font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#33} = \text{rank}((-1 \times ((1 - (\text{open} / \text{close}))^1)))",
            font_size=28
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "旨在捕捉基于开盘价和收盘价关系的价格反转信号",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
        self.show_summary_alpha33()
        self.end_scene()
    
    def create_data_table_alpha33(self):
        headers = ["日期", "资产ID", "开盘价 (O)", "收盘价 (C)", "Alpha#33"]
        # Data from alpha/alpha33/alpha33_results.csv for 2025-01-01
        data_values = [
            ["2025-01-01", "asset_1", "100.30", "100.00", "0.80"],
            ["2025-01-01", "asset_2", "100.53", "100.00", "1.00"],
            ["2025-01-01", "asset_3", "99.92", "100.00", "0.60"],
            ["2025-01-01", "asset_4", "99.66", "100.00", "0.20"],
            ["2025-01-01", "asset_5", "99.90", "100.00", "0.40"]
        ]
        
        header_mobjects = [Text(h, font_size=24, weight=BOLD) for h in headers]

        table = Table(
            data_values,
            col_labels=header_mobjects,
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": WHITE},
            element_to_mobject=Text, 
            element_to_mobject_config={"font_size": 20},
            h_buff=0.5, 
            v_buff=0.25
        )
        return table

    def show_calculation_steps(self):
        steps_title = Text("计算步骤演示 (Alpha#33)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (2025-01-01 所有资产)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha33()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.85)
        self.play(Create(data_table))

        # Highlight the target row (asset_1)
        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((2, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title))
        
        # Store calculated values for asset_1 from 2025-01-01
        calc_results = {
            'open': 100.30,
            'close': 100.00,
            'intermediate_ratio': -0.003, # (1 - (open / close))
            'intermediate_negated': 0.003, # -1 * (1 - (open / close))
            'alpha33': 0.80
        }

        self.show_step1_intermediate_calc(steps_title, calc_results)
        self.show_step2_cross_sectional_rank(steps_title, calc_results)
        self.show_final_result_alpha33(steps_title, calc_results)

    def show_step1_intermediate_calc(self, title_obj, calc_results):
        step_title = Text("步骤1: 计算中间值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_part1 = MathTex(
            r"\text{Temp}_1 = (1 - (\text{open} / \text{close}))",
            font_size=24
        )
        formula_part1.next_to(step_title, DOWN, buff=0.4)
        
        example_calc1 = MathTex(
            f"\text{{Temp}}_1 = 1 - ({calc_results['open']:.2f} / {calc_results['close']:.2f}) = 1 - 1.003 = {calc_results['intermediate_ratio']:.3f}", font_size=24, color=YELLOW
        )
        example_calc1.next_to(formula_part1, DOWN, buff=0.2)

        formula_part2 = MathTex(
            r"\text{Temp}_2 = -1 \times \text{Temp}_1",
            font_size=24
        )
        formula_part2.next_to(example_calc1, DOWN, buff=0.4)

        example_calc2 = MathTex(
            f"\text{{Temp}}_2 = -1 \times ({calc_results['intermediate_ratio']:.3f}) = {calc_results['intermediate_negated']:.3f}", font_size=24, color=YELLOW
        )
        example_calc2.next_to(formula_part2, DOWN, buff=0.2)
        
        description = Text(
            "首先计算 (1 - (开盘价 / 收盘价))，然后取其负值。",
            font_size=20, line_spacing=1.2
        )
        description.next_to(example_calc2, DOWN, buff=0.3)
        
        self.play(Write(formula_part1), Write(example_calc1))
        self.wait(2)
        self.play(Write(formula_part2), Write(example_calc2))
        self.play(Write(description))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_part1), FadeOut(example_calc1), FadeOut(formula_part2), FadeOut(example_calc2), FadeOut(description))

    def show_step2_cross_sectional_rank(self, title_obj, calc_results):
        step_title = Text("步骤2: 截面排名", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_rank = MathTex(
            r"\text{Alpha\#33} = \text{rank}(\text{Temp}_2)",
            font_size=24
        )
        formula_rank.next_to(step_title, DOWN, buff=0.4)

        rank_description = Text(
            "对所有资产的中间结果进行截面百分比排名。",
            font_size=20, line_spacing=1.2
        )
        rank_description.next_to(formula_rank, DOWN, buff=0.3)
        
        # Values for 2025-01-01 and their sorted order / rank
        rank_values = Text(
            "2025-01-01 中间结果 (Temp2):\n"
            "asset_4: -0.0034\n"
            "asset_5: -0.0010\n"
            "asset_3: -0.0008\n"
            "asset_1: 0.0030\n"
            "asset_2: 0.0053",
            font_size=20, line_spacing=1.2, t2c={"-0.0034":RED_E, "0.0053":GREEN_E}
        ).next_to(rank_description, DOWN, buff=0.3).align_to(rank_description, LEFT)

        final_alpha_result = MathTex(
            f"\text{{Alpha\#33}} (\text{{asset\_1}}) = {calc_results['alpha33']:.2f}",
            font_size=28, color=GREEN
        )
        final_alpha_result.next_to(rank_values, DOWN, buff=0.5)
        
        self.play(Write(formula_rank), Write(rank_description))
        self.play(Write(rank_values))
        self.play(Write(final_alpha_result))
        self.wait(4)
        
        self.play(FadeOut(step_title), FadeOut(formula_rank), FadeOut(rank_description), FadeOut(rank_values), FadeOut(final_alpha_result))
        
    def show_final_result_alpha33(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=9, height=3.5, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(
            f"asset_1 在 2025-01-01 的 Alpha#33 值: {calc_results['alpha33']:.2f}", font_size=24, weight=BOLD
        )
        result_text_header.move_to(result_box.get_center() + UP * 1.0)

        result_text_body = Text(
            f"计算结果 {calc_results['alpha33']:.2f} 反映了当日相对价格反转的强度。",
            font_size=20, line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)
        
        summary_box = Rectangle(width=11, height=4, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "解读：Alpha#33 因子基于开盘价与收盘价的关系，\n"+
            "通过截面排名识别当日价格反转的潜力。较高的Alpha值\n"+
            "可能指示相对更强的反转信号。",
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

    def show_summary_alpha33(self):
        title = Text("策略总结 (Alpha#33)", font_size=36, color=BLUE)
        title.to_edge(UP, buff=1)
        self.play(Write(title))
        
        summary_box = RoundedRectangle(width=9, height=5, corner_radius=0.5, fill_color=BLUE_E, fill_opacity=0.1, stroke_color=BLUE).next_to(title, DOWN, buff=0.5)
        
        summary_points = VGroup(
            Text("✓ 捕捉基于开盘价/收盘价的价格反转信号", font_size=22, color=GREEN),
            Text("✓ 使用截面排名进行标准化", font_size=22, color=WHITE),
            Text("✗ 依赖于日内价格行为", font_size=22, color=RED),
            Text("✗ 可能对市场噪音敏感", font_size=22, color=RED),
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
    # manim -pqh alpha33_visualization.py Alpha33Visualization
    pass 