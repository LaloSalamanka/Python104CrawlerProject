import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 讀取 CSV 檔案
df = pd.read_csv('crawler.csv', encoding='utf-8')

# 建立一個字典，將需要轉換的地區映射到新的地區名稱
region_mapping = {
    '北': '雙北',
    '桃園': '桃園',
    '新竹': '新竹',
    '苗栗': '苗栗',
    '台中': '台中',
    '彰化': '彰化',
    '雲林': '雲林',
    '嘉義': '嘉義',
    '台南': '台南',
    '高雄': '高雄',
    '屏東': '屏東',
    '台東': '台東',
    '花蓮': '花蓮',
    '南投': '南投',
    '宜蘭': '宜蘭'
}

# 使用迴圈進行映射
for keyword, replacement in region_mapping.items():
    df.loc[df['company_district'].str.contains(keyword), 'company_district'] = replacement

# 將台灣地區外的資料設為"其他"
not_in_dict = ~df['company_district'].str.contains("|".join(region_mapping.keys()))
df.loc[not_in_dict, 'company_district'] = "其他"

district_counts = df['company_district'].value_counts()

# 將結果轉換為 DataFrame
result_df = pd.DataFrame({'company_district': district_counts.index, 'count': district_counts.values})
# result_df = result_df.sort_values('company_district')
pd.options.display.max_rows = None


# 顯示 DataFrame 的內容
print(result_df)

# 設定中文字型
font = FontProperties(fname=r'C:\Windows\Fonts\msjh.ttc', size=12)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']

# 畫長條圖
bars = plt.bar(result_df['company_district'], result_df['count'])
# 在每個長條圖上方加上整數數字
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 5, int(yval), ha='center', va='bottom', fontproperties=font, size=10)

# 加上標題及標籤
plt.title('職缺分布圖', fontproperties=font)
# plt.xlabel('公司地區', fontproperties=font)
plt.ylabel('職缺數量', fontproperties=font, rotation=0)
plt.gca().yaxis.set_label_coords(-0.08, 0.95)
# 顯示圖表
plt.savefig('job_district_chart.png')
plt.show()
