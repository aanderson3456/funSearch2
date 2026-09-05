import torch
import torch.nn as nn
import torch.nn.functional as F

class ResBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(channels)
        
    def forward(self, x):
        residual = x
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.bn2(self.conv2(x))
        x += residual
        x = F.relu(x)
        return x

class SnakyNet(nn.Module):
    def __init__(self, num_resBlocks=16, num_channels=256, board_size=13):
        super().__init__()
        self.board_size = board_size
        self.startBlock = nn.Sequential(
            nn.Conv2d(5, num_channels, 3, padding=1),
            nn.BatchNorm2d(num_channels),
            nn.ReLU()
        )
        
        self.resBlocks = nn.ModuleList(
            [ResBlock(num_channels) for _ in range(num_resBlocks)]
        )
        
        self.policyHead = nn.Sequential(
            nn.Conv2d(num_channels, 2, 1),
            nn.BatchNorm2d(2),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(2 * board_size * board_size, board_size * board_size)
        )
        
        self.valueHead = nn.Sequential(
            nn.Conv2d(num_channels, 1, 1),
            nn.BatchNorm2d(1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(1 * board_size * board_size, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Tanh()
        )
        
    def forward(self, x):
        # x is (batch_size, 2, board_size, board_size)
        x = self.startBlock(x)
        for resBlock in self.resBlocks:
            x = resBlock(x)
            
        policy = self.policyHead(x)
        value = self.valueHead(x)
        return policy, value
