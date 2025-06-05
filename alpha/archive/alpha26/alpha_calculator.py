import pandas as pd
import numpy as np
from typing import Union, Optional
from pathlib import Path
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Alpha26Calculator:
    """Alpha#26 因子计算器
    
    计算公式: (-1 * ts_max(correlation(ts_rank(volume, 5), ts_rank(high, 5), 5), 3))
    """
    
    def __init__(self, data_path: Union[str, Path]):
        """初始化计算器
        
        Args:
            data_path: 数据文件路径
        """
        self.data_path = Path(data_path)
        self.data = None
        self.result = None
        
    def load_data(self) -> None:
        """加载数据"""
        logger.info(f"正在从 {self.data_path} 加载数据...")
        try:
            self.data = pd.read_csv(self.data_path, index_col=0)
            self.data.index = pd.to_datetime(self.data.index)
            logger.info(f"数据加载完成，共 {len(self.data)} 条记录")
        except Exception as e:
            logger.error(f"数据加载失败: {e}")
            raise
            
    def ts_rank(self, series: pd.Series, window: int) -> pd.Series:
        """计算时序排名
        
        Args:
            series: 输入序列
            window: 窗口大小
            
        Returns:
            排名序列
        """
        return series.rolling(window).rank(pct=True)
        
    def calculate_alpha(self) -> None:
        """计算 Alpha#26 因子值"""
        try:
            # 确保数据已加载
            if self.data is None:
                self.load_data()
                
            # 计算成交量和最高价的5日排名
            volume_rank = self.ts_rank(self.data['volume'], 5)
            high_rank = self.ts_rank(self.data['high'], 5)
            
            # 计算5日相关系数
            correlation = volume_rank.rolling(5).corr(high_rank)
            
            # 计算3日最大值
            max_correlation = correlation.rolling(3).max()
            
            # 取负值并保留两位小数
            self.result = (-1 * max_correlation).round(2)
            
            # 添加原始数据列
            result_df = pd.DataFrame({
                'volume': self.data['volume'],
                'high': self.data['high'],
                'alpha26': self.result
            })
            
            self.result = result_df
            logger.info("Alpha#26 因子计算完成")
            
        except Exception as e:
            logger.error(f"因子计算失败: {e}")
            raise
            
    def save_result(self, save_path: Optional[Union[str, Path]] = None) -> None:
        """保存计算结果
        
        Args:
            save_path: 保存路径，默认为当前目录下的 alpha26_results.csv
        """
        if self.result is None:
            logger.warning("没有可保存的结果")
            return
            
        save_path = Path(save_path) if save_path else Path('alpha26_results.csv')
        try:
            self.result.to_csv(save_path)
            logger.info(f"结果已保存至 {save_path}")
        except Exception as e:
            logger.error(f"结果保存失败: {e}")
            raise

def main():
    """主函数"""
    # 设置数据路径
    data_path = Path("../../data/mock_data.csv")
    
    # 创建计算器实例
    calculator = Alpha26Calculator(data_path)
    
    try:
        # 计算因子
        calculator.calculate_alpha()
        
        # 保存结果
        save_path = Path("alpha26_results.csv")
        calculator.save_result(save_path)
        
    except Exception as e:
        logger.error(f"程序执行失败: {e}")
        raise

if __name__ == "__main__":
    main() 