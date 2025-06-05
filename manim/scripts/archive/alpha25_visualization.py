#!/usr/bin/env python3
"""
Alpha#25 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha25_visualization.py Alpha25Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha25Visualization.mp4 --flush_cache
manim -qk alpha25_visualization.py Alpha25Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha25Visualization.mp4

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

class Alpha25Visualization(Scene):
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
        
        # Alpha#25公式
        formula_title = Text("Alpha#25 多因子综合排名策略", font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#25} = \text{rank}(((-1 \times \text{returns}) \times \text{adv20} \times \text{vwap} \times (\text{high} - \text{close})))",
            font_size=24
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "结合回报率、成交量、价格水平和日内波动的综合排名",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha25(self):
        headers = ["日期", "回报率", "20日均量", "VWAP", "最高价", "收盘价", "Alpha#25"]
        data_values = [
            ["2025-02-01", "-0.015", "1,105,200", "98.50", "99.20", "98.50", "0.6"],
            ["2025-02-02", "-0.025", "1,106,800", "99.30", "100.10", "99.20", "0.7"],
            ["2025-02-03", "-0.035", "1,108,400", "100.20", "101.30", "100.10", "0.8"],
            ["2025-02-04", "-0.045", "1,110,000", "101.40", "102.80", "101.30", "0.9"],
            ["2025-02-05", "-0.055", "1,111,600", "102.60", "104.50", "102.80", "1.0"] # Target row
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
        steps_title = Text("计算步骤演示 (Alpha#25)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-02-05 Alpha#25)", font_size=26, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha25()
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
            'returns': -0.055,
            'adv20': 1111600,
            'vwap': 102.60,
            'high': 104.50,
            'close': 102.80,
            'factor': 17611032.418,
            'alpha25': 1.0
        }

        self.show_step1_returns_volume(steps_title, calc_results)
        self.show_step2_price_diff(steps_title, calc_results)
        self.show_step3_factor_calc(steps_title, calc_results)
        self.show_step4_ranking(steps_title, calc_results)
        self.show_final_result(steps_title, calc_results)

    def show_step1_returns_volume(self, title_obj, calc_results): 
        step_title = Text("步骤1: 计算回报率反转与成交量因子", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{factor1} = (-1 \times \text{returns}) \times \text{adv20}",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        result_text = Text(
            f"回报率: {calc_results['returns']:.3f}\n"
            f"20日均量: {calc_results['adv20']:,.0f}",
            font_size=20, line_spacing=1.2
        )
        result_text.next_to(formula_text, DOWN, buff=0.3)
        
        self.play(Write(formula_text))
        self.play(Write(result_text))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(result_text))

    def show_step2_price_diff(self, title_obj, calc_results): 
        step_title = Text("步骤2: 计算价格水平与日内波动", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{factor2} = \text{vwap} \times (\text{high} - \text{close})",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        result_text = Text(
            f"VWAP: {calc_results['vwap']:.2f}\n"
            f"高收差价: {calc_results['high'] - calc_results['close']:.2f}",
            font_size=20, line_spacing=1.2
        )
        result_text.next_to(formula_text, DOWN, buff=0.3)
        
        self.play(Write(formula_text))
        self.play(Write(result_text))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(result_text))

    def show_step3_factor_calc(self, title_obj, calc_results):
        step_title = Text("步骤3: 计算综合因子值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{factor} = \text{factor1} \times \text{factor2}",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        calculation = Text(
            f"综合因子值: {calc_results['factor']:.2f}",
            font_size=20, line_spacing=1.2
        )
        calculation.next_to(formula_text, DOWN, buff=0.3)
        
        self.play(Write(formula_text))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(calculation))

    def show_step4_ranking(self, title_obj, calc_results):
        step_title = Text("步骤4: 因子值排名标准化", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{alpha25} = \text{rank}(\text{factor})",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        result_text = Text(
            f"排名值: {calc_results['alpha25']:.1f}\n"
            "(在所有资产中排名最高)",
            font_size=20, line_spacing=1.2
        )
        result_text.next_to(formula_text, DOWN, buff=0.3)
        
        self.play(Write(formula_text))
        self.play(Write(result_text))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(result_text))

    def show_final_result(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=11, height=3, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(
            f"asset_1 在 2025-02-05 的 Alpha#25 值: {calc_results['alpha25']:.1f}",
            font_size=20, weight=BOLD
        )
        result_text_header.move_to(result_box.get_center() + UP * 0.8)

        result_text_body = Text(
            "解读：负回报率、高成交量、高价格水平和大日内波动\n"
            "综合表现最强，获得最高排名。",
            font_size=18, line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)
        
        summary_box = Rectangle(width=12, height=4, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#25 是一个多因子综合排名策略。\n"
            "通过结合回报率反转、成交量、价格水平和日内波动，\n"
            "构建综合因子，并通过排名实现跨资产标准化。\n"
            "策略偏好高流动性、价格回落和可能反转的资产。",
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