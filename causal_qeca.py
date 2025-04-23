import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.cm as cm

# Parameters
num_points = 100
width = 10
height = 10
alpha = 1.0
omega = 1.0
k = 0.5

# 1. Sprinkle points uniformly in 1+1D Minkowski space
# Modify sprinkle_points to use a Poisson process for sprinkling points
def sprinkle_points(num_points, width, height):
    density = num_points / (width * height)  # Points per unit area
    num_poisson_points = np.random.poisson(density * width * height)
    t = np.random.uniform(0, height, num_poisson_points)
    x = np.random.uniform(0, width, num_poisson_points)
    return np.column_stack((x, t))

# 2. Build causal set (transitive reduction)
def build_causal_links(points):
    n = len(points)
    links = [[] for _ in range(n)]
    for i in range(n):
        xi, ti = points[i]
        for j in range(n):
            if i == j:
                continue
            xj, tj = points[j]
            if tj < ti and (ti - tj)**2 >= (xi - xj)**2:
                links[i].append(j)
    return links

# 3. Kernel function

def kernel(p_i, p_j):
    dt = p_i[1] - p_j[1]
    dx = p_i[0] - p_j[0]
    tau2 = dt**2 - dx**2
    if tau2 <= 0:
        return 0.0 + 0.0j
    tau = np.sqrt(tau2)
    amp = 1 / (tau ** alpha)
    phase = omega * dt - k * dx
    return amp * np.exp(1j * phase)

# 4. Evolve state of each point

def evolve_state(i, states, links, points):
    psi = 0.0 + 0.0j
    for j in links[i]:
        kij = kernel(points[i], points[j])
        psi += kij * states[j]
    return psi

# Initialize
points = sprinkle_points(num_points, width, height)
num_points = len(points)
order = np.argsort(points[:, 1])
points = points[order]  # sort by time
links = build_causal_links(points)
states = [0.0 + 0.0j for _ in range(num_points)]

# Assign initial states to minimal elements
for i in range(num_points):
    if not links[i]:
        angle = np.random.uniform(0, 2 * np.pi)
        states[i] = np.exp(1j * angle)

# Track progress
computed = set(i for i in range(num_points) if states[i] != 0.0 + 0.0j)

def next_step(event):
    global states, computed
    updated = False
    for i in range(num_points):
        if i in computed:
            continue
        if all(j in computed for j in links[i]):
            states[i] = evolve_state(i, states, links, points)
            computed.add(i)
            updated = True
            break
    if updated:
        update_plot()

# Update the plot to use the first subfigure
fig, ax = plt.subplots(1, 1)
plt.subplots_adjust(bottom=0.2)
ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])
button = Button(ax_button, 'Next Step')
button.on_clicked(next_step)

# Modify update_plot to use the first subfigure
def update_plot():
    ax.cla()  # Clear the first subfigure
    colors = [np.angle(s) if abs(s) > 0 else -10 for s in states]
    ax.scatter(points[:, 0], points[:, 1], c=colors, cmap=cm.hsv, s=30)
    ax.set_title("Causal Set Evolution (color = phase)")
    ax.set_xlabel("x")
    ax.set_ylabel("t")
    # fig.colorbar(cm.ScalarMappable(cmap=cm.hsv), ax=ax, label="Phase (radians)")
    plt.draw()

update_plot()
plt.show()
