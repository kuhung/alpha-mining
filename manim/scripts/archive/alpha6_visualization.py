#!/usr/bin/env python3
"""
Alpha#6 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha6_visualization.py Alpha6Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha6Visualization.mp4 --flush_cache

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

class Alpha6Visualization(Scene):
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
        
        # Alpha#6公式
        formula_title = Text("Alpha#6 量价负相关因子", font_size=36, color=GREEN)
        formula_title.move_to([0, 2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#6} = -1 \times \text{correlation}(\text{open}, \text{volume}, 10)",
            font_size=32
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "计算开盘价与成交量10日滚动相关性的相反数",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -1, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(3)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha6(self):
        headers = ["日期", "开盘价 (Open)", "成交量 (Volume)"]
        data_values = [
            ["2025-01-01", "100.30", "690896"],
            ["2025-01-02", "100.53", "1236310"],
            ["2025-01-03", "100.88", "794092"],
            ["2025-01-04", "101.01", "1279416"],
            ["2025-01-05", "98.99", "1327947"],
            ["2025-01-06", "102.35", "1421350"],
            ["2025-01-07", "100.68", "2713351"],
            ["2025-01-08", "100.79", "594738"],
            ["2025-01-09", "100.71", "811805"],
            ["2025-01-10", "99.45", "1548483"] # Target row
        ]
        
        header_mobjects = [Text(h, font_size=20, weight=BOLD) for h in headers]

        table = Table(
            data_values,
            col_labels=header_mobjects,
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": WHITE},
            element_to_mobject=Text, 
            element_to_mobject_config={"font_size": 14}, # Reduced font size for longer numbers
            h_buff=0.3, # Adjusted h_buff for potentially wider volume column
            v_buff=0.25
        )
        return table

    def show_calculation_steps(self):
        steps_title = Text("计算步骤演示", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 10日窗口期数据)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha6()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.75) # Scale down slightly more if needed
        self.play(Create(data_table))

        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1):
            highlight_cells_group.add(data_table.get_highlighted_cell((11, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title))
        
        self.show_step1(steps_title)
        self.show_step2(steps_title)
        self.show_step3(steps_title)
        self.show_final_result(steps_title)

    def show_step1(self, title_obj): 
        step_title = Text("步骤1: 提取10日开盘价和成交量序列", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        open_data_text = Text("Open Prices (asset_1, 2025-01-01 to 2025-01-10):", font_size=20)
        open_data_text.next_to(step_title, DOWN, buff=0.4).align_to(step_title, LEFT)
        
        open_values = (
            "[100.30, 100.53, 100.88, 101.01, 98.99, \n"
            "102.35, 100.68, 100.79, 100.71, 99.45]"
        )
        open_data_values = Text(open_values, font_size=18, line_spacing=1.2, color=GREEN)
        open_data_values.next_to(open_data_text, DOWN, buff=0.2).align_to(open_data_text, LEFT)

        volume_data_text = Text("Volume (asset_1, 2025-01-01 to 2025-01-10):", font_size=20)
        volume_data_text.next_to(open_data_values, DOWN, buff=0.4).align_to(open_data_text, LEFT)
        
        volume_values = (
            "[690896, 1236310, 794092, 1279416, 1327947, \n"
            "1421350, 2713351, 594738, 811805, 1548483]"
        )
        volume_data_values = Text(volume_values, font_size=18, line_spacing=1.2, color=GREEN)
        volume_data_values.next_to(volume_data_text, DOWN, buff=0.2).align_to(volume_data_text, LEFT)
        
        self.play(Write(open_data_text), Write(open_data_values))
        self.play(Write(volume_data_text), Write(volume_data_values))
        self.wait(4)
        
        self.play(FadeOut(step_title), FadeOut(open_data_text), FadeOut(open_data_values),
                  FadeOut(volume_data_text), FadeOut(volume_data_values))

    def show_step2(self, title_obj): 
        step_title = Text("步骤2: 计算Open与Volume的10日相关系数", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        formula_text = MathTex(r"\text{corr} = \text{PearsonCorrelation}(\text{opens}_{10d}, \text{volumes}_{10d})", font_size=24)
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        description = Text(
            "使用步骤1中展示的两组10日数据序列，\n"
            "计算它们之间的皮尔逊相关系数。",
            font_size=20, line_spacing=1.2
        )
        description.next_to(formula_text, DOWN, buff=0.3)
        
        result_text = Text("示例计算结果 (asset_1, 2025-01-10):", font_size=20, color=YELLOW)
        result_text.next_to(description, DOWN, buff=0.3)
        
        correlation_value = MathTex(r"\text{correlation} \approx -0.03", font_size=24, color=GREEN)
        correlation_value.next_to(result_text, DOWN, buff=0.2)
        
        interpretation = Text(
            "负相关性(-0.03)表明在这10天内，\n"
            "开盘价和成交量整体上呈现轻微的反向变动趋势。",
            font_size=18, line_spacing=1.2, color=BLUE
        )
        interpretation.next_to(correlation_value, DOWN, buff=0.3)

        self.play(Write(step_title))
        self.play(Write(formula_text), Write(description))
        self.play(Write(result_text), Write(correlation_value))
        self.play(Write(interpretation))
        self.wait(4)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description),
                  FadeOut(result_text), FadeOut(correlation_value), FadeOut(interpretation))

    def show_step3(self, title_obj): 
        step_title = Text("步骤3: 将相关系数乘以 -1", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        formula_text = MathTex(r"\text{Alpha\#6} = -1 \times \text{correlation}", font_size=24)
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        calculation = MathTex(r"\text{Alpha\#6} = -1 \times (-0.03)", font_size=22)
        calculation.next_to(formula_text, DOWN, buff=0.3)
        
        result_value = MathTex(r"\text{Alpha\#6} = 0.03", font_size=24, color=GREEN)
        result_value.next_to(calculation, DOWN, buff=0.2)
        
        interpretation = Text(
            "最终Alpha值为0.03。正值表示原始相关性为负，\n"
            "即开盘价与成交量呈负相关。",
            font_size=18, line_spacing=1.2, color=BLUE
        )
        interpretation.next_to(result_value, DOWN, buff=0.3)

        self.play(Write(step_title))
        self.play(Write(formula_text), Write(calculation), Write(result_value))
        self.play(Write(interpretation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(calculation),
                  FadeOut(result_value), FadeOut(interpretation))

    def show_final_result(self, title_obj):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=11, height=3, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text("asset_1 在 2025-01-10 的 Alpha#6 值: 0.03", font_size=20, weight=BOLD)
        result_text_header.move_to(result_box.get_center() + UP * 0.8)

        result_text_body = Text(
            "这表明在该观察期内，开盘价与成交量呈现轻微的负相关性。\n"
            "例如，成交量增加时，开盘价可能略有下降，反之亦然。",
            font_size=18, line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)
        
        summary_box = Rectangle(width=12, height=4.5, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#6 旨在捕捉开盘价与成交量之间的短期负相关性。\n"
            "正的Alpha值表示价量负相关（如放量下跌开盘），\n"
            "负的Alpha值表示价量正相关（如放量上涨开盘）。\n"
            "该因子试图识别那些开盘时价量行为表现出\n"
            "特定反向模式的资产，可能预示着某种市场情绪或短期趋势。",
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