import json
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import GridSearchCV, KFold, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "content_platform_mock_data.csv"
OUTPUT_DIR = PROJECT_ROOT / "reports" / "outputs"
FIGURE_DIR = PROJECT_ROOT / "reports" / "figures"

METRICS_PATH = OUTPUT_DIR / "nested_cv_model_comparison_metrics.csv"
SUMMARY_PATH = OUTPUT_DIR / "nested_cv_model_comparison_summary.md"
FIGURE_PATH = FIGURE_DIR / "nested_cv_model_comparison.png"

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
METRIC_COLUMNS = ["accuracy", "precision", "recall", "f1_score", "roc_auc"]

OUTER_FOLDS = 3
INNER_FOLDS = 3
RANDOM_STATE = 42


def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df["conversion_rate"] = df["conversion_cnt"] / df["click"].clip(lower=1)
    df["is_weekend"] = df["week_day"].isin(["Saturday", "Sunday"]).astype(int)
    return df


def make_logistic_pipeline() -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
            ("num", StandardScaler(), NUMERIC_FEATURES),
        ]
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("select", SelectKBest(score_func=f_classif)),
            (
                "model",
                LogisticRegression(
                    max_iter=1000,
                    solver="liblinear",
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )


def make_random_forest_pipeline() -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
            ("num", "passthrough", NUMERIC_FEATURES),
        ]
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("select", SelectKBest(score_func=f_classif)),
            (
                "model",
                RandomForestClassifier(
                    random_state=RANDOM_STATE,
                    n_jobs=1,
                ),
            ),
        ]
    )


def get_model_specs() -> dict:
    return {
        "Logistic Regression": {
            "pipeline": make_logistic_pipeline(),
            "param_grid": {
                "select__k": [10, 20, "all"],
                "model__C": [0.1, 1.0, 3.0],
                "model__penalty": ["l1", "l2"],
            },
        },
        "Random Forest": {
            "pipeline": make_random_forest_pipeline(),
            "param_grid": {
                "select__k": [10, "all"],
                "model__n_estimators": [80],
                "model__max_depth": [8, 12],
                "model__min_samples_leaf": [20, 50],
                "model__max_features": ["sqrt"],
            },
        },
    }


def compute_fold_target(train_df: pd.DataFrame, test_df: pd.DataFrame) -> tuple[pd.Series, pd.Series, float]:
    threshold = float(train_df["conversion_rate"].median())
    y_train = (train_df["conversion_rate"] >= threshold).astype(int)
    y_test = (test_df["conversion_rate"] >= threshold).astype(int)
    return y_train, y_test, threshold


def evaluate_predictions(y_true: pd.Series, y_pred: pd.Series, y_prob: pd.Series) -> dict:
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1_score": f1_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_true, y_prob),
    }


