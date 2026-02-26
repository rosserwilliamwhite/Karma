import torch
import torch.nn as nn
import numpy as np
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions.categorical import Categorical

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from game.KarmaV2 import Karma

# architecture
class Policy(nn.Module):
    def __init__(self):
        super(Policy, self).__init__()
    
        self.linear1 = nn.Linear(105,256)
        self.linear2 = nn.Linear(256,256)
        self.linear3 = nn.Linear(256,104)

        self.optimiser = optim.Adam(self.parameters())
        self.to('cuda')

    def forward(self, x: torch.Tensor):
        x = self.linear1(x)
        x = F.relu(x)
        x = self.linear2(x)
        x = F.relu(x)
        x = self.linear3(x)
        return x
    
    def get_bi(self, x): 
        self.eval()
        x = self.forward(x)
        m1, m2 = Categorical(logits=x[:52]), Categorical(logits=x[52:])
        b1, b2 = m1.sample(), m2.sample()
        p1, p2 = m1.log_prob(b1), m2.log_prob(b2)
        bi = torch.stack((b1,b2))
        probs = torch.stack((p1,p2))
        return bi, probs
    
    def learn(self, logprobs: torch.Tensor, rewards: torch.Tensor): 
        self.train()
        GAMMA = 0.9 

        R = 0
        discounted_rewards = torch.zeros_like(rewards)
        for i in range(len(rewards)):
            R = rewards[-(i+1)] + GAMMA * R
            discounted_rewards[-(i+1)] = R

        losses = logprobs.T * discounted_rewards
        loss = losses.sum()
        self.optimiser.zero_grad()
        loss.backward()
        self.optimiser.step()

if __name__ == "__main__":
    import logging
    logging.basicConfig(filename='learning/vpg/run.log', level=logging.INFO, filemode='w')
    policy = Policy()
    info = {'bot':None, 'vpg': policy}

    for i in range(100000):
        game = Karma(info)
        game.run()
        rewards = torch.Tensor(game.players[1].rewards).to('cuda') # (N,1)
        logprobs = torch.stack(game.players[1].logprobs) # (N,2)
        print((torch.numel(rewards) - torch.count_nonzero(rewards)).item())
        policy.learn(logprobs, rewards)
        
