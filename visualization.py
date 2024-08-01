import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Sample data
np.random.seed(42)
x = np.random.rand(100)
y = np.random.rand(100)
colors = np.random.rand(100)
sizes = 1000 * np.random.rand(100)

# Setting the theme
sns.set(style="whitegrid")

# Create the scatter plot
plt.figure(figsize=(10, 6))
scatter = plt.scatter(x, y, c=colors, s=sizes, alpha=0.6, edgecolors="w", cmap='viridis')

# Adding a color bar
plt.colorbar(scatter)

# Adding titles and labels
plt.title('Beautiful Scatter Plot', fontsize=18)
plt.xlabel('HLTV Rating', fontsize=14)
plt.ylabel('WAR', fontsize=14)

# Customizing ticks and spines
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Show the plot
plt.show()
