# ailabx

AI量化实验室，专注将前沿人工智能技术(深度学习/强化学习/知识图谱)应用于金融量化投资。

### 项目说明

传统的量化平台，主要是以提供技术面、基本面的数据为基础，需要用户自行按自己的思路和需求编写策略。
用户需要写大量的模板代码，ailabx首先通过“模块化”精减大量的模板代码。

### “积木式”实现策略示例

“买入并持有”策略：
buy_and_hold = Strategy([
    RunOnce(),

    PrintBar(),

    SelectAll(),

    WeighEqually(),
])

“均线交叉策略”：

long_expr = 'cross_up(ma(close,5),ma(close,10))'

flat_expr = 'cross_down(ma(close,5),ma(close,10))'

ma_cross = Strategy([

    SelectByExpr(long_expr=long_expr,flat_expr=flat_expr),

    WeighEqually(),

])

另外，传统量化平台本质上是用户思路的自动化，“自动化”只是量化的初级阶段。

“智能化”才是量化的核心与终级目标。

基于机器学习、深度学习、强化学习等人工智能前沿工具，机器自动发现数据中的模式，并优化相应的策略，是这个我们这个平台的核心目标。

### 开发环境
anaconda python3.6

![image](https://note.youdao.com/yws/public/resource/624f4972c4f89ff3aaa41a5251b17d9c/xmlnote/CFAC02F6DFDD4F43890D7C173965DB21/12862)

### 联系我们


也可以关注微信公众号：ailabx。

![image](https://note.youdao.com/yws/public/resource/624f4972c4f89ff3aaa41a5251b17d9c/xmlnote/E21A03876FCA476F8ED330062407C379/12867)

有任何问题或者建议，欢迎加入QQ群讨论：8430159，
扫码进QQ群：

![image](https://note.youdao.com/yws/public/resource/624f4972c4f89ff3aaa41a5251b17d9c/xmlnote/D05091011E854FACA0ADB25D03F61101/12859)