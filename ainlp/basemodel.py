import torch
from torch import nn
from torch import optim

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
        for data in loader:
            img, y_train = data
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

    def fit_dataloader(self,loader,num_epochs=10,step=20,batch_size=32):
        for epoch in range(num_epochs):

            batch_loss = 0.0
            batch_acc = 0.0
            for i,data in enumerate(loader):
                img,y_train = data
                y_pred = self(img)

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
                          .format(epoch + 1, num_epochs,i+1, batch_loss/step,batch_acc/(step*batch_size)))
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
