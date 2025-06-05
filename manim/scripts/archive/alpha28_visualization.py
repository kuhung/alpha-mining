 #!/usr/bin/env python3
"""
Alpha#28 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha28_visualization.py Alpha28Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha28Visualization.mp4 --flush_cache
manim -qk alpha28_visualization.py Alpha28Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha28Visualization.mp4

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

class Alpha28Visualization(Scene):
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
        
        # Alpha#28公式
        formula_title_text = "Alpha#28: 成交量最低价相关性与价格中枢偏离的标准化"
        formula_title = Text(formula_title_text, font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#28} = \text{scale}((\text{correlation}(\text{adv20}, \text{low}, 5) + ((\text{high} + \text{low}) / 2)) - \text{close})",
            font_size=28
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "捕捉成交量与最低价的相关性，结合价格中枢偏离度",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha28(self):
        headers = ["日期", "最低价 (L)", "最高价 (H)", "收盘价 (C)", "adv20"]
        # Data for asset_1, 2025-01-05 calculation
        data_values = [
            ["2025-01-03", "98.69", "100.58", "100.50", "1,389,671.40"],
            ["2025-01-04", "97.20", "99.40", "97.90", "1,389,671.40"],
            ["2025-01-05", "98.50", "100.20", "100.50", "1,389,671.40"]  # Target row
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

    def show_calculation_steps(self):
        steps_title = Text("计算步骤演示 (Alpha#28)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-01-05 Alpha#28)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha28()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.85)
        self.play(Create(data_table))

        # Highlight the target row (2025-01-05)
        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((4, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title))
        
        # Store calculated values to pass between steps
        calc_results = {
            'correlation_adv20_low_5': 0.65,
            'mid_price': 99.35,
            'close_price': 100.50,
            'raw_alpha': -0.50,
            'alpha28': -0.61
        }

        self.show_step1_correlation(steps_title, calc_results)
        self.show_step2_mid_price(steps_title, calc_results)
        self.show_step3_price_deviation(steps_title, calc_results)
        self.show_step4_scale(steps_title, calc_results)
        self.show_final_result_alpha28(steps_title, calc_results)

    def show_step1_correlation(self, title_obj, calc_results): 
        step_title = Text("步骤1: 计算 correlation(adv20, low, 5)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        intro_text = Text(
            "计算20日平均成交量与最低价在过去5日的相关系数",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        correlation_result = MathTex(
            r"\text{correlation\_adv20\_low\_5} = " + f"{calc_results['correlation_adv20_low_5']:.2f}", 
            font_size=24, color=YELLOW
        )
        correlation_result.next_to(intro_text, DOWN, buff=0.3)
        
        self.play(Write(intro_text))
        self.play(Write(correlation_result))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(correlation_result))

    def show_step2_mid_price(self, title_obj, calc_results): 
        step_title = Text("步骤2: 计算中间价格 (high + low) / 2", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        formula_text = MathTex(
            r"\text{mid\_price} = (\text{high} + \text{low}) / 2", 
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        calculation = MathTex(
            r"\text{mid\_price} = (100.20 + 98.50) / 2 = " + f"{calc_results['mid_price']:.2f}",
            font_size=24, color=YELLOW
        )
        calculation.next_to(formula_text, DOWN, buff=0.3)
        
        self.play(Write(step_title))
        self.play(Write(formula_text))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(calculation))

    def show_step3_price_deviation(self, title_obj, calc_results):
        step_title = Text("步骤3: 计算价格偏离度", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{raw\_alpha} = \text{correlation} + \text{mid\_price} - \text{close}", 
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.3)
        
        calculation = MathTex(
            f"{calc_results['correlation_adv20_low_5']:.2f} + {calc_results['mid_price']:.2f} - {calc_results['close_price']:.2f} = {calc_results['raw_alpha']:.2f}",
            font_size=24, color=YELLOW
        )
        calculation.next_to(formula_text, DOWN, buff=0.3)
        
        self.play(Write(formula_text))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(calculation))
        
    def show_step4_scale(self, title_obj, calc_results):
        step_title = Text("步骤4: 标准化处理 scale", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        intro_text = Text(
            "对所有资产的raw_alpha进行横截面标准化处理，\n"
            "使其均值为0，标准差为1。",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        calculation = MathTex(
            r"\text{alpha28} = \text{scale}(" + f"{calc_results['raw_alpha']:.2f}) = {calc_results['alpha28']:.2f}", 
            font_size=24, color=GREEN
        )
        calculation.next_to(intro_text, DOWN, buff=0.3)
        
        self.play(Write(intro_text))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(calculation))

    def show_final_result_alpha28(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=9, height=4.5, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(f"asset_1 在 2025-01-05 的 Alpha#28 值: {calc_results['alpha28']:.2f}", font_size=20, weight=BOLD)
        result_text_header.move_to(result_box.get_center() + UP * 1.5)

        result_text_body = Text(
            f"解读:\n"
            f"• 成交量与最低价呈正相关 ({calc_results['correlation_adv20_low_5']:.2f})\n"
            f"• 中间价 ({calc_results['mid_price']:.2f}) 低于收盘价 ({calc_results['close_price']:.2f})\n"
            f"• 原始Alpha值为 {calc_results['raw_alpha']:.2f}\n"
            f"• 标准化后的Alpha值为 {calc_results['alpha28']:.2f}",
            font_size=16,
            line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)

        summary_box = Rectangle(width=10, height=5, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#28 通过组合三个关键信号：\n"
            "1. 成交量与最低价的相关性\n"
            "2. 价格中枢水平\n"
            "3. 收盘价偏离度\n"
            "负的 Alpha 值表示资产可能处于相对高估状态，\n"
            "或存在潜在的下行压力。",
            font_size=17,
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
        self.wait(5)
        
        self.play(FadeOut(title_obj), FadeOut(final_title), FadeOut(summary_box), FadeOut(summary))

        # 片尾动画序列
        self.play(FadeOut(self.reference_watermark), run_time=0.5)
        
        end_brand_text = self.brand_watermark 
        end_brand_text.set_color(BLUE_D).set_weight(BOLD)
        
        self.play(
            end_brand_text.animate.move_to([0, 1, 0]).scale(3),
            run_time=1.0
        )

        series_title = Text("101量化因子研究系列", font_size=36, color=BLUE_D, weight=BOLD)
        series_title.next_to(self.brand_watermark, DOWN, buff=0.5)
        self.play(Write(series_title))
        self.wait(0.2)

        cta_text = Text("点赞👍 关注🔔 转发🚀", font_size=20, color=WHITE, font="Apple Color Emoji")
        cta_text.next_to(series_title, DOWN, buff=0.8)

        self.play(Write(cta_text), run_time=1.5)
        self.wait(3)

if __name__ == "__main__":
    # This script is intended to be run with Manim.
    # To render, use a command like:
    # manim -pqh alpha28_visualization.py Alpha28Visualization
    pass 