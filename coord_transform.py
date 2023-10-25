import numpy as np
import matplotlib.pyplot as plt

# Beacon movement coords
beacon_coords = np.array([[6, 10], [13, 19], [24, 30]])

# AGV movement coords
agv_coords = np.array([[10, 20], [20, 30], [30, 40]])

differences = agv_coords - beacon_coords

translation = np.mean(differences, axis=0)


def transform_beacon_to_agv(beacon_point, translation):
    agv_point = beacon_point + translation
    return agv_point


transformed_coords = transform_beacon_to_agv(beacon_coords, translation)

# Test with new points
test_beacon_point = np.array([8, 15])
known_agv_point = np.array([13, 25])

test_agv_point = transform_beacon_to_agv(test_beacon_point, translation)
error = known_agv_point - test_agv_point

# Create a plot to visualize the points and paths.
plt.figure(figsize=(10, 8))

# Plot the paths as lines instead of scattered points.
plt.plot(
    beacon_coords[:, 0],
    beacon_coords[:, 1],
    c="blue",
    linestyle="-",
    marker="o",
    label="Path of Beacon",
)
plt.plot(
    agv_coords[:, 0],
    agv_coords[:, 1],
    c="red",
    linestyle="-",
    marker="x",
    label="Path of AGV",
)
plt.plot(
    transformed_coords[:, 0],
    transformed_coords[:, 1],
    c="green",
    linestyle="-",
    marker="o",
    label="Transformed Path of Beacon",
    alpha=0.7,
)

# Mark the test and known points on the AGV's path.
plt.scatter(
    test_agv_point[0],
    test_agv_point[1],
    c="black",
    marker="+",
    s=150,
    label="Test AGV Point",
)
plt.scatter(
    known_agv_point[0],
    known_agv_point[1],
    c="purple",
    marker="s",
    s=150,
    label="Known AGV Point",
)

# Draw a line representing the error between the test point and the known point.
plt.plot(
    [known_agv_point[0], test_agv_point[0]],
    [known_agv_point[1], test_agv_point[1]],
    "k--",
)

# Show the error value on the plot.
error_text = f"Error: {np.linalg.norm(error):.2f}"
# mid_point = (known_agv_point + test_agv_point) / 2
# plt.text(mid_point[0], mid_point[1], error_text, ha="center", va="center")

# Enhance the plot with appropriate labels and legends.
plt.title("Comparison of Paths in Different Coordinate Systems")
plt.xlabel("X Coordinates")
plt.ylabel("Y Coordinates")
plt.legend()
plt.grid(True)
plt.show()
