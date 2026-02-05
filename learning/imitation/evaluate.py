import torch
import numpy as np

data = np.load('learning/imitation/imitation_demo.npz')
state = torch.tensor(data['state'],  dtype=torch.float).to('cuda')
action = torch.tensor(data['action'],  dtype=torch.float).to('cuda')
net = torch.load('learning/imitation/imitation.pt', weights_only=False)

def neteval(net, state, action, n):
    x = state[n]
    y = action[n]
    yhat = net(x)
    cond: torch.Tensor = yhat.round() == y
    print(cond.all().item())