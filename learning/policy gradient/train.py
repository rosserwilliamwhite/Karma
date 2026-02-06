import torch
import torch.nn as nn
import numpy as np
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions.categorical import Categorical

data = np.zeros((105,int(1e6)))

# architecture
class Policy(nn.Module):
    def __init__(self):
        super(Policy, self).__init__()
        self.optimiser = optim.Adam()

        self.linear1 = nn.Linear(105,256)
        self.linear2 = nn.Linear(256,256)
        self.linear3 = nn.Linear(256,104)
        

    def forward(self,x: torch.Tensor):
        x = self.linear1(x)
        x = F.relu(x)
        x = self.linear2(x)
        x = F.relu(x)
        x = self.linear3(x)
        return x
    
    def get_dists(self, x): 
        x = self.forward(x)
        m1 = Categorical(logits=x[:52])
        m2 = Categorical(logits=x[52:])
        return m1, m2
    
    def learn(self, logprobs: np.ndarray, rewards: np.ndarray):
        # find avg of: - log probs * R  = loss  

        # TODO ALL ACTIONS CARRY FUTURE REWARDS
        discounted_rewards: np.ndarray

        losses = - logprobs * discounted_rewards
        loss = torch.cat(losses).sum()
        self.optimiser.zero_grad()
        loss.backward()
        self.optimiser.step()



    