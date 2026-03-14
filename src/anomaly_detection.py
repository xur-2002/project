import os
from typing import Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def compute_daily_metrics(df: pd.DataFrame) -> pd.DataFrame:
    daily = (
        df.groupby("date", as_index=False)
        .agg(
            {
                "exposure": "sum",
                "click": "sum",
                "view_complete": "sum",
                "like_cnt": "sum",
                "comment_cnt": "sum",
                "share_cnt": "sum",
                "report_cnt": "sum",
                "conversion_cnt": "sum",
            }
        )
        .sort_values("date")
    )

    daily["interaction_cnt"] = daily["like_cnt"] + daily["comment_cnt"] + daily["share_cnt"]
    daily["ctr"] = daily["click"] / daily["exposure"]
    daily["complete_rate"] = daily["view_complete"] / daily["click"].clip(lower=1)
    daily["interaction_rate"] = daily["interaction_cnt"] / daily["click"].clip(lower=1)
    daily["report_rate"] = daily["report_cnt"] / daily["exposure"]
    daily["conversion_rate"] = daily["conversion_cnt"] / daily["click"].clip(lower=1)

    return daily


def detect_anomalies(daily: pd.DataFrame, metric_cols: List[str]) -> pd.DataFrame:
    records: List[Dict] = []

    for metric in metric_cols:
        s = daily[metric]
        baseline = s.rolling(window=7, min_periods=5).mean().shift(1)
        std = s.rolling(window=7, min_periods=5).std(ddof=0).shift(1)
        pct_change = (s - baseline) / baseline

        flag = (
            baseline.notna()
            & std.notna()
            & ((s - baseline).abs() > 2.5 * std.clip(lower=1e-8))
            & (pct_change.abs() > 0.12)
        )

        flagged = daily.loc[flag, ["date", metric]].copy()
        for idx, row in flagged.iterrows():
            b = baseline.loc[idx]
            val = row[metric]
            delta = val - b
            direction = "up" if delta > 0 else "down"
            records.append(
                {
                    "date": row["date"],
                    "metric": metric,
                    "value": round(float(val), 6),
                    "baseline_7d": round(float(b), 6),
                    "delta": round(float(delta), 6),
                    "delta_pct": round(float((delta / b) * 100), 2),
                    "direction": direction,
                    "scope": "overall",
                    "dimension": "all",
                    "segment": "all",
                }
            )

    res = pd.DataFrame(records).sort_values(["date", "metric"]) if records else pd.DataFrame(
        columns=[
            "date",
            "metric",
            "value",
            "baseline_7d",
            "delta",
            "delta_pct",
            "direction",
            "scope",
            "dimension",
            "segment",
        ]
    )
    return res


def detect_segment_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    records: List[Dict] = []
    watch_items = [
        ("content_category", "entertainment", "ctr"),
        ("content_category", "food", "report_rate"),
        ("traffic_source", "follow", "conversion_rate"),
        ("traffic_source", "search", "report_rate"),
        ("user_type", "new_user", "conversion_rate"),
        ("traffic_source", "recommendation", "ctr"),
    ]

    for dim, segment, metric in watch_items:
        sub = df[df[dim] == segment].copy()
        if sub.empty:
            continue

        daily = (
            sub.groupby("date", as_index=False)
            .agg(
                {
                    "exposure": "sum",
                    "click": "sum",
                    "view_complete": "sum",
                    "like_cnt": "sum",
                    "comment_cnt": "sum",
                    "share_cnt": "sum",
                    "report_cnt": "sum",
                    "conversion_cnt": "sum",
                }
            )
            .sort_values("date")
        )
        daily["ctr"] = daily["click"] / daily["exposure"].clip(lower=1)
        daily["report_rate"] = daily["report_cnt"] / daily["exposure"].clip(lower=1)
        daily["conversion_rate"] = daily["conversion_cnt"] / daily["click"].clip(lower=1)

        s = daily[metric]
        baseline = s.rolling(window=7, min_periods=5).mean().shift(1)
        std = s.rolling(window=7, min_periods=5).std(ddof=0).shift(1)
        pct_change = (s - baseline) / baseline

        flag = (
            baseline.notna()
            & std.notna()
            & ((s - baseline).abs() > 2.0 * std.clip(lower=1e-8))
            & (pct_change.abs() > 0.08)
        )

        flagged = daily.loc[flag, ["date", metric]].copy()
        for idx, row in flagged.iterrows():
            b = baseline.loc[idx]
            val = row[metric]
            delta = val - b
            direction = "up" if delta > 0 else "down"
            records.append(
                {
                    "date": row["date"],
                    "metric": metric,
                    "value": round(float(val), 6),
                    "baseline_7d": round(float(b), 6),
                    "delta": round(float(delta), 6),
                    "delta_pct": round(float((delta / b) * 100), 2),
                    "direction": direction,
                    "scope": "segment",
                    "dimension": dim,
                    "segment": segment,
                }
            )

    if not records:
        return pd.DataFrame(
            columns=[
                "date",
                "metric",
                "value",
                "baseline_7d",
                "delta",
                "delta_pct",
                "direction",
                "scope",
                "dimension",
                "segment",
            ]
        )
    return pd.DataFrame(records).sort_values(["date", "dimension", "segment", "metric"])


