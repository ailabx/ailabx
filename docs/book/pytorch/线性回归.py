import numpy as np
import matplotlib.pyplot as plt
#https://github.com/L1aoXingyu/pytorch-beginner/blob/master/01-Linear%20Regression/Linear_Regression.py
x_train = np.array([[3.3], [4.4], [5.5], [6.71], [6.93], [4.168],
                    [9.779], [6.182], [7.59], [2.167], [7.042],
                    [10.791], [5.313], [7.997], [3.1]])

y_train = np.array([[1.7], [2.76], [2.09], [3.19], [1.694], [1.573],
                    [3.366], [2.596], [2.53], [1.221], [2.827],
                    [3.465], [1.65], [2.904], [1.3]])

plt.plot(x_train, y_train, 'ro', label='Original data')
plt.legend()



import torch
from torch import nn

# 线性模型
class LinearRegression(nn.Module):
    def __init__(self):
        super(LinearRegression, self).__init__()
        self.linear = nn.Linear(1, 1)  # input and output is 1 dimension

    def forward(self, x):
        #print(type(x))
        out = self.linear(x)
        return out

from torch import optim
model = LinearRegression()
# 定义损失函数和优化函数
loss_fn = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=1e-4)

# 开始训练
num_epochs = 1000
for epoch in range(num_epochs):
    inputs = torch.Tensor(x_train)
    target = torch.Tensor(y_train)

    # forward
    out = model(inputs)
    loss = loss_fn(out, target)
    # backward
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch+1) % 20 == 0:
        print('Epoch[{}/{}], loss: {:.6f}'
              .format(epoch+1, num_epochs, loss.data[0]))





model.eval()
predict = model(torch.Tensor(x_train))
predict = predict.data
plt.plot(x_train, predict.numpy(), label='Fitting Line')
plt.show()
# 保存模型
torch.save(model.state_dict(), './linear.pth')

