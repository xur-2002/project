# Step 8 Dashboard 设计方案

## 工具选型
- 方案：Streamlit + Plotly
- 目标：面向业务团队展示监控、异常、归因、实验评估闭环。

## 页面结构草图

### 页面 1：核心指标总览
1. KPI 卡片：曝光、CTR、完播率、互动率、举报率、转化率
2. 日期筛选器、类目筛选器、来源筛选器、用户类型筛选器
3. 当日 vs 近7日基线偏离提示

推荐图表：
- KPI 大数字卡片
- 指标对比子弹图或环比箭头

### 页面 2：趋势监控与异常预警
1. 核心指标日趋势折线图
2. 异常点高亮
3. 异常清单表（时间、指标、分层、偏离幅度）

推荐图表：
- 多折线趋势图
- 带标注散点图
- 可排序异常明细表

### 页面 3：分层归因分析
1. 异常 Case 选择器（CTR 下滑、举报率上升、CVR 下滑）
2. 按类目、来源、用户类型贡献条形图
3. 业务结论与建议动作卡片

推荐图表：
- Top N 贡献条形图
- 分层对比表

### 页面 4：A/B Test 对比
1. A/B 核心与护栏指标对比
2. Lift 和显著性展示
3. 上线决策建议（全量/灰度/不推广）

推荐图表：
- Lift 柱状图
- 指标矩阵表
- 结论文本框

## Python 图表版
- 已产出图表：
  - reports/figures/step5_metric_trend_with_anomalies.png
  - reports/figures/ab_test_comparison.png
  - reports/figures/case_xxx_contribution.png

## Streamlit 运行方式
1. 激活虚拟环境
2. 执行 streamlit run dashboard/app.py
3. 浏览器中查看交互式页面
