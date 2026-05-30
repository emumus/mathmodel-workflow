## 四、最终输出

### 前提
用户已确定论文已没有任何问题。

### 步骤
1. 用户使用 Typora 打开 `text/frozen/Main.md` 和 `text/frozen/Appendix.md`，选择预设主题导出为 PDF
    - 导出到原目录位置即可。即默认的`text/frozen/Main.pdf`和`text/frozen/Appendix.pdf`
2. 运行第二次构建脚本，自动：
    - 计算当前时间戳，格式为 `YYYYMMDD_HHMMSS`
    - 整合论文PDF文件
        - 合并两个 PDF(如有 `Prefix.pdf` 也会自动识别添加在前面)
        - 输出到 `frozen/[time]/我的论文.pdf`
    - 打包所有参考资料文件
        - 打包所有代码文件、原始数据集、引用论文为 `我的参考资料.zip`
    - 计算两个文件的 MD5(国赛需要)，输出到 `frozen/[time]/md5.txt`。包含md5、SHA256、开始和结束输出时间等

### 输出结构

```
frozen/
    └─20260510_1345/
        ├─ 我的论文.pdf
        ├─ 我的参考资料.zip
        └─ md5.txt
```
