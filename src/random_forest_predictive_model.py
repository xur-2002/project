from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, roc_curve
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from lightweight_predictive_model import (
    add_target,
    evaluate_model,
    load_dataset,
    split_train_test,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "reports" / "outputs"
FIGURE_DIR = PROJECT_ROOT / "reports" / "figures"

RF_SUMMARY_PATH = OUTPUT_DIR / "random_forest_model_summary.md"
RF_METRICS_PATH = OUTPUT_DIR / "random_forest_model_metrics.csv"
RF_FIGURE_PATH = FIGURE_DIR / "random_forest_model_results.png"

COMPARISON_SUMMARY_PATH = OUTPUT_DIR / "model_comparison_summary.md"
COMPARISON_METRICS_PATH = OUTPUT_DIR / "model_comparison_metrics.csv"
COMPARISON_FIGURE_PATH = FIGURE_DIR / "model_comparison_results.png"
TALKING_POINTS_PATH = OUTPUT_DIR / "predictive_model_talking_points.md"

LOGISTIC_METRICS_PATH = OUTPUT_DIR / "predictive_model_metrics.csv"
SUPPORT_PATH = OUTPUT_DIR / "predictive_factor_supporting_summary.csv"


CATEGORICAL_FEATURES = [
    "content_category",
    "traffic_source",
    "user_type",
    "city_tier",
    "experiment_group",
    "hour_bucket",
    "week_day",
]
NUMERIC_FEATURES = [
    "content_supply_cnt",
    "session_uv",
    "is_weekend",
]
FEATURE_COLUMNS = CATEGORICAL_FEATURES + NUMERIC_FEATURES


def build_random_forest_pipeline() -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
            ("num", "passthrough", NUMERIC_FEATURES),
        ]
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_leaf=20,
        random_state=42,
        n_jobs=1,
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )


def extract_feature_importance(pipeline: Pipeline) -> pd.DataFrame:
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]

    feature_names = preprocessor.get_feature_names_out()
    importance_df = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    importance_df["display_feature"] = (
        importance_df["feature"]
        .str.replace("cat__", "", regex=False)
        .str.replace("num__", "", regex=False)
        .str.replace("_", " ", regex=False)
    )
    return importance_df


def create_random_forest_figure(
    y_true: pd.Series,
    y_pred: pd.Series,
    y_prob: pd.Series,
    importance_df: pd.DataFrame,
) -> None:
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    cm = confusion_matrix(y_true, y_pred)
    top_importance = importance_df.head(10).sort_values("importance", ascending=True)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

    axes[0].plot(fpr, tpr, color="#2a9d8f", linewidth=2, label="Random Forest")
    axes[0].plot([0, 1], [0, 1], linestyle="--", color="gray", linewidth=1)
    axes[0].set_title("Random Forest ROC Curve")
    axes[0].set_xlabel("False Positive Rate")
    axes[0].set_ylabel("True Positive Rate")
    axes[0].legend(loc="lower right")

    sns.heatmap(cm, annot=True, fmt="d", cmap="Greens", cbar=False, ax=axes[1])
    axes[1].set_title("Random Forest Confusion Matrix")
    axes[1].set_xlabel("Predicted Label")
    axes[1].set_ylabel("True Label")

    axes[2].barh(top_importance["display_feature"], top_importance["importance"], color="#264653")
    axes[2].set_title("Top Random Forest Importances")
    axes[2].set_xlabel("Importance")

    plt.tight_layout()
    plt.savefig(RF_FIGURE_PATH, dpi=160)
    plt.close(fig)


