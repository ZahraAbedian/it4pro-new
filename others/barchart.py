mport matplotlib.pyplot as plt

fig = plt.figure()
fig.subplots_adjust(bottom=0.3)
ax = fig.add_subplot(111)

categories = ['Availability Management', 'Capacity Management', 'Change Management', 'Configuration Managenment', 'Continuity Management', 'Financial Management', 'Incident Management', 'Problem Management', 'Release Management', 'Service Level Management']
scores = [4, 1, 3, 5, 1, 1, 2, 5, 1, 4]

ax.bar(categories, scores, color="blue")

ax.set_ylabel('Level', fontsize=8)
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.savefig("my_bar_chart.png")