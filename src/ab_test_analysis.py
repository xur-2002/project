import math
import os
from typing import Dict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm


def two_prop_z_test(success_a: int, total_a: int, success_b: int, total_b: int) -> Dict[str, float]:
    p1 = success_a / max(total_a, 1)
    p2 = success_b / max(total_b, 1)
    p_pool = (success_a + success_b) / max(total_a + total_b, 1)
    se = math.sqrt(max(p_pool * (1 - p_pool) * (1 / max(total_a, 1) + 1 / max(total_b, 1)), 1e-12))
    z = (p2 - p1) / se
    p = 2 * (1 - norm.cdf(abs(z)))
    return {"z": z, "p_value": p, "lift": (p2 - p1) / max(p1, 1e-12)}


def main() -> None:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(project_root, "data", "raw", "content_platform_mock_data.csv")
    out_table = os.path.join(project_root, "reports", "tables", "ab_test_summary.csv")
    out_md = os.path.join(project_root, "reports", "step7_ab_test_evaluation.md")
    out_fig = os.path.join(project_root, "reports", "figures", "ab_test_comparison.png")

    df = pd.read_csv(raw_path)
    df["date"] = pd.to_datetime(df["date"])
    test_df = df[df["date"] >= pd.to_datetime("2026-02-01")].copy()

    agg = (
        test_df.groupby("experiment_group", as_index=False)
        .agg(
            {
                "exposure": "sum",
                "click": "sum",
                "view_complete": "sum",
                "report_cnt": "sum",
                "conversion_cnt": "sum",
                "monetization_revenue": "sum",
            }
        )
    )

    agg["ctr"] = agg["click"] / agg["exposure"]
    agg["complete_rate"] = agg["view_complete"] / agg["click"].clip(lower=1)
    agg["report_rate"] = agg["report_cnt"] / agg["exposure"]
    agg["conversion_rate"] = agg["conversion_cnt"] / agg["click"].clip(lower=1)

    a = agg[agg["experiment_group"] == "A"].iloc[0]
    b = agg[agg["experiment_group"] == "B"].iloc[0]

    tests = {
        "ctr": two_prop_z_test(int(a["click"]), int(a["exposure"]), int(b["click"]), int(b["exposure"])),
        "complete_rate": two_prop_z_test(
            int(a["view_complete"]), int(a["click"]), int(b["view_complete"]), int(b["click"])
        ),
        "report_rate": two_prop_z_test(
            int(a["report_cnt"]), int(a["exposure"]), int(b["report_cnt"]), int(b["exposure"])
        ),
        "conversion_rate": two_prop_z_test(
            int(a["conversion_cnt"]), int(a["click"]), int(b["conversion_cnt"]), int(b["click"])
        ),
    }

    summary_rows = []
    for m in ["ctr", "complete_rate", "report_rate", "conversion_rate"]:
        summary_rows.append(
            {
                "metric": m,
                "group_a": float(a[m]),
                "group_b": float(b[m]),
                "lift_pct": round((float(b[m]) - float(a[m])) / max(float(a[m]), 1e-12) * 100, 2),
                "z_score": round(float(tests[m]["z"]), 4),
                "p_value": float(tests[m]["p_value"]),
                "is_significant_0_05": bool(tests[m]["p_value"] < 0.05),
            }
        )

    rev_lift = (float(b["monetization_revenue"]) - float(a["monetization_revenue"])) / max(float(a["monetization_revenue"]), 1e-12)
    summary_rows.append(
        {
            "metric": "monetization_revenue",
            "group_a": float(a["monetization_revenue"]),
            "group_b": float(b["monetization_revenue"]),
            "lift_pct": round(rev_lift * 100, 2),
            "z_score": None,
            "p_value": None,
            "is_significant_0_05": None,
        }
    )

    summary = pd.DataFrame(summary_rows)
    summary.to_csv(out_table, index=False, encoding="utf-8-sig")

    plot_df = summary[summary["metric"].isin(["ctr", "conversion_rate", "complete_rate", "report_rate"])].copy()
    fig = plt.figure(figsize=(10, 5))
    bars = plt.bar(plot_df["metric"], plot_df["lift_pct"], color=["#2a9d8f", "#2a9d8f", "#e9c46a", "#e76f51"])
    plt.axhline(0, color="black", linewidth=1)
    plt.ylabel("Lift % (B vs A)")
    plt.title("A/B Test Metric Lift")
    for b_ in bars:
        h = b_.get_height()
        plt.text(b_.get_x() + b_.get_width() / 2, h, f"{h:.2f}%", ha="center", va="bottom", fontsize=9)
    plt.tight_layout()
    plt.savefig(out_fig, dpi=140)
    plt.close(fig)

    ctr_ok = summary.loc[summary["metric"] == "ctr", "lift_pct"].iloc[0] > 0
    cvr_ok = summary.loc[summary["metric"] == "conversion_rate", "lift_pct"].iloc[0] > 0
    report_risk = summary.loc[summary["metric"] == "report_rate", "lift_pct"].iloc[0] > 10
    complete_drop = summary.loc[summary["metric"] == "complete_rate", "lift_pct"].iloc[0] < -2

    if ctr_ok and cvr_ok and (report_risk or complete_drop):
        decision = "建议灰度放量，不建议直接全量。先上线到20%-30%并叠加风险治理策略。"
    elif ctr_ok and cvr_ok:
        decision = "建议推广上线。"
    else:
        decision = "不建议推广，需继续迭代实验策略。"

    md_lines = [
        "# Step 7 A/B Test 评估",
        "",
        "## 实验背景",
        "针对推荐卡片样式改版进行 A/B Test，目标是在提升点击与转化的同时控制生态风险。",
        "",
        "## 指标角色",
        "1. 核心指标: CTR, Conversion Rate, Revenue",
        "2. 护栏指标: Report Rate, Complete Rate",
        "",
        "## 结果摘要",
        "| 指标 | A组 | B组 | Lift% | p-value |",
        "|---|---:|---:|---:|---:|",
    ]

    for _, r in summary.iterrows():
        p = "-" if pd.isna(r["p_value"]) else f"{r['p_value']:.6f}"
        md_lines.append(f"| {r['metric']} | {r['group_a']:.6f} | {r['group_b']:.6f} | {r['lift_pct']:.2f}% | {p} |")

    md_lines.extend(
        [
            "",
            "## 业务结论",
            decision,
            "",
            "## 上线建议",
            "1. 采用分阶段灰度发布，按日跟踪举报率与完播率。",
            "2. 对高风险分层设置自动回滚阈值。",
            "3. 保留A组10%流量作为长期对照。",
        ]
    )

    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"Saved: {out_table}")
    print(f"Saved: {out_md}")
    print(f"Saved: {out_fig}")


if __name__ == "__main__":
    main()
