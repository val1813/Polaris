# Polaris 知识分类法

> 用户可以自由填，但建议从已有标签里选。**既不是完全自由（会乱），也不是强制枚举（会限制发现）。**

## 一级：领域（复用 arXiv 分类）

用户选一个主领域。可以填不在列表里的——但建议先从下面选。

| 代码 | 领域 | 覆盖什么 |
|------|------|---------|
| `cond-mat.str-el` | 强关联电子 | 超导、磁性、Mott绝缘体、奇异金属、量子相变 |
| `cond-mat.mes-hall` | 介观/量子霍尔 | 拓扑绝缘体、量子输运、纳米结构 |
| `cond-mat.stat-mech` | 统计力学 | 相变、临界现象、非平衡统计、热化 |
| `cond-mat.mtrl-sci` | 材料科学 | DFT预测、2D材料、电池、催化 |
| `hep-th` | 高能理论 | 弦论、AdS/CFT、量子引力、共形场论 |
| `hep-ph` | 高能唯象 | 暗物质、中微子、对撞机、B物理 |
| `gr-qc` | 广义相对论/宇宙学 | 黑洞、引力波、暴涨、暗能量 |
| `quant-ph` | 量子物理 | 量子信息、纠缠、量子计算、量子基础 |
| `physics.atom-ph` | 原子/分子/光学 | 冷原子、量子模拟、精密测量 |
| `physics.bio-ph` | 生物物理 | 蛋白质折叠、神经网络物理、主动物质 |
| `physics.chem-ph` | 化学物理 | 反应动力学、光谱、电化学 |
| `physics.data-an` | 数据分析/ML | 物理中的机器学习、统计方法 |
| `nlin` | 非线性/混沌 | 孤子、湍流、可积系统 |
| `math-ph` | 数学物理 | 严格统计力学、算子代数、拓扑方法 |
| `astro-ph` | 天体物理 | 恒星、星系、系外行星 |

## 二级：矛盾类型（Polaris 专用）

描述"这个课题发现了什么类型的矛盾"。

| 代码 | 类型 | 示例 |
|------|------|------|
| `exp-vs-theory` | 实验数据与理论预言矛盾 | 中微子失踪 vs 标准太阳模型 |
| `theory-vs-theory` | 两个成熟理论在边界处冲突 | QM vs GR 在普朗克尺度 |
| `hidden-assumption` | 所有人默认的前提被质疑 | 同时性是绝对的 → 狭义相对论 |
| `structural-isomorphism` | 跨学科结构同构暗示深层连接 | 自旋玻璃 ↔ 组合优化 |
| `no-go-violation` | 禁止定理的边界被突破 | Mermin-Wagner 在长程相互作用下失效 |
| `computational-barrier` | 经典不可解但子问题可打 | 符号问题 vs 变分蒙特卡罗 |
| `data-reinterpretation` | 已有数据的新解释 | 重新分析 CMB 数据推翻某个假设 |

## 三级：方法标签（自由填写，建议从已有选）

| 标签 | 含义 |
|------|------|
| `symmetry-breaking` | 对称性破缺分析 |
| `topological-invariant` | 拓扑不变量 |
| `entanglement-measure` | 纠缠度量 |
| `information-theoretic` | 信息论方法 |
| `category-theory` | 范畴论 |
| `holographic-duality` | 全息对偶 |
| `mean-field` | 平均场近似 |
| `renormalization-group` | 重整化群 |
| `monte-carlo` | 蒙特卡罗模拟 |
| `tensor-network` | 张量网络 |
| `conformal-bootstrap` | 共形 bootstrap |
| `effective-field-theory` | 有效场论 |

## JSON 中的用法

```json
"project": {
  "domain": "cond-mat.str-el",
  "contradiction_type": "hidden-assumption",
  "tags": ["information-theoretic", "renormalization-group"]
}
```

- `domain`：必填，建议从一级表选
- `contradiction_type`：必填，从二级表选
- `tags`：可选，自由填，建议从三级表选——也可以自创

**不在表里的领域/类型也可以填。** 分类法会随着社区贡献增长而扩展。
