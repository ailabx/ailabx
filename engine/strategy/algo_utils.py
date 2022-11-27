# encoding:utf8
import numpy as np
import scipy.optimize as sco


def calculate_half_cov_matrix(train_set):
    # 计算半衰协方差矩阵
    M = 60
    train_subset = train_set.iloc[0:60]
    cov_matrix = train_subset.cov()*M * (1 / 10)
    for i in range(1, 4):
        if len(train_set) < i * 60:
            break
        # print(len(train_set))
        train_subset = train_set.iloc[i * 60:(i + 1) * 60]
        #print(train_subset)
        sub_cov_matrix = train_subset.cov()*M
        if i == 1:
            sub_cov_matrix = sub_cov_matrix * (2 / 10)
        if i == 2:
            sub_cov_matrix = sub_cov_matrix * (3 / 10)
        else:
            sub_cov_matrix = sub_cov_matrix * (4 / 10)
        cov_matrix = cov_matrix + sub_cov_matrix
    # print(cov_matrix)
    return np.matrix(cov_matrix)


# import scipy.interpolate as sci
# 根据资产预期目标风险贡献度来计算各资产的权重
def calculate_portfolio_weight(one_cov_matrix, risk_budget_objective):
    '''
约束条件的类型只有'eq'和'ineq'两种
eq表示约束方程的返回结果为0
ineq表示约束方程的返回结果为非负数
'''
    num = one_cov_matrix.shape[1]  # 一种有num种资产
    x0 = np.array([1.0 / num for _ in range(num)])  # 初始资产权重
    bounds = tuple((0, 1) for _ in range(num))  # 取值范围(0,1)

    cons_1 = ({'type': 'eq', 'fun': lambda x: sum(x) - 1},)  # 权重和为1
    RC_set_ratio = np.array([1.0 / num for _ in range(num)])  # 风险平价下每个资产的目标风险贡献度相等
    optv = sco.minimize(risk_budget_objective, x0, args=[one_cov_matrix, RC_set_ratio], method='SLSQP', bounds=bounds,
                        constraints=cons_1)
    return optv.x


# 标准风险平价下的风险贡献
def calculate_risk_contribution(weight, one_cov_matrix):
    weight = np.matrix(weight)
    sigma = np.sqrt(weight * one_cov_matrix * weight.T)
    # 边际风险贡献 Marginal Risk Contribution (MRC)
    MRC = one_cov_matrix * weight.T / sigma
    # 风险贡献 Risk Contribution (RC)
    RC = np.multiply(MRC, weight.T)
    return RC


# 定义优化问题的目标函数，即最小化资产之间的风险贡献差
def naive_risk_parity(weight, parameters):
    # weight: 待求解的资产权重,
    # parameters: 参数列表
    # parameters[0]: 协方差矩阵
    # parameters[1]: 风险平价下的目标风险贡献度向量

    one_cov_matrix = parameters[0]
    RC_target_ratio = parameters[1]
    # RC_target为风险平价下的目标风险贡献，一旦参数传递以后，RC_target就是一个常数，不随迭代而改变
    sigma_portfolio = np.sqrt(weight * one_cov_matrix * np.matrix(weight).T)  # 组合波动率
    RC_target = np.asmatrix(np.multiply(sigma_portfolio, RC_target_ratio))  # 目标风险贡献
    # RC_real是 每次迭代以后最新的真实风险贡献，随迭代而改变
    RC_real = calculate_risk_contribution(weight, one_cov_matrix)
    sum_squared_error = sum(np.square(RC_real - RC_target.T))[0, 0]
    return sum_squared_error


# 基于主成分分析的风险平价下的风险贡献
def calculate_risk_contribution_pca(weight, one_cov_matrix):
    weight = np.matrix(weight)
    sigma = np.sqrt(weight * one_cov_matrix * weight.T)
    # 奇异值分解，其中uv=I ,u,v是特征向量矩阵，是正交阵，d是对角矩阵，对角元素是特征值，tr(d)=tr(one_cov_matrix)
    u, d, v = np.linalg.svd(one_cov_matrix)
    a = v * weight.T
    b = v * (one_cov_matrix * weight.T)
    # 风险贡献 Risk Contribution (RC)
    RC = np.multiply(a, b)
    RC = RC / sigma
    return RC


# 定义优化问题的目标函数，即最小化资产之间的风险贡献差
def pca_risk_parity(weight, parameters):
    # weight: 待求解的资产权重,
    # parameters: 参数列表
    # parameters[0]: 协方差矩阵
    # parameters[1]: 风险平价下的目标风险贡献度向量

    one_cov_matrix = parameters[0]
    RC_target_ratio = parameters[1]
    # RC_target为风险平价下的目标风险贡献，一旦参数传递以后，RC_target就是一个常数，不随迭代而改变
    sigma_portfolio = np.sqrt(weight * one_cov_matrix * np.matrix(weight).T)  # 组合波动率
    RC_target = np.asmatrix(np.multiply(sigma_portfolio, RC_target_ratio))  # 目标风险贡献
    # RC_real是 每次迭代以后最新的真实风险贡献，随迭代而改变
    RC_real = calculate_risk_contribution_pca(weight, one_cov_matrix)
    sum_squared_error = sum(np.square(RC_real - RC_target.T))[0, 0]
    return sum_squared_error
