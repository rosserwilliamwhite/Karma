import torch
import torch.nn as nn
import numpy as np
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions.categorical import Categorical

# architecture
class Policy(nn.Module):
    def __init__(self):
        super(Policy, self).__init__()
        self.optimiser = optim.Adam()

        self.linear1 = nn.Linear(105,256)
        self.linear2 = nn.Linear(256,256)
        self.linear3 = nn.Linear(256,52)

    def forward(self,x: torch.Tensor):
        x = self.linear1(x)
        x = F.relu(x)
        x = self.linear2(x)
        x = F.relu(x)
        x = self.linear3(x)
        return x
    
    def get_dist(self, x): 
        self.eval()
        x = self.forward(x)
        m = Categorical(logits=x[:52])
        return m
    
    def learn(self, logprobs: np.ndarray, rewards: np.ndarray):
        self.train()
        GAMMA = 0.9
        # find avg of: - log probs * R  = loss  

        R = 0
        discounted_rewards = np.zeros_like(rewards)
        for i in range(len(rewards)):
            R = rewards[-(i+1)] + GAMMA * R
            discounted_rewards[-(i+1)] = R

        losses = - logprobs * discounted_rewards
        loss = torch.cat(losses).sum()
        self.optimiser.zero_grad()
        loss.backward()
        self.optimiser.step()



    