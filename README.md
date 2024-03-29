# ailabx

AI量化投资实验室，专注将前沿人工智能技术(机器学习、深度学习、强化学习、遗传算法、图计算、知识图谱等)应用于金融量化投资。

金融投资领域是高度信息密集型，而且信息相对结构化，照理讲是最适合机器计算的领域。可是，当前投资仍然处于“刀耕火种”的年代，有人忙于调研，读报表；有人忙于盯盘，画线条。
alphago master登顶围棋之巅都过去五年之久了，算法、算力日新月异的发展，不应该是当前这个样子。

尽管金融数据低“信噪比”，也不要指望打造一台永动机。

但请相信一句话就是：

No man is better than a machine, but no machine is better than a man with a machine!

让机器辅助我们投资，将无往而不利。

按照个人积极参与主动决策的程度，把投资分成三个层次：
- 一、全天候大类资产配置。
被动管理，很少参与。在坐好资产后长期持续，只做一些被动再平衡的操作； 
- 二、战术资产配置。
关注宏观层面大的周期，在周期偏好的资产上持有更多的仓位。
- 三、择时
积极判断市场方向，期望做到“低买高卖”。

这三个层次，从上到下，越来越不确定，越来越难，风险也越来越高。当然如果做好，收益也是越来越大。

建议普通人都从第一层次做起，比较容易做到从理财往投资过渡。

但是很遗憾，大部分人一上手就是冲着第三层次来的，“追涨杀跌”却常常做错方向，最终成为韭菜。

![图片](https://gitee.com/ailabx/ailabx/raw/master/images/mainwindow.png)
### 项目说明
传统的量化投资，使用技术指标比如均值，MACD，RSI,KDJ等以及它们的线性变种来产生信号。
有几个缺点：

一则这是线性的，

二是参数全凭经验，没有调优的过程，

三是规则是静态的，无法根据市场变化自主进化。

我们的目标，是把前沿人工智能技术，包括机器学习，深度学习，深度强化学习，知识图谱，时间序列分析等技术应用于金融大数据挖掘，
更好的赋能量化投资。

金融数据的低信噪比，让这件事情变更很难，

难，才有意思。

### “积木式”回测引擎

algo_list_rolling = [

        SelectFix(instruments=['sh000300', 'sh000905', 'sz399006']),

        SelectBySignal(signal_buy='to_buy', signal_sell='to_sell'),

        SelectTopK(K=1,col='五日动量'),

        WeightEqually()
    ]

### 开发环境与安装部署

python3.7

直接git或者下载源码包，安装相关依赖，然后运行main.py即可。

git clone https://github.com/ailabx/ailabx.git

cd ailabx

pip install -r requirements.txt

python main.py

### 联系我们

也可以关注微信公众号：**七年实现财富自由**(ailabx)。
持续分享我的 七年实现财务自由 实盘及逻辑。
投资理财前沿观察与思考。

![WAI](https://gitee.com/ailabx/ailabx/raw/master/images/weixin.jpg)

有任何问题，可以到**知识星球**——**AI量化投资实验室** 找我，每天都在。

持续分享前沿**人工智能技术如何赋能金融投资**，并找到一帮志同道合的朋友！

![WAI](https://gitee.com/ailabx/ailabx/raw/master/images/xingqiu.png)