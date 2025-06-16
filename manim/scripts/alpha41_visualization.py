#!/usr/bin/env python3
"""
Alpha#41 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -ql alpha41_visualization.py Alpha41Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha41Visualization.mp4
manim -qk alpha41_visualization.py Alpha41Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha41Visualization.mp4

3. 合并音频
PROCESS_PATH="/Users/kuhung/roy/alpha-mining/process"
FILE_PATH="/Users/kuhung/roy/alpha-mining/manim/outputs/"
${PROCESS_PATH}/process_videos.sh ${PROCESS_PATH}/origin.mov ${FILE_PATH}/Alpha41Visualization.mp4 ${FILE_PATH}/Alpha41Visualization.png

提示:
- `-pql` : 预览并使用低质量渲染 (加快速度). 可选: `-pqm` (中等), `-pqh` (高).
- `-o YOUR_ABSOLUTE_PATH_TO_PROJECT/manim/outputs/YourSceneName.mp4`: 指定输出文件的绝对路径和名称.
- `--flush_cache`: 移除缓存的片段电影文件.
- 查看您版本的所有可用选项: `manim render --help`
"""

from manim import *
import os

# 配置中文字体
config.font = "PingFang SC"

class Alpha41Visualization(Scene):
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

        # 风险警示 (新增)
        risk_warning_text = "风险提示：本视频仅供科普，不构成投资建议。"
        self.risk_warning = Text(risk_warning_text, font_size=16, color=DARK_GRAY,weight=LIGHT)
        self.risk_warning.to_corner(DR, buff=0.3)
        self.add(self.risk_warning)

        # 标题
        title = Text("解读101个量化因子", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.add(title)
        
        # Alpha#41公式
        formula_title = Text("Alpha#41 价格几何平均与VWAP偏离度", font_size=32, color=GREEN)
        formula_title.move_to([0, 2.2, 0])
        
        formula = MathTex(
            r"Alpha\ \#41 = \sqrt{high \times low} - vwap",
            font_size=40
        )
        formula.move_to([0, 0.8, 0])
        
        explanation = Text(
            "衡量价格内在价值与市场成交重心的偏离度",
            font_size=28,
            color=YELLOW
        )
        explanation.next_to(formula, DOWN, buff=0.8)
        
        self.add(formula_title, formula, explanation)
        self.wait(4)
        
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        self.show_calculation_steps()
        self.show_summary_alpha41() # 调用策略总结场景
        self.end_scene() # 调用结束场景

    def create_data_table(self):
        headers = ["日期", "资产ID", "High", "Low", "VWAP"]
        # 数据源: alpha/alpha41/alpha41_results.csv
        data_values = [
            ["2024-06-01", "asset_1", "100.28", "99.08", "99.41"],
        ]
        
        # 使用与 alpha40_visualization.py 相同的表格创建方式
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
        steps_title = Text("计算步骤演示 (Alpha#41)", font_size=38, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        data_title = Text("示例数据 (asset_1, 2024-06-01)", font_size=28, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        self.play(Write(data_title))
        
        data_table = self.create_data_table()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.85) # 缩放表格
        self.play(Create(data_table))

        # 高亮目标行
        highlight_cells_group = VGroup()
        for col_idx in range(1, len(data_table.col_labels) + 1): 
            highlight_cells_group.add(data_table.get_highlighted_cell((2, col_idx), color=YELLOW))
        
        data_table.add_to_back(highlight_cells_group)
        self.play(FadeIn(highlight_cells_group), run_time=0.8)
        self.wait(2)

        # 淡出表格，准备显示计算
        self.play(FadeOut(data_table), FadeOut(data_title))

        # 硬编码计算值
        calc_results = {
            'high': 100.28,
            'low': 99.08,
            'vwap': 99.41,
            'geometric_mean': 99.68,
            'alpha41': 0.27
        }

        # 显示计算过程 (新风格)
        self.show_step_component_alpha41(
            steps_title, 
            "几何平均价 (GeoMean)", 
            r"\text{GeoMean} = \sqrt{high \times low}", 
            rf"\sqrt{{{calc_results['high']:.2f} \times {calc_results['low']:.2f}}} = {calc_results['geometric_mean']:.2f}"
        )
        self.show_final_calculation_alpha41(steps_title, calc_results)
        self.show_final_result_alpha41(steps_title, calc_results)

    def show_step_component_alpha41(self, title_obj, step_name, formula_str, calc_str):
        step_title = Text(f"步骤: 计算 {step_name}", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula = MathTex(formula_str, font_size=24)
        formula.next_to(step_title, DOWN, buff=0.4)
        
        calc = MathTex(calc_str, font_size=26, color=YELLOW)
        calc.next_to(formula, DOWN, buff=0.3)

        self.play(Write(formula))
        self.play(Write(calc))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula), FadeOut(calc))

    def show_final_calculation_alpha41(self, title_obj, calc_results):
        step_title = Text("最终步骤: 计算 Alpha#41", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        self.play(Write(step_title))

        formula_final = MathTex(
            r"\text{Alpha\#41} = \text{GeoMean} - \text{vwap}",
            font_size=24
        )
        formula_final.next_to(step_title, DOWN, buff=0.4)
        
        final_calc = MathTex(
            f"= {calc_results['geometric_mean']:.2f} - {calc_results['vwap']:.2f} = {calc_results['alpha41']:.2f}",
            font_size=26, color=GREEN
        )
        final_calc.next_to(formula_final, DOWN, buff=0.3)
        
        self.play(Write(formula_final))
        self.play(Write(final_calc))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_final), FadeOut(final_calc))

    def show_final_result_alpha41(self, title_obj, calc_results):
        final_title = Text("最终结果与解读", font_size=36, color=BLUE)
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=9.5, height=4, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.4)
        
        result_text_header = Text(
            f"asset_1 在 2024-06-01 的 Alpha#41 值: {calc_results['alpha41']:.2f}", font_size=20, weight=BOLD
        )
        result_text_header.move_to(result_box.get_center()).shift(UP * 1.5)

        result_text_body = Text(
            f"几何平均价 (GeoMean) = {calc_results['geometric_mean']:.2f}\n"
            f"成交量加权均价 (VWAP) = {calc_results['vwap']:.2f}\n"
            f"最终 Alpha = {calc_results['geometric_mean']:.2f} - {calc_results['vwap']:.2f} = {calc_results['alpha41']:.2f}",
            font_size=18, line_spacing=1.2
        )
        result_text_body.next_to(result_text_header, DOWN, buff=0.3)
        
        self.play(Write(final_title))
        self.play(Create(result_box))
        self.play(Write(result_text_header), Write(result_text_body))
        self.wait(4) 
        
        self.play(FadeOut(result_box), FadeOut(result_text_header), FadeOut(result_text_body))
        
        summary_box = Rectangle(width=11, height=2.5, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.4)

        summary = Text(
            "解读：因子值为正，表明当日价格的内在价值中枢\n"
            "高于市场成交重心，可能是一个看涨信号。",
            font_size=24,
            line_spacing=1.3,
            color=WHITE
        )
        summary.move_to(summary_box.get_center())

        self.play(Create(summary_box))
        self.play(Write(summary))
        self.wait(5)
        
        self.play(FadeOut(title_obj), FadeOut(final_title), FadeOut(summary_box), FadeOut(summary))

    def show_summary_alpha41(self):
        title = Text("策略总结 (Alpha#41)", font_size=36, color=BLUE)
        title.to_edge(UP, buff=1)
        self.play(Write(title))
        
        summary_box = RoundedRectangle(width=9, height=5, corner_radius=0.5, fill_color=BLUE_E, fill_opacity=0.1, stroke_color=BLUE).next_to(title, DOWN, buff=0.5)
        
        summary_points = VGroup(
            Text("✓ 衡量价格内在价值与市场成交重心的偏离", font_size=22, color=GREEN),
            Text("✓ 结构简单，易于理解和实现", font_size=22, color=WHITE),
            Text("✗ 对极端价格波动敏感", font_size=22, color=RED),
            Text("✗ 可能无法捕捉复杂市场情绪", font_size=22, color=RED),
            Text("★ 需在不同市场环境回测验证有效性", font_size=24, color=YELLOW),
            Text("★ 可与其他因子结合构建多元化策略", font_size=22, color=YELLOW)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(summary_box)
        
        self.play(Create(summary_box))
        self.play(Write(summary_points))
        self.wait(5)
        
        self.play(FadeOut(title), FadeOut(summary_box), FadeOut(summary_points))

    def end_scene(self):
        # 移除参考和风险警告水印
        self.play(FadeOut(self.reference_watermark), FadeOut(self.risk_warning), run_time=0.5)
        
        end_brand_text = self.brand_watermark 
        end_brand_text.set_color(BLUE_D).set_weight(BOLD)
        
        self.play(
            end_brand_text.animate.move_to([0, 1, 0]).scale(3),
            run_time=1.0
        )

        series_title = Text("101量化因子研究系列", font_size=36, color=BLUE_D, weight=BOLD)
        series_title.next_to(end_brand_text, DOWN, buff=0.5)
        self.play(Write(series_title))
        
        cta_text = Text("点赞👍 关注🔔 转发🚀", font_size=24, color=WHITE, font="Apple Color Emoji")
        cta_text.next_to(series_title, DOWN, buff=0.5)

        self.play(FadeIn(cta_text, shift=UP), run_time=1.5)
        self.wait(2)
        
        self.play(
            FadeOut(end_brand_text), FadeOut(series_title), FadeOut(cta_text)
        ) 