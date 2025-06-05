#!/usr/bin/env python3
"""
Alpha#10 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha10_visualization.py Alpha10Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha10Visualization.mp4 --flush_cache
manim -qk alpha10_visualization.py Alpha10Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha10Visualization.mp4 --flush_cache

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

class Alpha10Visualization(Scene):
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

        # Alpha#10公式
        formula_title = Text("Alpha#10 条件趋势/反转与排名因子", font_size=36, color=GREEN)
        formula_title.move_to([0, 2.2, 0])

        formula_part1 = r"\text{intermediate\_value} = \begin{cases} \text{delta(close,1)} & \text{if } 0 < \text{ts\_min}(\text{delta(close,1)}, 4) \\ \text{delta(close,1)} & \text{if } \text{ts\_max}(\text{delta(close,1)}, 4) < 0 \\ -1 \times \text{delta(close,1)} & \text{otherwise} \end{cases}"
        formula_part2 = r"\text{Alpha\#10} = \text{rank}(\text{intermediate\_value})"

        formula_full_tex = MathTex(
            formula_part1 + r"\\ \\" + formula_part2,
            font_size=28
        )
        formula_full_tex.move_to([0, 0, 0])

        explanation = Text(
            "结合短期趋势判断和横截面排名的因子",
            font_size=28,
            color=YELLOW
        )
        explanation.next_to(formula_full_tex, DOWN, buff=0.7)

        self.add(formula_title, formula_full_tex, explanation)
        self.wait(4)

        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula_full_tex), FadeOut(explanation))

        self.show_calculation_steps()

    def create_data_table_alpha10(self):
        headers = ["日期", "收盘价 (Close)"]
        data_values = [
            ["2025-01-01", "100.00"], # Needed for delta calculation of 01-02
            ["2025-01-02", "100.10"],
            ["2025-01-03", "100.20"],
            ["2025-01-04", "99.40"],
            ["2025-01-05", "100.50"]  # Target row for calculation
        ]

        header_mobjects = [Text(h, font_size=20, weight=BOLD) for h in headers]

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
        steps_title = Text("计算步骤演示 (Alpha#10)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))

        data_title = Text("示例数据 (计算 Alpha#10 for 2025-01-05)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)

        self.play(Write(data_title))

        data_table = self.create_data_table_alpha10()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.75)
        self.play(Create(data_table))

        highlight_cells_group = VGroup()
        # Data for 2025-01-05 is the 5th data row, which is mobject table row 6.
        for col_idx in range(1, len(data_table.col_labels) + 1):
            highlight_cells_group.add(data_table.get_highlighted_cell((6, col_idx), color=YELLOW))

        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title))

        self.show_step1_delta(steps_title)
        self.show_step2_ts_min(steps_title)
        self.show_step3_ts_max(steps_title)
        self.show_step4_intermediate_value(steps_title)
        self.show_step5_rank(steps_title)
        self.show_final_result_alpha10(steps_title)

    def show_step1_delta(self, title_obj):
        step_title = Text("步骤1: 计算当日价格变动 delta(close, 1)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(r"\text{delta}(\text{close}, 1)_t = \text{close}_t - \text{close}_{t-1}", font_size=24)
        formula_text.next_to(step_title, DOWN, buff=0.4)

        description = Text(
            "计算 2025-01-05 的价格变动 (d1_today):",
            font_size=20
        )
        description.next_to(formula_text, DOWN, buff=0.3)

        calculation = Text(
            "d1_today = close(2025-01-05) - close(2025-01-04)\n"
            "d1_today = 100.50 - 99.40 = 1.10",
            font_size=18, color=GREEN, line_spacing=1.2
        )
        calculation.next_to(description, DOWN, buff=0.2)

        self.play(Write(formula_text), Write(description))
        self.play(Write(calculation))
        self.wait(3)

        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description),
                  FadeOut(calculation))

    def show_step2_ts_min(self, title_obj):
        step_title = Text("步骤2: 计算过去4日 delta(close,1) 的最小值 (ts_min)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        delta_series_intro = Text("过去4日（含当日）的 delta(close,1) 序列:", font_size=20)
        delta_series_intro.next_to(step_title, DOWN, buff=0.4)

        deltas = [
            "d(01-02) = 100.10 - 100.00 = 0.10",
            "d(01-03) = 100.20 - 100.10 = 0.10",
            "d(01-04) = 99.40 - 100.20 = -0.80",
            "d(01-05) = 100.50 - 99.40 = 1.10 (d1_today)"
        ]
        delta_values_text = VGroup(*[Text(d, font_size=18, line_spacing=1.2, color=GREEN) for d in deltas])
        delta_values_text.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        delta_values_text.next_to(delta_series_intro, DOWN, buff=0.2)

        ts_min_calc_text = MathTex(r"\text{ts\_min}(\text{delta(close,1)}, 4) = \text{min}([0.10, 0.10, -0.80, 1.10])", font_size=22)
        ts_min_calc_text.next_to(delta_values_text, DOWN, buff=0.3)

        ts_min_result = MathTex(r"\text{ts\_min} = -0.80", font_size=24, color=YELLOW)
        ts_min_result.next_to(ts_min_calc_text, DOWN, buff=0.2)

        self.play(Write(step_title))
        self.play(Write(delta_series_intro))
        self.play(Write(delta_values_text))
        self.play(Write(ts_min_calc_text), Write(ts_min_result))
        self.wait(4)

        self.play(FadeOut(step_title), FadeOut(delta_series_intro), FadeOut(delta_values_text),
                  FadeOut(ts_min_calc_text), FadeOut(ts_min_result))

    def show_step3_ts_max(self, title_obj):
        step_title = Text("步骤3: 计算过去4日 delta(close,1) 的最大值 (ts_max)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        delta_series_intro = Text("同步骤2的 delta(close,1) 序列:", font_size=20)
        delta_series_intro.next_to(step_title, DOWN, buff=0.4)

        delta_series_display = Text("[0.10, 0.10, -0.80, 1.10]", font_size=18, color=GREEN)
        delta_series_display.next_to(delta_series_intro, DOWN, buff=0.2)

        ts_max_calc_text = MathTex(r"\text{ts\_max}(\text{delta(close,1)}, 4) = \text{max}([0.10, 0.10, -0.80, 1.10])", font_size=22)
        ts_max_calc_text.next_to(delta_series_display, DOWN, buff=0.3)

        ts_max_result = MathTex(r"\text{ts\_max} = 1.10", font_size=24, color=YELLOW)
        ts_max_result.next_to(ts_max_calc_text, DOWN, buff=0.2)

        self.play(Write(step_title))
        self.play(Write(delta_series_intro), Write(delta_series_display))
        self.play(Write(ts_max_calc_text), Write(ts_max_result))
        self.wait(3)

        self.play(FadeOut(step_title), FadeOut(delta_series_intro), FadeOut(delta_series_display),
                  FadeOut(ts_max_calc_text), FadeOut(ts_max_result))

    def show_step4_intermediate_value(self, title_obj):
        step_title = Text("步骤4: 计算中间值 (intermediate_value)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        values_recap = Text(
            "已知: d1_today = 1.10, ts_min = -0.80, ts_max = 1.10",
            font_size=20
        )
        values_recap.next_to(step_title, DOWN, buff=0.4)

        condition1_text = Text("条件1: 0 < ts_min (0 < -0.80) ?", font_size=20)
        condition1_text.next_to(values_recap, DOWN, buff=0.3)
        condition1_result = Text("否", font_size=20, color=RED)
        condition1_result.next_to(condition1_text, RIGHT, buff=0.2)

        condition2_text = Text("条件2: ts_max < 0 (1.10 < 0) ?", font_size=20)
        condition2_text.next_to(condition1_text, DOWN, buff=0.2)
        condition2_result = Text("否", font_size=20, color=RED)
        condition2_result.next_to(condition2_text, RIGHT, buff=0.2)

        condition3_text = Text("否则 (条件1和2均不满足):", font_size=20)
        condition3_text.next_to(condition2_text, DOWN, buff=0.2)

        inter_calc = MathTex(r"\text{intermediate\_value} = -1 \times \text{d1\_today}", font_size=22)
        inter_calc.next_to(condition3_text, DOWN, buff=0.2)

        inter_result_calc = MathTex(r"\text{intermediate\_value} = -1 \times 1.10 = -1.10", font_size=24, color=GREEN)
        inter_result_calc.next_to(inter_calc, DOWN, buff=0.2)

        self.play(Write(step_title))
        self.play(Write(values_recap))
        self.play(Write(condition1_text), Write(condition1_result))
        self.wait(0.5)
        self.play(Write(condition2_text), Write(condition2_result))
        self.wait(0.5)
        self.play(Write(condition3_text))
        self.play(Write(inter_calc), Write(inter_result_calc))
        self.wait(3)

        self.play(FadeOut(step_title), FadeOut(values_recap),
                  FadeOut(condition1_text), FadeOut(condition1_result),
                  FadeOut(condition2_text), FadeOut(condition2_result),
                  FadeOut(condition3_text), FadeOut(inter_calc), FadeOut(inter_result_calc))

    def show_step5_rank(self, title_obj):
        step_title = Text("步骤5: 横截面排名 (rank)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        rank_formula = MathTex(r"\text{Alpha\#10} = \text{rank}(\text{intermediate\_value})", font_size=24)
        rank_formula.next_to(step_title, DOWN, buff=0.4)

        rank_explanation = Text(
            "将当日所有资产计算得到的 intermediate_value (-1.10 for asset_1)\n"
            "进行横向比较并排序，得到百分位排名。",
            font_size=20, line_spacing=1.2
        )
        rank_explanation.next_to(rank_formula, DOWN, buff=0.3)
        
        example_intermediate_values = Text(
            "示例 (假设当日所有资产的 intermediate_value):\n"
            "asset_1: -1.10\n"
            "asset_2: 0.80\n"
            "asset_3: -2.10\n"
            "asset_4: -1.80\n"
            "asset_5: 0.10",
            font_size=18, line_spacing=1.2, color=LIGHT_GRAY
        )
        example_intermediate_values.next_to(rank_explanation, DOWN, buff=0.3)


        rank_result = Text(
            "对这些值进行排名 (例如，值越小排名越高，再转换为百分比)\n"
            "asset_1 (-1.10) 的 Alpha#10 结果为: 0.60 (示例)",
            font_size=20, color=YELLOW, line_spacing=1.2
        )
        rank_result.next_to(example_intermediate_values, DOWN, buff=0.3)

        self.play(Write(rank_formula))
        self.play(Write(rank_explanation))
        self.play(Write(example_intermediate_values))
        self.play(Write(rank_result))
        self.wait(5)

        self.play(FadeOut(step_title), FadeOut(rank_formula), FadeOut(rank_explanation),
                  FadeOut(example_intermediate_values), FadeOut(rank_result))


    def show_final_result_alpha10(self, title_obj):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)

        result_box = Rectangle(width=7, height=3.5, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)

        result_text_header = Text("asset_1 在 2025-01-05 的 Alpha#10 值: 0.60", font_size=20, weight=BOLD)
        result_text_header.move_to(result_box.get_center() + UP * 1.2)

        result_text_body = Text(
            "intermediate_value = -1.10. 过去4日价格震荡，\n"
            "采取反转当日价格变动 (1.10) 的操作。\n"
            "该 intermediate_value 在当日所有资产中排名为0.60。",
            font_size=18, line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)

        summary_box = Rectangle(width=9, height=5, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#10 结合了短期市场状态判断与横截面排名。\n"
            "1. 观察过去4天价格变动，若持续上涨或下跌，则预期趋势持续。\n"
            "2. 若价格震荡，则预期当日趋势反转。\n"
            "3. 将此逻辑计算出的中间值在所有资产间排名，得到最终Alpha。\n"
            "Alpha值越高，表明该资产在该日基于此逻辑的信号越强。",
            font_size=18,
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
        self.wait(6)

        self.play(FadeOut(title_obj), FadeOut(final_title), FadeOut(summary_box), FadeOut(summary))

        # 片尾动画序列
        original_position = self.brand_watermark.get_center()
        original_scale = self.brand_watermark.get_height() / 22

        self.play(FadeOut(self.reference_watermark))
        self.wait(0.2)

        end_brand_text = self.brand_watermark
        end_brand_text.set_color(BLUE_D).set_weight(BOLD)

        self.play(
            end_brand_text.animate.move_to([0, 1, 0]).scale(3),
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
    # manim -pqh alpha10_visualization.py Alpha10Visualization
    pass 