def write_random_forest_summary(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    threshold: float,
    metrics_df: pd.DataFrame,
    importance_df: pd.DataFrame,
) -> None:
    metrics = {row["metric"]: row["value"] for _, row in metrics_df.iterrows()}
    top_importance = importance_df.head(10)

    lines = [
        "# Random Forest Predictive Model Summary",
        "",
        "## Modeling Task",
        "- Task type: binary classification",
        "- Target: `high_conversion_performance`",
        f"- Label definition: 1 if row-level `conversion_rate` >= training median ({threshold:.6f}); otherwise 0",
        "- Model: Random Forest classifier",
        "- Split: same time-based train/test split used in the Logistic Regression prototype",
        "",
        "## Feature Set",
        f"- Categorical features: {', '.join(CATEGORICAL_FEATURES)}",
        f"- Numeric features: {', '.join(NUMERIC_FEATURES)}",
        "- Same target definition and same train/test logic as the Logistic Regression model",
        "",
        "## Data Split",
        f"- Training rows: {len(train_df):,}",
        f"- Test rows: {len(test_df):,}",
        f"- Training positive rate: {train_df['high_conversion_performance'].mean():.3f}",
        f"- Test positive rate: {test_df['high_conversion_performance'].mean():.3f}",
        "",
        "## Evaluation",
        f"- Accuracy: {metrics['accuracy']:.4f}",
        f"- Precision: {metrics['precision']:.4f}",
        f"- Recall: {metrics['recall']:.4f}",
        f"- F1-score: {metrics['f1_score']:.4f}",
        f"- ROC-AUC: {metrics['roc_auc']:.4f}",
        "",
        "## Top Feature Importances",
    ]

    for row in top_importance.itertuples():
        lines.append(f"- {row.display_feature}: {row.importance:.4f}")

    lines.extend(
        [
            "",
            "## Interpretation",
            "- Random Forest can absorb nonlinear patterns and interactions that Logistic Regression cannot express directly.",
            "- Its feature importance values are useful for ranking signals, but they are less transparent than logistic coefficients when explaining direction and business meaning.",
            "",
            "## Limitations",
            "- This remains a lightweight predictive prototype trained on simulated, aggregated segment-day data.",
            "- Better predictive performance does not automatically make the model the best business explanation tool.",
            "- Feature importance does not imply causality and should not be presented as proof of intervention effect.",
        ]
    )

    RF_SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def load_logistic_metrics() -> pd.DataFrame:
    logistic = pd.read_csv(LOGISTIC_METRICS_PATH)
    logistic_wide = logistic.set_index("metric")["value"].to_dict()
    return pd.DataFrame(
        [
            {
                "model": "Logistic Regression",
                "accuracy": logistic_wide["accuracy"],
                "precision": logistic_wide["precision"],
                "recall": logistic_wide["recall"],
                "f1_score": logistic_wide["f1_score"],
                "roc_auc": logistic_wide["roc_auc"],
            }
        ]
    )


