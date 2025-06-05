#!/usr/bin/env python3
"""
Alpha#4 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha4_visualization.py Alpha4Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha4Visualization.mp4 --flush_cache

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

class Alpha4Visualization(Scene):
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
        
        # Alpha#4公式
        formula_title = Text("Alpha#4 反向低价时序因子", font_size=36, color=GREEN)
        formula_title.move_to([0, 2, 0])  # 居中显示，y坐标设为2
        
        formula = MathTex(
            r"\text{Alpha\#4} = -1 \times \text{Ts\_Rank}(\text{rank}(\text{low}), 9)",
            font_size=32
        )
        formula.move_to([0, 0.5, 0])  # 居中显示，y坐标设为0.5
        
        # 公式解释
        explanation = Text(
            "计算最低价排名的9日时序排名后取负值",
            font_size=28,
            color=YELLOW
        )
        explanation.move_to([0, -1, 0])  # 居中显示，y坐标设为-1
        
        self.add(formula_title)
        self.add(formula)
        self.add(explanation)
        self.wait(3)
        
        # 清除屏幕
        self.play(FadeOut(title), FadeOut(formula_title), FadeOut(formula), FadeOut(explanation))
        
        # 开始计算步骤演示
        self.show_calculation_steps()
    
    def show_calculation_steps(self):
        # 步骤标题
        steps_title = Text("计算步骤演示", font_size=42, color=BLUE)
        steps_title.to_edge(UP)
        self.play(Write(steps_title))
        
        # 示例数据
        data_title = Text("示例数据 (asset_1)", font_size=32, color=GREEN)
        data_title.next_to(steps_title, DOWN, buff=0.5)
        
        # 创建数据表格
        data_table = self.create_data_table()
        data_table.next_to(data_title, DOWN, buff=0.3)
        data_table.scale(0.8)
        
        self.play(Write(data_title))
        self.play(Create(data_table))
        
        # 创建高亮背景并添加动画效果
        highlight_cell1 = data_table.get_highlighted_cell((10,1), color=YELLOW)
        highlight_cell2 = data_table.get_highlighted_cell((10,2), color=YELLOW)
        
        # 先添加到表格背景，然后播放渐入动画
        data_table.add_to_back(highlight_cell1)
        data_table.add_to_back(highlight_cell2)
        self.play(FadeIn(highlight_cell1), FadeIn(highlight_cell2), run_time=0.8)
        self.wait(1)
        
        # 清除数据表格
        self.play(FadeOut(data_table), FadeOut(data_title))
        
        # 步骤1: 最低价截面排名
        self.show_step1(steps_title)
        
        # 步骤2: 时间序列排名
        self.show_step2(steps_title)
        
        # 步骤3: 取负值
        self.show_step3(steps_title)
        
        # 最终结果
        self.show_final_result(steps_title)
    
    def create_data_table(self):
        # 创建表格数据
        headers = ["日期", "最低价"]
        data_values = [
            ["2025-01-16", "98.35"],
            ["2025-01-17", "98.85"],
            ["2025-01-18", "100.46"],
            ["2025-01-19", "100.82"],
            ["2025-01-20", "100.23"],
            ["2025-01-21", "99.90"],
            ["2025-01-22", "101.29"],
            ["2025-01-23", "101.19"],
            ["2025-01-24", "101.37"] # 此行应高亮显示
        ]
        
        # 为表头创建Text Mobjects
        header_mobjects = [Text(h, font_size=26, weight=BOLD) for h in headers]

        table = Table(
            data_values,
            col_labels=header_mobjects,
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": WHITE},
            # 为数据条目使用Text并设置字体大小
            element_to_mobject=Text, 
            element_to_mobject_config={"font_size": 20},
            h_buff=0.4, # 调整水平缓冲区
            v_buff=0.25  # 调整垂直缓冲区
        )
        
        # 不在这里添加高亮，让外部控制高亮时机
        return table
    
    def show_step1(self, title):
        step1_title = Text("步骤1: 最低价截面排名", font_size=32, color=ORANGE)
        step1_title.next_to(title, DOWN, buff=0.5)
        
        description = Text("对当日所有资产的最低价进行横截面排名 (0-1百分位)", font_size=24)
        description.next_to(step1_title, DOWN, buff=0.3)
        
        example_date = Text("2025-01-24 各资产最低价:", font_size=24, color=YELLOW)
        example_date.next_to(description, DOWN, buff=0.3)
        
        price_ranking = Text(
            "asset_3: 109.72 → rank = 1.0 (最高)\n" +
            "asset_5: 108.91 → rank = 0.8 (第2高)\n" +
            "asset_4: 101.94 → rank = 0.6 (第3高)\n" +
            "asset_1: 101.37 → rank = 0.4 (第4高)\n" +
            "asset_2: 94.01  → rank = 0.2 (最低)",
            font_size=18,
            line_spacing=1.2,
            color=GREEN
        )
        price_ranking.next_to(example_date, DOWN, buff=0.2)
        
        highlight = Text("asset_1的最低价排名: 0.4", font_size=20, color=RED)
        highlight.next_to(price_ranking, DOWN, buff=0.3)
        
        interpretation = Text(
            "rank=0.4 表示asset_1的最低价在当日排第4位\n" +
            "属于相对较低的价格水平",
            font_size=18,
            line_spacing=1.2,
            color=BLUE
        )
        interpretation.next_to(highlight, DOWN, buff=0.2)
        
        self.play(Write(step1_title))
        self.play(Write(description))
        self.play(Write(example_date))
        self.play(Write(price_ranking))
        self.play(Write(highlight))
        self.play(Write(interpretation))
        self.wait(3)
        
        self.play(FadeOut(step1_title), FadeOut(description), FadeOut(example_date),
                 FadeOut(price_ranking), FadeOut(highlight), FadeOut(interpretation))
    
    def show_step2(self, title):
        step2_title = Text("步骤2: 时间序列排名 (Ts_Rank)", font_size=32, color=ORANGE)
        step2_title.next_to(title, DOWN, buff=0.5)
        
        description = Text("计算当前截面排名在过去9天中的时序排名", font_size=24)
        description.next_to(step2_title, DOWN, buff=0.3)
        
        time_series_concept = Text(
            "Ts_Rank原理:\n" +
            "• 观察过去9天的截面排名序列\n" +
            "• 计算当前值在这9个值中的排名位置\n" +
            "• 返回0-1之间的百分位排名",
            font_size=18,
            line_spacing=1.2,
            color=YELLOW
        )
        time_series_concept.next_to(description, DOWN, buff=0.3)
        
        example_data = Text(
            "asset_1 过去9天的截面排名:\n" +
            "[0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]\n" +
            "当前值 0.4 在这9个值中的排名计算:",
            font_size=18,
            line_spacing=1.2,
            color=GREEN
        )
        example_data.next_to(time_series_concept, DOWN, buff=0.3)
        
        calculation = Text(
            "• 所有9个值都等于0.4\n" +
            "• 排名 = (小于当前值的个数 + 0.5×等于当前值的个数) / 总数\n" +
            "• 排名 = (0 + 0.5×9) / 9 = 0.5",
            font_size=16,
            line_spacing=1.2,
            color=BLUE
        )
        calculation.next_to(example_data, DOWN, buff=0.2)
        
        result = Text("Ts_Rank = 0.5", font_size=20, color=RED)
        result.next_to(calculation, DOWN, buff=0.2)
        
        self.play(Write(step2_title))
        self.play(Write(description))
        self.play(Write(time_series_concept))
        self.play(Write(example_data))
        self.play(Write(calculation))
        self.play(Write(result))
        self.wait(3)
        
        self.play(FadeOut(step2_title), FadeOut(description), FadeOut(time_series_concept),
                 FadeOut(example_data), FadeOut(calculation), FadeOut(result))
    
    def show_step3(self, title):
        step3_title = Text("步骤3: 反向化处理", font_size=32, color=ORANGE)
        step3_title.next_to(title, DOWN, buff=0.5)
        
        description = Text("将时序排名取负值，实现反向逻辑", font_size=24)
        description.next_to(step3_title, DOWN, buff=0.3)
        
        calculation = MathTex(
            r"\text{Alpha\#4} = -1 \times 0.5 = -0.5",
            font_size=28
        )
        calculation.next_to(description, DOWN, buff=0.3)
        
        interpretation = Text(
            "反向逻辑的含义:\n" +
            "• 负值表示当前低价排名在历史上相对较高\n" +
            "• 暗示价格可能存在回调压力\n" +
            "• 体现均值回归的交易理念",
            font_size=20,
            line_spacing=1.2,
            color=GREEN
        )
        interpretation.next_to(calculation, DOWN, buff=0.3)
        
        comparison = Text(
            "对比情况:\n" +
            "• 如果Ts_Rank = 0.9 → Alpha#4 = -0.9 (强反向信号)\n" +
            "• 如果Ts_Rank = 0.1 → Alpha#4 = -0.1 (弱反向信号)",
            font_size=18,
            line_spacing=1.2,
            color=BLUE
        )
        comparison.next_to(interpretation, DOWN, buff=0.2)
        
        self.play(Write(step3_title))
        self.play(Write(description))
        self.play(Write(calculation))
        self.play(Write(interpretation))
        self.play(Write(comparison))
        self.wait(3)
        
        self.play(FadeOut(step3_title), FadeOut(description),
                 FadeOut(calculation), FadeOut(interpretation), FadeOut(comparison))
    
    def show_final_result(self, title):
        final_title = Text("最终结果", font_size=36, color=BLUE)
        final_title.next_to(title, DOWN, buff=0.5)
        
        result_box = Rectangle(width=8, height=3, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.3)
        
        result_text = Text(
            "asset_1 在 2025-01-24 的 Alpha#4 值: -0.5\n" +
            "这表明该资产的低价排名在过去9天中\n处于中等水平，产生中等强度的反向信号",
            font_size=20,
            line_spacing=1.2
        )
        result_text.move_to(result_box.get_center())
        
        summary = Text(
            "总结：Alpha#4 策略通过对股票最低价的\n"
            "截面排名进行时间序列分析，识别价格水平\n"
            "在短期内的相对变化趋势，并采用反向逻辑\n"
            "寻找可能的均值回归机会。该因子结合了\n"
            "价格水平分析和短期动量反转特性，适用于\n"
            "捕捉短期过度表现的股票。",
            font_size=20,
            line_spacing=1.4,
            color=RED
        )
        summary.move_to(result_box.get_center())
        
        # 先显示标题和结果框
        self.play(Write(final_title))
        self.play(Create(result_box))
        self.play(Write(result_text))
        self.wait(2)
        
        # 淡出结果框，为总结腾出空间
        self.play(FadeOut(result_box), FadeOut(result_text))
        
        # 显示总结
        self.play(Write(summary))
        self.wait(4)
        
        # 结束动画
        self.play(FadeOut(title), FadeOut(final_title), FadeOut(summary))

        # --- 新的片尾动画序列 ---
        # 1. 将左上角的水印移动到中心并放大
        # 保存原始水印的位置和样式
        original_position = self.brand_watermark.get_center()
        original_scale = self.brand_watermark.get_height() / 22  # 原始字号是22
        
        # 淡出参考来源水印
        self.play(FadeOut(self.reference_watermark))
        self.wait(0.2)  # 短暂等待
        
        # 2. 将品牌水印移动到中心并放大
        end_brand_text = self.brand_watermark  # 重用现有的水印对象
        end_brand_text.set_color(BLUE_D).set_weight(BOLD)  # 更新样式
        
        # 创建移动和缩放的动画
        self.play(
            end_brand_text.animate
            .move_to([0, 1, 0])  # 移动到中间偏上的位置
            .scale(3),  # 直接放大到合适大小
            run_time=1.0
        )

        # 添加系列标题
        series_title = Text(
            "101量化因子研究系列",
            font_size=36,
            color=BLUE_D,
            weight=BOLD
        )
        series_title.next_to(end_brand_text, DOWN, buff=0.5)
        self.play(Write(series_title))
        self.wait(0.2)  # 短暂停留

        # 3. 创建并动画引导三连文本
        cta_text = Text(
            "点赞👍 关注🔔 转发🚀",
            font_size=20, # 设置合适的字号
            color=WHITE,   # 使用白色，确保可见
            font="Apple Color Emoji" # 添加字体指定
        )
        # 定位在放大的品牌文字下方
        cta_text.next_to(series_title, DOWN, buff=0.8)

        self.play(Write(cta_text), run_time=1.5) # 文字书写动画
        self.wait(3) # 最后停留3秒展示
        # --- 片尾动画序列结束 ---


# 运行脚本的主函数
if __name__ == "__main__":
    # Manim通过命令行参数处理场景渲染，此处无需额外代码
    pass 