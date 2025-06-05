import pandas as pd

# 读取数据
def load_data():
    # 假设数据存储在data文件夹下的某个CSV文件中
    data_path = '../../data/mock_data.csv'
    df = pd.read_csv(data_path)
    # 确保 'date' 列是 datetime 对象，以便正确排序和分组
    df['date'] = pd.to_datetime(df['date'])
    return df

# 计算Alpha#8
def calculate_alpha8(df):
    # 确保数据按 asset_id 和 date 排序
    df = df.sort_values(by=['asset_id', 'date']).reset_index(drop=True)

    # 按 asset_id 分组计算时间序列相关的指标
    df['sum_open_5'] = df.groupby('asset_id')['open'].rolling(window=5).sum().reset_index(level=0, drop=True).round(2)
    df['sum_returns_5'] = df.groupby('asset_id')['returns'].rolling(window=5).sum().reset_index(level=0, drop=True).round(2)
    
    df['open_returns_product'] = (df['sum_open_5'] * df['sum_returns_5']).round(2)
    
    # 按 asset_id 分组进行 shift 操作
    df['delayed_product'] = df.groupby('asset_id')['open_returns_product'].transform(lambda x: x.shift(10)).round(2)
    
    df['product_diff'] = (df['open_returns_product'] - df['delayed_product']).round(2)
    
    # 按 date 分组进行截面排名
    df['rank_diff'] = df.groupby('date')['product_diff'].rank(method='average', ascending=True, pct=True, na_option='keep')
    
    # 对排名结果取负值，得到Alpha#8，并保留两位小数
    df['alpha8'] = (-1 * df['rank_diff']).round(2)
    
    return df

# 保存结果
def save_results(df):
    output_path = 'alpha8_results.csv'
    df.to_csv(output_path, index=False)
    print(f"结果已保存到 {output_path}")

# 主函数
def main():
    # 加载数据
    df = load_data()
    
    # 计算Alpha#8
    df = calculate_alpha8(df)
    
    # 保存结果
    save_results(df)

if __name__ == "__main__":
    main() 