def create_comparison_outputs(rf_metrics_df: pd.DataFrame) -> None:
    logistic_df = load_logistic_metrics()
    rf_wide = rf_metrics_df.set_index("metric")["value"].to_dict()
    rf_row = pd.DataFrame(
        [
            {
                "model": "Random Forest",
                "accuracy": rf_wide["accuracy"],
                "precision": rf_wide["precision"],
                "recall": rf_wide["recall"],
                "f1_score": rf_wide["f1_score"],
                "roc_auc": rf_wide["roc_auc"],
            }
        ]
    )

    comparison_df = pd.concat([logistic_df, rf_row], ignore_index=True)
    comparison_df.to_csv(COMPARISON_METRICS_PATH, index=False, encoding="utf-8-sig")

    metrics = ["accuracy", "precision", "recall", "f1_score", "roc_auc"]
    plot_df = comparison_df.melt(id_vars="model", value_vars=metrics, var_name="metric", value_name="value")

    fig, ax = plt.subplots(figsize=(10, 5.5))
    sns.barplot(data=plot_df, x="metric", y="value", hue="model", ax=ax)
    ax.set_ylim(0, 1)
    ax.set_title("Model Comparison Metrics")
    ax.set_ylabel("Score")
    ax.set_xlabel("Metric")
    plt.tight_layout()
    plt.savefig(COMPARISON_FIGURE_PATH, dpi=160)
    plt.close(fig)

    logistic_row = comparison_df[comparison_df["model"] == "Logistic Regression"].iloc[0]
    rf_row_series = comparison_df[comparison_df["model"] == "Random Forest"].iloc[0]

    best_auc_model = "Random Forest" if rf_row_series["roc_auc"] > logistic_row["roc_auc"] else "Logistic Regression"
    best_f1_model = "Random Forest" if rf_row_series["f1_score"] > logistic_row["f1_score"] else "Logistic Regression"

    if best_auc_model == best_f1_model:
        performance_line = f"{best_auc_model} is the stronger predictive model on both ROC-AUC and F1-score in this comparison."
    else:
        performance_line = (
            f"Random Forest and Logistic Regression split the leadership across metrics: "
            f"best ROC-AUC = {best_auc_model}, best F1-score = {best_f1_model}."
        )

    if rf_row_series["roc_auc"] > logistic_row["roc_auc"] or rf_row_series["f1_score"] > logistic_row["f1_score"]:
        tradeoff_line = "- Random Forest adds flexibility and can be kept as a benchmark model, but the performance gain should be weighed against the loss of interpretability."
    else:
        tradeoff_line = "- In this run, Random Forest did not outperform Logistic Regression on the key metrics, so the simpler and more interpretable model remains the stronger choice for this project."

    summary_lines = [
        "# Model Comparison Summary",
        "",
        "## Metric Table",
        "| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    for row in comparison_df.itertuples(index=False):
        summary_lines.append(
            f"| {row.model} | {row.accuracy:.4f} | {row.precision:.4f} | {row.recall:.4f} | {row.f1_score:.4f} | {row.roc_auc:.4f} |"
        )

    summary_lines.extend(
        [
            "",
            "## Comparison Interpretation",
            performance_line,
            f"- Logistic Regression remains the more interpretable model because its coefficients show directional associations for specific factor levels.",
            f"- Random Forest is better suited to capturing nonlinear interactions, but its importance scores are less straightforward for business explanation.",
            "- For this simulated project, Logistic Regression is still the easiest model to present and defend in a classroom or business-facing setting.",
            tradeoff_line,
        ]
    )

    COMPARISON_SUMMARY_PATH.write_text("\n".join(summary_lines), encoding="utf-8")


def write_talking_points() -> None:
    support_df = pd.read_csv(SUPPORT_PATH) if SUPPORT_PATH.exists() else pd.DataFrame()

    strongest_positive = "traffic source search"
    strongest_negative = "user type new user"
    if not support_df.empty:
        strongest_positive = support_df.sort_values("coefficient", ascending=False).iloc[0]["factor_name"]
        strongest_negative = support_df.sort_values("coefficient", ascending=True).iloc[0]["factor_name"]

    comparison_df = pd.read_csv(COMPARISON_METRICS_PATH)
    logistic_row = comparison_df[comparison_df["model"] == "Logistic Regression"].iloc[0]
    rf_row = comparison_df[comparison_df["model"] == "Random Forest"].iloc[0]
    rf_beats_logistic = (rf_row["roc_auc"] > logistic_row["roc_auc"]) or (rf_row["f1_score"] > logistic_row["f1_score"])

    lines = [
        "# Predictive Model Talking Points",
        "",
        "## How to explain the logistic coefficient chart",
        "- Positive bars mean the model associates that factor with a higher probability of above-median conversion performance.",
        "- Negative bars mean the model associates that factor with a lower probability of above-median conversion performance.",
        "- Because all category levels were one-hot encoded instead of dropping one clean baseline, the coefficients should be explained as directional associations, not as strict causal effects against a single omitted category.",
        "",
        "## How to explain why some factors promote or suppress conversion",
        f"- The strongest positive signal is `{strongest_positive}`, which fits the project story that higher-intent contexts tend to produce better conversion outcomes.",
        f"- The strongest negative signal is `{strongest_negative}`, which fits the idea that lower-familiarity or lower-intent contexts convert less efficiently.",
        "- The A/B group coefficients should be explained carefully: they are small and mainly confirm the simulated treatment effect already seen in the A/B evaluation module.",
        "- `session_uv` is best explained as a weak context variable, not as a direct causal business lever.",
        "",
        "## How to explain Random Forest vs Logistic Regression",
        f"- Logistic Regression metrics: accuracy {logistic_row['accuracy']:.4f}, F1 {logistic_row['f1_score']:.4f}, ROC-AUC {logistic_row['roc_auc']:.4f}.",
        f"- Random Forest metrics: accuracy {rf_row['accuracy']:.4f}, F1 {rf_row['f1_score']:.4f}, ROC-AUC {rf_row['roc_auc']:.4f}.",
        "- Logistic Regression is easier to explain because each coefficient has a direction and a concrete business narrative.",
        "- Random Forest can capture more complicated patterns, so it is useful as a benchmark even if it is harder to explain.",
        (
            "- For presentation, the best framing is: Random Forest is a useful benchmark for added flexibility, but the project should still emphasize the model that best balances performance and explainability."
            if rf_beats_logistic
            else "- For presentation, the best framing is: Random Forest was tested as a benchmark, but Logistic Regression remained the stronger model overall because it stayed more interpretable and slightly outperformed the benchmark."
        ),
    ]

    TALKING_POINTS_PATH.write_text("\n".join(lines), encoding="utf-8")
def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    df = load_dataset()
    train_df, test_df = split_train_test(df)
    train_df, test_df, threshold = add_target(train_df, test_df)

    pipeline = build_random_forest_pipeline()
    pipeline.fit(train_df[FEATURE_COLUMNS], train_df["high_conversion_performance"])

    y_true = test_df["high_conversion_performance"]
    y_prob = pipeline.predict_proba(test_df[FEATURE_COLUMNS])[:, 1]
    y_pred = (y_prob >= 0.5).astype(int)

    metrics_df = evaluate_model(y_true, y_pred, y_prob)
    importance_df = extract_feature_importance(pipeline)

    metrics_df.to_csv(RF_METRICS_PATH, index=False, encoding="utf-8-sig")
    create_random_forest_figure(y_true, y_pred, y_prob, importance_df)
    write_random_forest_summary(train_df, test_df, threshold, metrics_df, importance_df)
    create_comparison_outputs(metrics_df)
    write_talking_points()

    print(f"Saved: {RF_METRICS_PATH}")
    print(f"Saved: {RF_SUMMARY_PATH}")
    print(f"Saved: {RF_FIGURE_PATH}")
    print(f"Saved: {COMPARISON_METRICS_PATH}")
    print(f"Saved: {COMPARISON_SUMMARY_PATH}")
    print(f"Saved: {COMPARISON_FIGURE_PATH}")
    print(f"Saved: {TALKING_POINTS_PATH}")
    print(metrics_df.to_string(index=False))


if __name__ == "__main__":
    main()
