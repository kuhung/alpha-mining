#!/usr/bin/env python3
"""
Alpha#24 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha24_visualization.py Alpha24Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha24Visualization.mp4 --flush_cache
manim -qk alpha24_visualization.py Alpha24Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha24Visualization.mp4

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

class Alpha24Visualization(Scene):
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
        
        # Alpha#24公式
        formula_title = Text("Alpha#24 价格变化率与历史最小值的条件选择策略", font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#24} = \begin{cases} -1 \times (close - \text{ts\_min}(close, 100)) & \text{if } \frac{\Delta MA_{100}}{close_{t-100}} \leq 0.05 \\ -1 \times \Delta close_3 & \text{otherwise} \end{cases}",
            font_size=24
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "根据价格变化率自适应选择信号生成方式",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha24(self):
        headers = ["日期", "收盘价", "100日均价", "变化率", "最小价", "3日差分", "Alpha#24"]
        data_values = [
            ["2025-02-01", "98.50", "97.80", "0.03", "95.20", "1.20", "-1.20"],
            ["2025-02-02", "99.20", "97.95", "0.04", "95.20", "1.50", "-1.50"],
            ["2025-02-03", "100.10", "98.15", "0.06", "95.20", "1.80", "-1.80"],
            ["2025-02-04", "101.30", "98.40", "0.07", "95.20", "2.10", "-2.10"],
            ["2025-02-05", "102.80", "98.70", "0.08", "95.20", "2.70", "-2.70"] # Target row
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
        steps_title = Text("计算步骤演示 (Alpha#24)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-02-05 Alpha#24)", font_size=26, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha24()
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
            'close': 102.80,
            'ma_100': 98.70,
            'change_rate': 0.08,
            'min_close_100': 95.20,
            'delta_close_3': 2.70,
            'alpha24': -2.70
        }

        self.show_step1_change_rate(steps_title, calc_results)
        self.show_step2_condition_check(steps_title, calc_results)
        self.show_step3_signal_generation(steps_title, calc_results)
        self.show_final_result(steps_title, calc_results)

    def show_step1_change_rate(self, title_obj, calc_results): 
        step_title = Text("步骤1: 计算100日均价变化率", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{change\_rate} = \frac{\Delta MA_{100}}{close_{t-100}}",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        result_text = Text(
            f"100日均价: {calc_results['ma_100']:.2f}\n"
            f"变化率: {calc_results['change_rate']:.2f}",
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
            r"\text{change\_rate} \leq 0.05",
            font_size=24
        )
        condition_text.next_to(step_title, DOWN, buff=0.4)
        
        check_text = Text(
            f"{calc_results['change_rate']:.2f} > 0.05\n"
            "条件不成立，使用3日差分策略",
            font_size=20, line_spacing=1.2
        )
        check_text.next_to(condition_text, DOWN, buff=0.3)
        
        self.play(Write(condition_text))
        self.play(Write(check_text))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(condition_text), FadeOut(check_text))

    def show_step3_signal_generation(self, title_obj, calc_results):
        step_title = Text("步骤3: 生成信号", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{alpha24} = -1 \times \Delta close_3",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        calculation = Text(
            f"3日差分: {calc_results['delta_close_3']:.2f}\n"
            f"最终信号: {calc_results['alpha24']:.2f}",
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
            f"asset_1 在 2025-02-05 的 Alpha#24 值: {calc_results['alpha24']:.2f}",
            font_size=20, weight=BOLD
        )
        result_text_header.move_to(result_box.get_center() + UP * 0.8)

        result_text_body = Text(
            "解读：由于价格变化率大于5%，采用3日差分策略。\n"
            "近3日价格持续上涨，生成较强的负向信号。",
            font_size=18, line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)
        
        summary_box = Rectangle(width=12, height=4, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#24 根据市场环境自适应选择策略。\n"
            "在低波动环境下（变化率≤5%）关注价格与历史最低点的距离，\n"
            "在高波动环境下（变化率>5%）关注短期价格变化。\n"
            "这种自适应机制有助于在不同市场环境下保持策略有效性。",
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