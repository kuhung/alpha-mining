#!/usr/bin/env python3
"""
Alpha#19 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha19_visualization.py Alpha19Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha19Visualization.mp4 --flush_cache
manim -qk alpha19_visualization.py Alpha19Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha19Visualization.mp4

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

class Alpha19Visualization(Scene):
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
        
        # Alpha#19公式
        formula_title_text = "Alpha#19: 趋势反转与长期回报的动态平衡"
        formula_title = Text(formula_title_text, font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"\text{Alpha\#19} = ((-1 \times \text{sign}((\text{close} - \text{delay}(\text{close}, 7)) + \text{delta}(\text{close}, 7))) \times (1 + \text{rank}((1 + \text{sum}(\text{returns}, 250)))))",
            font_size=24
        )
        formula.move_to([0, 0.5, 0])
        
        explanation = Text(
            "结合趋势反转信号和长期回报表现的复合因子",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -0.8, 0])
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
    
    def create_data_table_alpha19(self):
        headers = ["日期", "收盘价 (C)", "7日前收盘价", "250日累计回报"]
        # Data for asset_1 from README.md example
        data_values = [
            ["2025-01-24", "97.20", "95.80", "0.156 (15.6%)"]
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
        steps_title = Text("计算步骤演示 (Alpha#19)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 计算 2025-01-24 Alpha#19)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table_alpha19()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.85)
        self.play(Create(data_table))

        # Highlight the target row
        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((2, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(data_table), FadeOut(data_title))
        
        # Store calculated values to pass between steps
        calc_results = {
            'close': 97.20,
            'close_delay_7': 95.80,
            'price_change_7d': 1.40,
            'double_price_change': 2.80,
            'trend_signal': -1,
            'sum_returns_250': 0.156,
            'one_plus_sum_returns': 1.156,
            'rank_sum_returns': 0.850,
            'return_rank_factor': 1.850,
            'alpha19': -1.850
        }

        self.show_step1_trend_signal(steps_title, calc_results)
        self.show_step2_returns_factor(steps_title, calc_results)
        self.show_step3_final_alpha(steps_title, calc_results)
        self.show_final_result_alpha19(steps_title, calc_results)

    def show_step1_trend_signal(self, title_obj, calc_results): 
        step_title = Text("步骤1: 计算趋势反转信号", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        intro_text = Text(
            "计算7日价格变动并确定趋势反转信号：\n"
            "1. 计算7日价格变动\n"
            "2. 将变动翻倍（因为delta和差值相加）\n"
            "3. 取符号并反转",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        calculation = VGroup(
            Text(f"price_change_7d = {calc_results['close']:.2f} - {calc_results['close_delay_7']:.2f} = {calc_results['price_change_7d']:.2f}", font_size=18),
            Text(f"double_price_change = 2 * {calc_results['price_change_7d']:.2f} = {calc_results['double_price_change']:.2f}", font_size=18),
            Text(f"trend_signal = -1 * sign({calc_results['double_price_change']:.2f}) = {calc_results['trend_signal']}", 
                 font_size=18, color=GREEN)
        ).arrange(DOWN, buff=0.2)
        calculation.next_to(intro_text, DOWN, buff=0.3)
        
        self.play(Write(intro_text))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(calculation))

    def show_step2_returns_factor(self, title_obj, calc_results): 
        step_title = Text("步骤2: 计算回报排名因子", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        intro_text = Text(
            "基于250日累计回报计算排名因子：\n"
            "1. 计算250日累计回报并加1\n"
            "2. 进行市场排名\n"
            "3. 排名结果加1得到最终因子",
            font_size=18, line_spacing=1.2
        )
        intro_text.next_to(step_title, DOWN, buff=0.3)
        
        calculation = VGroup(
            Text(f"sum_returns_250 = {calc_results['sum_returns_250']:.3f} (15.6%)", font_size=18),
            Text(f"one_plus_sum_returns = 1 + {calc_results['sum_returns_250']:.3f} = {calc_results['one_plus_sum_returns']:.3f}", font_size=18),
            Text(f"rank_sum_returns = {calc_results['rank_sum_returns']:.3f} (85%分位)", font_size=18),
            Text(f"return_rank_factor = 1 + {calc_results['rank_sum_returns']:.3f} = {calc_results['return_rank_factor']:.3f}", 
                 font_size=18, color=GREEN)
        ).arrange(DOWN, buff=0.2)
        calculation.next_to(intro_text, DOWN, buff=0.3)
        
        self.play(Write(step_title))
        self.play(Write(intro_text))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(intro_text), FadeOut(calculation))
        
    def show_step3_final_alpha(self, title_obj, calc_results):
        step_title = Text("步骤3: 计算最终 Alpha#19 值", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_recap = MathTex(r"\text{Alpha\#19} = \text{trend\_signal} \times \text{return\_rank\_factor}", font_size=24)
        formula_recap.next_to(step_title, DOWN, buff=0.4)
        
        values_text = Text(
            f"trend_signal = {calc_results['trend_signal']}\n"
            f"return_rank_factor = {calc_results['return_rank_factor']:.3f}",
            font_size=20, line_spacing=1.2
        )
        values_text.next_to(formula_recap, DOWN, buff=0.3)
        
        calculation_final = MathTex(
            f"\\text{{Alpha\#19}} = {calc_results['trend_signal']} \\times {calc_results['return_rank_factor']:.3f} = {calc_results['alpha19']:.3f}", 
            font_size=24, color=GREEN
        )
        calculation_final.next_to(values_text, DOWN, buff=0.2)
        
        self.play(Write(formula_recap), Write(values_text))
        self.play(Write(calculation_final))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_recap), FadeOut(values_text), FadeOut(calculation_final))

    def show_final_result_alpha19(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=9, height=4.5, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(f"asset_1 在 2025-01-24 的 Alpha#19 值: {calc_results['alpha19']:.3f}", font_size=20, weight=BOLD)
        result_text_header.move_to(result_box.get_center() + UP * 1.5)

        result_text_body = Text(
            f"解读 (asset_1, 2025-01-24):\n"
            f"• 7日价格上涨 {calc_results['price_change_7d']:.2f}，趋势反转信号为负\n"
            f"• 250日累计回报为 15.6%，市场排名靠前（85%分位）\n"
            f"• 长期表现好（回报排名因子为 {calc_results['return_rank_factor']:.3f}）\n"
            f"• 放大了负向的趋势反转信号",
            font_size=16,
            line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)

        summary_box = Rectangle(width=10, height=5, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "总结：Alpha#19 通过结合两个关键信号：\n"
            "1. 短期趋势反转信号（7日价格变动）\n"
            "2. 长期回报表现（250日累计回报）\n\n"
            "负的 Alpha 值（-1.850）表明该资产：\n"
            "近期上涨但长期表现优异，可能即将出现回调",
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
    # manim -pqh alpha19_visualization.py Alpha19Visualization
    pass 