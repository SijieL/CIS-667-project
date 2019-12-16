import numpy as np
from torch.utils.data import Dataset, DataLoader
import torch

# data = np.load('train_data_6.npz')
# data = np.load('train_data_7.npz')
# data = np.load('train_data.npz')
# data = np.load('train_data_9.npz')
data = np.load('train_data_10.npz')

boader_state = data['state']
action = data['action']


class train_data(Dataset):
    def __init__(self, boader_state, action):
        self.boader_state = boader_state
        self.action = action

    def __getitem__(self, i):
        inpt = boader_state[i]
        re_inpt = self.transform_inpt(inpt)

        act = action[i]
        label = self.ac_trans(act)
        # new_inpt,new_ouput=change_coordi(board_size=10,re_inpt,label)
        return re_inpt, label


    def transform_inpt(self, inpt):
        # img = torch.zeros((6, 6))  # 6x6
        # img = torch.zeros((7, 7))    # 7x7
        # img = torch.zeros((8, 8))  # 8x8
        # img = torch.zeros((9, 9))  # 9x9
        img = torch.zeros((10, 10))  # 10x10

        img_op = torch.zeros_like(img)

        cu = np.where(inpt == 1)
        op = np.where(inpt == -1)

        img[cu[0], cu[1]] = 1
        img_op[op[0], op[1]] = 1
        img = img.unsqueeze(0)
        img_op = img_op.unsqueeze(0)

        re_inpt = torch.cat((img, img_op), 0)
        re_inpt = torch.FloatTensor(re_inpt).squeeze()

        return re_inpt

    def ac_trans(self, act):
        row_th, col_th = act[0], act[1]
        # output = row_th * 5 + col_th      # 6x6
        # output = row_th * 6 + col_th    # 7x7
        # output = row_th * 7 + col_th    # 8x8
        # output = row_th * 8 + col_th      # 9x9
        output = row_th * 9 + col_th      # 10x10

        output = torch.LongTensor([output])
        return output

    def __len__(self):
        len = self.action.shape[0]
        return len


if __name__ == '__main__':
    train = train_data(boader_state, action)
    ipt, oupt = train[6]
    print(ipt.shape)
    print(oupt)
