#!/usr/bin/env python3
"""
Alpha#7 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha7_visualization.py Alpha7Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha7Visualization.mp4 --flush_cache

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

class Alpha7Visualization(Scene):
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
        
        # Alpha#7公式
        formula_title = Text("Alpha#7 条件性趋势反转因子", font_size=36, color=GREEN)
        formula_title.move_to([0, 2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#7} = \begin{cases} (-1 \times \text{ts\_rank}(\text{abs}(\text{delta}(\text{close}, 7)), 60)) \times \text{sign}(\text{delta}(\text{close}, 7)) & \text{if } \text{adv20} < \text{volume} \\ -1 & \text{otherwise} \end{cases}",
            font_size=28
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "基于成交量条件的价格趋势反转策略",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -1, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(3)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha7(self):
        headers = ["日期", "收盘价 (Close)", "成交量 (Volume)"]
        data_values = [
            ["2025-03-06", "90.20", "663704"],
            ["2025-03-07", "91.00", "330321"],
            ["2025-03-08", "89.50", "699867"],
            ["2025-03-09", "88.00", "538664"],
            ["2025-03-10", "87.50", "661218"],
            ["2025-03-11", "89.00", "618297"],
            ["2025-03-12", "90.20", "3514264"]  # Target row
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
        
        data_title = Text("示例数据 (asset_1, 2025-03-12)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha7()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.75)
        self.play(Create(data_table))

        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1):
            highlight_cells_group.add(data_table.get_highlighted_cell((8, col_idx), color=YELLOW))
        
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
        step_title = Text("步骤1: 计算20日平均成交量 (adv20)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(r"\text{adv20} = \frac{\sum_{i=1}^{20} \text{volume}_{t-i+1}}{20}", font_size=24)
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        description = Text(
            "计算截至2025-03-12的过去20日平均成交量。",
            font_size=20
        )
        description.next_to(formula_text, DOWN, buff=0.3)
        
        result_text = Text("示例计算结果 (asset_1, 2025-03-12):", font_size=20, color=YELLOW)
        result_text.next_to(description, DOWN, buff=0.3)
        
        adv20_value = MathTex(r"\text{adv20} = 962190.65", font_size=24, color=GREEN)
        adv20_value.next_to(result_text, DOWN, buff=0.2)
        
        self.play(Write(formula_text), Write(description))
        self.play(Write(result_text), Write(adv20_value))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description),
                  FadeOut(result_text), FadeOut(adv20_value))

    def show_step2(self, title_obj): 
        step_title = Text("步骤2: 成交量条件判断", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        condition_text = MathTex(r"\text{adv20} < \text{volume} ?", font_size=24)
        condition_text.next_to(step_title, DOWN, buff=0.4)
        
        data_text = Text("asset_1, 2025-03-12 数据:", font_size=20)
        data_text.next_to(condition_text, DOWN, buff=0.3)
        
        values_text = Text("adv20 = 962190.65, volume = 3514264", font_size=18, color=GREEN)
        values_text.next_to(data_text, DOWN, buff=0.2)
        
        result_text = Text("962190.65 < 3514264 为真", font_size=20, color=YELLOW)
        result_text.next_to(values_text, DOWN, buff=0.2)
        
        conclusion_text = Text("因此，执行趋势反转逻辑。", font_size=18, color=BLUE)
        conclusion_text.next_to(result_text, DOWN, buff=0.3)
        
        self.play(Write(step_title))
        self.play(Write(condition_text), Write(data_text))
        self.play(Write(values_text), Write(result_text))
        self.play(Write(conclusion_text))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(condition_text), FadeOut(data_text),
                  FadeOut(values_text), FadeOut(result_text), FadeOut(conclusion_text))

    def show_step3(self, title_obj): 
        step_title = Text("步骤3: 计算7日价格变动及方向", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        delta_formula = MathTex(r"\text{delta\_close\_7} = \text{close}_t - \text{close}_{t-7}", font_size=24)
        delta_formula.next_to(step_title, DOWN, buff=0.4)
        
        data_text = Text("asset_1, 2025-03-12 数据:", font_size=20)
        data_text.next_to(delta_formula, DOWN, buff=0.3)
        
        values_text = Text("close_t = 90.20, close_(t-7) = 90.20", font_size=18, color=GREEN)
        values_text.next_to(data_text, DOWN, buff=0.2)
        
        delta_result = MathTex(r"\text{delta\_close\_7} = 90.20 - 90.20 = 0.00", font_size=20, color=YELLOW)
        delta_result.next_to(values_text, DOWN, buff=0.2)
        
        sign_result = MathTex(r"\text{sign}(\text{delta\_close\_7}) = \text{sign}(0.00) = 0.00", font_size=20, color=YELLOW)
        sign_result.next_to(delta_result, DOWN, buff=0.2)
        
        self.play(Write(step_title))
        self.play(Write(delta_formula), Write(data_text))
        self.play(Write(values_text), Write(delta_result))
        self.play(Write(sign_result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(delta_formula), FadeOut(data_text),
                  FadeOut(values_text), FadeOut(delta_result), FadeOut(sign_result))

    def show_step4(self, title_obj): 
        step_title = Text("步骤4: 计算时间序列排名及最终Alpha值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        rank_formula = MathTex(r"\text{ts\_rank}(\text{abs}(\text{delta}(\text{close}, 7)), 60)", font_size=24)
        rank_formula.next_to(step_title, DOWN, buff=0.4)
        
        rank_description = Text(
            "计算过去60天内，7日价格变动绝对值的排名。",
            font_size=20
        )
        rank_description.next_to(rank_formula, DOWN, buff=0.3)
        
        rank_result = Text("asset_1, 2025-03-12 的排名值为 0.03", font_size=18, color=YELLOW)
        rank_result.next_to(rank_description, DOWN, buff=0.2)
        
        alpha_formula = MathTex(
            r"\text{Alpha\#7} = (-1 \times \text{ts\_rank}) \times \text{sign}(\text{delta\_close\_7})",
            font_size=24
        )
        alpha_formula.next_to(rank_result, DOWN, buff=0.3)
        
        alpha_calculation = MathTex(r"\text{Alpha\#7} = (-1 \times 0.03) \times 0.00 = 0.00", font_size=22, color=GREEN)
        alpha_calculation.next_to(alpha_formula, DOWN, buff=0.2)
        
        self.play(Write(step_title))
        self.play(Write(rank_formula), Write(rank_description))
        self.play(Write(rank_result), Write(alpha_formula))
        self.play(Write(alpha_calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(rank_formula), FadeOut(rank_description),
                  FadeOut(rank_result), FadeOut(alpha_formula), FadeOut(alpha_calculation))

    def show_final_result(self, title_obj):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=8, height=3, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text("asset_1 在 2025-03-12 的 Alpha#7 值: 0.00", font_size=20, weight=BOLD)
        result_text_header.move_to(result_box.get_center() + UP * 0.8)

        result_text_body = Text(
            "成交量条件满足，但价格无明显变动，信号为中性。",
            font_size=18, line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)
        
        summary_box = Rectangle(width=10, height=4.5, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#7 是一个条件性反转策略。\n"
            "当成交量显著放大时，策略对近期价格趋势采取反向操作。\n"
            "如果价格上涨明显，预期回调；如果下跌明显，预期反弹。\n"
            "成交量未放大时，策略固定输出负信号。",
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