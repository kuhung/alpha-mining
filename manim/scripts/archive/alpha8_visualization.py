#!/usr/bin/env python3
"""
Alpha#8 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha8_visualization.py Alpha8Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha8Visualization.mp4 --flush_cache
manim -qk alpha8_visualization.py Alpha8Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha8Visualization.mp4 --flush_cache

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

class Alpha8Visualization(Scene):
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
        
        # Alpha#8公式
        formula_title = Text("Alpha#8 开盘价与回报率相关性变化因子", font_size=36, color=GREEN)
        formula_title.move_to([0, 2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#8} = -1 \times \text{rank}((\text{sum}(\text{open}, 5) \times \text{sum}(\text{returns}, 5)) - \text{delay}((\text{sum}(\text{open}, 5) \times \text{sum}(\text{returns}, 5)), 10))",
            font_size=28
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "捕捉开盘价与回报率短期相关性的变化趋势",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -1, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(3)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha8(self):
        headers = ["日期", "开盘价 (Open)", "回报率 (Returns)"]
        data_values = [
            ["2025-01-11", "99.58", "-0.0119"],
            ["2025-01-12", "100.42", "-0.003"],
            ["2025-01-13", "98.46", "-0.002"],
            ["2025-01-14", "98.54", "0.002"],
            ["2025-01-15", "99.38", "-0.0232"]
        ]
        
        header_mobjects = [Text(h, font_size=20, weight=BOLD) for h in headers]

        table = Table(
            data_values,
            col_labels=header_mobjects,
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": WHITE},
            element_to_mobject=Text, 
            element_to_mobject_config={"font_size": 16},
            h_buff=0.3,
            v_buff=0.25
        )
        return table

    def show_calculation_steps(self):
        steps_title = Text("计算步骤演示", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 2025-01-15)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha8()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.75)
        self.play(Create(data_table))

        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1):
            highlight_cells_group.add(data_table.get_highlighted_cell((6, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title))
        
        self.show_step1(steps_title)
        self.show_step2(steps_title)
        self.show_step3(steps_title)
        self.show_step4(steps_title)
        self.show_final_result(steps_title)

    def show_step1(self, title_obj): 
        step_title = Text("步骤1: 计算5日开盘价和回报率总和", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\begin{cases} \text{sum\_open\_5} = \sum_{i=1}^{5} \text{open}_{t-i+1} \\ \text{sum\_returns\_5} = \sum_{i=1}^{5} \text{returns}_{t-i+1} \end{cases}",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        description = Text(
            "计算截至2025-01-15的过去5日数据总和",
            font_size=20
        )
        description.next_to(formula_text, DOWN, buff=0.3)
        
        result_text = Text("示例计算结果 (asset_1, 2025-01-15):", font_size=20, color=YELLOW)
        result_text.next_to(description, DOWN, buff=0.3)
        
        values_text = Text(
            "sum_open_5 = 496.38\n"
            "sum_returns_5 = -0.04",
            font_size=18, color=GREEN
        )
        values_text.next_to(result_text, DOWN, buff=0.2)
        
        self.play(Write(formula_text), Write(description))
        self.play(Write(result_text), Write(values_text))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description),
                  FadeOut(result_text), FadeOut(values_text))

    def show_step2(self, title_obj): 
        step_title = Text("步骤2: 计算乘积及其10日延迟值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        formula_text = MathTex(
            r"\begin{cases} \text{product} = \text{sum\_open\_5} \times \text{sum\_returns\_5} \\ \text{delayed\_product} = \text{delay}(\text{product}, 10) \end{cases}",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        current_calc = Text(
            "当前乘积计算:\n"
            "product = 496.38 × (-0.04) = -19.86",
            font_size=18, color=GREEN
        )
        current_calc.next_to(formula_text, DOWN, buff=0.3)
        
        delayed_calc = Text(
            "10日前乘积值:\n"
            "delayed_product = 20.07",
            font_size=18, color=GREEN
        )
        delayed_calc.next_to(current_calc, DOWN, buff=0.2)
        
        diff_calc = Text(
            "差值计算:\n"
            "diff = -19.86 - 20.07 = -39.93",
            font_size=18, color=YELLOW
        )
        diff_calc.next_to(delayed_calc, DOWN, buff=0.2)
        
        self.play(Write(step_title))
        self.play(Write(formula_text))
        self.play(Write(current_calc), Write(delayed_calc))
        self.play(Write(diff_calc))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text),
                  FadeOut(current_calc), FadeOut(delayed_calc), FadeOut(diff_calc))

    def show_step3(self, title_obj): 
        step_title = Text("步骤3: 计算差值排名", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        formula_text = MathTex(r"\text{rank\_diff} = \text{rank}(\text{diff})", font_size=24)
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        data_text = Text(
            "当日各资产的差值 (示例):\n"
            "asset_1: -39.93\n"
            "asset_2: -20.19\n"
            "asset_3: 33.67\n"
            "asset_4: -43.91\n"
            "asset_5: 14.89",
            font_size=18, line_spacing=1.2
        )
        data_text.next_to(formula_text, DOWN, buff=0.3)
        
        rank_result = Text("asset_1 的 rank_diff = 0.4", font_size=20, color=YELLOW)
        rank_result.next_to(data_text, DOWN, buff=0.2)
        
        self.play(Write(step_title))
        self.play(Write(formula_text))
        self.play(Write(data_text))
        self.play(Write(rank_result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text),
                  FadeOut(data_text), FadeOut(rank_result))

    def show_step4(self, title_obj): 
        step_title = Text("步骤4: 计算最终Alpha值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        formula_text = MathTex(r"\text{Alpha\#8} = -1 \times \text{rank\_diff}", font_size=24)
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        calculation = MathTex(r"\text{Alpha\#8} = -1 \times 0.4", font_size=22)
        calculation.next_to(formula_text, DOWN, buff=0.3)
        
        result = MathTex(r"\text{Alpha\#8} = -0.4", font_size=24, color=GREEN)
        result.next_to(calculation, DOWN, buff=0.2)
        
        interpretation = Text(
            "负值表示相关性变化较强，\n"
            "预期价格与回报率的关系趋于稳定。",
            font_size=18, line_spacing=1.2, color=BLUE
        )
        interpretation.next_to(result, DOWN, buff=0.3)
        
        self.play(Write(step_title))
        self.play(Write(formula_text))
        self.play(Write(calculation))
        self.play(Write(result))
        self.play(Write(interpretation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text),
                  FadeOut(calculation), FadeOut(result), FadeOut(interpretation))

    def show_final_result(self, title_obj):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=8, height=3, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text("asset_1 在 2025-01-15 的 Alpha#8 值: -0.4", font_size=20, weight=BOLD)
        result_text_header.move_to(result_box.get_center() + UP * 0.8)

        result_text_body = Text(
            "开盘价与回报率的短期相关性变化较强，\n"
            "预期这种关系将趋于稳定。",
            font_size=18, line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)
        
        summary_box = Rectangle(width=10, height=4.5, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#8 通过分析开盘价与回报率的短期相关性变化，\n"
            "捕捉价格与回报率之间的动态关系。正的Alpha值表示相关性\n"
            "变化较弱，可能存在套利机会；负的Alpha值表示相关性变化\n"
            "较强，预期关系趋于稳定。该因子适合用于发现价格与回报率\n"
            "关系的异常变化，可用于均值回归策略。",
            font_size=18,
            line_spacing=1.3,
            color=RED
        )
        summary.move_to(summary_box.get_center())
        
        self.play(Write(final_title))
        self.play(Create(result_box))
        self.play(Write(result_text_header), Write(result_text_body))
        self.wait(3)
        
        self.play(FadeOut(result_box), FadeOut(result_text_header), FadeOut(result_text_body))
        self.play(Create(summary_box))
        self.play(Write(summary))
        self.wait(5)
        
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
    pass 