from simulator import Simulator, BracketSimulator
import pandas as pd
from collections import Counter
import csv
import matplotlib.pyplot as plt

DATA_FILEPATH = 'data/March_Madness_2024_Silver_Bulletin_03_18_2024.csv'
PICK_DATA_FILEPATH = 'data/yahoo_pick_distributions.csv'


data = pd.read_csv(DATA_FILEPATH).drop(['Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17', 'Unnamed: 18'], axis='columns')
data.team_seed = data.team_seed.str[0:2].astype(int)

tournament_sim = Simulator(data)

pick_data = pd.read_csv(PICK_DATA_FILEPATH)

bracket_sim = BracketSimulator(pick_data)

# winning_champions = []
# for i in range(0,10000):
#     result_sim = tournament_sim.simulate_tournament()

#     champions = []
#     scores = []
#     # for j in range(0,100):
#     #     sim = bracket_sim.simulate_tournament()
#     #     score = sim.score_bracket(result_sim)
#     #     champions.append(sim.data[1].iloc[0]['team_name'])
#     #     scores.append(score)

#     # winning_champions.append(champions[scores.index(max(scores))])
#     # print(f'Champion: {result_sim.data[1].iloc[0]['team_name']}')
#     winning_champions.append(result_sim.data[1].iloc[0]['team_name'])
#     if (i+1)%100 == 0:
#         print(f'{(i+1)//100}% finished')
#     # print(f'Winning score: {max(scores)}\nWinning bracket champion: {champions[scores.index(max(scores))]}\nActual champion: {result_sim.data[1].iloc[0]['team_name']}')


# counter_dict = dict(Counter(winning_champions))

# # Specify the filename
filename = 'data/counter_results.csv'

# # Write the dictionary to a CSV file
# with open(filename, 'w', newline='') as csvfile:
#     csv_writer = csv.writer(csvfile)
#     csv_writer.writerow(['Key', 'Value'])  # Write header

#     team_name = []
#     freq = []
#     for key, value in counter_dict.items():
#         team_name.append(key)
#         freq.append(value/100)
#         csv_writer.writerow([key, value/100])
# print(counter_dict)



# plot_df = pd.DataFrame({'team_name': team_name, 'freq': freq})
plot_df = pd.read_csv(filename).rename(columns={'Key':'team_name', 'Value':'freq'})
plot_df = pd.merge(plot_df, pick_data.loc[:,['team_name', 'rd7_pick']], on='team_name', how='left')
plot_df.freq = plot_df.freq / 100
plot_df.rd7_pick = plot_df.rd7_pick * 100

# Create scatterplot
plt.figure(figsize=(8, 6))
plt.scatter(plot_df.rd7_pick, plot_df.freq)

# Add labels to points
for label, x_point, y_point in zip(plot_df.team_name, plot_df.rd7_pick, plot_df.freq):
    plt.annotate(label, (x_point, y_point), textcoords="offset points", xytext=(0,10), ha='center')

# Add axis labels and title
plt.xlabel('Probability of Being Picked to Win Tournament')
plt.ylabel('Probability of Actually Winning Tournament')
plt.title('Probability of Being Picked to With vs. Actually Winning Tournament')

# Show plot
plt.grid(True)
plt.show()
