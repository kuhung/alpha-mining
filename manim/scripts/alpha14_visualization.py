#!/usr/bin/env python3
"""
Alpha#14 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha14_visualization.py Alpha14Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha14Visualization.mp4 --flush_cache
manim -qk alpha14_visualization.py Alpha14Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha14Visualization.mp4

提示:
- `-pql` : 预览并使用低质量渲染 (加快速度). 可选: `-pqm` (中等), `-pqh` (高).
- `-o YOUR_ABSOLUTE_PATH_TO_PROJECT/manim/outputs/YourSceneName.mp4`: 指定输出文件的绝对路径和名称.
- `--flush_cache`: 移除缓存的片段电影文件.
- 查看您版本的所有可用选项: `manim render --help`
"""

from manim import *
import numpy as np
# import pandas as pd # Not strictly needed for this script's logic, data is hardcoded

# 配置中文字体
config.font = "PingFang SC"

class Alpha14Visualization(Scene):
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
        
        # Alpha#14公式
        formula_title_text = "Alpha#14: 收益率变动排名与开盘价成交量相关性的组合因子"
        formula_title = Text(formula_title_text, font_size=28, color=GREEN) # Adjusted font size for longer title
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#14} = ((-1 \times \text{rank}(\text{delta}(\text{returns}, 3))) \times \text{correlation}(\text{open}, \text{volume}, 10))",
            font_size=26 # Adjusted font size
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "结合收益率变动排名和价量历史相关性的复合因子",
            font_size=26, # Adjusted font size
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0]) # Adjusted position
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha14(self):
        headers = ["日期", "开盘价 (O)", "成交量 (V)", "收益率 (R)"]
        # Data for asset_1, relevant for 2025-01-10 calculation
        data_values = [
            ["2025-01-07", "100.68", "2,713,351", "0.0139"], # returns_t-3
            ["2025-01-08", "100.79", "594,738",  "-0.0206"],
            ["2025-01-09", "100.71", "811,805",  "0.0010"],
            ["2025-01-10", "99.45", "1,548,483", "0.0060"]  # Target row (returns_t)
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
        steps_title = Text("计算步骤演示 (Alpha#14)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-01-10 Alpha#14)", font_size=26, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha14()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.80) # Adjusted scale
        self.play(Create(data_table))

        # Highlight the target row (2025-01-10), which is the 4th data row, mobject table row 5.
        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((5, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        
        corr_note = Text(
            "注: correlation(open, volume, 10) 使用 asset_1 从 2025-01-01 至 2025-01-10 的数据。",
            font_size=16, color=GRAY
        )
        corr_note.next_to(data_table, DOWN, buff=0.3)
        self.play(Write(corr_note))
        self.wait(2.5) # Wait a bit longer to read the note

        self.play(FadeOut(data_table), FadeOut(data_title), FadeOut(corr_note), FadeOut(highlight_cells_group))
        
        calc_results = {
            'returns_today': 0.0060,
            'returns_3_days_ago': 0.0139,
            'delta_returns_3': -0.0079,
            'rank_delta_returns_3': 0.8000,
            'neg_rank_delta_returns_3': -0.8000,
            'corr_open_volume_10': -0.0347,
            'alpha14_raw': 0.02776,
            'alpha14_formatted': "0.028" 
        }

        self.show_step1_delta_returns(steps_title, calc_results)
        self.show_step2_rank_delta_returns(steps_title, calc_results)
        self.show_step3_neg_rank(steps_title, calc_results)
        self.show_step4_correlation_open_volume(steps_title, calc_results)
        self.show_step5_final_alpha(steps_title, calc_results)
        self.show_final_result_alpha14(steps_title, calc_results)

    def show_step1_delta_returns(self, title_obj, calc_results): 
        step_title = Text("步骤1: 计算 delta(returns, 3)", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_text = MathTex(r"\text{delta}(\text{returns}, 3)_t = \text{returns}_t - \text{returns}_{t-3}", font_size=24)
        formula_text.next_to(step_title, DOWN, buff=0.4)
        
        description = Text(
            f"returns (2025-01-10) = {calc_results['returns_today']:.4f}\n"
            f"returns (2025-01-07, 3日前) = {calc_results['returns_3_days_ago']:.4f}",
            font_size=18, line_spacing=1.2
        )
        description.next_to(formula_text, DOWN, buff=0.3)
        
        calculation = MathTex(
            f"\\text{{delta\_returns\_3}} = {calc_results['returns_today']:.4f} - {calc_results['returns_3_days_ago']:.4f} = {calc_results['delta_returns_3']:.4f}",
            font_size=22, color=GREEN
        )
        calculation.next_to(description, DOWN, buff=0.2)
        
        self.play(Write(formula_text), Write(description))
        self.play(Write(calculation))
        self.wait(3.5)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(description), FadeOut(calculation))

    def show_step2_rank_delta_returns(self, title_obj, calc_results): 
        step_title = Text("步骤2: 计算 rank(delta(returns, 3))", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        intro_text = Text(
            f"将 asset_1 在 2025-01-10 的 delta_returns_3 ({calc_results['delta_returns_3']:.4f})\n"
            "与当日所有其他资产的 delta_returns_3 进行横截面百分比排名\n"
            "(升序排名, 即值越小排名越靠前，越接近0)。",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        rank_result_text = MathTex(
            r"\text{rank\_delta\_returns\_3} = " + f"{calc_results['rank_delta_returns_3']:.4f}", 
            font_size=24, color=YELLOW
        )
        rank_result_text.next_to(intro_text, DOWN, buff=0.3)
        
        self.play(Write(step_title))
        self.play(Write(intro_text))
        self.play(Write(rank_result_text))
        self.wait(4.5)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(rank_result_text))

    def show_step3_neg_rank(self, title_obj, calc_results):
        step_title = Text("步骤3: 计算 -1 * rank(delta(returns, 3))", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        
        formula_text = MathTex(r"\text{neg\_rank} = -1 \times \text{rank\_delta\_returns\_3}", font_size=24)
        formula_text.next_to(step_title, DOWN, buff=0.4)

        calculation = MathTex(
            f"\\text{{neg\_rank}} = -1 \\times {calc_results['rank_delta_returns_3']:.4f} = {calc_results['neg_rank_delta_returns_3']:.4f}",
            font_size=24, color=YELLOW
        )
        calculation.next_to(formula_text, DOWN, buff=0.3)
        
        self.play(Write(step_title))
        self.play(Write(formula_text))
        self.play(Write(calculation))
        self.wait(3.5)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(calculation))

    def show_step4_correlation_open_volume(self, title_obj, calc_results):
        step_title = Text("步骤4: 计算 correlation(open, volume, 10)", font_size=26, color=ORANGE) # Adjusted font size
        step_title.next_to(title_obj, DOWN, buff=0.5)

        intro_text = Text(
            "计算 asset_1 过去10日 (截至 2025-01-10) 的每日开盘价 (open)\n"
            "与每日成交量 (volume) 序列之间的皮尔逊相关系数。",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        corr_result_text = MathTex(
            r"\text{corr\_open\_volume\_10} = " + f"{calc_results['corr_open_volume_10']:.4f}", 
            font_size=24, color=YELLOW
        )
        corr_result_text.next_to(intro_text, DOWN, buff=0.3)
        
        self.play(Write(step_title))
        self.play(Write(intro_text))
        self.play(Write(corr_result_text))
        self.wait(4.5)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(corr_result_text))
        
    def show_step5_final_alpha(self, title_obj, calc_results):
        step_title = Text("步骤5: 计算最终 Alpha#14 值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        formula_recap = MathTex(
            r"\text{Alpha\#14} = \text{neg\_rank\_delta\_returns\_3} \times \text{corr\_open\_volume\_10}", 
            font_size=24
        )
        formula_recap.next_to(step_title, DOWN, buff=0.4)
        
        values_text = Text(
            f"neg_rank_delta_returns_3 = {calc_results['neg_rank_delta_returns_3']:.4f}\n"
            f"corr_open_volume_10 = {calc_results['corr_open_volume_10']:.4f}",
            font_size=20, line_spacing=1.2
        )
        values_text.next_to(formula_recap, DOWN, buff=0.3)
        
        calculation_final = MathTex(
            f"\\text{{Alpha\#14}} = {calc_results['neg_rank_delta_returns_3']:.4f} \\times {calc_results['corr_open_volume_10']:.4f} = {calc_results['alpha14_raw']:.5f}", # Show more precision before formatting
            font_size=22, color=GREEN # Adjusted font size
        )
        calculation_final.next_to(values_text, DOWN, buff=0.2)

        formatted_result = Text(f"(格式化为两位有效数字: {calc_results['alpha14_formatted']})", font_size=18, color=GREEN)
        formatted_result.next_to(calculation_final, DOWN, buff=0.2)
        
        self.play(Write(step_title))
        self.play(Write(formula_recap), Write(values_text))
        self.play(Write(calculation_final))
        self.play(Write(formatted_result))
        self.wait(4)
        
        self.play(FadeOut(step_title), FadeOut(formula_recap), FadeOut(values_text), FadeOut(calculation_final), FadeOut(formatted_result))

    def show_final_result_alpha14(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        # 创建结果框
        result_box = Rectangle(width=9, height=4.5, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(
            f"asset_1 在 2025-01-10 的 Alpha#14 值: {calc_results['alpha14_formatted']}", 
            font_size=20, 
            weight=BOLD
        )
        result_text_header.move_to(result_box.get_center() + UP * 1.5)

        result_text_body = Text(
            f"解读 (asset_1, 2025-01-10):\n"
            f"• 3日收益率变化 (delta_returns_3) = {calc_results['delta_returns_3']:.4f}\n"
            f"• 该变化在当日排名 (rank_delta_returns_3) = {calc_results['rank_delta_returns_3']:.4f} (80%分位, 排名较高)\n"
            f"• 负排名 (neg_rank) = {calc_results['neg_rank_delta_returns_3']:.4f}\n"
            f"• 10日开盘价-成交量相关性 (corr) = {calc_results['corr_open_volume_10']:.4f} (轻微负相关)\n"
            f"• Alpha 值 = {calc_results['neg_rank_delta_returns_3']:.4f} * {calc_results['corr_open_volume_10']:.4f} = {calc_results['alpha14_formatted']}",
            font_size=16,
            line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)

        # 创建总结框
        summary_box = Rectangle(width=10, height=5, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#14 结合了资产近期收益率变化的相对表现\n"
            "(通过其负排名体现，排名高则因子项接近-1)\n"
            "以及其历史开盘价与成交量的相关性模式。\n"
            f"因子值为正({calc_results['alpha14_formatted']})可能表示：收益率变化排名靠后(neg_rank接近-1)\n"
            "且价量历史呈负相关 (corr < 0)，两者相乘为正。\n"
            "具体投资含义需结合更多数据和回测分析。",
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
    # manim -pqh alpha14_visualization.py Alpha14Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha14Visualization.mp4 --flush_cache
    pass 