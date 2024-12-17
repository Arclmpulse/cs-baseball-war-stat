import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Sample data
df = pd.read_csv('player_war.csv')
np.random.seed(42)
x = df['Rating']
y = df['RAR']
colors = np.random.rand(len(x))  # Make sure the length matches `x` and `y`

# Setting the theme
sns.set(style="whitegrid")

# Create the scatter plot
plt.figure(figsize=(10, 6))
scatter = plt.scatter(x, y, c=colors, alpha=0.6, edgecolors="w", cmap='viridis')

# Adding a color bar
plt.colorbar(scatter)

# Adding titles and labels
plt.title('Rating vs RAR Visualization', fontsize=18)
plt.xlabel('HLTV Rating', fontsize=14)
plt.ylabel('RAR', fontsize=14)

# Customizing ticks and spines
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Add horizontal and vertical lines to create 4 quadrants
plt.axhline(1, color='black',linewidth=1)  # Horizontal line at y=0
plt.axvline(1, color='black',linewidth=1)  # Vertical line at x=1

# Adjust the limits to make the quadrants more visible (optional)
plt.xlim(min(x)-1, max(x)+1)
plt.ylim(min(y)-1, max(y)+1)

# Show the plot
plt.show()
