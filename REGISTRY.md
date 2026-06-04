# Polaris Registry — 社区知识库

> **独立仓库。** 这里只放 JSON。没有代码，没有 SOP。
> URL: `github.com/val1813/polaris-registry`（待建）

## 架构

```
polaris (引擎)              polaris-registry (图书馆)
├── research-group/         ├── entries/
├── topic-selector/         │   ├── LP27_v1.0_20260604.json
├── validation/             │   ├── LP24_v1.0_20260603.json
├── benchmarks/             │   └── ...
└── ...                     ├── index.json          ← linker.py 自动生成
                            ├── TAXONOMY.md
                            ├── REVIEW_POLICY.md
                            └── .github/workflows/  ← 自动校验
```

## 用户怎么提交

```
1. 跑完课题 → GATE 7 产出 JSON
2. Fork polaris-registry
3. 把 JSON 放到 entries/
4. 提 PR
5. GitHub Actions 自动跑 schema 校验 + metrics.py
6. 通过 → 你审核合并（3 分钟/份）
7. 合入 → index.json 自动更新
```

## 审核工作流

```
用户提 PR
    │
    ▼
GitHub Actions 自动检查：
  ├─ JSON schema 合法？
  ├─ metrics.py ≥ 70%？
  ├─ contributor.github 存在？
  └─ 至少 1 个 DOI 格式有效？
    │
    ├─ 全过 → 标 "ready for review"
    └─ 失败 → PR comment 自动写原因
    │
    ▼
你人工过一遍（3 分钟）：
  ├─ 有 ≥1 个 confidence≥0.6 的节点？
  ├─ surviving + killed 都不为空？
  └─ 抽查 1 个 DOI 真实存在？
    │
    ▼
合入 → index.json 自动重建 → 网站自动更新
```

## 网站

GitHub Pages 纯静态。不需要服务器。

```
polaris-registry.github.io
  ├─ 首页：最新提交 + 按领域浏览
  ├─ 搜索：linker.py 生成的 index.json → 前端 JS 全文搜索
  ├─ 条目页：单条 JSON 的美化展示
  └─ 统计：总条目、覆盖领域、贡献者排行
```

index.json 只有几 KB，前端搜索零延迟。
