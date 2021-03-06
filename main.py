import argparse
import pandas as pd
from timeit import default_timer as timer
from qlearner import QLearner

from agents import MyAgent
from wrapper import LunarLanderWrapper

# Parse the arguments
parser = argparse.ArgumentParser(description="Experiment parameters")
parser.add_argument('-e', '--episodes', type=int, default=500,
                    help="The maximum number of episodes per run")
parser.add_argument('-r', '--runs', type=int, default=10,
                    help="The number of runs (repeats) of the experiment")
args = parser.parse_args()
num_episodes = args.episodes
num_runs = args.runs

################################################################################
#                                                                              #
#                           ASSIGNMENT: LUNAR LANDER                           #
#                                                                              #
################################################################################

# Initialise result data structures
rewards_per_run = dict()
runtime_per_run = []

# For each run, train agent until environment is solved, or episode budget 
# runs out:
for run in range(num_runs):
    # Initialise result helpers
    end_episode = num_episodes  # indicates in which run the environment was solved
    start = timer()
    rewards = [0.0] * num_episodes  # reward per episode

    # Initialise environment and agent
    wrapper = LunarLanderWrapper()              # TODO: you have to implement this environment
    agent = MyAgent(wrapper=wrapper, seed=run)  # TODO: you have to implement this agent

    # For each episode, train the agent on the environment and record the
    # reward of each episode
    for episode in range(num_episodes):
        rewards[episode] = agent.train()
        # Check if environment is solved
        if wrapper.solved(rewards[:episode]):
            end_episode = episode
            break

    # Record and print performance
    runtime_per_run.append(timer() - start)
    rewards_per_run['run' + str(run)] = rewards
    print('end episode # = ', end_episode)

    # Close environment
    wrapper.close()

# Store results
df_rewards = pd.DataFrame(rewards_per_run)
df_rewards.to_csv('lunarlander_rewards.csv')

df_time = pd.DataFrame(runtime_per_run, columns=['time [s]'])
df_time.to_csv('lunarlander_runtimes.csv')




































































################################################################################
#                                                                              #
#                              EXAMPLE: CART POLE                              #
#                                                                              #
################################################################################

# # Initialise result data structures
# rewards_per_run = dict()
# runtime_per_run = []

# # For each run, train agent until environment is solved, or episode budget
# # runs out:
# for run in range(num_runs):
#     # Initialise result helpers
#     end_episode = num_episodes      # indicates in which run the environment was solved
#     start = timer()
#     rewards = [0.0] * num_episodes          # reward per episode

#     # Initialise environment and agent
#     wrapper = CartPoleWrapperDiscrete()
#     agent = QLearner(wrapper=wrapper, seed=run)

#     # For each episode, train the agent on the environment and record the
#     # reward of each episode
#     for episode in range(num_episodes):
#         rewards[episode] = agent.train()
#         # Check if environment is solved
#         if wrapper.solved(rewards[:episode]):
#             end_episode = episode
#             break

#     # Record and print performance
#     runtime_per_run.append(timer() - start)
#     rewards_per_run['run' + str(run)] = rewards
#     if end_episode >= 99:
#         print('average reward of last 100 episodes of run', run,
#               '=', float(sum(rewards[-100:])) / 100)
#     print('end episode # = ', end_episode)

#     # Close environment
#     wrapper.close()

# # Store results
# df_rewards = pd.DataFrame(rewards_per_run)
# df_rewards.to_csv('cartpole_rewards.csv')

# df_time = pd.DataFrame(runtime_per_run, columns=['time [s]'])
# df_time.to_csv('cartpole_runtimes.csv')
