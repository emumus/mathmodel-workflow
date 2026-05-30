## 三、完成论文

### 阶段 1: 设计论文骨架

{
  "todos": [
    {"id":"1","content":"根据已有成果设计章节结构","status":"in_progress","priority":"medium"},
    {"id":"2","content":"文献整理","status":"pending","priority":"medium"},
    {"id":"3","content":"写入structure.md","status":"pending","priority":"medium"},
  ]
}

**(A) 根据已有成果设计章节结构**

一般普通论文的结构如下：

- 摘要 // 必须且占第一个位置
- 问题重述
- 问题分析
- 模型假设
- 符号说明
- 问题X模型的建立与求解 // `X` - 中文简体大写数字
- 模型优缺点
- 参考文献

对于解题步骤，如果有特别的步骤如[eda]，可能插入额外的章节，如：

- 数据来源与处理/数据预处理
- 灵敏度分析

确保所有在text/raw中研究的内容都被包含在论文中。

确保每个章节都独自且必须占有一个文件和一个二级标题(`##`)，否则脚本报错。摘要除外，摘要块必须没有二级标题，有一个一级标题(`#`)，即论文大标题。

**(B) 文献整理**

检查所有

所有研究，对所有指定的引用来源以国标形式整理编号。

**(C) 写入structure.md**

以上两个步骤的成果需要总结到`text/raw/structure.md`中。
```md[text/raw/structure.md]
论文结构：
0. 摘要
1. 问题重述
2. 问题分析
3. 模型假设
...
引用：
[1] 中国精算师协会. 中国人身保险业经验生命表（2025）[R]. 北京: 中国精算师协会, 2025-10-29.
[2] 重庆市统计局. 重庆市第三、四次人口普查资料汇编[EB/OL]. 重庆: 重庆市统计局, 2001-08.
[3] United Nations, DESA, Population Division. World Population Prospects 2024[R]. New York: United Nations, 2024-07-11.
...
```

### 阶段 2: 填充论文内容

对于已经总结好的`text/raw/structure.md`，根据章节结构填充论文内容。

{
  "todos": [
    {
        "id":f"{i}",
        "content":f"完成{i}_{name}.md",
        "status":"pending",
        "priority":"medium"
    } for i, name in 论文结构,
  ]
}

执行内容：
- 在各个步骤期间，认真研究该步骤的小结`text/raw/[step].md`
- 确保小结中所有值得写出的内容都被包含在论文中。
- 在 `text/paper/` 下生成各章节 `{i}_{name}.md` 文件，如`text/paper/0_摘要.md`。

注意：写作说明在项目根目录的`docs/writing.md`中。

### 阶段 3: 第一次构建

运行 `python utils/build.py`，脚本自动：
1. 查找所有模型代码文件并读取
2. 添加 `text/appendix/` 下的每个文件作为额外附录
3. 自动编号后输出 `text/frozen/Appendix.md`
4. 合并各章节 `.md` 为 `text/frozen/Main.md`

构建完成后，检查`utils/cache/desc.json`，添加缺少的描述，简要一句。然后再次运行脚本。

完成以上三个阶段后，交由用户审核以下输出：
- `text/frozen/Main.md` - 完整的Markdown格式论文，包含标题所有章节。
- `text/frozen/Appendix.md` - 完整的Markdown格式附录，包含所有额外的代码、数据、图表等。

强调如果有任何问题或错误：
- 必须找到 `text/paper/` 下对应章节原文修改
- 修改后重跑 `python utils/build.py`
- 切勿直接修改 `text/frozen/Main.md`或`text/frozen/Appendix.md`，否则会被覆盖。

建议用户：
- 从头到尾把问题全部记下来之后再一一修改，避免 solo 时注意力和流程分崩离析

### 阶段 4: 审核意见

用户审核以上输出，用户指出某节的问题后：

- 定位产生问题的步骤和阶段，如步骤`q2`的`写论文`阶段，无需改动代码等，直接修改`text/paper/6_q2.md`
- 可能需要修改模型代码，可能需要修改图表等。需要动代码时遵循最小改动原则。如要新增图等必须在论文中新增图对应引用。

本阶段原则上不能破坏项目结构，此外均可自由发挥，包括部分步骤返回阶段二返工。