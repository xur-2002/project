import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "content_platform_mock_data.csv"
OUTPUT_DIR = PROJECT_ROOT / "reports" / "outputs"
FIGURE_DIR = PROJECT_ROOT / "reports" / "figures"
SUMMARY_PATH = OUTPUT_DIR / "predictive_model_summary.md"
METRICS_PATH = OUTPUT_DIR / "predictive_model_metrics.csv"
SNIPPET_PATH = OUTPUT_DIR / "predictive_model_notebook_snippet.txt"
FIGURE_PATH = FIGURE_DIR / "predictive_model_results.png"


def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df["conversion_rate"] = df["conversion_cnt"] / df["click"].clip(lower=1)
    df["is_weekend"] = df["week_day"].isin(["Saturday", "Sunday"]).astype(int)
    return df


def split_train_test(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    unique_dates = sorted(df["date"].unique())
    split_idx = int(len(unique_dates) * 0.78)
    split_date = pd.Timestamp(unique_dates[split_idx - 1])

    train_df = df[df["date"] <= split_date].copy()
    test_df = df[df["date"] > split_date].copy()
    return train_df, test_df


def add_target(train_df: pd.DataFrame, test_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, float]:
    threshold = float(train_df["conversion_rate"].median())
    train_df["high_conversion_performance"] = (train_df["conversion_rate"] >= threshold).astype(int)
    test_df["high_conversion_performance"] = (test_df["conversion_rate"] >= threshold).astype(int)
    return train_df, test_df, threshold


def build_pipeline(categorical_features: list[str], numeric_features: list[str]) -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", StandardScaler(), numeric_features),
        ]
    )

    model = LogisticRegression(max_iter=1000, solver="lbfgs")

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )


def evaluate_model(y_true: pd.Series, y_pred: pd.Series, y_prob: pd.Series) -> pd.DataFrame:
    metrics = [
        {"metric": "accuracy", "value": accuracy_score(y_true, y_pred)},
        {"metric": "precision", "value": precision_score(y_true, y_pred, zero_division=0)},
        {"metric": "recall", "value": recall_score(y_true, y_pred, zero_division=0)},
        {"metric": "f1_score", "value": f1_score(y_true, y_pred, zero_division=0)},
        {"metric": "roc_auc", "value": roc_auc_score(y_true, y_prob)},
    ]
    return pd.DataFrame(metrics)


def extract_coefficients(pipeline: Pipeline) -> pd.DataFrame:
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]

    feature_names = preprocessor.get_feature_names_out()
    coefficients = model.coef_[0]

    coef_df = pd.DataFrame(
        {
            "feature": feature_names,
            "coefficient": coefficients,
            "abs_coefficient": abs(coefficients),
        }
    ).sort_values("abs_coefficient", ascending=False)

    coef_df["display_feature"] = (
        coef_df["feature"]
        .str.replace("cat__", "", regex=False)
        .str.replace("num__", "", regex=False)
        .str.replace("_", " ", regex=False)
    )
    return coef_df


def create_figure(y_true: pd.Series, y_pred: pd.Series, y_prob: pd.Series, coef_df: pd.DataFrame) -> None:
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    cm = confusion_matrix(y_true, y_pred)

    top_positive = coef_df.sort_values("coefficient", ascending=False).head(5)
    top_negative = coef_df.sort_values("coefficient", ascending=True).head(5)
    coef_plot = pd.concat([top_negative, top_positive], ignore_index=True)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

    axes[0].plot(fpr, tpr, color="#1f77b4", linewidth=2, label="Logistic regression")
    axes[0].plot([0, 1], [0, 1], linestyle="--", color="gray", linewidth=1)
    axes[0].set_title("ROC Curve")
    axes[0].set_xlabel("False Positive Rate")
    axes[0].set_ylabel("True Positive Rate")
    axes[0].legend(loc="lower right")

    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=axes[1])
    axes[1].set_title("Confusion Matrix")
    axes[1].set_xlabel("Predicted Label")
    axes[1].set_ylabel("True Label")

    bar_colors = ["#d62728" if x < 0 else "#2ca02c" for x in coef_plot["coefficient"]]
    axes[2].barh(coef_plot["display_feature"], coef_plot["coefficient"], color=bar_colors)
    axes[2].axvline(0, color="black", linewidth=1)
    axes[2].set_title("Top Logistic Coefficients")
    axes[2].set_xlabel("Coefficient")

    plt.tight_layout()
    plt.savefig(FIGURE_PATH, dpi=160)
    plt.close(fig)


