import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties

df = pd.read_csv('final_data.csv', encoding='utf-8')

# 設定中文字型
font = FontProperties(fname=r'C:\Windows\Fonts\msjh.ttc', size=12)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams.update({'font.size': 9})

# 工作經歷
experience_counts = df['工作經歷'].value_counts()
total_records = len(df)
# 畫圓餅圖
explode = (0.2, 0, 0, 0, 0, 0)
plt.pie(experience_counts.values, labels=experience_counts.index, autopct=lambda p: '{:.0f}筆 ({:.0f}%)'.format(p * total_records / 100, p), startangle=140, pctdistance=0.7, explode=explode)

# 設定圖表標題
plt.title('工作經歷統計圖', fontsize=16)
plt.text(1.15, 0.95, f'總筆數: {total_records}', ha='center', va='center', transform=plt.gca().transAxes)

# 存檔
plt.savefig('new_pie_chart.png')
# 顯示圖表
plt.show()