#!/usr/bin/env python3
"""
Alpha#2 因子可视化脚本 (Manim Community v0.19.0)

使用方法 (建议从 manim/scripts/ 目录运行):

1. 确保输出目录存在:
   mkdir -p ../outputs

2. 渲染并清理缓存 (推荐使用绝对路径以避免错误):
manim -pqh alpha2_visualization.py Alpha2Visualization -o /Users/kuhung/roy/alpha-mining/manim/outputs/Alpha2Visualization.mp4 --flush_cache

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

class Alpha2Visualization(Scene):
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
        
        # Alpha#2公式
        formula_title = Text("Alpha#2 捕捉成交量与日内收益负相关", font_size=36, color=GREEN)
        formula_title.move_to([0, 2, 0])  # 居中显示，y坐标设为2
        
        formula = MathTex(
            r"\text{Alpha\#2} = -1 \times \text{correlation}(\text{rank}(\text{delta}(\log(\text{volume}), 2)), \text{rank}(\frac{\text{close} - \text{open}}{\text{open}}), 6)",
            font_size=32
        )
        formula.move_to([0, 0.5, 0])  # 居中显示，y坐标设为0.5
        
        # 公式解释
        explanation = Text(
            "计算成交量变化排名与日内收益率排名的6日滚动负相关",
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
        self.wait(2)
        
        # 清除数据表格
        self.play(FadeOut(data_table), FadeOut(data_title))
        
        # 步骤1: 成交量对数差分
        self.show_step1(steps_title)
        
        # 步骤2: 日内收益率计算
        self.show_step2(steps_title)
        
        # 步骤3: 排名计算
        self.show_step3(steps_title)
        
        # 步骤4: 滚动相关系数
        self.show_step4(steps_title)
        
        # 步骤5: 取负值
        self.show_step5(steps_title)
        
        # 最终结果
        self.show_final_result(steps_title)
    
    def create_data_table(self):
        # 创建表格数据
        headers = ["日期", "开盘价", "收盘价", "成交量"]
        data_values = [
            ["2025-01-20", "99.93", "100.5", "3507861"],
            ["2025-01-21", "100.79", "99.6", "1016495"],
            ["2025-01-22", "98.92", "101.6", "825693"], # 此行应高亮显示
            ["2025-01-23", "103.09", "102.5", "1496721"],
            ["2025-01-24", "102.22", "100.9", "1692425"],
            ["2025-01-25", "98.64", "102.4", "1677999"]
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
            element_to_mobject_config={"font_size": 22},
            h_buff=0.4, # 调整水平缓冲区
            v_buff=0.25  # 调整垂直缓冲区
        )
        
        return table
    
    def show_step1(self, title):
        step1_title = Text("步骤1: 成交量对数差分", font_size=32, color=ORANGE)
        step1_title.next_to(title, DOWN, buff=0.5)
        
        formula_text = MathTex(
            r"\text{delta}(\log(\text{volume}), 2) = \log(\text{volume}[t]) - \log(\text{volume}[t-2])",
            font_size=26
        )
        formula_text.next_to(step1_title, DOWN, buff=0.3)
        
        example_date = Text("2025-01-22 计算示例:", font_size=24, color=YELLOW)
        example_date.next_to(formula_text, DOWN, buff=0.3)
        
        calc1 = MathTex(r"\log(825693) = 13.624", font_size=22, color=GREEN)
        calc1.next_to(example_date, DOWN, buff=0.2)
        
        calc2 = MathTex(r"\log(3507861) = 15.071", font_size=22, color=GREEN)
        calc2.next_to(calc1, DOWN, buff=0.1)
        
        result = MathTex(r"\text{delta} = 13.624 - 15.071 = -1.447", font_size=22, color=RED)
        result.next_to(calc2, DOWN, buff=0.2)
        
        interpretation = Text("负值表示成交量相比2天前减少", font_size=20, color=BLUE)
        interpretation.next_to(result, DOWN, buff=0.2)
        
        self.play(Write(step1_title))
        self.play(Write(formula_text))
        self.play(Write(example_date))
        self.play(Write(calc1))
        self.play(Write(calc2))
        self.play(Write(result))
        self.play(Write(interpretation))
        self.wait(3)
        
        self.play(FadeOut(step1_title), FadeOut(formula_text), FadeOut(example_date),
                 FadeOut(calc1), FadeOut(calc2), FadeOut(result), FadeOut(interpretation))
    
    def show_step2(self, title):
        step2_title = Text("步骤2: 日内收益率计算", font_size=32, color=ORANGE)
        step2_title.next_to(title, DOWN, buff=0.5)
        
        formula_text = MathTex(
            r"\text{Intraday Return} = \frac{\text{close} - \text{open}}{\text{open}}",
            font_size=28
        )
        formula_text.next_to(step2_title, DOWN, buff=0.3)
        
        example_date = Text("2025-01-22 计算示例:", font_size=24, color=YELLOW)
        example_date.next_to(formula_text, DOWN, buff=0.3)
        
        calc = MathTex(
            r"\frac{101.6 - 98.92}{98.92} = \frac{2.68}{98.92} = 0.0271",
            font_size=24, color=GREEN
        )
        calc.next_to(example_date, DOWN, buff=0.2)
        
        interpretation = Text("正值表示当日收盘价高于开盘价", font_size=20, color=BLUE)
        interpretation.next_to(calc, DOWN, buff=0.3)
        
        self.play(Write(step2_title))
        self.play(Write(formula_text))
        self.play(Write(example_date))
        self.play(Write(calc))
        self.play(Write(interpretation))
        self.wait(3)
        
        self.play(FadeOut(step2_title), FadeOut(formula_text), FadeOut(example_date),
                 FadeOut(calc), FadeOut(interpretation))
    
    def show_step3(self, title):
        step3_title = Text("步骤3: 横截面排名计算", font_size=32, color=ORANGE)
        step3_title.next_to(title, DOWN, buff=0.5)
        
        description = Text("对当日所有资产的指标值进行排名 (0-1百分位)", font_size=24)
        description.next_to(step3_title, DOWN, buff=0.3)
        
        # 成交量变化排名示例
        volume_ranking = Text(
            "成交量变化排名 (2025-01-22):\n" +
            "asset_1: -1.447 → rank = 0.2\n" +
            "asset_2: -0.500 → rank = 0.4 (示例)\n" +
            "asset_3: 0.200  → rank = 0.6 (示例)\n" +
            "asset_4: 0.800  → rank = 0.8 (示例)\n" +
            "asset_5: 1.200  → rank = 1.0 (示例)",
            font_size=18,
            line_spacing=1.2,
            color=GREEN
        )
        volume_ranking.next_to(description, DOWN, buff=0.3)
        
        # 日内收益率排名示例
        return_ranking = Text(
            "日内收益率排名 (2025-01-22):\n" +
            "asset_1: 0.0271 → rank = 0.8\n" +
            "asset_2: 0.0100 → rank = 0.4 (示例)\n" +
            "asset_3: 0.0200 → rank = 0.6 (示例)\n" +
            "asset_4: 0.0050 → rank = 0.2 (示例)\n" +
            "asset_5: 0.0300 → rank = 1.0 (示例)",
            font_size=18,
            line_spacing=1.2,
            color=BLUE
        )
        return_ranking.next_to(volume_ranking, DOWN, buff=0.3)
        
        self.play(Write(step3_title))
        self.play(Write(description))
        self.play(Write(volume_ranking))
        self.play(Write(return_ranking))
        self.wait(3)
        
        self.play(FadeOut(step3_title), FadeOut(description),
                 FadeOut(volume_ranking), FadeOut(return_ranking))
    
    def show_step4(self, title):
        step4_title = Text("步骤4: 6日滚动相关系数", font_size=32, color=ORANGE)
        step4_title.next_to(title, DOWN, buff=0.5)
        
        description = Text("计算两个排名序列在过去6天的相关系数", font_size=24)
        description.next_to(step4_title, DOWN, buff=0.3)
        
        correlation_data = Text(
            "asset_1 过去6天的排名数据:\n" +
            "成交量变化排名: [0.4, 0.6, 0.8, 0.3, 0.5, 0.2]\n" +
            "日内收益率排名: [0.7, 0.3, 0.5, 0.9, 0.4, 0.8]\n" +
            "相关系数 = -0.3 (示例)",
            font_size=18,
            line_spacing=1.2
        )
        correlation_data.next_to(description, DOWN, buff=0.3)
        
        interpretation = Text(
            "负相关表示：成交量增加时日内收益率下降\n" +
            "或成交量减少时日内收益率上升",
            font_size=20,
            line_spacing=1.2,
            color=YELLOW
        )
        interpretation.next_to(correlation_data, DOWN, buff=0.3)
        
        self.play(Write(step4_title))
        self.play(Write(description))
        self.play(Write(correlation_data))
        self.play(Write(interpretation))
        self.wait(3)
        
        self.play(FadeOut(step4_title), FadeOut(description),
                 FadeOut(correlation_data), FadeOut(interpretation))
    
    def show_step5(self, title):
        step5_title = Text("步骤5: 取负值", font_size=32, color=ORANGE)
        step5_title.next_to(title, DOWN, buff=0.5)
        
        description = Text("将相关系数取负值，使负相关变为正的Alpha信号", font_size=24)
        description.next_to(step5_title, DOWN, buff=0.3)
        
        calculation = MathTex(
            r"\text{Alpha\#2} = -1 \times (-0.3) = 0.3",
            font_size=28
        )
        calculation.next_to(description, DOWN, buff=0.3)
        
        interpretation = Text(
            "正值Alpha信号表示：\n" +
            "• 成交量异动与价格表现呈负相关\n" +
            "• 可能反映恐慌性抛售或理性回调",
            font_size=20,
            line_spacing=1.2,
            color=GREEN
        )
        interpretation.next_to(calculation, DOWN, buff=0.3)
        
        self.play(Write(step5_title))
        self.play(Write(description))
        self.play(Write(calculation))
        self.play(Write(interpretation))
        self.wait(3)
        
        self.play(FadeOut(step5_title), FadeOut(description),
                 FadeOut(calculation), FadeOut(interpretation))
    
    def show_final_result(self, title):
        final_title = Text("最终结果", font_size=36, color=BLUE)
        final_title.next_to(title, DOWN, buff=0.5)
        
        result_box = Rectangle(width=8, height=3, color=BLUE, fill_opacity=0.1)
        result_box.next_to(final_title, DOWN, buff=0.3)
        
        result_text = Text(
            "asset_1 在 2025-01-22 的 Alpha#2 值: 0.3\n" +
            "这表明该资产的成交量变化与日内收益率\n呈现负相关关系，产生正的Alpha信号",
            font_size=20,
            line_spacing=1.2
        )
        result_text.move_to(result_box.get_center())
        
        summary = Text(
            "总结：Alpha#2 策略通过捕捉成交量异动与\n"
            "价格表现的负相关性，识别出市场情绪与\n"
            "理性定价分歧的投资机会。当成交量放大\n"
            "但价格下跌时，或成交量萎缩但价格稳定\n"
            "上涨时，该策略会产生正的Alpha信号。",
            font_size=22,
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
        self.wait(0.2)  # 短暂停留

        # 3. 创建并动画引导三连文本
        cta_text = Text(
            "点赞👍 关注🔔 转发🚀",
            font_size=30, # 设置合适的字号
            color=WHITE,   # 使用白色，确保可见
            font="Apple Color Emoji" # 添加字体指定
        )
        # 定位在放大的品牌文字下方
        cta_text.next_to(end_brand_text, DOWN, buff=0.8)

        self.play(Write(cta_text), run_time=1.5) # 文字书写动画
        self.wait(3) # 最后停留3秒展示
        # --- 片尾动画序列结束 ---


# 运行脚本的主函数
if __name__ == "__main__":
    # Manim通过命令行参数处理场景渲染，此处无需额外代码
    pass 