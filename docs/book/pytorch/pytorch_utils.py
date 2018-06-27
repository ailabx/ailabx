import torch
from torch import nn
from torch import optim
from copy import deepcopy

class BaseModel(nn.Module):
    def __init__(self,sequential=None):
        super(BaseModel,self).__init__()
        self.sequential = sequential

    def forward(self, x):
        if self.sequential:
            out = self.sequential(x)
            return out
        return None

    def predict(self,x_test):
        self.eval()
        y_pred = self(x_test)
        return y_pred

    def predict_dataloader(self,loader):
        self.eval()
        total_loss = 0.0
        acc = 0.0
        for data in test_loader:
            img, y_train = data
            #img = img.view(img.size(0), -1)
            y_pred = self(img)

            loss = self.loss_fn(y_pred, y_train)
            total_loss += loss.data.item()

            _, pred = torch.max(y_pred, 1)
            num_correct = (pred == y_train).sum()
            acc += num_correct.data.item()

        print(total_loss/len(loader),acc/32/len(loader))

    def save(self,path):
        torch.save(self.state_dict(), path)

    def compile(self,optimizer,loss,metrics=None):


        self.optimizer = optimizer(self.parameters(), lr=1e-4)
        self.loss_fn = loss()
        if metrics is not None:
            self.metrics = metrics()

    def fit_dataloader(self,loader):
        num_epochs = 100
        for epoch in range(num_epochs):

            batch_loss = 0.0
            batch_acc = 0.0
            step = 300
            for i,data in enumerate(loader):
                img,y_train = data
                #print('input size:',img.size())
                y_pred = self(img)
                #print(y_pred.size())
                #y_pred = self(img.view(img.size()[0],-1))

                #计算当前批次的准确率（max:返回每列最大的，第二个返回值是对应的下标)
                _, pred = torch.max(y_pred, 1)
                num_correct = (pred == y_train).sum()
                batch_acc += num_correct.data.item()

                # 反向传播
                self.optimizer.zero_grad()
                loss = self.loss_fn(y_pred, y_train)

                #计算当前批次的损失
                batch_loss += loss.data.item()

                loss.backward()
                self.optimizer.step()

                if (i+1) % step == 0:
                    print('Epoch[{}/{}],batch:{}, avg loss: {:.6f},train acc:{:.6f}'
                          .format(epoch + 1, num_epochs,i+1, batch_loss/step,batch_acc/(step*32)))
                    batch_loss = 0.0
                    batch_acc = 0.0

    def fit(self, x_train, y_train):
        # 开始训练
        num_epochs = 1000
        for epoch in range(num_epochs):
            y_pred = self(x_train)
            # 这里顺序不能反，前者是预测值out，后者是target

            # backward
            self.optimizer.zero_grad()
            loss = self.loss_fn(y_pred, y_train)
            loss.backward()
            self.optimizer.step()

            if (epoch + 1) % 20 == 0:
                print('Epoch[{}/{}], loss: {:.6f}'
                      .format(epoch + 1, num_epochs, loss.data.item()))


# 线性模型
class LinearRegression(BaseModel):
    def __init__(self):
        super(LinearRegression, self).__init__()
        self.linear = nn.Linear(1, 1)  # input and output is 1 dimension

    def forward(self, x):
        out = self.linear(x)
        return out

# 定义 Logistic Regression 模型
class Logstic_Regression(BaseModel):
    def __init__(self, in_dim, n_class):
        super(Logstic_Regression, self).__init__()
        self.logstic = nn.Linear(in_dim, n_class)

    def forward(self, x):
        out = self.logstic(x)
        return out

class MLP(BaseModel):
    def __init__(self,n_input,n_hidden_1,n_hidden_2,n_output):
        super(MLP,self).__init__()
        self.layer1 = nn.Linear(n_input,n_hidden_1)
        self.layer2 = nn.Linear(n_hidden_1,n_hidden_2)
        self.layer3 = nn.Linear(n_hidden_2,n_output)

    def forward(self, x):
        out =  self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        return out

# 定义 Convolution Network 模型
class Cnn(BaseModel):
    def __init__(self, in_dim, n_class):
        super(Cnn, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_dim, 6, 3, stride=1, padding=1),
            nn.ReLU(True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(6, 16, 5, stride=1, padding=0),
            nn.ReLU(True), nn.MaxPool2d(2, 2))

        self.fc = nn.Sequential(
            nn.Linear(400, 120), nn.Linear(120, 84), nn.Linear(84, n_class))

    def forward(self, x):
        out = self.conv(x)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out

