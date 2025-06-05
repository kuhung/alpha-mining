#!/usr/bin/env python3
"""
Alpha#23 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha23_visualization.py Alpha23Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha23Visualization.mp4 --flush_cache
manim -qk alpha23_visualization.py Alpha23Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha23Visualization.mp4

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

class Alpha23Visualization(Scene):
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
        
        # Alpha#23公式
        formula_title = Text("Alpha#23 高价与移动平均的条件差分策略", font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#23} = \begin{cases} -1 \times \text{delta}(\text{high}, 2) & \text{if } \frac{\sum \text{high}_{20}}{20} < \text{high} \\ 0 & \text{otherwise} \end{cases}",
            font_size=24
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "当价格突破20日高价均线时，生成反转信号",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha23(self):
        headers = ["日期", "最高价 (High)", "20日均价", "2日差分", "Alpha#23"]
        data_values = [
            ["2025-01-01", "100.30", "99.85", "-", "-"],
            ["2025-01-02", "101.20", "99.92", "0.90", "-0.90"],
            ["2025-01-03", "101.80", "100.05", "0.60", "-0.60"],
            ["2025-01-04", "102.30", "100.25", "0.50", "-0.50"],
            ["2025-01-05", "102.90", "100.50", "0.60", "-0.60"] # Target row
        ]
        
        header_mobjects = [Text(h, font_size=16, weight=BOLD) for h in headers]

        table = Table(
            data_values,
            col_labels=header_mobjects,
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": WHITE},
            element_to_mobject=Text, 
            element_to_mobject_config={"font_size": 14},
            h_buff=0.4, 
            v_buff=0.2
        )
        return table

    def show_calculation_steps(self):
        steps_title = Text("计算步骤演示 (Alpha#23)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-01-05 Alpha#23)", font_size=26, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha23()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.80)
        self.play(Create(data_table))

        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((6, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title))
        
        calc_results = {
            'high': 102.90,
            'high_ma_20': 100.50,
            'delta_high_2': 0.60,
            'alpha23': -0.60
        }

        self.show_step1_moving_average(steps_title, calc_results)
        self.show_step2_condition_check(steps_title, calc_results)
        self.show_step3_delta_calculation(steps_title, calc_results)
        self.show_final_result(steps_title, calc_results)

    def show_step1_moving_average(self, title_obj, calc_results): 
        step_title = Text("步骤1: 计算20日高价移动平均", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{high\_ma\_20} = \frac{\sum \text{high}_{20}}{20}",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        result_text = Text(
            f"当日最高价: {calc_results['high']:.2f}\n"
            f"20日均价: {calc_results['high_ma_20']:.2f}",
            font_size=20, line_spacing=1.2
        )
        result_text.next_to(formula_text, DOWN, buff=0.3)
        
        self.play(Write(formula_text))
        self.play(Write(result_text))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(result_text))

    def show_step2_condition_check(self, title_obj, calc_results): 
        step_title = Text("步骤2: 条件判断", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        condition_text = MathTex(
            r"\text{high\_ma\_20} < \text{high}",
            font_size=24
        )
        condition_text.next_to(step_title, DOWN, buff=0.4)
        
        check_text = Text(
            f"{calc_results['high_ma_20']:.2f} < {calc_results['high']:.2f}\n"
            "条件成立，继续计算信号",
            font_size=20, line_spacing=1.2
        )
        check_text.next_to(condition_text, DOWN, buff=0.3)
        
        self.play(Write(condition_text))
        self.play(Write(check_text))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(condition_text), FadeOut(check_text))

    def show_step3_delta_calculation(self, title_obj, calc_results):
        step_title = Text("步骤3: 计算2日差分并生成信号", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{alpha23} = -1 \times \text{delta}(\text{high}, 2)",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        calculation = Text(
            f"2日差分: {calc_results['delta_high_2']:.2f}\n"
            f"最终信号: {calc_results['alpha23']:.2f}",
            font_size=20, line_spacing=1.2
        )
        calculation.next_to(formula_text, DOWN, buff=0.3)
        
        self.play(Write(formula_text))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(calculation))

    def show_final_result(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=11, height=3, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(
            f"asset_1 在 2025-01-05 的 Alpha#23 值: {calc_results['alpha23']:.2f}",
            font_size=20, weight=BOLD
        )
        result_text_header.move_to(result_box.get_center() + UP * 0.8)

        result_text_body = Text(
            "解读：价格突破20日高价均线，且近2日价格持续上涨。\n"
            "生成负向信号，预期价格可能出现回落。",
            font_size=18, line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)
        
        summary_box = Rectangle(width=12, height=4, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#23 是一个价格突破反转策略。\n"
            "当价格突破20日高价均线时，根据近期价格变动\n"
            "生成反向信号。策略假设价格在突破后可能回落，\n"
            "信号强度取决于近期价格变动幅度。",
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
    pass 