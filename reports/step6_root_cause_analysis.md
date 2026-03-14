# Step 6 分层归因分析

## 分析方法
1. 针对异常窗口，选择异常前 7 天作为基线窗口。
2. 以指标变化量为目标，按内容类目、流量来源、用户类型拆解贡献。
3. 输出主驱动分层与可执行建议。

## CASE_1: CTR下滑归因
- 异常窗口: 2026-01-20 到 2026-01-28
- 对比基线: 2026-01-13 到 2026-01-19
- 指标整体变化: -0.003127
- content_category 主要贡献分层: entertainment (-0.003078), local_services (-0.000072), food (0.000046)
- traffic_source 主要贡献分层: recommendation (-0.002932), nearby (-0.000163), search (-0.000111)
- user_type 主要贡献分层: active_user (-0.001217), new_user (-0.001018), returning_user (-0.000892)
- hour_bucket 主要贡献分层: evening (-0.001231), afternoon (-0.000985), morning (-0.000910)
- 业务结论: 整体 CTR 下滑主要由推荐流量下的娱乐类内容驱动，新用户受影响更明显。
- 建议动作: 对异常时窗内娱乐类新增供给做质量回溯，临时降低低质素材在推荐流量中的分发权重。

## CASE_2: 举报率上升归因
- 异常窗口: 2026-02-05 到 2026-02-12
- 对比基线: 2026-01-29 到 2026-02-04
- 指标整体变化: 0.000242
- content_category 主要贡献分层: food (0.000205), entertainment (0.000024), local_services (0.000017)
- traffic_source 主要贡献分层: search (0.000184), recommendation (0.000023), nearby (0.000018)
- user_type 主要贡献分层: active_user (0.000091), new_user (0.000085), returning_user (0.000066)
- hour_bucket 主要贡献分层: evening (0.000089), afternoon (0.000081), morning (0.000072)
- 业务结论: 举报率抬升主要集中在搜索流量中的美食类内容，晚间时段贡献更高。
- 建议动作: 强化搜索召回侧敏感词和标题党过滤规则，并在高风险时段追加审核阈值。

## CASE_3: 转化率下滑归因
- 异常窗口: 2026-02-15 到 2026-02-22
- 对比基线: 2026-02-08 到 2026-02-14
- 指标整体变化: -0.001513
- content_category 主要贡献分层: local_services (-0.000521), food (-0.000320), entertainment (-0.000251)
- traffic_source 主要贡献分层: follow (-0.001698), nearby (0.000286), recommendation (-0.000232)
- user_type 主要贡献分层: new_user (-0.001536), active_user (0.000192), returning_user (-0.000169)
- hour_bucket 主要贡献分层: evening (-0.000642), morning (-0.000440), afternoon (-0.000431)
- 业务结论: 转化率下降主要由关注流量的新用户贡献，表现为点击后转化衰减。
- 建议动作: 优化新用户转化链路文案和权益呈现，分渠道回收低意图流量。

## 总结
异常并非全局均匀波动，而是由少数关键分层驱动。建议将分层告警纳入常态化监控。