import os
from datetime import datetime

import numpy as np
import pandas as pd


RNG = np.random.default_rng(42)


def safe_binomial(n: int, p: float) -> int:
    p = min(max(p, 0.0001), 0.9999)
    return int(RNG.binomial(n=n, p=p))


def generate_mock_data() -> pd.DataFrame:
    start_date = datetime(2025, 12, 1)
    end_date = datetime(2026, 2, 28)
    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    categories = ["food", "travel", "entertainment", "knowledge", "local_services"]
    sources = ["recommendation", "search", "follow", "nearby"]
    user_types = ["new_user", "active_user", "returning_user"]
    groups = ["A", "B"]
    hour_buckets = ["morning", "afternoon", "evening"]
    city_tiers = ["tier1", "tier2", "tier3"]

    cat_weight = {
        "food": 1.10,
        "travel": 0.95,
        "entertainment": 1.25,
        "knowledge": 0.90,
        "local_services": 1.05,
    }
    src_weight = {
        "recommendation": 1.35,
        "search": 1.05,
        "follow": 0.80,
        "nearby": 0.90,
    }
    user_weight = {
        "new_user": 0.95,
        "active_user": 1.20,
        "returning_user": 0.85,
    }
    hour_weight = {
        "morning": 0.90,
        "afternoon": 1.00,
        "evening": 1.25,
    }
    city_weight = {
        "tier1": 1.20,
        "tier2": 1.00,
        "tier3": 0.85,
    }

    rows = []

    for d in dates:
        weekly_factor = 1.10 if d.weekday() in [5, 6] else 1.00

        for cat in categories:
            for src in sources:
                for user in user_types:
                    for grp in groups:
                        for hb in hour_buckets:
                            for tier in city_tiers:
                                base_exposure = 1400
                                factor = (
                                    cat_weight[cat]
                                    * src_weight[src]
                                    * user_weight[user]
                                    * hour_weight[hb]
                                    * city_weight[tier]
                                    * weekly_factor
                                )
                                noise = float(RNG.normal(1.0, 0.08))
                                exposure = int(max(120, base_exposure * factor * noise))

                                # Baseline rates
                                ctr = 0.095
                                complete_rate = 0.52
                                interaction_rate = 0.28
                                report_rate = 0.0018
                                conversion_rate = 0.072

                                if cat == "entertainment":
                                    ctr += 0.008
                                    report_rate += 0.0003
                                if src == "recommendation":
                                    ctr += 0.010
                                if src == "search":
                                    conversion_rate += 0.010
                                if user == "new_user":
                                    complete_rate -= 0.03
                                    conversion_rate -= 0.01
                                if hb == "evening":
                                    ctr += 0.004
                                    interaction_rate += 0.02

                                # A/B experiment effect from 2026-02-01 onward
                                if d >= datetime(2026, 2, 1) and grp == "B":
                                    ctr *= 1.08
                                    conversion_rate *= 1.06
                                    report_rate *= 1.18
                                    complete_rate *= 0.96

                                # Anomaly 1: CTR drop on entertainment + recommendation
                                if datetime(2026, 1, 20) <= d <= datetime(2026, 1, 28):
                                    if cat == "entertainment" and src == "recommendation":
                                        ctr *= 0.65

                                # Anomaly 2: report spike on food + search
                                if datetime(2026, 2, 5) <= d <= datetime(2026, 2, 12):
                                    if cat == "food" and src == "search":
                                        report_rate *= 2.6

                                # Anomaly 3: conversion drop for new users on follow source
                                if datetime(2026, 2, 15) <= d <= datetime(2026, 2, 22):
                                    if user == "new_user" and src == "follow":
                                        conversion_rate *= 0.55

                                click = safe_binomial(exposure, ctr)
                                view_complete = safe_binomial(click, complete_rate) if click > 0 else 0

                                interaction_cnt = safe_binomial(click, interaction_rate) if click > 0 else 0
                                like_ratio, comment_ratio = 0.72, 0.20
                                like_cnt = int(interaction_cnt * like_ratio)
                                comment_cnt = int(interaction_cnt * comment_ratio)
                                share_cnt = max(0, interaction_cnt - like_cnt - comment_cnt)

                                report_cnt = safe_binomial(exposure, report_rate)
                                conversion_cnt = safe_binomial(click, conversion_rate) if click > 0 else 0

                                avg_watch_seconds = max(6.0, RNG.normal(32.0, 4.0))
                                if user == "new_user":
                                    avg_watch_seconds -= 2.2
                                if hb == "evening":
                                    avg_watch_seconds += 1.3
                                if grp == "B" and d >= datetime(2026, 2, 1):
                                    avg_watch_seconds -= 0.8

                                monetization_revenue = round(
                                    conversion_cnt * float(RNG.normal(37.0, 6.0)),
                                    2,
                                )
                                session_uv = int(max(50, exposure * float(RNG.normal(0.33, 0.03))))

                                rows.append(
                                    {
                                        "date": d.strftime("%Y-%m-%d"),
                                        "week_day": d.day_name(),
                                        "hour_bucket": hb,
                                        "content_category": cat,
                                        "traffic_source": src,
                                        "user_type": user,
                                        "city_tier": tier,
                                        "experiment_group": grp,
                                        "content_supply_cnt": int(max(50, exposure / 6.5)),
                                        "exposure": exposure,
                                        "click": click,
                                        "view_complete": view_complete,
                                        "like_cnt": like_cnt,
                                        "comment_cnt": comment_cnt,
                                        "share_cnt": share_cnt,
                                        "report_cnt": report_cnt,
                                        "conversion_cnt": conversion_cnt,
                                        "avg_watch_seconds": round(avg_watch_seconds, 2),
                                        "monetization_revenue": monetization_revenue,
                                        "session_uv": session_uv,
                                    }
                                )

    df = pd.DataFrame(rows)
    return df


def main() -> None:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(project_root, "data", "raw", "content_platform_mock_data.csv")

    df = generate_mock_data()
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"Generated file: {output_path}")
    print(f"Rows: {df.shape[0]}, Cols: {df.shape[1]}")
    print(df.head(3).to_string(index=False))


if __name__ == "__main__":
    main()
