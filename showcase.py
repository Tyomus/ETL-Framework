import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine("mariadb+pymysql://tyomus:@localhost/etl_project")
sql = """
SELECT created_at, name, price FROM assets WHERE name IN ('Gold','Bitcoin') ORDER BY id;
"""
df = pd.read_sql(sql, engine)

df_pivot = df.pivot(index='created_at', columns='name', values='price')

fig, ax1 = plt.subplots(figsize=(10,5))
ax1.plot(df_pivot.index, df_pivot['Gold'], color='gold', label='Gold')
ax1.set_ylabel("Gold Price (USD/oz)", color='gold')

ax2 = ax1.twinx()
ax2.plot(df_pivot.index, df_pivot['Bitcoin'], color='darkorange', label='Bitcoin')
ax2.set_ylabel("Bitcoin Price (USD)", color='darkorange')

fig.write_html("gold_bitcoin_dualaxis.html", include_plotlyjs="cdn")