def run_nested_cv(df: pd.DataFrame) -> pd.DataFrame:
    outer_cv = KFold(n_splits=OUTER_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    outer_splits = list(outer_cv.split(df))
    model_specs = get_model_specs()
    records = []

    for fold_id, (train_idx, test_idx) in enumerate(outer_splits, start=1):
        train_df = df.iloc[train_idx].copy()
        test_df = df.iloc[test_idx].copy()
        y_train, y_test, threshold = compute_fold_target(train_df, test_df)

        x_train = train_df[FEATURE_COLUMNS]
        x_test = test_df[FEATURE_COLUMNS]

        inner_cv = StratifiedKFold(
            n_splits=INNER_FOLDS,
            shuffle=True,
            random_state=RANDOM_STATE + fold_id,
        )

        for model_name, spec in model_specs.items():
            search = GridSearchCV(
                estimator=spec["pipeline"],
                param_grid=spec["param_grid"],
                scoring="roc_auc",
                cv=inner_cv,
                n_jobs=1,
                refit=True,
            )
            search.fit(x_train, y_train)

            y_pred = search.predict(x_test)
            y_prob = search.predict_proba(x_test)[:, 1]
            metrics = evaluate_predictions(y_test, y_pred, y_prob)

            records.append(
                {
                    "model": model_name,
                    "fold": fold_id,
                    "row_type": "outer_fold",
                    "outer_train_rows": len(train_df),
                    "outer_test_rows": len(test_df),
                    "target_threshold": threshold,
                    "train_positive_rate": float(y_train.mean()),
                    "test_positive_rate": float(y_test.mean()),
                    "best_inner_roc_auc": float(search.best_score_),
                    "best_params": json.dumps(search.best_params_, sort_keys=True),
                    **metrics,
                }
            )

    fold_df = pd.DataFrame(records)
    summary_rows = []
    for model_name, group in fold_df.groupby("model"):
        mean_row = {
            "model": model_name,
            "fold": "mean",
            "row_type": "mean",
            "outer_train_rows": "",
            "outer_test_rows": "",
            "target_threshold": group["target_threshold"].mean(),
            "train_positive_rate": group["train_positive_rate"].mean(),
            "test_positive_rate": group["test_positive_rate"].mean(),
            "best_inner_roc_auc": group["best_inner_roc_auc"].mean(),
            "best_params": most_common_params(group["best_params"]),
        }
        std_row = {
            "model": model_name,
            "fold": "std",
            "row_type": "std",
            "outer_train_rows": "",
            "outer_test_rows": "",
            "target_threshold": group["target_threshold"].std(ddof=0),
            "train_positive_rate": group["train_positive_rate"].std(ddof=0),
            "test_positive_rate": group["test_positive_rate"].std(ddof=0),
            "best_inner_roc_auc": group["best_inner_roc_auc"].std(ddof=0),
            "best_params": "",
        }

        for metric in METRIC_COLUMNS:
            mean_row[metric] = group[metric].mean()
            std_row[metric] = group[metric].std(ddof=0)

        summary_rows.extend([mean_row, std_row])

    return pd.concat([fold_df, pd.DataFrame(summary_rows)], ignore_index=True)


def most_common_params(params: pd.Series) -> str:
    counts = Counter(params)
    return counts.most_common(1)[0][0]


def create_comparison_figure(metrics_df: pd.DataFrame) -> None:
    mean_df = metrics_df[metrics_df["row_type"] == "mean"].copy()
    std_df = metrics_df[metrics_df["row_type"] == "std"].copy().set_index("model")
    plot_df = mean_df.melt(id_vars="model", value_vars=METRIC_COLUMNS, var_name="metric", value_name="mean_score")
    plot_df["std_score"] = plot_df.apply(lambda row: std_df.loc[row["model"], row["metric"]], axis=1)

    fig, ax = plt.subplots(figsize=(11, 6))
    sns.barplot(data=plot_df, x="metric", y="mean_score", hue="model", ax=ax)

    patches = ax.patches
    for patch, (_, row) in zip(patches, plot_df.iterrows()):
        x = patch.get_x() + patch.get_width() / 2
        y = patch.get_height()
        ax.errorbar(x=x, y=y, yerr=row["std_score"], color="black", capsize=3, linewidth=1)

    ax.set_ylim(0, 1)
    ax.set_title("Nested Cross-Validation Model Comparison")
    ax.set_xlabel("Metric")
    ax.set_ylabel("Mean outer-fold score")
    plt.tight_layout()
    plt.savefig(FIGURE_PATH, dpi=160)
    plt.close(fig)


def write_summary(metrics_df: pd.DataFrame) -> None:
    mean_df = metrics_df[metrics_df["row_type"] == "mean"].copy().set_index("model")
    std_df = metrics_df[metrics_df["row_type"] == "std"].copy().set_index("model")
    fold_df = metrics_df[metrics_df["row_type"] == "outer_fold"].copy()

    lr_mean = mean_df.loc["Logistic Regression"]
    rf_mean = mean_df.loc["Random Forest"]
    best_auc_model = "Logistic Regression" if lr_mean["roc_auc"] >= rf_mean["roc_auc"] else "Random Forest"
    best_f1_model = "Logistic Regression" if lr_mean["f1_score"] >= rf_mean["f1_score"] else "Random Forest"

    lines = [
        "# Nested Cross-Validation Model Comparison Summary",
        "",
        "## Why This Update Was Added",
        "The earlier predictive comparison used a single train/test split as an initial baseline. This nested cross-validation workflow provides a more reliable estimate of general predictive performance by tuning hyperparameters and selecting features inside the validation process.",
        "",
        "## Nested CV Setup",
        f"- Dataset: `{DATA_PATH.relative_to(PROJECT_ROOT)}`",
        "- Task: binary classification of `high_conversion_performance`",
        "- Target threshold: computed separately from the training rows of each outer fold, using the median row-level conversion rate in that outer training set",
        f"- Outer CV: {OUTER_FOLDS}-fold shuffled KFold, shared by both models",
        f"- Inner CV: {INNER_FOLDS}-fold StratifiedKFold inside each outer training fold",
        "- Tuning metric: ROC-AUC in the inner CV",
        "- Feature selection: `SelectKBest(f_classif)` inside each model pipeline",
        "- Leakage control: downstream variables such as click, conversion count, view completion count, report count, monetization revenue, and row-level conversion rate are excluded from the feature matrix",
        "",
        "## Average Outer-Fold Metrics",
        "| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    for model_name in ["Logistic Regression", "Random Forest"]:
        row = mean_df.loc[model_name]
        lines.append(
            f"| {model_name} | {row['accuracy']:.4f} | {row['precision']:.4f} | {row['recall']:.4f} | {row['f1_score']:.4f} | {row['roc_auc']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Metric Standard Deviations Across Outer Folds",
            "| Model | Accuracy SD | Precision SD | Recall SD | F1-score SD | ROC-AUC SD |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )

    for model_name in ["Logistic Regression", "Random Forest"]:
        row = std_df.loc[model_name]
        lines.append(
            f"| {model_name} | {row['accuracy']:.4f} | {row['precision']:.4f} | {row['recall']:.4f} | {row['f1_score']:.4f} | {row['roc_auc']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Best Hyperparameters Selected by Inner CV",
        ]
    )

    for model_name in ["Logistic Regression", "Random Forest"]:
        lines.append(f"### {model_name}")
        model_folds = fold_df[fold_df["model"] == model_name].sort_values("fold")
        for row in model_folds.itertuples(index=False):
            lines.append(f"- Outer fold {row.fold}: `{row.best_params}`")
        lines.append(f"- Most common selected setting: `{mean_df.loc[model_name, 'best_params']}`")
        lines.append("")

    lines.extend(
        [
            "## Model Comparison Conclusion",
            f"- Best average ROC-AUC: {best_auc_model}",
            f"- Best average F1-score: {best_f1_model}",
        ]
    )

    if best_auc_model == best_f1_model:
        lines.append(f"- Overall, {best_auc_model} is the stronger nested-CV performer on the primary comparison metrics.")
    else:
        lines.append("- The models split leadership across metrics, so the comparison should be framed as a tradeoff rather than a single winner.")

    lines.extend(
        [
            "- Logistic Regression remains the more interpretable model because its coefficients can be explained as directional associations.",
            "- Random Forest remains useful as a flexible benchmark, but stronger performance should still be weighed against lower explainability.",
            "- Results are still based on simulated, aggregated platform data and should not be presented as production deployment evidence.",
        ]
    )

    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    df = load_dataset()
    metrics_df = run_nested_cv(df)
    metrics_df.to_csv(METRICS_PATH, index=False, encoding="utf-8-sig")
    create_comparison_figure(metrics_df)
    write_summary(metrics_df)

    print(f"Saved: {METRICS_PATH}")
    print(f"Saved: {SUMMARY_PATH}")
    print(f"Saved: {FIGURE_PATH}")
    print(metrics_df[metrics_df["row_type"] == "mean"][["model", *METRIC_COLUMNS]].to_string(index=False))


if __name__ == "__main__":
    main()
