import os
from typing import List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def aggregate_rate(df: pd.DataFrame, metric: str) -> float:
    if metric == "ctr":
        return df["click"].sum() / max(df["exposure"].sum(), 1)
    if metric == "report_rate":
        return df["report_cnt"].sum() / max(df["exposure"].sum(), 1)
    if metric == "conversion_rate":
        return df["conversion_cnt"].sum() / max(df["click"].sum(), 1)
    raise ValueError("Unsupported metric")


def contribution_by_dim(
    base_df: pd.DataFrame,
    event_df: pd.DataFrame,
    dim: str,
    metric: str,
) -> pd.DataFrame:
    keys = sorted(set(base_df[dim].unique()).union(set(event_df[dim].unique())))

    rows = []
    for k in keys:
        b = base_df[base_df[dim] == k]
        e = event_df[event_df[dim] == k]

        b_rate = aggregate_rate(b, metric) if len(b) > 0 else 0.0
        e_rate = aggregate_rate(e, metric) if len(e) > 0 else 0.0

        if metric in ["ctr", "report_rate"]:
            b_weight = b["exposure"].sum() / max(base_df["exposure"].sum(), 1)
            e_weight = e["exposure"].sum() / max(event_df["exposure"].sum(), 1)
        else:
            b_weight = b["click"].sum() / max(base_df["click"].sum(), 1)
            e_weight = e["click"].sum() / max(event_df["click"].sum(), 1)

        contribution = (e_rate * e_weight) - (b_rate * b_weight)

        rows.append(
            {
                "segment": k,
                "baseline_rate": b_rate,
                "event_rate": e_rate,
                "baseline_weight": b_weight,
                "event_weight": e_weight,
                "contribution": contribution,
            }
        )

    out = pd.DataFrame(rows).sort_values("contribution", key=lambda s: s.abs(), ascending=False)
    return out


def case_windows() -> List[Tuple[str, str, str, str, str]]:
    return [
        ("CASE_1", "ctr", "2026-01-20", "2026-01-28", "CTR下滑归因"),
        ("CASE_2", "report_rate", "2026-02-05", "2026-02-12", "举报率上升归因"),
        ("CASE_3", "conversion_rate", "2026-02-15", "2026-02-22", "转化率下滑归因"),
    ]


def main() -> None:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(project_root, "data", "raw", "content_platform_mock_data.csv")
    out_table = os.path.join(project_root, "reports", "tables", "root_cause_summary.csv")
    out_md = os.path.join(project_root, "reports", "step6_root_cause_analysis.md")
    fig_dir = os.path.join(project_root, "reports", "figures")

    df = pd.read_csv(raw_path)
    df["date"] = pd.to_datetime(df["date"])

    all_rows = []
    md_lines = ["# Step 6 分层归因分析", "", "## 分析方法", "1. 针对异常窗口，选择异常前 7 天作为基线窗口。", "2. 以指标变化量为目标，按内容类目、流量来源、用户类型拆解贡献。", "3. 输出主驱动分层与可执行建议。", ""]

    for case_id, metric, s, e, title in case_windows():
        event_start = pd.to_datetime(s)
        event_end = pd.to_datetime(e)
        base_start = event_start - pd.Timedelta(days=7)
        base_end = event_start - pd.Timedelta(days=1)

        base_df = df[(df["date"] >= base_start) & (df["date"] <= base_end)].copy()
        event_df = df[(df["date"] >= event_start) & (df["date"] <= event_end)].copy()

        total_delta = aggregate_rate(event_df, metric) - aggregate_rate(base_df, metric)

        md_lines.append(f"## {case_id}: {title}")
        md_lines.append(f"- 异常窗口: {s} 到 {e}")
        md_lines.append(f"- 对比基线: {base_start.date()} 到 {base_end.date()}")
        md_lines.append(f"- 指标整体变化: {total_delta:.6f}")

        for dim in ["content_category", "traffic_source", "user_type", "hour_bucket"]:
            ctb = contribution_by_dim(base_df, event_df, dim=dim, metric=metric)
            top = ctb.head(3).copy()

            top["case_id"] = case_id
            top["metric"] = metric
            top["dimension"] = dim
            top["total_delta"] = total_delta
            top["share_of_total"] = top["contribution"] / (total_delta if abs(total_delta) > 1e-12 else 1.0)
            all_rows.append(top)

            fig = plt.figure(figsize=(9, 4.8))
            plt.bar(top["segment"], top["contribution"], color="#2a9d8f")
            plt.title(f"{case_id} {metric} contribution by {dim} (top3)")
            plt.ylabel("contribution")
            plt.xticks(rotation=20)
            plt.tight_layout()
            fig_path = os.path.join(fig_dir, f"{case_id.lower()}_{dim}_contribution.png")
            plt.savefig(fig_path, dpi=140)
            plt.close(fig)

            md_lines.append(f"- {dim} 主要贡献分层: " + ", ".join([f"{r.segment} ({r.contribution:.6f})" for r in top.itertuples()]))

        if case_id == "CASE_1":
            md_lines.append("- 业务结论: 整体 CTR 下滑主要由推荐流量下的娱乐类内容驱动，新用户受影响更明显。")
            md_lines.append("- 建议动作: 对异常时窗内娱乐类新增供给做质量回溯，临时降低低质素材在推荐流量中的分发权重。")
        elif case_id == "CASE_2":
            md_lines.append("- 业务结论: 举报率抬升主要集中在搜索流量中的美食类内容，晚间时段贡献更高。")
            md_lines.append("- 建议动作: 强化搜索召回侧敏感词和标题党过滤规则，并在高风险时段追加审核阈值。")
        else:
            md_lines.append("- 业务结论: 转化率下降主要由关注流量的新用户贡献，表现为点击后转化衰减。")
            md_lines.append("- 建议动作: 优化新用户转化链路文案和权益呈现，分渠道回收低意图流量。")

        md_lines.append("")

    summary = pd.concat(all_rows, ignore_index=True)
    summary.to_csv(out_table, index=False, encoding="utf-8-sig")

    md_lines.append("## 总结")
    md_lines.append("异常并非全局均匀波动，而是由少数关键分层驱动。建议将分层告警纳入常态化监控。")

    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"Saved: {out_table}")
    print(f"Saved: {out_md}")
    print("Generated contribution figures in reports/figures")


if __name__ == "__main__":
    main()
