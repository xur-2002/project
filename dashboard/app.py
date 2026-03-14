import os

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="Content Platform Analytics Dashboard", layout="wide")

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_path = os.path.join(project_root, "data", "raw", "content_platform_mock_data.csv")
anomaly_path = os.path.join(project_root, "reports", "tables", "anomaly_summary.csv")
root_path = os.path.join(project_root, "reports", "tables", "root_cause_summary.csv")
ab_path = os.path.join(project_root, "reports", "tables", "ab_test_summary.csv")

st.title("内容平台核心指标监控与实验评估 Dashboard")

if not os.path.exists(raw_path):
    st.error("未找到数据文件，请先运行 src/generate_data.py")
    st.stop()

raw = pd.read_csv(raw_path)
raw["date"] = pd.to_datetime(raw["date"])
raw["interaction_cnt"] = raw["like_cnt"] + raw["comment_cnt"] + raw["share_cnt"]

with st.sidebar:
    st.header("筛选条件")
    category_sel = st.multiselect("内容类目", sorted(raw["content_category"].unique()), default=sorted(raw["content_category"].unique()))
    source_sel = st.multiselect("流量来源", sorted(raw["traffic_source"].unique()), default=sorted(raw["traffic_source"].unique()))
    user_sel = st.multiselect("用户类型", sorted(raw["user_type"].unique()), default=sorted(raw["user_type"].unique()))

f = raw[
    raw["content_category"].isin(category_sel)
    & raw["traffic_source"].isin(source_sel)
    & raw["user_type"].isin(user_sel)
].copy()

agg = f.agg(
    {
        "exposure": "sum",
        "click": "sum",
        "view_complete": "sum",
        "interaction_cnt": "sum",
        "report_cnt": "sum",
        "conversion_cnt": "sum",
    }
)

ctr = agg["click"] / max(agg["exposure"], 1)
complete_rate = agg["view_complete"] / max(agg["click"], 1)
interaction_rate = agg["interaction_cnt"] / max(agg["click"], 1)
report_rate = agg["report_cnt"] / max(agg["exposure"], 1)
conversion_rate = agg["conversion_cnt"] / max(agg["click"], 1)

st.subheader("核心指标总览")
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Exposure", f"{int(agg['exposure']):,}")
c2.metric("CTR", f"{ctr:.2%}")
c3.metric("Complete Rate", f"{complete_rate:.2%}")
c4.metric("Interaction Rate", f"{interaction_rate:.2%}")
c5.metric("Report Rate", f"{report_rate:.3%}")
c6.metric("Conversion Rate", f"{conversion_rate:.2%}")

daily = (
    f.groupby("date", as_index=False)
    .agg(
        {
            "exposure": "sum",
            "click": "sum",
            "view_complete": "sum",
            "interaction_cnt": "sum",
            "report_cnt": "sum",
            "conversion_cnt": "sum",
        }
    )
    .sort_values("date")
)
daily["ctr"] = daily["click"] / daily["exposure"].clip(lower=1)
daily["complete_rate"] = daily["view_complete"] / daily["click"].clip(lower=1)
daily["interaction_rate"] = daily["interaction_cnt"] / daily["click"].clip(lower=1)
daily["report_rate"] = daily["report_cnt"] / daily["exposure"].clip(lower=1)
daily["conversion_rate"] = daily["conversion_cnt"] / daily["click"].clip(lower=1)

st.subheader("趋势监控")
line_df = daily[["date", "ctr", "complete_rate", "interaction_rate", "report_rate", "conversion_rate"]].melt("date", var_name="metric", value_name="value")
fig_line = px.line(line_df, x="date", y="value", color="metric", title="核心指标日趋势")
st.plotly_chart(fig_line, use_container_width=True)

st.subheader("异常告警")
if os.path.exists(anomaly_path):
    anomaly = pd.read_csv(anomaly_path)
    st.dataframe(anomaly.sort_values("date", ascending=False), use_container_width=True)
else:
    st.info("未找到异常结果文件。")

st.subheader("分层归因")
if os.path.exists(root_path):
    root = pd.read_csv(root_path)
    case_options = sorted(root["case_id"].dropna().unique())
    case_sel = st.selectbox("选择 Case", case_options)
    dim_sel = st.selectbox("选择维度", sorted(root["dimension"].dropna().unique()))
    sub = root[(root["case_id"] == case_sel) & (root["dimension"] == dim_sel)].copy()
    fig_bar = px.bar(sub, x="segment", y="contribution", color="segment", title=f"{case_sel} - {dim_sel} 贡献")
    st.plotly_chart(fig_bar, use_container_width=True)
    st.dataframe(sub, use_container_width=True)
else:
    st.info("未找到归因结果文件。")

st.subheader("A/B Test 对比")
if os.path.exists(ab_path):
    ab = pd.read_csv(ab_path)
    st.dataframe(ab, use_container_width=True)
    plot_ab = ab[ab["metric"].isin(["ctr", "conversion_rate", "complete_rate", "report_rate"])].copy()
    fig_ab = px.bar(plot_ab, x="metric", y="lift_pct", color="metric", title="B组相对A组 Lift%")
    st.plotly_chart(fig_ab, use_container_width=True)
else:
    st.info("未找到 A/B 评估文件。")
