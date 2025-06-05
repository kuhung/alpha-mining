#!/usr/bin/env python3
"""
Alpha#27 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha27_visualization.py Alpha27Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha27Visualization.mp4 --flush_cache
manim -qk alpha27_visualization.py Alpha27Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha27Visualization.mp4

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

class Alpha27Visualization(Scene):
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
        
        # Alpha#27公式
        formula_title = Text("Alpha#27 成交量与均价排名相关性趋势因子", font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#27} = \begin{cases} -1 & \text{if } 0.5 < \text{rank}(\frac{\sum \text{correlation}(\text{rank}(\text{volume}), \text{rank}(\text{vwap}), 6)}{2}) \\ 1 & \text{otherwise} \end{cases}",
            font_size=24
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "通过分析成交量和均价的排名相关性来判断市场趋势",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha27(self):
        headers = ["日期", "成交量", "VWAP", "Alpha#27"]
        data_values = [
            ["2025-01-03", "794,092", "100.39", "1.0"],
            ["2025-01-04", "1,279,416", "100.42", "1.0"],
            ["2025-01-05", "1,327,947", "100.40", "1.0"],
            ["2025-01-06", "1,421,350", "101.42", "1.0"],
            ["2025-01-07", "2,713,351", "101.60", "-1.0"]
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
        steps_title = Text("计算步骤演示 (Alpha#27)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-01-07 Alpha#27)", font_size=26, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha27()
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
            'volume': 2713351,
            'vwap': 101.60,
            'volume_rank': 0.8,
            'vwap_rank': 0.75,
            'correlation': 0.52,
            'rank_result': 0.6,
            'alpha27': -1.0
        }

        self.show_step1_rank_calculation(steps_title, calc_results)
        self.show_step2_correlation(steps_title, calc_results)
        self.show_step3_final_rank(steps_title, calc_results)
        self.show_final_result(steps_title, calc_results)

    def show_step1_rank_calculation(self, title_obj, calc_results): 
        step_title = Text("步骤1: 计算横截面排名", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{rank}(\text{volume}), \text{rank}(\text{vwap})",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        result_text = Text(
            f"成交量排名: {calc_results['volume_rank']:.2f}\n"
            f"VWAP排名: {calc_results['vwap_rank']:.2f}",
            font_size=20, line_spacing=1.2
        )
        result_text.next_to(formula_text, DOWN, buff=0.3)
        
        self.play(Write(formula_text))
        self.play(Write(result_text))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(result_text))

    def show_step2_correlation(self, title_obj, calc_results): 
        step_title = Text("步骤2: 计算6日相关系数并求和", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\frac{\sum \text{correlation}(\text{volume\_rank}, \text{vwap\_rank}, 6)}{2}",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        result_text = Text(
            f"相关系数: {calc_results['correlation']:.2f}\n"
            "显示较强的正相关性",
            font_size=20, line_spacing=1.2
        )
        result_text.next_to(formula_text, DOWN, buff=0.3)
        
        self.play(Write(formula_text))
        self.play(Write(result_text))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(result_text))

    def show_step3_final_rank(self, title_obj, calc_results):
        step_title = Text("步骤3: 最终排名与信号生成", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(
            r"\text{alpha27} = \begin{cases} -1 & \text{if } 0.5 < \text{rank\_result} \\ 1 & \text{otherwise} \end{cases}",
            font_size=24
        )
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        calculation = Text(
            f"最终排名: {calc_results['rank_result']:.2f} > 0.5\n"
            f"生成信号: {calc_results['alpha27']:.0f}",
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
            f"asset_1 在 2025-01-07 的 Alpha#27 值: {calc_results['alpha27']:.0f}",
            font_size=20, weight=BOLD
        )
        result_text_header.move_to(result_box.get_center() + UP * 0.8)

        result_text_body = Text(
            "解读：成交量和均价排名高度相关，且相关性排名高于0.5，\n"
            "生成负向信号，预示当前趋势可能即将减弱。",
            font_size=18, line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)
        
        summary_box = Rectangle(width=12, height=4, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#27 通过分析成交量和均价的排名相关性\n"
            "来判断市场趋势。当相关性排名较高时，生成负向信号，\n"
            "反之生成正向信号。这种机制有助于捕捉市场趋势的\n"
            "持续性和可能的转折点。",
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