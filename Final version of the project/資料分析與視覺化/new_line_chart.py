import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 讀取 CSV 檔案
df = pd.read_csv('final_data.csv', encoding='utf-8')

# 只用不拘經歷的資料
df = df[df['工作經歷'] == '不拘']

# 定義條件和對應的值
conditions = [
    (df['工作待遇'] <= 30000),
    (df['工作待遇'] <= 40000),
    (df['工作待遇'] <= 45000),
    (df['工作待遇'] <= 50000),
    (df['工作待遇'] <= 55000),
    (df['工作待遇'] <= 60000),
    (df['工作待遇'] <= 65000),
    (df['工作待遇'] <= 1000000000)
]
values = [30000, 40000, 45000, 50000, 55000, 60000, 65000, 70000] # 添加其他對應的值

# 使用 numpy.select 進行條件選擇
df['工作待遇'] = np.select(conditions, values, default=df['工作待遇'])

salary = df['工作待遇'].value_counts()

result_df = pd.DataFrame({'salary_index': salary.index, 'count': salary.values})

# 設定中文字型
font = FontProperties(fname=r'C:\Windows\Fonts\msjh.ttc', size=12)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']

x = result_df['salary_index']
y = result_df['count']

# 繪製折線圖
plt.plot(x, y, marker='o', linestyle='')
plt.xticks([30000, 40000, 45000, 50000, 55000, 60000, 65000, 70000], ['小於等於30000元', '30000元~40000元', '40000元~45000元', '45000元~50000元', '50000元~55000元', '55000元~60000元', '60000元~65000元', '70000元以上'], rotation=18)

# 在折線圖的每個資料點上標示該點的數值
for i in range(len(x)):
    plt.text(x[i], y[i], f'{y[i]}', ha='left', va='bottom')

# 添加標題
plt.title('薪資分析圖 (月薪)')

# 總筆數
total_records = len(df)
plt.text(0.87, 0.95, f'總筆數: {total_records}', ha='center', va='center', transform=plt.gca().transAxes)

# 存檔
plt.savefig('line_chart.png')

# 顯示圖形
plt.show()