import pandas as pd
import numpy as np
import os

def calculate_alpha41(df: pd.DataFrame) -> pd.DataFrame:
    """
    计算 Alpha#41: (((high * low)^0.5) - vwap)
    """
    required_cols = ['high', 'low', 'vwap']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"缺少必需列 '{col}'")

    # 确保数据按日期和资产ID排序
    df = df.sort_values(by=['date', 'asset_id']).copy()

    # --- Alpha#41 计算 ---
    # 步骤1: 计算 high 和 low 的几何平均数
    df['geometric_mean_high_low'] = (df['high'] * df['low']) ** 0.5

    # 步骤2: 减去 vwap
    df['alpha41'] = df['geometric_mean_high_low'] - df['vwap']

    # --- 格式化输出 ---
    # 将alpha及相关中间列四舍五入到两位小数
    cols_to_round = ['geometric_mean_high_low', 'alpha41']
    for col in cols_to_round:
        if col in df.columns:
            df[col] = df[col].round(2)

    return df

if __name__ == "__main__":
    # --- 配置 ---
    # 假设此脚本位于 alpha/alpha41/
    # 数据文件位于 data/
    # 输出文件保存到当前目录
    ALPHA_NUMBER = 41
    DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'mock_data.csv')
    OUTPUT_DIR = os.path.dirname(__file__)
    OUTPUT_FILE_PATH = os.path.join(OUTPUT_DIR, f'alpha{ALPHA_NUMBER}_results.csv')

    # --- 加载数据 ---
    try:
        print(f"正在从 {DATA_FILE_PATH} 加载数据...")
        input_df = pd.read_csv(DATA_FILE_PATH)
        print("数据加载成功。")
    except FileNotFoundError:
        print(f"错误: 在 {DATA_FILE_PATH} 未找到数据文件。")
        exit(1)

    # --- 数据预处理 ---
    input_df['date'] = pd.to_datetime(input_df['date'])
    if 'asset_id' in input_df.columns:
        input_df['asset_id'] = input_df['asset_id'].astype(str)
    print("数据预处理完成。")

    # --- 计算 Alpha ---
    try:
        print(f"正在计算 Alpha#{ALPHA_NUMBER}...")
        alpha_df = calculate_alpha41(input_df.copy())
        print(f"Alpha#{ALPHA_NUMBER} 计算完成。")
    except ValueError as ve:
        print(f"计算Alpha时出错: {ve}")
        exit(1)

    # --- 后处理和保存 ---
    # 筛选掉 alpha 列为 NaN 的行
    alpha_df_filtered = alpha_df.dropna(subset=[f'alpha{ALPHA_NUMBER}'])
    print(f"已移除 alpha{ALPHA_NUMBER} 为 NaN 的行，剩余 {len(alpha_df_filtered)} 条记录。")

    # 确保所有原始列都包含在输出中
    original_cols = list(input_df.columns)
    new_cols = ['geometric_mean_high_low', f'alpha{ALPHA_NUMBER}']
    output_cols = original_cols + [col for col in new_cols if col not in original_cols]
    
    # 重新排列列顺序，将新列放在最后
    final_df = alpha_df_filtered[output_cols]

    try:
        final_df.to_csv(OUTPUT_FILE_PATH, index=False, float_format='%.2f')
        print(f"Alpha#{ALPHA_NUMBER} 结果已保存至 {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"保存结果至CSV时出错: {e}")
        exit(1)

    # --- 显示示例结果 ---
    print(f"\n--- Alpha#{ALPHA_NUMBER} 结果示例 ---")
    if not final_df.empty:
        print(final_df.head().to_string())
    else:
        print("结果DataFrame为空。") 