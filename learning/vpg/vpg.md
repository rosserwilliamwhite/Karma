# policy gradient
need state, action, reward
maximise expected reward -> collect batch of data (karma game)
loss = 1/N * sum log(prob) * reward  (for each move), where prob is the probability of the selected action = m.log_prob()

# sampling
need to be able to get bi from categorical distribution
how i want to do this is to output two categorical distributions and use each to get the bi
theoretically id want to have the neural network to somehow output the stack
GAVE UP JUST GOING TO CHOOSE ONE CARD... :( maybe one day the answer will be clear...
SOLUTION IS ACTUALLY JUST TO THINK OF THE LOG PROB IS THE LOG PROB OF THE WHOLE ACTION... so just add the probs

# 

# reference
https://github.com/pytorch/examples/blob/main/reinforcement_learning/reinforce.py