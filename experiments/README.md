# Experiments — A/B 测试框架

> 用数据驱动 PolarS 自身迭代。不同 Prompt 版本、Agent 策略的对比实验。

## 目录结构

```
experiments/
  EXP-001-描述/
    config.md       ← 实验配置（模型/策略/轮次）
    variant_a/      ← 对照组 Prompt
    variant_b/      ← 实验组 Prompt
    results.md      ← 对比结果
```

## 实验模板

### config.md

```markdown
# EXP-00X: [实验名称]
日期: 
目的: [一句话]

## 配置
- 模型: [DeepSeek V4 / Claude Sonnet / ...]
- 课题: [同一课题，控制变量]
- 轮次: [N轮]

## 变量
- A组: [当前默认配置]
- B组: [改动描述]

## 评估指标
- [ ] Token 消耗
- [ ] Agent 总耗时
- [ ] INSPECTOR 阻断数
- [ ] REVIEWER 致命指控数
- [ ] 结论确信度
```

### results.md

```markdown
# 结果

| 指标 | A组 | B组 | 胜者 |
|------|-----|-----|------|
| Token | X | Y | |
| 耗时 | X | Y | |
| 阻断 | X | Y | |
| 致命 | X | Y | |
| 确信度 | X | Y | |

## 结论
[哪个更好，为什么，是否合入主分支]
```

## 当前实验

（待提交）
