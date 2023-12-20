# Tic-Tac-Toe Q-Learning

This project implements a Q-learning algorithm to train an agent to play Tic-Tac-Toe. The game is played on a 3x3 board, and the agent learns to make optimal moves through reinforcement learning.

## Usage

This will simulate a specified number of games, where the Q-learning agent faces a random opponent. After the simulation, it will display the percentage of victories for the Q-learning agent, the random opponent, and draws.

Q-Learning Algorithm
The Q-learning algorithm is used to iteratively update a Q-table, which stores the expected future rewards for each state-action pair. The agent makes decisions based on the Q-values, gradually improving its strategy through learning.

Important Note
While training against a random opponent is a good start, achieving optimal results may require training against more sophisticated opponents. The current implementation uses a random opponent, and therefore, the agent's performance may not be optimal in all scenarios.

To further enhance the agent's capabilities, i trainined it against mimmax.