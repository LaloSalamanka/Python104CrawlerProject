import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 讀取 CSV 檔案
df = pd.read_csv('final_data.csv', encoding='utf-8')

# 只用不拘經歷的資料
df = df[df['工作經歷'] == '不拘']

district_counts = df['上班地點'].value_counts()

# 將結果轉換為 DataFrame
result_df = pd.DataFrame({'company_district': district_counts.index, 'count': district_counts.values})

# 設定中文字型
font = FontProperties(fname=r'C:\Windows\Fonts\msjh.ttc', size=12)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']

# 畫長條圖
bars = plt.bar(result_df['company_district'], result_df['count'])
# 在每個長條圖上方加上整數數字
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 4, int(yval), ha='center', va='bottom', fontproperties=font, size=10)

# 加上標題及標籤
plt.title('職缺分布圖', fontsize=16)
plt.ylabel('職缺數量', rotation=0)
plt.gca().yaxis.set_label_coords(-0.08, 0.98)

# 總筆數
total_records = len(df)
plt.text(0.9, 0.95, f'總筆數: {total_records}', ha='center', va='center', transform=plt.gca().transAxes)

# 顯示圖表
plt.savefig('new_bar_chart.png')
plt.show()
