import pandas as pd
import re
import numpy as np

# 讀取 CSV 檔案
df = pd.read_csv('crawler_data.csv', encoding='utf-8')

# 整理工作經歷
replace_values = ['10年以上', '4年以上', '8年以上', '6年以上', '7年以上']
df['工作經歷'] = df['工作經歷'].replace(replace_values, '其他')

# 把日期的'更新'拿掉
df['職缺更新時間'] = df['職缺更新時間'].str.replace('更新', '')


# 工作待遇資料整理; 將工作待遇轉為int
# -------------------------------------------------------------------------------------------
df = df.dropna(subset=['工作待遇']) # 刪除包含 NaN 的行
def extract_salary(salary_str):
    if pd.isna(salary_str):
        return None

    if isinstance(salary_str, (float, int)):
        return int(salary_str)  # 直接返回整數

    salary_str = salary_str.replace(',', '')  # 去除逗號
    if '待遇面議' in salary_str:
        return int(40000)  # 或者你可以使用其他預設值
    if '月薪' in salary_str:
        match = re.search(r'(\d+)', salary_str)
        if match:
            return int(match.group(1))
    elif '年薪' in salary_str:
        match = re.search(r'(\d+)~?(\d+)?', salary_str)
        if match:
            return int(match.group(1)) / 12
    return None
# 將薪資字串轉換為整數，並添加到 DataFrame
df['工作待遇'] = df['工作待遇'].apply(extract_salary).astype(int)

# 定義區間 bins
bins = [0, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 200000]
# 使用 cut 函數將分數劃分為不同的等級, 且新增一個salary_range欄位
df['工作待遇範圍'] = pd.cut(df['工作待遇'], bins)
# -------------------------------------------------------------------------------------------


# 員工人數資料整理
# -------------------------------------------------------------------------------------------
#   將員工人數轉為int，且新增一欄位"公司規模": 小型企業-小於50人; 中型企業-小於250人; 大型企業-大於250人
df = df[df['員工人數'] != '暫不提供']  # 只取得有人數的資料

# 將員工人數轉換為int
df['員工人數'] = df['員工人數'].str.replace('人', '')
df['員工人數'] = pd.to_numeric(df['員工人數'], errors='coerce')

# 定義條件和對應的值
conditions = [
    (df['員工人數'] <= 50),
    (df['員工人數'] < 250),
    (df['員工人數'] >= 250)
]
values = ['小型企業', '中型企業', '大型企業']

# 使用 np.select 創建新的企業規模欄位 '企業規模'
df['企業規模'] = np.select(conditions, values, default=None)
# -------------------------------------------------------------------------------------------
df.to_csv('final_data.csv', index=False, encoding='utf-8')
