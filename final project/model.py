import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from data_loader import train_data
import torch.nn as nn
import matplotlib.pyplot as plt

# data = np.load('train_data_6.npz')  # 6x6
# data = np.load('train_data_7.npz')  # 7x7
# data = np.load('train_data.npz')  # 8x8
# data = np.load('train_data_9.npz') # 9x9
data = np.load('train_data_10.npz')  # 10x10


boader_state = data['state']
action = data['action']

dataset = train_data(boader_state, action)
train_loader = DataLoader(dataset=dataset, batch_size=3, shuffle=2)


class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Sequential(nn.Conv2d(2, 3, 3, 1, 1),
                                   nn.ReLU())

        self.conv2 = nn.Sequential(nn.Conv2d(3, 64, 3, 1, 1),
                                   nn.ReLU())

        self.conv3 = nn.Sequential(nn.Conv2d(64, 64, 3, 1, 1),
                                   nn.ReLU())

        self.conv4 = nn.Sequential(nn.Conv2d(64, 128, 3, 1, 1),
                                   nn.ReLU())

        self.conv5 = nn.Sequential(nn.Conv2d(128, 128, 3, 1, 1),
                                   nn.ReLU())

        self.conv6 = nn.Sequential(nn.Conv2d(128, 128, 3, 1, 1),
                                   nn.ReLU())

        # self.fc1 = nn.Linear(128 * 6 * 6, 128)  # 6X6
        # self.fc2 = nn.Linear(128, 36)

        # self.fc1 = nn.Linear(128 * 7 * 7, 128)  # 7x7
        # self.fc2 = nn.Linear(128, 49)

        # self.fc1 = nn.Linear(128 * 8 * 8, 128)  # 8x8
        # self.fc2 = nn.Linear(128, 64)

        # self.fc1 = nn.Linear(128 * 9 * 9, 128)  # 9x9
        # self.fc2 = nn.Linear(128, 81)

        self.fc1 = nn.Linear(128 * 10 * 10, 128)  # 10X10
        self.fc2 = nn.Linear(128, 100)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.conv5(x)

        x = x.view(x.size(0), -1)

        x = self.fc1(x)
        x = self.fc2(x)

        return x


if __name__ == '__main__':
    cnn = CNN()
    # cnn.cuda()
    optimizer = torch.optim.SGD(cnn.parameters(), lr=0.005)
    loss_func = nn.CrossEntropyLoss()
    loss_list = []
    for epoch in range(20):
        for step, (inpt, label) in enumerate(train_loader):
            # inpt=inpt.cuda()
            label = label.squeeze()
            # label=label.cuda()
            out = cnn(inpt)
            loss = loss_func(out, label)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if step % 50 == 0:
                loss_list.append(loss)
                print(loss)

    plt.plot(np.arange(len(loss_list)), loss_list)
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.title("Learning Curve (Loss)")
    plt.show()
    # plt.savefig("learning curve(6*6).png")
    # plt.savefig("learning curve(7*7).png")
    # plt.savefig("learning curve(8*8).png")
    # plt.savefig("learning curve(9*9).png")
    # plt.savefig("learning curve(10*10).png")

    # torch.save(cnn.state_dict(), 'net_params_6.pkl')  # 6X6
    # torch.save(cnn.state_dict(), 'net_params_7.pkl')  # 7X7
    # torch.save(cnn.state_dict(), 'net_params.pkl')   # 8X8
    # torch.save(cnn.state_dict(), 'net_params_9.pkl')   # 9X9
    torch.save(cnn.state_dict(), 'net_params_10.pkl')  # 10X10
