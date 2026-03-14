# Step 3 模拟数据生成逻辑

## 数据范围与粒度
1. 时间范围：2025-12-01 至 2026-02-28，共 90 天。
2. 数据粒度：日期 × 内容类目 × 流量来源 × 用户类型 × 实验组别 × 时段 × 城市层级。
3. 产出文件：data/raw/content_platform_mock_data.csv。

## 维度设计
- 内容类目：food, travel, entertainment, knowledge, local_services
- 流量来源：recommendation, search, follow, nearby
- 用户类型：new_user, active_user, returning_user
- 实验分组：A, B
- 时段：morning, afternoon, evening
- 城市层级：tier1, tier2, tier3

## 正常波动机制
1. 引入周末系数，模拟内容消费在周末提升。
2. 引入类目、来源、用户、时段、城市层级权重差异。
3. 对曝光和率指标叠加随机噪声，形成真实业务中的自然波动。

## 异常事件清单
1. 异常事件 A：CTR 下滑
   - 时间：2026-01-20 至 2026-01-28
   - 范围：entertainment + recommendation
   - 机制：CTR 乘以 0.65
2. 异常事件 B：举报率上升
   - 时间：2026-02-05 至 2026-02-12
   - 范围：food + search
   - 机制：report_rate 乘以 2.6
3. 异常事件 C：转化率下降
   - 时间：2026-02-15 至 2026-02-22
   - 范围：new_user + follow
   - 机制：conversion_rate 乘以 0.55

## A/B Test 设定
1. 实验开始时间：2026-02-01。
2. B 组效果设定：
   - CTR 提升 8%
   - 转化率提升 6%
   - 举报率上升 18%
   - 完播率下降 4%
3. 目的：模拟真实业务中增长收益与风险/体验指标的权衡。

## 落地代码说明
- 脚本位置：src/generate_data.py
- 输出路径：data/raw/content_platform_mock_data.csv
- 运行命令：python src/generate_data.py
