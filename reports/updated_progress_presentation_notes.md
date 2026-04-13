# Project Title
Data-Driven Decision Support for Evaluating AI-Generated Advertising Content in a Simulated Content Platform

# Authors and Team
Rui

## 1. What the project is
This project is a simulated analytics and decision-support prototype for a content platform. It combines KPI monitoring, anomaly detection, segmented diagnosis, A/B evaluation, a dashboard prototype, and now a small predictive-modeling package.

## 2. What has been completed since midterm
- Cleaned and reorganized the ESE submission materials into an English-named package.
- Added structured appendix outputs such as dataset summary, missing-values summary, KPI summary, A/B summary, and an appendix HTML dashboard report.
- Prepared presentation exports in notebook, HTML, and PDF form.
- Updated the dashboard working tree toward an English presentation version.
- Added a logistic-regression classifier that predicts above-median conversion performance for segment-day observations.
- Added a detailed interpretation note for every factor shown in the logistic coefficient chart.
- Added a Random Forest benchmark on the same task for direct comparison against Logistic Regression.

## 3. What the key current results are
- The simulated dataset contains 97,200 rows, 20 variables, and no missing or duplicate rows in the current outputs.
- The anomaly workflow currently flags 24 anomalies using 7-day rolling baselines and segment-level rules.
- Root-cause analysis isolates three main cases: CTR decline, report-rate spike, and conversion-rate decline.
- The A/B module shows that variant B improves CTR, conversion rate, and revenue, but worsens report rate and complete rate, so the current recommendation is staged rollout rather than full launch.
- The new predictive prototype uses logistic regression and reached accuracy of 0.6219, precision of 0.6082, recall of 0.7879, F1-score of 0.6865, and ROC-AUC of 0.6606 on a time-based test split.
- The strongest positive signal is `traffic_source = search`, while `user_type = new_user` is the strongest negative signal for above-median conversion performance.
- The Random Forest benchmark did not outperform Logistic Regression on this task, so the more interpretable model remains the better presentation choice.

## 4. What the next steps are
- Finalize the updated report and presentation storyline for April 24.
- Polish the dashboard screenshots and supporting appendix figures.
- If time permits, extend the predictive work from classification into one additional forecasting or risk-scoring direction.

## 5. 6-8 Minute Presentation Outline
1. Introduce the business problem and why KPI monitoring alone is not enough.
2. Explain the simulated dataset and the decision-support goal of the project.
3. Show the KPI framework and anomaly detection workflow.
4. Walk through one root-cause case to show how segmented diagnosis works.
5. Present the A/B evaluation and explain the tradeoff between growth and guardrail metrics.
6. Explain the logistic coefficient chart and what the strongest positive and negative factors mean.
7. Show the Random Forest comparison and explain why Logistic Regression still remains the better project-facing model.
8. Show the dashboard prototype and appendix outputs.
9. Close with what is complete, what is still in progress, and the limitations of the predictive extension.
