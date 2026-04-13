import math
from pathlib import Path

import pandas as pd

from lightweight_predictive_model import (
    add_target,
    build_pipeline,
    extract_coefficients,
    load_dataset,
    split_train_test,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "reports" / "outputs"
INTERPRETATION_PATH = OUTPUT_DIR / "predictive_factor_interpretation.md"
SUPPORT_PATH = OUTPUT_DIR / "predictive_factor_supporting_summary.csv"


FEATURE_COLUMNS = {
    "categorical": [
        "content_category",
        "traffic_source",
        "user_type",
        "city_tier",
        "experiment_group",
        "hour_bucket",
        "week_day",
    ],
    "numeric": [
        "content_supply_cnt",
        "session_uv",
        "is_weekend",
    ],
}


FACTOR_DETAILS = {
    "user type new user": {
        "kind": "categorical",
        "column": "user_type",
        "level": "new_user",
        "business_context": "This factor flags segment-day observations dominated by new users who are still early in their relationship with the platform.",
        "business_explanation": "New users usually have weaker habit strength, less trust in the platform, and more friction between click and conversion. They may browse because the content is interesting but still fail to complete the monetization step.",
        "signal_type": "Mostly structural and contextual, with an additional simulated-data component because the generator explicitly lowers conversion tendency for new users.",
        "action_idea": "Treat new-user traffic as a separate conversion funnel: simplify landing pages, shorten onboarding friction, and use lighter-weight first-conversion offers instead of assuming the same flow works for established users.",
        "caution": "This does not mean new users are unimportant. It means they convert less efficiently in this simulated setup, and the effect is measured on aggregated segment-days rather than on individual users.",
    },
    "traffic source recommendation": {
        "kind": "categorical",
        "column": "traffic_source",
        "level": "recommendation",
        "business_context": "This factor represents traffic delivered through the recommendation feed rather than intent-led discovery.",
        "business_explanation": "Recommendation traffic often carries broader reach but weaker immediate purchase intent. Users may click because content is engaging, not because they have already decided to convert.",
        "signal_type": "Primarily contextual, but partly simulated-data-specific because search traffic receives an explicit conversion advantage in the data generator, making recommendation look weaker by contrast.",
        "action_idea": "Keep recommendation traffic for scale, but improve pre-click relevance and post-click call-to-action design if conversion is the goal. It may be better suited to engagement growth than direct monetization.",
        "caution": "A negative coefficient here is not a verdict that recommendation traffic is bad overall. It only says recommendation contexts are less associated with above-median conversion performance than the stronger alternatives in this model.",
    },
    "traffic source follow": {
        "kind": "categorical",
        "column": "traffic_source",
        "level": "follow",
        "business_context": "This factor captures traffic from follow-based content exposure, where users are consuming content from creators or sources they already follow.",
        "business_explanation": "Follow traffic may reflect loyalty and repeat consumption, but not necessarily immediate transactional intent. In this simulated project it also overlaps with a designed conversion dip for a follow-related anomaly window.",
        "signal_type": "Contextual, with a meaningful simulated-data component because the generated anomaly includes weaker conversion performance in a follow-related slice.",
        "action_idea": "Use follow traffic for retention and upsell design rather than assuming it is the best direct-conversion channel. Conversion-focused experiments on follow traffic should target clearer intent capture.",
        "caution": "Part of this negative association may be absorbing the simulated anomaly pattern rather than representing a clean channel effect in a real platform.",
    },
    "traffic source nearby": {
        "kind": "categorical",
        "column": "traffic_source",
        "level": "nearby",
        "business_context": "This factor corresponds to location-based or nearby-discovery traffic, which is often exploratory and context-dependent.",
        "business_explanation": "Nearby traffic may generate useful discovery, but it can include users who are browsing locally relevant options without a strong immediate conversion decision. That can suppress conversion efficiency relative to search.",
        "signal_type": "Mostly contextual, with some simulated-data influence because only search gets an explicit conversion lift in the data generator.",
        "action_idea": "Improve local landing pages, geo-specific offers, and clearer next-step prompts if nearby traffic is expected to convert rather than simply drive discovery.",
        "caution": "The effect is modest compared with the strongest factors, so it should be treated as a directional signal rather than a standalone strategy decision.",
    },
    "experiment group A": {
        "kind": "categorical",
        "column": "experiment_group",
        "level": "A",
        "business_context": "This factor indicates the control version in the simulated A/B experiment.",
        "business_explanation": "Its negative sign is mostly the mirror image of the positive B-group signal. Because the data generator directly gives group B a conversion improvement, group A naturally looks slightly less associated with high conversion performance.",
        "signal_type": "Mostly simulated-data-specific and experimental by design, not a naturally occurring structural business factor.",
        "action_idea": "Use it as supporting evidence that the experiment produced lift, but keep the interpretation tied to experiment evaluation and guardrail review rather than turning it into a broad user-segmentation insight.",
        "caution": "This coefficient is small and should not be over-read. With full one-hot encoding, A and B appear as small opposing coefficients rather than a single clean treatment-vs-control contrast.",
    },
    "traffic source search": {
        "kind": "categorical",
        "column": "traffic_source",
        "level": "search",
        "business_context": "This factor captures users arriving from search, where demand and intent are usually clearer than in recommendation-led discovery.",
        "business_explanation": "Search traffic often has the strongest purchase or action intent because users are actively looking for something. In the simulated generator, search also gets an explicit conversion advantage, which reinforces this pattern.",
        "signal_type": "Both structural/contextual and simulated-data-specific. The business logic is plausible, but the effect is also intentionally built into the synthetic data design.",
        "action_idea": "Prioritize high-quality landing experiences, keyword-to-content relevance, and monetization placement for search traffic because it is the most conversion-oriented segment in this prototype.",
        "caution": "Search may convert better than other channels while still contributing less total volume. A strong coefficient does not automatically mean search should replace the rest of the traffic mix.",
    },
    "user type active user": {
        "kind": "categorical",
        "column": "user_type",
        "level": "active_user",
        "business_context": "This factor represents users with ongoing platform engagement rather than first-time or sporadic usage.",
        "business_explanation": "Active users usually understand the product better, trust the experience more, and are less likely to drop off between click and monetization. They often respond better to optimized flows.",
        "signal_type": "Mostly structural and contextual. It fits the broader business logic that established users tend to convert more reliably than new users.",
        "action_idea": "Use active users as the most promising audience for monetization experiments, premium offers, and higher-friction conversion flows because they are more resilient in the funnel.",
        "caution": "This is still an association, not proof that making someone more active will automatically cause the same conversion lift.",
    },
    "user type returning user": {
        "kind": "categorical",
        "column": "user_type",
        "level": "returning_user",
        "business_context": "This factor covers users who are not brand new, but are also not as consistently engaged as the active-user group.",
        "business_explanation": "Returning users retain some familiarity and trust, so they tend to convert better than new users, even if they are not as reliable as highly active users.",
        "signal_type": "Mostly structural and contextual, with a reasonable business interpretation inside the simulated platform setting.",
        "action_idea": "Use returning users for reactivation or remarketing flows. They may be a practical middle segment for conversion optimization without the high acquisition friction of new users.",
        "caution": "This signal is weaker than the active-user effect, so the model suggests a spectrum of user familiarity rather than a simple active-vs-not-active split.",
    },
    "experiment group B": {
        "kind": "categorical",
        "column": "experiment_group",
        "level": "B",
        "business_context": "This factor indicates the treatment version in the simulated A/B experiment.",
        "business_explanation": "Its small positive sign is consistent with the experiment design: version B was simulated to improve conversion performance, so it slightly increases the probability of above-median conversion outcomes.",
        "signal_type": "Mostly simulated-data-specific and experimental by design rather than a naturally persistent business segment.",
        "action_idea": "Use this as one more consistency check between the predictive model and the separate A/B evaluation module. It helps show that the predictive prototype is directionally aligned with the experiment results.",
        "caution": "Because this is a designed experiment effect, it should not be generalized as a universal causal truth. The standalone coefficient is small and should always be interpreted alongside guardrail metrics.",
    },
    "session uv": {
        "kind": "numeric",
        "column": "session_uv",
        "level": None,
        "business_context": "This factor is the session-level user-volume measure included as a numeric context variable.",
        "business_explanation": "Higher session UV may be associated with healthier or more active platform contexts, which can slightly improve the likelihood of above-median conversion performance. It can also proxy for demand concentration or stronger daily traffic conditions.",
        "signal_type": "Mostly contextual and relatively weak. It is plausible as a broad environment signal, but it is also the least cleanly interpretable factor among the top coefficients.",
        "action_idea": "Use session UV as a context variable for forecasting or scenario analysis, not as a direct optimization lever. It is more useful for explaining environment conditions than prescribing a single product change.",
        "caution": "This is the weakest and most confounded factor in the chart. Higher session UV does not cause higher conversion on its own, and the effect is small after standardization.",
    },
}


def fit_logistic_model() -> tuple[pd.DataFrame, float, pd.DataFrame]:
    df = load_dataset()
    train_df, test_df = split_train_test(df)
    train_df, test_df, threshold = add_target(train_df, test_df)

    pipeline = build_pipeline(FEATURE_COLUMNS["categorical"], FEATURE_COLUMNS["numeric"])
    feature_columns = FEATURE_COLUMNS["categorical"] + FEATURE_COLUMNS["numeric"]
    pipeline.fit(train_df[feature_columns], train_df["high_conversion_performance"])
    coef_df = extract_coefficients(pipeline)

    full_df = df.copy()
    full_df["high_conversion_performance"] = (full_df["conversion_rate"] >= threshold).astype(int)
    return coef_df, threshold, full_df


def get_chart_factors(coef_df: pd.DataFrame) -> pd.DataFrame:
    top_positive = coef_df.sort_values("coefficient", ascending=False).head(5).copy()
    top_negative = coef_df.sort_values("coefficient", ascending=True).head(5).copy()
    chart_factors = pd.concat([top_negative, top_positive], ignore_index=True)
    chart_factors["odds_ratio"] = chart_factors["coefficient"].apply(math.exp)
    return chart_factors


def categorical_support(df: pd.DataFrame, factor_name: str, factor_row: pd.Series) -> dict:
    column = FACTOR_DETAILS[factor_name]["column"]
    level = FACTOR_DETAILS[factor_name]["level"]

    group_stats = (
        df.groupby(column)
        .agg(
            rows=("high_conversion_performance", "size"),
            positive_rate=("high_conversion_performance", "mean"),
            avg_conversion_rate=("conversion_rate", "mean"),
        )
        .reset_index()
        .sort_values("positive_rate", ascending=False)
    )
    group_stats["positive_rate_rank"] = range(1, len(group_stats) + 1)

    subset = df[df[column] == level].copy()
    other = df[df[column] != level].copy()
    level_row = group_stats[group_stats[column] == level].iloc[0]

    return {
        "factor_name": factor_name,
        "feature_family": column,
        "factor_level": level,
        "coefficient": factor_row["coefficient"],
        "odds_ratio": factor_row["odds_ratio"],
        "association": "positive" if factor_row["coefficient"] > 0 else "negative",
        "summary_scope": "full dataset with target threshold fixed from training median",
        "support_view": f"{level} versus all other levels in {column}",
        "group_rows": int(len(subset)),
        "comparison_rows": int(len(other)),
        "group_avg_conversion_rate": float(subset["conversion_rate"].mean()),
        "comparison_avg_conversion_rate": float(other["conversion_rate"].mean()),
        "group_positive_rate": float(subset["high_conversion_performance"].mean()),
        "comparison_positive_rate": float(other["high_conversion_performance"].mean()),
        "positive_rate_rank_within_family": int(level_row["positive_rate_rank"]),
        "family_levels_count": int(group_stats.shape[0]),
        "interpretation_reference_note": "Because all category levels are one-hot encoded without dropping a single baseline, this is best read as a directional contribution rather than a strict omitted-category contrast.",
    }


def numeric_support(df: pd.DataFrame, factor_name: str, factor_row: pd.Series) -> dict:
    column = FACTOR_DETAILS[factor_name]["column"]

    q1 = float(df[column].quantile(0.25))
    q3 = float(df[column].quantile(0.75))
    low = df[df[column] <= q1].copy()
    high = df[df[column] >= q3].copy()
    pos = df[df["high_conversion_performance"] == 1].copy()
    neg = df[df["high_conversion_performance"] == 0].copy()

    return {
        "factor_name": factor_name,
        "feature_family": column,
        "factor_level": "higher values",
        "coefficient": factor_row["coefficient"],
        "odds_ratio": factor_row["odds_ratio"],
        "association": "positive" if factor_row["coefficient"] > 0 else "negative",
        "summary_scope": "full dataset with target threshold fixed from training median",
        "support_view": f"top quartile ({q3:.2f}+) versus bottom quartile ({q1:.2f} and below)",
        "group_rows": int(len(high)),
        "comparison_rows": int(len(low)),
        "group_avg_conversion_rate": float(high["conversion_rate"].mean()),
        "comparison_avg_conversion_rate": float(low["conversion_rate"].mean()),
        "group_positive_rate": float(high["high_conversion_performance"].mean()),
        "comparison_positive_rate": float(low["high_conversion_performance"].mean()),
        "positive_class_mean_value": float(pos[column].mean()),
        "negative_class_mean_value": float(neg[column].mean()),
        "interpretation_reference_note": "This numeric coefficient is applied after standardization, so it represents the direction of the log-odds change for higher session UV rather than a binary category jump.",
    }


def build_support_summary(chart_factors: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
    records = []
    for row in chart_factors.itertuples(index=False):
        factor_name = row.display_feature
        if FACTOR_DETAILS[factor_name]["kind"] == "numeric":
            records.append(numeric_support(df, factor_name, pd.Series(row._asdict())))
        else:
            records.append(categorical_support(df, factor_name, pd.Series(row._asdict())))
    support_df = pd.DataFrame(records)
    return support_df


def format_pct(value: float) -> str:
    return f"{value:.2%}"


def format_decimal(value: float) -> str:
    return f"{value:.4f}"


def write_interpretation_report(chart_factors: pd.DataFrame, support_df: pd.DataFrame) -> None:
    lines = [
        "# Predictive Factor Interpretation",
        "",
        "## Scope",
        "This note interprets every factor shown in the third panel of the current logistic-regression figure, `Top Logistic Coefficients`.",
        "",
        "## Important Modeling Note",
        "The logistic model uses one-hot encoding for all category levels without dropping a single omitted baseline category. That means these coefficients should be read as directional contributions after regularization, not as perfect one-level-versus-baseline causal effects. The supporting summary CSV therefore compares each categorical factor level against the other levels in the same feature family.",
        "",
        f"Supporting dataset summary: `reports/outputs/{SUPPORT_PATH.name}`",
        "",
    ]

    for idx, row in enumerate(chart_factors.itertuples(index=False), start=1):
        factor_name = row.display_feature
        detail = FACTOR_DETAILS[factor_name]
        support = support_df[support_df["factor_name"] == factor_name].iloc[0]
        sign = "positive" if row.coefficient > 0 else "negative"
        statistical_meaning = (
            f"In this logistic model, the coefficient is {format_decimal(row.coefficient)}, which means this factor is associated with {'higher' if row.coefficient > 0 else 'lower'} log-odds of `high_conversion_performance`. "
            f"The corresponding odds ratio is approximately {row.odds_ratio:.3f}."
        )
        if detail["kind"] == "categorical":
            statistical_meaning += " Because full one-hot encoding is used, the coefficient is best interpreted as directional support for this level rather than as a strict comparison to one omitted baseline category."
        else:
            statistical_meaning += " Because `session_uv` is standardized before modeling, this effect should be read as the approximate direction of the odds change for a higher-value context, not as a direct raw-unit business lever."

        lines.extend(
            [
                f"## {idx}. {factor_name.title()}",
                "",
                f"1. Factor name: `{factor_name}`",
                f"2. Association with high conversion performance: {sign}",
                f"3. Statistical meaning: {statistical_meaning}",
                f"4. Dataset / business context: {detail['business_context']}",
                f"5. Plausible business explanation: {detail['business_explanation']}",
                f"6. Signal type: {detail['signal_type']}",
                f"7. Practical optimization idea: {detail['action_idea']}",
                f"8. Caution: {detail['caution']}",
                "",
                "### Lightweight supporting evidence",
                f"- Support view used: {support['support_view']}",
                f"- Factor-level average conversion rate: {format_pct(support['group_avg_conversion_rate'])}",
                f"- Comparison average conversion rate: {format_pct(support['comparison_avg_conversion_rate'])}",
                f"- Factor-level high-conversion positive rate: {format_pct(support['group_positive_rate'])}",
                f"- Comparison positive rate: {format_pct(support['comparison_positive_rate'])}",
            ]
        )

        if detail["kind"] == "categorical":
            lines.append(
                f"- Positive-rate rank within `{detail['column']}` levels: {int(support['positive_rate_rank_within_family'])} of {int(support['family_levels_count'])}"
            )
        else:
            lines.append(
                f"- Mean session UV for positive class vs negative class: {support['positive_class_mean_value']:.2f} vs {support['negative_class_mean_value']:.2f}"
            )

        lines.extend(
            [
                f"- Interpretation note: {support['interpretation_reference_note']}",
                "",
            ]
        )

    INTERPRETATION_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    coef_df, _, full_df = fit_logistic_model()
    chart_factors = get_chart_factors(coef_df)
    support_df = build_support_summary(chart_factors, full_df)

    support_df.to_csv(SUPPORT_PATH, index=False, encoding="utf-8-sig")
    write_interpretation_report(chart_factors, support_df)

    print(f"Saved: {SUPPORT_PATH}")
    print(f"Saved: {INTERPRETATION_PATH}")
    print(chart_factors[['display_feature', 'coefficient', 'odds_ratio']].to_string(index=False))


if __name__ == "__main__":
    main()