def write_summary(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    threshold: float,
    metrics_df: pd.DataFrame,
    coef_df: pd.DataFrame,
    categorical_features: list[str],
    numeric_features: list[str],
) -> None:
    top_positive = coef_df.sort_values("coefficient", ascending=False).head(5)
    top_negative = coef_df.sort_values("coefficient", ascending=True).head(5)

    metrics = {row["metric"]: row["value"] for _, row in metrics_df.iterrows()}

    lines = [
        "# Lightweight Predictive Model Summary",
        "",
        "## Modeling Task",
        "- Task type: binary classification",
        "- Target: `high_conversion_performance`",
        f"- Label definition: 1 if row-level `conversion_rate` >= training median ({threshold:.6f}); otherwise 0",
        "- Model: logistic regression",
        "- Split: time-based train/test split using the earlier 78% of dates for training and the latest 22% for testing",
        "",
        "## Feature Set",
        f"- Categorical features: {', '.join(categorical_features)}",
        f"- Numeric features: {', '.join(numeric_features)}",
        "- Excluded downstream fields: click, conversion_cnt, view_complete, report_cnt, monetization_revenue, and other direct outcome columns",
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
        "## Interpretation",
        "- This model predicts whether a segment-day observation is likely to have relatively strong conversion performance, not absolute business value or causal impact.",
        "- Positive coefficients indicate segment contexts associated with a higher probability of above-median conversion performance in the simulated data.",
        "- Negative coefficients indicate contexts associated with lower predicted conversion performance.",
        "",
        "## Top Positive Coefficients",
    ]

    for row in top_positive.itertuples():
        lines.append(f"- {row.display_feature}: {row.coefficient:.4f}")

    lines.extend(["", "## Top Negative Coefficients"])
    for row in top_negative.itertuples():
        lines.append(f"- {row.display_feature}: {row.coefficient:.4f}")

    lines.extend(
        [
            "",
            "## Limitations",
            "- The data is simulated and the target is threshold-based, so this is a lightweight predictive prototype rather than a production-ready model.",
            "- The model should be interpreted as a presentation-friendly extension beyond descriptive analytics, not as a validated deployment decision engine.",
            "- Because the source data is aggregated at the segment-day level, the model predicts segment performance patterns rather than individual content outcomes.",
        ]
    )

    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_notebook_snippet() -> None:
    lines = [
        "# Notebook snippet: predictive model outputs",
        "import pandas as pd",
        "",
        "metrics = pd.read_csv('reports/outputs/predictive_model_metrics.csv')",
        "print(metrics)",
        "",
        "summary_path = 'reports/outputs/predictive_model_summary.md'",
        "figure_path = 'reports/figures/predictive_model_results.png'",
        "print(summary_path)",
        "print(figure_path)",
    ]
    SNIPPET_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(FIGURE_DIR, exist_ok=True)

    df = load_dataset()
    train_df, test_df = split_train_test(df)
    train_df, test_df, threshold = add_target(train_df, test_df)

    categorical_features = [
        "content_category",
        "traffic_source",
        "user_type",
        "city_tier",
        "experiment_group",
        "hour_bucket",
        "week_day",
    ]
    numeric_features = [
        "content_supply_cnt",
        "session_uv",
        "is_weekend",
    ]

    feature_columns = categorical_features + numeric_features

    pipeline = build_pipeline(categorical_features, numeric_features)
    pipeline.fit(train_df[feature_columns], train_df["high_conversion_performance"])

    y_true = test_df["high_conversion_performance"]
    y_prob = pipeline.predict_proba(test_df[feature_columns])[:, 1]
    y_pred = (y_prob >= 0.5).astype(int)

    metrics_df = evaluate_model(y_true, y_pred, y_prob)
    coef_df = extract_coefficients(pipeline)

    metrics_df.to_csv(METRICS_PATH, index=False, encoding="utf-8-sig")
    create_figure(y_true, y_pred, y_prob, coef_df)
    write_summary(train_df, test_df, threshold, metrics_df, coef_df, categorical_features, numeric_features)
    write_notebook_snippet()

    print(f"Saved: {METRICS_PATH}")
    print(f"Saved: {SUMMARY_PATH}")
    print(f"Saved: {SNIPPET_PATH}")
    print(f"Saved: {FIGURE_PATH}")
    print(metrics_df.to_string(index=False))


if __name__ == "__main__":
    main()
