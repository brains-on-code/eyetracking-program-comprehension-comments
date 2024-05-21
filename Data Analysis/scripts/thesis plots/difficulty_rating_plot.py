import matplotlib.pyplot as plt
import pandas as pd
from adjustText import adjust_text

# Create DataFrame from the provided data
data = {
    'Task': range(1, 13),
    'Effect of CP (%)': [-4, 14, -6, 4, 6, -12, 2, 0, -34, -10, 0, -8],
    'Comment Contribution Rating': [2.9, 3.4, 3.4, 3.7, 3.4, 3.5, 2.9, 2.8, 3.9, 3.8, 3.4, 2.8]
}

df = pd.DataFrame(data)

# Plot
plt.figure(figsize=(5, 5), dpi=600)
plt.scatter(df['Effect of CP (%)'], df['Comment Contribution Rating'], color='#5a3495', s=20)
# label each point with its task number
texts = []
for i, txt in enumerate(df['Task']):
    texts.append(plt.annotate(' '+str(txt), (df['Effect of CP (%)'][i], df['Comment Contribution Rating'][i])))

# auto adjust text positions to avoid overlapping with other points
adjust_text(texts, avoid_points=True, avoid_text=True, expand_points=(2, 2), expand_align=(10, 8), autoalign='xy')

# Aesthetics
plt.xlabel('Effect of Comments on Difficulty (%)')
plt.ylabel('Comment Contribution Rating')
# set y axis limits
plt.ylim(0.8, 5)
# set x axis limits
plt.xlim(-38, 38)
# set y axis ticks
plt.yticks(range(1, 6, 1))
# set x axis ticks
plt.xticks(range(-35, 36, 10))
# set spines to invisible
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_position('center')
plt.setp(plt.gca().get_yticklabels(), transform=plt.gca().get_yaxis_transform())
# Save plot
plt.tight_layout()
plt.savefig('/Users/Youssef/Desktop/DifficultyRatingPlot.pdf', dpi=600, bbox_inches='tight')

