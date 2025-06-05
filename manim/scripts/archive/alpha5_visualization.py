#!/usr/bin/env python3
"""
Alpha#5 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha5_visualization.py Alpha5Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha5Visualization.mp4 --flush_cache

   (请将 YOUR_ABSOLUTE_PATH_TO_PROJECT 替换为您项目的实际绝对路径, 例如 /Users/username/my_project)

提示:
- `-pql` : 预览并使用低质量渲染 (加快速度). 可选: `-pqm` (中等), `-pqh` (高).
- `-o YOUR_ABSOLUTE_PATH_TO_PROJECT/manim/outputs/YourSceneName.mp4`: 指定输出文件的绝对路径和名称. 这是最可靠的方法。
- `--flush_cache`: 移除缓存的片段电影文件 (Manim v0.19.0 支持).
  (注意: 这可能不会删除所有类型的中间文件，例如 TeX 日志。
   对于更彻底的清理，您可能需要检查并手动删除 `manim/scripts/media/` 目录下的内容，
   特别是 `media/tex/` 和 `media/texts/` 等子目录，在渲染过程后。)
- 查看您版本的所有可用选项: `manim render --help`
"""

from manim import *
import numpy as np
import pandas as pd

# 配置中文字体
config.font = "PingFang SC"

class Alpha5Visualization(Scene):
    def construct(self):
        # 品牌标识
        brand_name = "✨仓满量化✨"
        # 使用稍小字号、深灰色、细体作为水印
        self.brand_watermark = Text(brand_name, font_size=22, color=GRAY, weight=NORMAL, font="Apple Color Emoji")
        self.brand_watermark.to_edge(UP, buff=0.7).to_edge(LEFT, buff=0.8) # 保持左侧，但垂直位置与标题对齐
        self.add(self.brand_watermark) # 将水印添加到场景中，使其持久显示

        # 参考来源
        reference_source_text = "Source: 101 Formulaic Alphas"
        self.reference_watermark = Text(reference_source_text, font_size=16, color=DARK_GRAY, weight=LIGHT) # 比品牌字号略小
        self.reference_watermark.to_corner(DL, buff=0.3) # DR 代表 DOWN + RIGHT，放置在右下角
        self.add(self.reference_watermark)

        # 标题
        title = Text("解读101个量化因子", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.add(title)
        
        # Alpha#5公式
        formula_title = Text("Alpha#5 VWAP偏差交互因子", font_size=36, color=GREEN)
        formula_title.move_to([0, 2, 0])  # 居中显示，y坐标设为2
        
        # 为了美观和可读性，将公式分为两行或调整大小
        formula_part1 = MathTex(
            r"\text{Alpha\#5} = \text{rank}(\text{open} - \frac{\sum_{i=1}^{10} \text{vwap}_{t-i+1}}{10})",
            font_size=32 # 调整字体大小以适应屏幕
        )
        formula_part2 = MathTex(
            r"\times (-1 \times |\text{rank}(\text{close} - \text{vwap}_t)|)",
            font_size=32 # 调整字体大小以适应屏幕
        )
        
        formula_group = VGroup(formula_part1, formula_part2).arrange(DOWN, buff=0.2)
        formula_group.move_to([0, 0.5, 0])  # 居中显示
        
        # 公式解释
        explanation = Text(
            "结合开盘价相对VWAP均值的偏离与收盘价相对当日VWAP的偏离",
            font_size=28, # 调整字体大小
            color=YELLOW,
            line_spacing=1.2
        )
        explanation.next_to(formula_group, DOWN, buff=0.4) # 调整位置
        
        self.add(formula_title)
        self.add(formula_group)
        self.add(explanation)
        self.wait(4) # 增加等待时间
        
        # 清除屏幕
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula_group), FadeOut(explanation))
        
        # 开始计算步骤演示
        self.show_calculation_steps()
    
    def show_calculation_steps(self):
        # 步骤标题
        steps_title = Text("计算步骤演示", font_size=38, color=BLUE) # 调整字号
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        # 示例数据
        data_title = Text("核心数据 (asset_3)", font_size=30, color=GREEN) # 调整字号
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        # 创建数据表格
        data_table = self.create_data_table()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.75) # 调整缩放
        
        self.play(Write(data_title))
        self.play(Create(data_table))
        
        # 创建高亮背景并添加动画效果 (第4行是2025-01-20)
        highlight_row_index = 4 
        cells_to_highlight = [(highlight_row_index, col_idx) for col_idx in range(1, len(data_table.col_labels) + 1)]
        
        highlight_rects = VGroup()
        for cell_coords in cells_to_highlight:
            highlight_rects.add(data_table.get_highlighted_cell(cell_coords, color=YELLOW))

        # 先添加到表格背景，然后播放渐入动画
        data_table.add_to_back(highlight_rects)
        self.play(FadeIn(highlight_rects), run_time=0.8)
        self.wait(2) # 增加等待时间
        
        # 清除数据表格
        self.play(FadeOut(data_table), FadeOut(data_title))
        
        # 步骤1: 计算10日VWAP移动平均
        self.show_step1(steps_title)
        
        # 步骤2: 开盘价与VWAP均值偏差及排名
        self.show_step2(steps_title)
        
        # 步骤3: 收盘价与当日VWAP偏差及排名
        self.show_step3(steps_title)
        
        # 步骤4: 最终Alpha#5值计算
        self.show_step4(steps_title)
        
        # 最终结果
        self.show_final_result(steps_title)
    
    def create_data_table(self):
        # 创建表格数据 (asset_3)
        headers = ["日期", "开盘价", "收盘价", "VWAP"]
        data_values = [
            ["2025-01-18", "102.64", "106.10", "104.99"],
            ["2025-01-19", "105.80", "105.90", "105.59"],
            ["2025-01-20", "105.50", "104.40", "104.15"], # Target row for example
            ["2025-01-21", "105.00", "105.50", "105.23"],
            ["2025-01-22", "105.68", "106.60", "105.65"]
        ]
        
        # 为表头创建Text Mobjects
        header_mobjects = [Text(h, font_size=22, weight=BOLD) for h in headers] # 调整字号

        table = Table(
            data_values,
            col_labels=header_mobjects,
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": WHITE},
            element_to_mobject=Text, 
            element_to_mobject_config={"font_size": 18}, # 调整字号
            h_buff=0.3, # 调整水平缓冲区
            v_buff=0.2  # 调整垂直缓冲区
        )
        return table
    
    def show_step1(self, title_obj): # Renamed title to title_obj to avoid conflict
        step_title = Text("步骤1: 计算10日VWAP移动平均 (vwap_ma_10)", font_size=28, color=ORANGE) # 调整字号
        step_title.next_to(title_obj, DOWN, buff=0.5)
        
        formula_text = MathTex(r"\text{vwap\_ma\_10} = \frac{\sum_{i=1}^{10} \text{vwap}_{t-i+1}}{10}", font_size=24) # 调整字号
        formula_text.next_to(step_title, DOWN, buff=0.3)
        
        vwap_values_text = Text("asset_3 在 2025-01-20 的过去10日VWAP:", font_size=20) # 调整字号
        vwap_values_text.next_to(formula_text, DOWN, buff=0.3)
        
        vwap_list = "[104.28, 103.44, 101.42, 100.52, 101.08,\n103.48, 102.44, 104.99, 105.59, 104.15]"
        vwap_data = Text(vwap_list, font_size=18, line_spacing=1.2) # 调整字号
        vwap_data.next_to(vwap_values_text, DOWN, buff=0.2)
        
        calculation = MathTex(r"\text{vwap\_ma\_10} = \frac{1031.39}{10} = 103.14", font_size=22, color=GREEN) # 调整字号
        calculation.next_to(vwap_data, DOWN, buff=0.3)
        
        self.play(Write(step_title))
        self.play(Write(formula_text))
        self.play(Write(vwap_values_text))
        self.play(Write(vwap_data))
        self.play(Write(calculation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(vwap_values_text),
                  FadeOut(vwap_data), FadeOut(calculation))
    
    def show_step2(self, title_obj):
        step_title = Text("步骤2: 开盘价与VWAP均值偏差及排名", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        
        part_a_title = Text("A. 计算偏差: open - vwap_ma_10", font_size=22, color=YELLOW)
        part_a_title.next_to(step_title, DOWN, buff=0.3)
        
        calc_a = MathTex(r"\text{open} - \text{vwap\_ma\_10} = 105.50 - 103.14 = 2.36", font_size=20, color=GREEN)
        calc_a.next_to(part_a_title, DOWN, buff=0.2)
        
        part_b_title = Text("B. 横截面排名 (rank_open_diff)", font_size=22, color=YELLOW)
        part_b_title.next_to(calc_a, DOWN, buff=0.3)
        
        ranking_data = Text(
            "当日各资产 open_vwap_diff 值 (示例):\n"
            "asset_1: -0.68\n"
            "asset_2: -1.91\n"
            "asset_3: 2.36 (最高)\n"
            "asset_4: -1.41\n"
            "asset_5: -1.82",
            font_size=16, line_spacing=1.2 # 调整字号
        )
        ranking_data.next_to(part_b_title, DOWN, buff=0.2)
        
        result_b = Text("asset_3 的 rank_open_diff = 1.0", font_size=20, color=RED)
        result_b.next_to(ranking_data, DOWN, buff=0.3)
        
        self.play(Write(step_title))
        self.play(Write(part_a_title), Write(calc_a))
        self.play(Write(part_b_title), Write(ranking_data), Write(result_b))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(part_a_title), FadeOut(calc_a),
                  FadeOut(part_b_title), FadeOut(ranking_data), FadeOut(result_b))

    def show_step3(self, title_obj):
        step_title = Text("步骤3: 收盘价与当日VWAP偏差及排名", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)

        part_a_title = Text("A. 计算偏差: close - vwap_t", font_size=22, color=YELLOW)
        part_a_title.next_to(step_title, DOWN, buff=0.3)

        calc_a = MathTex(r"\text{close} - \text{vwap}_t = 104.40 - 104.15 = 0.25", font_size=20, color=GREEN)
        calc_a.next_to(part_a_title, DOWN, buff=0.2)

        part_b_title = Text("B. 横截面排名 (rank_close_diff)", font_size=22, color=YELLOW)
        part_b_title.next_to(calc_a, DOWN, buff=0.3)
        
        ranking_data = Text(
            "当日各资产 close_vwap_diff 值 (示例):\n"
            "asset_1: 1.01\n"
            "asset_2: 0.71\n"
            "asset_3: 0.25\n"
            "asset_4: -0.01\n"
            "asset_5: 1.11",
            font_size=16, line_spacing=1.2
        )
        ranking_data.next_to(part_b_title, DOWN, buff=0.2)
        
        result_b = Text("asset_3 的 rank_close_diff = 0.4 (示例排名)", font_size=20, color=RED)
        result_b.next_to(ranking_data, DOWN, buff=0.3)

        self.play(Write(step_title))
        self.play(Write(part_a_title), Write(calc_a))
        self.play(Write(part_b_title), Write(ranking_data), Write(result_b))
        self.wait(3)

        self.play(FadeOut(step_title), FadeOut(part_a_title), FadeOut(calc_a),
                  FadeOut(part_b_title), FadeOut(ranking_data), FadeOut(result_b))

    def show_step4(self, title_obj):
        step_title = Text("步骤4: 最终Alpha#5值计算", font_size=28, color=ORANGE)
        step_title.next_to(title_obj, DOWN, buff=0.5)
        
        formula_text = MathTex(
            r"\text{Alpha\#5} = \text{rank\_open\_diff} \times (-1 \times |\text{rank\_close\_diff}|)",
            font_size=22 # 调整字号
        )
        formula_text.next_to(step_title, DOWN, buff=0.3)
        
        calculation = MathTex(
            r"= 1.0 \times (-1 \times |0.4|)",
            font_size=22
        )
        calculation.next_to(formula_text, DOWN, buff=0.2)
        
        result = MathTex(
            r"= 1.0 \times (-0.4) = -0.40",
            font_size=24, color=GREEN # 调整字号
        )
        result.next_to(calculation, DOWN, buff=0.2)
        
        interpretation = Text(
            "开盘强势 (rank_open_diff=1.0)，日内表现一般 (rank_close_diff=0.4)\n"
            "策略给出负信号，预期价格可能回归",
            font_size=18, line_spacing=1.2, color=BLUE # 调整字号
        )
        interpretation.next_to(result, DOWN, buff=0.3)
        
        self.play(Write(step_title))
        self.play(Write(formula_text))
        self.play(Write(calculation))
        self.play(Write(result))
        self.play(Write(interpretation))
        self.wait(3)
        
        self.play(FadeOut(step_title), FadeOut(formula_text), FadeOut(calculation), 
                  FadeOut(result), FadeOut(interpretation))
    
    def show_final_result(self, title_obj):
        final_title = Text("最终结果解读", font_size=36, color=BLUE) # 调整字号
        final_title.next_to(title_obj, DOWN, buff=0.5)
        
        result_box = Rectangle(width=10, height=2.5, color=BLUE, fill_opacity=0.1) # 调整尺寸
        result_box.next_to(final_title, DOWN, buff=0.3)
        
        result_text = Text(
            "asset_3 在 2025-01-20 的 Alpha#5 值: -0.40\n" +
            "表明开盘价相对历史VWAP偏高，且日内收盘价\n"
            "相对当日VWAP偏离不大，整体信号为负。",
            font_size=18, line_spacing=1.2 # 调整字号
        )
        result_text.move_to(result_box.get_center())
        
        # 缩小总结文本框和字体
        summary_box = Rectangle(width=12, height=4, color=BLUE, fill_opacity=0.1)
        summary_box.next_to(final_title, DOWN, buff=0.3)

        summary = Text(
            "总结：Alpha#5策略通过分析开盘价相对于VWAP移动平均\n"
            "的偏差和收盘价相对于当日VWAP的偏差，识别价格相对\n"
            "于成交量加权基准的偏离情况。该因子结合了中期VWAP\n"
            "基准比较和当日VWAP表现评估，采用反向逻辑寻找价格\n"
            "偏离过度的交易机会，适用于基于VWAP的均值回归和\n"
            "日内反转策略。",
            font_size=18, # 显著减小字体
            line_spacing=1.3, # 调整行间距
            color=RED
        )
        summary.move_to(summary_box.get_center()) # 移动到新的总结框中心
        
        # 先显示标题和结果框
        self.play(Write(final_title))
        self.play(Create(result_box))
        self.play(Write(result_text))
        self.wait(2)
        
        # 淡出结果框，为总结腾出空间 (使用新的总结框)
        self.play(FadeOut(result_box), FadeOut(result_text))
        self.play(Create(summary_box)) # 创建总结框
        self.play(Write(summary))
        self.wait(5) # 增加等待时间
        
        # 结束动画
        self.play(FadeOut(title_obj), FadeOut(final_title), FadeOut(summary_box), FadeOut(summary))

        # --- 新的片尾动画序列 ---
        # 1. 将左上角的水印移动到中心并放大
        original_position = self.brand_watermark.get_center()
        original_scale = self.brand_watermark.get_height() / 22
        
        self.play(FadeOut(self.reference_watermark))
        self.wait(0.2)
        
        end_brand_text = self.brand_watermark
        end_brand_text.set_color(BLUE_D).set_weight(BOLD)
        
        self.play(
            end_brand_text.animate
            .move_to([0, 1, 0])
            .scale(3),
            run_time=1.0
        )

        series_title = Text(
            "101量化因子研究系列",
            font_size=36,
            color=BLUE_D,
            weight=BOLD
        )
        series_title.next_to(end_brand_text, DOWN, buff=0.5)
        self.play(Write(series_title))
        self.wait(0.2)

        cta_text = Text(
            "点赞👍 关注🔔 转发🚀",
            font_size=20,
            color=WHITE,
            font="Apple Color Emoji"
        )
        cta_text.next_to(series_title, DOWN, buff=0.8)

        self.play(Write(cta_text), run_time=1.5)
        self.wait(3)
        # --- 片尾动画序列结束 ---

# 运行脚本的主函数
if __name__ == "__main__":
    pass 