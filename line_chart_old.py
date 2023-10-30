import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import re
# 讀取 CSV 檔案
df = pd.read_csv('crawler.csv', encoding='utf-8')

experience_counts = df['company_required_experience'].value_counts()

result_df = pd.DataFrame({'experience_index': experience_counts.index, 'count': experience_counts.values})

# 設定中文字型
font = FontProperties(fname=r'C:\Windows\Fonts\msjh.ttc', size=12)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']

x = result_df['experience_index']
y = result_df['count']

# 繪製折線圖
plt.plot(x, y, marker='o', linestyle='-')
plt.xticks(rotation=35)

for i in range(len(x)):
    plt.text(x[i], y[i], f'{y[i]}', ha='left', va='bottom')

# 添加 x 和 y 軸標籤
plt.xlabel('要求經歷')
plt.ylabel('職缺數量', rotation=0)
plt.gca().yaxis.set_label_coords(-0.08, 1.02)
# 添加標題
plt.title('職缺經歷圖')

# 存檔
plt.savefig('pie_chart.png')

# 顯示圖形
plt.show()