---
name: emu-mathmodel-workflow
description: 月宫绘梦的数学建模 Solo 工作流。在特定环境特定项目下或用户明确说明使用数学建模工作流时使用。
---

# 月宫绘梦的数学建模 Solo 工作流

## 触发条件

当用户正在进行数学建模比赛，或提出与以下相关的请求时触发：
- 数学建模论文写作
- 数学建模代码实现
- 数模论文排版与输出
- 数学建模工作流/流水线
- 数模 SOLO 参赛流程

## 工作流概述

面向零编程、零论文基础但走过一次完整数模流程的选手。基于 Deepseek V4 Pro 和 Trae IDE的纯 SOLO 数学建模工作流。

**四个阶段：**
1. **宏观建模** — 读题、讨论模型选型
2. **逐个击破** — 每个子问题的建模、编码、结晶
3. **完成论文** — 自动分段生成、合并、检查
4. **最终输出** — Typora 导出 PDF、脚本打包

## 快速开始

使用户确保自身具备能力：

- 完整的数模参赛经验(至少走过一次完整流程并成功提交)
- 基本的数学模型理解能力
- Markdown 语法基础

使用户确认电脑已有：

- Typora(必需)
  用于导出PDF，确保用户安装了位于`docs/typora/emu-paper.css`的样式文件。
  引导用户阅读`docs/typora/index.md`，了解Typora设置。

自己确保环境包含：

- Python 运行环境(必需)
  `python -V`
  引导用户安装Python

- 本工作流的必需初始工作区
  检查项目中有没有`docs/writing.md`文件。
  检查项目根目录下是否存在`utils/build.py`和`utils/build_final.py`两个文件。
  如不存在，提示用户下载git并使用`git clone https://github.com/emumus/emu_mm_workflow.git`下载项目。

## 工作区目录结构

项目根目录下严格划分以下文件夹：

```
project-root/
├─ doc/         # [不变] 给 AI 看的分阶段任务说明
├─ utils/       # [不变] 工具脚本与样式
├─ ques/        # [不改] 原始问题描述
├─ cit/         # [不改] 下载的论文、原始数据集
├─ code/        # 所有探索性代码与中间数据，不进入正式论文
│  ├─ raw/      # 探索阶段的 .py 文件，命名可随意如 q1_v1.py
│  └─ q1/...    # 最终冻结后的拆分代码，会直接进入论文附录
│      └─ img/  # 代码产出的图片目录，会直接用于论文正文
├─ text/        # 一切过程文本：分析、草稿、半成品、成品论文
│  ├─ raw/      # 模型分析与求解过程记录
│  ├─ paper/    # 生成论文的各个章节块及合并文件
│  ├─ appendix/ # 额外的附录，可以无
│  └─ frozen/   # 生成拼接好的 Markdown 形式论文和完整附录
└─ frozen/      # 脚本会自动在此文件夹中创建打包好的论文、参考资料、md5 信息
```

如果目录不为空，根据实际情况灵活调整结构

## 一、宏观建模

读题、讨论整道题目的类型、方案。记录大体的模型选型、可能性。

此阶段的完成标志是`text/raw/初步分析.md`中解题步骤的出现。

产出文件：
- `text/raw/题目原文.md` - 原始问题原文
- `text/raw/初步分析.md` - **解决步骤**、初步思路、模型大致选型、对比表格、创新点思路

[阶段一规则](reference/Stage1.md)

## 二、逐个击破

对于每道题，进行建模、代码、结果结晶。

此阶段的完成标志为:

for `text/raw/初步分析.md`中的所有解题步骤 as `[step]`: 
  - `code/raw/[step]/`下所有求解、画图代码、数据成果的完善。
  - `text/raw/[step].md`中结果、结论的完善。

[阶段二规则](reference/Stage2.md)

## 三、完成论文

将每道题的分析总结成论文段落，然后进行最终论文的检查。

此阶段的完成标志是`text/frozen/Main.md`和`text/frozen/Appendix.md`的完善(由用户确认)。

产出文件：
- `text/raw/structure.md` - 论文骨架
- `text/paper/*.md` - 各个章节的论文部分
- `text/frozen/Main.md` - 完整的Markdown格式论文，包含标题所有章节。
- `text/frozen/Appendix.md` - 完整的Markdown格式附录，包含所有额外的代码、数据、图表等。

[阶段三规则](reference/Stage3.md)

## 四、最终输出

当用户确认论文已没有任何问题后，执行此阶段导出所有最终材料。

产出文件：
- `frozen/[time]/我的论文.pdf` - 最终的PDF格式论文，包含所有章节。
- `frozen/[time]/我的参考资料.zip` - 所有代码文件、原始数据集、引用论文的压缩包。
- `frozen/[time]/md5.txt` - 两个文件的 MD5 值和其他必要信息。

[阶段四规则](reference/Stage4.md)

## 重要提醒

- 本工作流完全基于 Python
- 可以使用虚拟环境，推荐使用`uv`。新手嫌麻烦大可以不配置。
- Deepseek V4 Pro 有 2.5 折优惠(截至 2026/05/31)，单次开销约 30 元
- 建议添加自己的 Deepseek API Key，避免使用内置 Auto 模型(效果差、需排队)。开放平台注册充值获取：https://platform.deepseek.com