# 定义 Recurrent Network - LSTM模型
class Lstm(BaseModel):
    def __init__(self, in_dim, hidden_dim, n_layer, n_class):
        super(Lstm, self).__init__()
        self.n_layer = n_layer
        self.hidden_dim = hidden_dim
        self.lstm = nn.LSTM(in_dim, hidden_dim, n_layer, batch_first=True)
        self.classifier = nn.Linear(28*hidden_dim, n_class)

    def forward(self, x):
        out, _ = self.lstm(x)
        #print(type(out),out.size())
        out = out[:, -1, :] #这里直接把（32，28，128） => (32,128)，直接扔掉？
        #out = out.view(32,-1) view操作竟然不行
        #print(out.size())
        out = self.classifier(out)
        return out


import numpy as np
def test_linear2():
    seq = nn.Sequential(
        nn.Linear(1,1)
    )
    model = BaseModel(seq)
    model.compile(optimizer=optim.SGD, loss=nn.MSELoss)
    x_train = np.array([[3.3], [4.4], [5.5], [6.71], [6.93], [4.168],
                        [9.779], [6.182], [7.59], [2.167], [7.042],
                        [10.791], [5.313], [7.997], [3.1]])

    y_train = np.array([[1.7], [2.76], [2.09], [3.19], [1.694], [1.573],
                        [3.366], [2.596], [2.53], [1.221], [2.827],
                        [3.465], [1.65], [2.904], [1.3]])

    model.fit(torch.Tensor(x_train), torch.Tensor(y_train))
    y_pred = model.predict(torch.Tensor(x_train))

    data = y_pred.data

    import matplotlib.pyplot as plt
    plt.plot(x_train, y_pred.data.numpy(), label='Fitting Line')
    plt.show()


def test_linear():
    model = LinearRegression()
    model.compile(optimizer=optim.SGD,loss=nn.MSELoss)



    x_train = np.array([[3.3], [4.4], [5.5], [6.71], [6.93], [4.168],
                        [9.779], [6.182], [7.59], [2.167], [7.042],
                        [10.791], [5.313], [7.997], [3.1]])

    y_train = np.array([[1.7], [2.76], [2.09], [3.19], [1.694], [1.573],
                        [3.366], [2.596], [2.53], [1.221], [2.827],
                        [3.465], [1.65], [2.904], [1.3]])

    model.fit(torch.Tensor(x_train),torch.Tensor(y_train))
    y_pred = model.predict(torch.Tensor(x_train))

    data = y_pred.data

    import matplotlib.pyplot as plt
    plt.plot(x_train, y_pred.data.numpy(), label='Fitting Line')
    plt.show()

    model.save('./mymodel.pth')

def test_logistic(loader):
    model = Logstic_Regression(28 * 28, 10)  # 图片大小是28x28
    model.compile(optimizer=optim.SGD,loss=nn.CrossEntropyLoss)
    model.fit_dataloader(loader)

def test_MLP(loader,test_loader):
    model = MLP(28*28,300,100,10)
    model.compile(optimizer=optim.SGD,loss=nn.CrossEntropyLoss)
    model.fit_dataloader(loader)
    model.predict_dataloader(test_loader)

def test_cnn(loader,test_loader):
    model = Cnn(1,10)
    model.compile(optimizer=optim.SGD, loss=nn.CrossEntropyLoss)
    model.fit_dataloader(loader)
    model.predict_dataloader(test_loader)

def test_lstm(loader,test_loader):
    model = Lstm(28, 128, 2, 10)  # 图片大小是28x28
    model.compile(optimizer=optim.Adam, loss=nn.CrossEntropyLoss)
    model.fit_dataloader(loader)
    model.predict_dataloader(test_loader)

class LstmTrans(object):
    def __call__(self, pic):
        out = pic.squeeze(0)# 1x28x28 =>28x28,把channel压缩掉
        return out

    def __repr__(self):
        return self.__class__.__name__ + '()'

class Trans(object):
    def __call__(self, pic):
        #print('pic:',pic.size())
        out = pic.view(-1)
        #print('out',out.size())
        return out

    def __repr__(self):
        return self.__class__.__name__ + '()'

if __name__ == '__main__':
    from torchvision import datasets,transforms
    from torch.utils.data import DataLoader

    composed = transforms.Compose([transforms.ToTensor(),
                                  LstmTrans()])

    train_dataset = datasets.MNIST(
        root='./data', train=True, transform=composed, download=True)

    test_dataset = datasets.MNIST(
        root='./data', train=False, transform=composed)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)


    #test_linear()
    #test_MLP(train_loader,test_loader)
    #test_cnn(train_loader,test_loader)
    test_lstm(train_loader,test_loader)
