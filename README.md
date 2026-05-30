# emu_mm_workflow

基于DeepSeek V4 Pro与Trae IDE的数学建模Solo工作流。面向零编程、零论文基础但有数模基础的选手。旨在低成本、充分利用人类优势，稳定产出结构完整、格式规范、包含创新的数学建模论文。

## 适用人群

- 至少参加过一次数学建模竞赛并完整走完提交流程
- 具备基本的电脑操作能力
- 理解基本数学模型概念
- 具有较强的自学能力
- 弱校一带二或零队友场景下的参赛者

## 核心思路

传统的数学建模团队分为建模手、编程手、论文手，**但有时并非所有三种高手都能找到他们彼此**。本工作流通过大模型完全替代编程手、通过放弃Word,LaTeX而是使用Markdown转PDF完成论文手的工作，将数学建模回归原本的数学建模：你来把握方向与创新，AI负责代码实现、论文生成与排版，完全利用人类的优势与价值，实现高质量、高效且合规的数学建模。

## 工具链

[Trae](https://www.trae.cn/) - AI代码编辑器，工作流的主战场。支持Skill，可按需加载预置的工作流提示词与脚本
[DeepSeek V4 Pro](https://platform.deepseek.com/) - 后端大模型，负责代码生成、模型分析、论文撰写。每次付费节点
[Typora](https://typora.io/) - Markdown编辑器，支持自定义CSS主题并将Markdown直接渲染导出为PDF。单次付费。

## 前置准备

1. 安装[Trae](https://www.trae.cn/)并添加自有DeepSeek API Key
2. 安装[Typora](https://typora.io/)，导入项目提供的`docs/typora/emu-paper.css`主题样式
3. 确保本地有Python运行环境
4. 安装项目依赖：

```bash
pip install matplotlib PyPDF2 reportlab pdfrw
```

5. 克隆本仓库到本地，并使用trae打开该目录：

```bash
git clone https://github.com/emumus/emu_mm_workflow.git
```

## 工作区目录结构

```
project-root/
├── .trae/              # Skill定义，此文件夹将被Trae自动加载
│   └── skills/
│       ├── emu-mathmodel-workflow/   # 数学建模主工作流Skill
│       └── openalex-paper-search/    # OpenAlex文献检索Skill
├── docs/               # [不变] 写作规范与Typora样式
│   ├── writing.md      # 论文写作格式规范
│   └── typora/
│       ├── emu-paper.css   # 数模论文Typora主题
│       └── index.md        # Typora配置说明
├── utils/              # [不变] 构建脚本与样式
│   ├── style.py        # Matplotlib全局绘图样式
│   ├── build.py        # 第一阶段构建：合并章节、生成附录
│   └── build_final.py  # 第二阶段构建：合并PDF、打包参考资料、计算MD5
├── ques/               # [不改] 原始题目描述与附件
├── cit/                # [不改] 引用论文与原始数据集
├── code/               # 探索性与最终代码
│   ├── raw/            # 探索阶段代码，允许冗余与调试痕迹
│   └── q*/             # 结晶后的最小可运行代码与图片
│       └── img/        # 论文用的图片输出目录
├── text/               # 所有过程文本与论文
│   ├── raw/            # 模型分析与求解过程记录
│   ├── paper/          # 论文各章节分段文件
│   ├── appendix/       # 额外附录内容
│   └── frozen/         # 合并后的 Markdown 论文与附录
└── frozen/             # 最终导出目录（PDF、参考资料包、MD5 校验）
```

## 四阶段工作流

### 阶段一：宏观建模

与AI讨论题目类型、模型选型、解题思路。产出的核心文件是`text/raw/初步分析.md`，其中包含完整的解题步骤、模型对比表格和创新点思路。此阶段约需3小时。

### 阶段二：逐个击破

对每个子问题依次执行：

1. **初始模型设计** - AI给出具体的模型建立计划，记录为`text/raw/问题X的建模与求解.md`。用户可在此阶段注入创新点或提供参考论文
2. **探索性代码实现** - AI生成代码、运行、画图，用户评估结果并决定接受或推倒重来。代码放在`code/raw/`
3. **结果结晶** - 满意度达标后，AI提取纯净的模型代码（`code/q*/q*_model_*.py`）、画图代码（`code/q*/q*_img_*.py`），并更新`text/raw/`中的最终结果记录 

此阶段最为耗时，是解题的核心阶段。

### 阶段三：完成论文

调用emu-mathmodel-workflow Skill，AI自动执行：

1. 设计论文章节分段（问题重述、模型假设、符号说明、各问题求解、模型评价、参考文献等）
2. 整理并编号参考文献
3. 在`text/paper/`下按章节生成分段 `.md` 文件
4. 运行`python utils/build.py`合并章节为`text/frozen/Main.md`，自动生成`text/frozen/Appendix.md`
5. 用户通读检查后，手动用Typora导出PDF

此阶段按论文的问题点数量，约需3-6小时调整。或有模型级别的改动，可能需要超过12小时。

### 阶段四：最终输出

运行`python utils/build_final.py`，自动完成：

- 合并`Main.pdf`与`Appendix.pdf`为最终论文
- 打包`code/`、`ques/`、`cit/`为参考资料压缩包
- 计算并记录MD5校验值

所有产出物存放在`frozen/[时间戳]/`目录下。一般不超过10秒。

## 重要提示

- 本工作流生成的模型中可能出现拍脑袋参数或虚构数据，需要人工审视与校验
- 每个子问题的结果结晶完成后建议更换对话以清空上下文
- 最终检查论文时建议先通读全文并逐个记录问题，再一次性交由AI修改，避免反复局部修改导致前后不一致
- Python依赖建议使用`uv`管理虚拟环境，新手可直接使用全局环境。

## 许可证

本仓库下所有SKILL提示词、脚本、代码等初始代码资源作为本项目资源依照MIT许可证进行开源。
