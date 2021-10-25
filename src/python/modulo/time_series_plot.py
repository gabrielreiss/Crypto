import plotly.express as px
import streamlit as st

def time_series_plot(df, coluna, titulo):
    fig = px.line(df, x=df.index, y=coluna, title=titulo)

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    return st.plotly_chart(fig)
