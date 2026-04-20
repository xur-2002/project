# 内容平台核心指标监控、异常归因与 A/B Test 评估系统

**中文标题**: 内容平台核心指标监控、异常归因与 A/B Test 评估系统  
**English Title**: Content Platform KPI Monitoring, Anomaly Attribution, and A/B Test Evaluation System

## 项目背景
面向本地生活内容平台的真实业务场景：在推荐流量扩张与商业化增长过程中，平台出现了点击质量波动、举报风险上升、实验评估标准不统一等问题。本项目构建从指标监控到异常归因再到实验决策的完整分析闭环。

## 项目目标
1. 建立可复用的业务指标体系（结果、过程、风险、实验）。
2. 实现日级异常监控与告警机制。
3. 完成分层归因分析并输出可执行建议。
4. 对策略 A/B Test 做收益与护栏平衡评估。
5. 提供可视化 Dashboard 方案，支持业务方快速理解结论。

## 核心功能
1. **模拟业务数据生成**: 自动生成 90 天日级多维数据，内置异常事件和实验效果。
2. **指标监控**: 计算 CTR、完播率、互动率、举报率、转化率等核心指标。
3. **异常检测**: 基于移动基线和偏离阈值识别全局与分层异常。
4. **归因分析**: 从内容类目、流量来源、用户类型、时段拆解异常贡献。
5. **A/B Test 评估**: 核心指标 + 护栏指标 + 显著性检验，输出上线建议。
6. **Dashboard 展示**: 提供 Streamlit 交互式分析页面。

## 技术栈
- Python 3
- pandas, numpy
- matplotlib, plotly
- scipy
- streamlit

## 项目结构
```text
content_platform_analysis_project/
├─ data/
│  ├─ raw/
│  └─ processed/
├─ notebooks/
├─ src/
│  ├─ generate_data.py
│  ├─ anomaly_detection.py
│  ├─ root_cause_analysis.py
│  └─ ab_test_analysis.py
├─ reports/
│  ├─ figures/
│  ├─ tables/
│  ├─ step1_project_background.md
│  ├─ step2_data_schema.md
│  ├─ step3_data_generation_logic.md
│  ├─ step4_metric_framework.md
│  ├─ step5_anomaly_analysis.md
│  ├─ step6_root_cause_analysis.md
│  ├─ step7_ab_test_evaluation.md
│  └─ final_project_report.md
├─ dashboard/
│  ├─ dashboard_plan.md
│  └─ app.py
├─ resume/
│  ├─ resume_bullets_cn.md
│  ├─ resume_bullets_en.md
│  └─ interview_pitch_cn.md
├─ README.md
└─ requirements.txt
```

## 如何运行
在项目根目录执行以下命令（Windows cmd）:

```bash
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt

.venv\Scripts\python src\generate_data.py
.venv\Scripts\python src\anomaly_detection.py
.venv\Scripts\python src\root_cause_analysis.py
.venv\Scripts\python src\ab_test_analysis.py

.venv\Scripts\streamlit run dashboard\app.py
```

## 项目亮点
1. 不是 Kaggle 风格建模项目，而是贴近互联网业务分析的决策型项目。
2. 形成“监控-预警-归因-实验评估”闭环，可直接迁移到真实业务场景。
3. 同时考虑增长收益与生态风险，强调多指标平衡决策。
4. 产出完整：代码、数据、图表、报告、简历表达、面试讲述。

## 简历价值与面试可讲点
1. 能完整讲清如何从业务问题拆解到指标体系设计。
2. 能展示异常监控方法与分层归因思路。
3. 能说明 A/B Test 中核心指标与护栏指标的权衡决策。
4. 能以可视化方式向非技术团队传递分析结论。

## 关键产出文件
1. 背景定义: reports/step1_project_background.md
2. 数据结构: reports/step2_data_schema.md, reports/tables/data_dictionary.csv
3. 异常分析: reports/step5_anomaly_analysis.md, reports/tables/anomaly_summary.csv
4. 归因分析: reports/step6_root_cause_analysis.md, reports/tables/root_cause_summary.csv
5. 实验评估: reports/step7_ab_test_evaluation.md, reports/tables/ab_test_summary.csv
6. 最终报告: reports/final_project_report.md

# Final Integrated Report

The final English report package for the ESE 527 project is available at:

- `reports/final_integrated_project_report.md`
- `reports/final_integrated_presentation_notes.md`
- `reports/outputs/final_report_asset_checklist.md`

This package integrates KPI monitoring, anomaly detection, segmented diagnosis, simulated A/B evaluation, the predictive modeling prototype, factor interpretation, Random Forest benchmarking, and nested cross-validation model comparison.
