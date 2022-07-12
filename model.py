import os

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class LinearQNetwork(nn.Module):

    def __init__(self, input_size, hidden_size, output_size):
        super(LinearQNetwork, self).__init__()

        self.linear_1 = nn.Linear(input_size, hidden_size)
        self.linear_2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear_1(x))
        x = self.linear_2(x)

        return x

    def save_model(self, path=None, file_name='model.pth'):
        folder_path = path if path else os.path.join(os.getcwd(), 'model')

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_name_path = os.path.join(folder_path, file_name)
        torch.save(self.state_dict(), file_name_path)


class QTrainer:

    def __init__(self, model, learning_rate=0.001, gamma=.999):
        self.model = model
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.criterion = nn.MSELoss()  # Mean Squared Error Loss

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(np.array(state), dtype=torch.float)
        next_state = torch.tensor(np.array(next_state), dtype=torch.float)
        action = torch.tensor(np.array(action), dtype=torch.long)
        reward = torch.tensor(np.array(reward), dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

        # Get the Q values for the current state.
        prediction = self.model(state)

        # Get the Q values for the next state.
        target_prediction = prediction.clone()
        for index in range(len(done)):
            new_Q_value = reward[index]

            if not done[index]:
                new_Q_value = reward[index] + self.gamma * torch.max(
                    self.model(next_state[index]))

            target_prediction[index][torch.argmax(
                action[index]).item()] = new_Q_value

        self.optimizer.zero_grad()
        loss = self.criterion(target_prediction, prediction)
        loss.backward()

        self.optimizer.step()