def plot_metrics(daily: pd.DataFrame, anomalies: pd.DataFrame, fig_dir: str) -> None:
    metrics = ["ctr", "complete_rate", "interaction_rate", "report_rate", "conversion_rate"]
    fig, axes = plt.subplots(5, 1, figsize=(14, 16), sharex=True)

    for i, metric in enumerate(metrics):
        ax = axes[i]
        ax.plot(daily["date"], daily[metric], label=metric, color="#1f77b4", linewidth=1.8)
        sub = anomalies[anomalies["metric"] == metric]
        if not sub.empty:
            mark = daily[daily["date"].isin(sub["date"])]
            ax.scatter(mark["date"], mark[metric], color="#d62728", s=28, label="anomaly")
        ax.set_ylabel(metric)
        ax.grid(alpha=0.25)
        ax.legend(loc="upper right")

    axes[-1].set_xlabel("date")
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "step5_metric_trend_with_anomalies.png"), dpi=140)
    plt.close(fig)


def save_markdown_report(daily: pd.DataFrame, anomalies: pd.DataFrame, path: str) -> None:
    lines = []
    lines.append("# Step 5 异常监控分析")
    lines.append("")
    lines.append("## 方法说明")
    lines.append("1. 按日聚合核心指标并计算 CTR、完播率、互动率、举报率、转化率。")
    lines.append("2. 使用前 7 日移动均值作为基线，结合标准差阈值与偏离比例识别异常。")
    lines.append("3. 全局规则：|当日值-基线| > 2.5*std 且偏离比例 > 12%。")
    lines.append("4. 分层规则：|当日值-基线| > 2.0*std 且偏离比例 > 8%。")
    lines.append("")
    lines.append("## 异常识别结果")
    lines.append(f"共识别异常点 {len(anomalies)} 个。")
    lines.append("")

    if anomalies.empty:
        lines.append("当前未识别到满足规则的异常点。")
    else:
        lines.append("| 日期 | 作用域 | 维度 | 分层 | 指标 | 当日值 | 基线 | 变动% | 业务判断 |")
        lines.append("|---|---|---|---|---:|---:|---:|---:|---|")
        for _, r in anomalies.head(20).iterrows():
            if r["metric"] == "ctr" and r["direction"] == "down":
                sentence = "点击吸引力下降，需优先排查推荐内容供给质量。"
            elif r["metric"] == "report_rate" and r["direction"] == "up":
                sentence = "生态风险抬升，建议联动审核策略和问题类目治理。"
            elif r["metric"] == "conversion_rate" and r["direction"] == "down":
                sentence = "商业转化效率下滑，需检查链路与人群匹配。"
            else:
                sentence = "指标偏离基线，建议进入分层归因排查。"

            lines.append(
                f"| {r['date']} | {r['scope']} | {r['dimension']} | {r['segment']} | {r['metric']} | {r['value']:.4f} | {r['baseline_7d']:.4f} | {r['delta_pct']:.2f}% | {sentence} |"
            )

    lines.append("")
    lines.append("## 下一步")
    lines.append("基于异常时间窗进入内容类目、流量来源、用户类型分层归因分析。")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> None:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(project_root, "data", "raw", "content_platform_mock_data.csv")
    out_table = os.path.join(project_root, "reports", "tables", "anomaly_summary.csv")
    out_report = os.path.join(project_root, "reports", "step5_anomaly_analysis.md")
    fig_dir = os.path.join(project_root, "reports", "figures")

    df = pd.read_csv(raw_path)
    daily = compute_daily_metrics(df)
    anomalies_overall = detect_anomalies(
        daily,
        metric_cols=["ctr", "complete_rate", "interaction_rate", "report_rate", "conversion_rate"],
    )
    anomalies_segment = detect_segment_anomalies(df)
    anomalies = pd.concat([anomalies_overall, anomalies_segment], ignore_index=True).drop_duplicates(
        subset=["date", "metric", "scope", "dimension", "segment"],
        keep="first",
    ).sort_values(["date", "scope", "dimension", "segment", "metric"])

    anomalies.to_csv(out_table, index=False, encoding="utf-8-sig")
    plot_metrics(daily, anomalies, fig_dir)
    save_markdown_report(daily, anomalies, out_report)

    print(f"Saved: {out_table}")
    print(f"Saved: {out_report}")
    print(f"Saved: {os.path.join(fig_dir, 'step5_metric_trend_with_anomalies.png')}")
    print(f"Detected anomalies: {len(anomalies)}")


if __name__ == "__main__":
    main()
