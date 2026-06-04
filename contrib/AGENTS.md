# Community Contribution Model

> 不是每个人来改 SOP。三层结构，各管各的。

---

## 三层架构

### 第一层：SOP 核心（宪法）

```
research-group/   ← 核心 SOP，PR + benchmark 验证才能改
topic-selector/   ← 选题引擎，同上
```

- 改得慢，要证据
- PR 必须附：在 ≥2 个基准上跑过的结果
- 硬规则修改 → 需要 ≥1 个真实课题案例

### 第二层：contrib/ 社区角色（市场）

```
contrib/
  cond-mat-inspector.md    ← 凝聚态专用 Inspector
  particle-reviewer.md     ← 粒子物理专用 Reviewer  
  cosmology-b-agent.md     ← 宇宙学专用 B博士
```

- 自由贡献，opt-in
- 用户装了自己启用，不装不影响核心流程
- 质量判断：experiments/ 里 A/B 对比，数据说话

### 第三层：knowledge_graph/ 发现记忆库（图书馆）

```
knowledge_graph/
  LP24-EulerUnification_v1.0_20260603.json
  LP27-Tlinear-NFL_v1.0_20260604.json
  ...社区提交的...
```

- 标准 JSON 格式（schema 已定义）
- 每个课题收官后产出一个
- 社区可搜索、碰撞、复现

---

## 怎么判断好不好？

| 层 | 判断标准 | 工具 |
|----|---------|------|
| SOP 改动 | benchmark 回归 + metrics.py ≥ 70% | `benchmarks/score.py` |
| contrib 角色 | 同课题 A/B 对比（有角色 vs 无角色） | `experiments/` 模板 |
| knowledge 条目 | schema 验证 + REVIEWER 引用核实 | `validation/validate.py` |

**不靠感觉。靠数据。**

---

## 布衣科学家怎么参与？

不需要会写代码。三种方式：

1. **提交发现**：跑完一个课题 → 把 `knowledge_graph.json` 提 PR 到 `knowledge_graph/`
2. **提交角色创意**：在 Issue 里描述"我想要一个专门检查 XXX 的 Agent"→ 社区帮忙写成 md
3. **反馈 SOP 卡点**：在 Issue 里说"第 X 步经常卡在 Y"→ 附 Phase清单截图
