import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm

# hyperparameters
LR = 1e-3
L2_REG = 1e-4

# load data
data = np.load('learning/imitation/imitation_demo.npz')
state = torch.tensor(data['state'],  dtype=torch.float)
action = torch.tensor(data['action'],  dtype=torch.float)

# choose device 
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

class Lambda(nn.Module):
    def __init__(self, func):
        super().__init__()
        self.func = func

    def forward(self, x):
        return self.func(x)

net = nn.Sequential(
    nn.Linear(105,256),
    nn.ReLU(),
    nn.Linear(256, 256),
    nn.ReLU(),
    nn.Linear(256, 256),
    nn.ReLU(),
    nn.Linear(256, 2),
    nn.ReLU()
)
net = net.to(device)
opt = optim.Adam(net.parameters(), lr=LR, weight_decay=L2_REG)

loss_fn = nn.MSELoss()

N = int(state.shape[0]/2)
for n in tqdm(range(N)):
    x = state[n].to(device)
    y = action[n].to(device)

    opt.zero_grad()
    yhat = net(x)

    loss: nn.MSELoss = loss_fn(yhat, y)
    loss.backward()

    opt.step()
torch.save(net,'learning/imitation/imitation.pt')
