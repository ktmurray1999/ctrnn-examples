# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 11:52:03 2021

@author: murra
"""
import torch
import torch.nn as nn

class ctrnnCell(nn.Module):
    def __init__(self, dim, dt):
        super(ctrnnCell, self).__init__()
        self.linear = nn.Linear(dim, dim, bias=True)
        self.tau = nn.Parameter(torch.ones(1, dim))
        self.dt = torch.tensor(dt)
        
        self.sig = nn.Sigmoid()

    def forward(self, state, inputs):
        dt_tau = self.dt/self.tau
        f = self.sig(self.linear(state))
        state_plus_1 = state*(1-dt_tau) + dt_tau*(f + inputs)
        
        return state_plus_1
    
class ctrnn(nn.Module):
    def __init__(self, dim, dt, initial, time):
        super(ctrnn, self).__init__()
        self.ctrnnCell = ctrnnCell(dim, dt)
        self.initial = initial
        self.dim = dim
        self.time = time
        
    def forward(self, inputs):
        states = torch.zeros(self.time, 1, self.dim)
        states[0,:,:] = self.initial
        
        for i in range(self.time-1):
            input_i = inputs[i,:,:]
            states[i+1,:,:] = self.ctrnnCell(states[i,:,:], input_i)
        
        return states

    def assignWeight(self, weight, bias, tau):
        self.ctrnnCell.linear.weight.data = weight
        self.ctrnnCell.linear.bias.data = bias
        self.ctrnnCell.tau.data = tau
        
    