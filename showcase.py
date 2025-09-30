import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine

engine = create_engine("mariadb+pymysql://tyomus:@localhost/etl_project")
sql = """
SELECT created_at, name, price 
FROM assets 
WHERE name IN ('Gold','Bitcoin') 
ORDER BY id;
"""
df = pd.read_sql(sql, engine)

df_pivot = df.pivot(index='created_at', columns='name', values='price')

fig = go.Figure()
fig.add_trace(go.Scatter(x=df_pivot.index,
                         y=df_pivot['Gold'],
                         name='Gold',
                         yaxis='y1',
                         line=dict(color='gold')))
fig.add_trace(go.Scatter(x=df_pivot.index,
                         y=df_pivot['Bitcoin'],
                         name='Bitcoin',
                         yaxis='y2',
                         line=dict(color='darkorange')))

fig.update_layout(
    title="Gold vs Bitcoin (30-min data)",
    yaxis=dict(title="Gold $/oz", side='left'),
    yaxis2=dict(title="Bitcoin $", overlaying='y', side='right')
)

fig.write_html("gold_bitcoin_dualaxis_plot.html", include_plotlyjs="cdn")
