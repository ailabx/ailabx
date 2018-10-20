# ailabx
AI量化实验室，专注将前沿人工智能技术(深度学习/强化学习/知识图谱)应用于金融量化投资。

### 项目说明

传统的量化平台，主要是以提供技术面、基本面的数据为基础，需要用户自行按自己的思路和需求编写策略。这些平台本质上是用户思路的自动化。

自动化只是量化的初级阶段，基于机器学习、深度学习、强化学习等人工智能前沿工具，机器自动发现数据中的模式，并优化相应的策略，
是这个我们这个平台的核心目标。

### 开发环境
anaconda python3.6

### “积木式”实现策略

buy_and_hold = Strategy([
    RunOnce(),
    PrintBar(),
    SelectAll(),
    WeighEqually(),
])

![image](https://note.youdao.com/yws/public/resource/624f4972c4f89ff3aaa41a5251b17d9c/xmlnote/A0F19587F7E9460B99BE62D3833E1457/12848)


### 联系我们

有任何问题或者建议，欢迎加入QQ群讨论：8430159，
也可以关注微信公众号：ailabx。
扫码进QQ群：

![image](https://note.youdao.com/yws/public/resource/624f4972c4f89ff3aaa41a5251b17d9c/xmlnote/D05091011E854FACA0ADB25D03F61101/12859)