#!/usr/bin/env python3
"""
Alpha#20 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha20_visualization.py Alpha20Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha20Visualization.mp4 --flush_cache
manim -qk alpha20_visualization.py Alpha20Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha20Visualization.mp4

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

class Alpha20Visualization(Scene):
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
        
        # Alpha#20公式
        formula_title_text = "Alpha#20: 开盘价与昨日价格关键点位差异的综合排名"
        formula_title = Text(formula_title_text, font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#20} = (((-1 \times \text{rank}(\text{open} - \text{delay}(\text{high}, 1))) \times \text{rank}(\text{open} - \text{delay}(\text{close}, 1))) \times \text{rank}(\text{open} - \text{delay}(\text{low}, 1)))",
            font_size=28
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "通过开盘价与昨日高低收价格的差异排名组合来预测市场走势",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha20(self):
        headers = ["日期", "开盘价 (O)", "昨日高 (pH)", "昨日收 (pC)", "昨日低 (pL)"]
        # Data for asset_1 from 2025-01-24 (based on README.md example)
        data_values = [
            ["2025-01-24", "97.20", "98.50", "97.80", "97.00"]  # Target row
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
        steps_title = Text("计算步骤演示 (Alpha#20)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-01-24 Alpha#20)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha20()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.85)
        self.play(Create(data_table))

        # Highlight the target row (2025-01-24)
        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((2, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title))
        
        # Store calculated values to pass between steps
        calc_results = {
            'diff_open_prev_high': -1.30,
            'diff_open_prev_close': -0.60,
            'diff_open_prev_low': 0.20,
            'rank_diff_oph': 0.300,
            'rank_diff_opc': 0.400,
            'rank_diff_opl': 0.600,
            'component_a': -0.300,
            'component_b': 0.400,
            'component_c': 0.600,
            'alpha20': -0.072
        }

        self.show_step1_price_differences(steps_title, calc_results)
        self.show_step2_rank_differences(steps_title, calc_results)
        self.show_step3_final_alpha(steps_title, calc_results)
        self.show_final_result_alpha20(steps_title, calc_results)

    def show_step1_price_differences(self, title_obj, calc_results): 
        step_title = Text("步骤1: 计算开盘价与昨日价格的差异", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        intro_text = Text(
            "计算当日开盘价与昨日最高价、收盘价、最低价的差值：",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        calculation = VGroup(
            Text(f"开盘价与昨日最高价差异 = 97.20 - 98.50 = {calc_results['diff_open_prev_high']:.2f}", font_size=18),
            Text(f"开盘价与昨日收盘价差异 = 97.20 - 97.80 = {calc_results['diff_open_prev_close']:.2f}", font_size=18),
            Text(f"开盘价与昨日最低价差异 = 97.20 - 97.00 = {calc_results['diff_open_prev_low']:.2f}", font_size=18)
        ).arrange(DOWN, buff=0.2)
        calculation.next_to(intro_text, DOWN, buff=0.3)
        
        self.play(Write(intro_text))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(calculation))

    def show_step2_rank_differences(self, title_obj, calc_results): 
        step_title = Text("步骤2: 计算差异值的市场排名", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        intro_text = Text(
            "对每个差异值在所有资产中进行百分位排名：",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        calculation = VGroup(
            Text(f"rank(开盘价-昨日最高价) = {calc_results['rank_diff_oph']:.3f}", font_size=18),
            Text(f"rank(开盘价-昨日收盘价) = {calc_results['rank_diff_opc']:.3f}", font_size=18),
            Text(f"rank(开盘价-昨日最低价) = {calc_results['rank_diff_opl']:.3f}", font_size=18)
        ).arrange(DOWN, buff=0.2)
        calculation.next_to(intro_text, DOWN, buff=0.3)
        
        self.play(Write(step_title))
        self.play(Write(intro_text))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(calculation))
        
    def show_step3_final_alpha(self, title_obj, calc_results):
        step_title = Text("步骤3: 计算最终 Alpha#20 值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_recap = MathTex(r"\text{Alpha\#20} = (-1 \times \text{rank\_diff\_oph}) \times \text{rank\_diff\_opc} \times \text{rank\_diff\_opl}", font_size=24)
        formula_recap.next_to(step_title, DOWN, buff=0.4)
        
        values_text = Text(
            f"component_a = -1 × {calc_results['rank_diff_oph']:.3f} = {calc_results['component_a']:.3f}\n"
            f"component_b = {calc_results['rank_diff_opc']:.3f}\n"
            f"component_c = {calc_results['rank_diff_opl']:.3f}",
            font_size=20, line_spacing=1.2
        )
        values_text.next_to(formula_recap, DOWN, buff=0.3)
        
        calculation_final = MathTex(
            f"\\text{{Alpha\#20}} = {calc_results['component_a']:.3f} \\times {calc_results['component_b']:.3f} \\times {calc_results['component_c']:.3f} = {calc_results['alpha20']:.3f}", 
            font_size=24, color=GREEN
        )
        calculation_final.next_to(values_text, DOWN, buff=0.2)
        
        self.play(Write(formula_recap), Write(values_text))
        self.play(Write(calculation_final))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_recap), FadeOut(values_text), FadeOut(calculation_final))

    def show_final_result_alpha20(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=9, height=4.5, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(f"asset_1 在 2025-01-24 的 Alpha#20 值: {calc_results['alpha20']:.3f}", font_size=20, weight=BOLD)
        result_text_header.move_to(result_box.get_center() + UP * 1.5)

        result_text_body = Text(
            f"解读 (asset_1, 2025-01-24):\n"
            f"• 开盘价低于昨日最高价 ({calc_results['diff_open_prev_high']:.2f})\n"
            f"• 开盘价低于昨日收盘价 ({calc_results['diff_open_prev_close']:.2f})\n"
            f"• 开盘价高于昨日最低价 ({calc_results['diff_open_prev_low']:.2f})\n"
            f"• 三个排名值分别为{calc_results['rank_diff_oph']:.1%}、{calc_results['rank_diff_opc']:.1%}和{calc_results['rank_diff_opl']:.1%}",
            font_size=16,
            line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)

        summary_box = Rectangle(width=10, height=5, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#20 通过分析开盘价相对于昨日价格的位置：\n"
            "1. 开盘价与昨日最高价的差异（反转信号）\n"
            "2. 开盘价与昨日收盘价的差异（跳空程度）\n"
            "3. 开盘价与昨日最低价的差异（价格强度）\n"
            "负的 Alpha 值表示资产可能处于价格调整阶段，\n"
            "但调整幅度相对温和。",
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
    # manim -pqh alpha20_visualization.py Alpha20Visualization
    pass 