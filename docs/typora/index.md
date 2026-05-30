# 关于Typora样式的安装和自定义

1. 打开Typora，点击"文件" -> "偏好设置" -> "外观" -> "打开主题文件夹"

2. 将本目录下的`emu-paper.css`文件复制到打开的Typora主题文件夹中(一般在`**\Typora\themes`目录下)

3. 重启Typora。

4. 点击"主题"即可看到"Emu Paper"选项。

# 关于Markdown及其编辑器

Markdown不像Word那样复杂，几乎所有效果无法通过简单的交互实现。Markdown预设一部分常用的语法对应的格式，如标题、粗体等，这些语法所显示的样式并没有统一标准，就像你也可以往word版论文里塞立体艺术字一样。

故此，你可以用一些好看的Typora主题如Purple Cesno(这需要你自己下载)来查看论文，然后最后切换到Emu Paper主题来导出PDF。Markdown本身不包含样式。

Markdown属于HTML分支，因此它继承HTML语法，如嵌入HTML代码。一般也使用CSS来定义样式。样式文件`emu-paper.css`就是CSS文件，你可以问AI修改样式文件，改变论文样式。

# 关于导出

Typora**不需要**Pandoc来导出PDF。

除非你需要导出到Word等格式。Typora需要[Pandoc](http://pandoc.org/)来支持部分高级功能。如果您尚未安装Pandoc（或版本低于v2.0），请从[Pandoc下载页面](https://github.com/jgm/pandoc/releases/latest)下载并运行安装程序。

安装 Pandoc 后，如果 Typora 提示找不到 Pandoc，您可能需要重启 Typora。

对于 Windows 用户，如果 Typora 仍提示找不到 Pandoc，您可能需要重启电脑。

# 关于Typora配置

1. 打开Typora，点击"文件" -> "偏好设置" -> "Markdown"

2. Markdown扩展语法：

- [x] 自动识别链接（例：https://typora.io/）
- [x] 内联公式（例：$\LaTeX$）
- [x] 上标（例：X^2^）
- [x] 图标（序列图、流程图 和 Mermaid 图）

3. 代码块

- [x] 显示行号

4. "偏好设置" -> "导出" -> "PDF"

这里有页面大小和页边距，一般A4都没问题，页边距有要求的自己改。

页尾处填入 `${pageNo} / ${pageCount}` 用于显示例如"4 / 10"的页码信息。如果有自己的页码需求也可以自己看着改。[文档](https://support.typora.io/Export/#header--footer)

# 最后

Typora确实是一个强大的工具。但如果你有可以完全抛弃Typora的**已经实际跑通**的平替方案，欢迎提出Issue。
