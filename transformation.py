import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Historical data points
beacon_coords = np.array([[6, 10], [13, 19], [24, 30]])
agv_coords = np.array([[10, 20], [20, 30], [30, 40]])

# Fit the model with the historical data
model = LinearRegression().fit(beacon_coords, agv_coords)

# Coefficients and intercept from the model
coef = model.coef_
intercept = model.intercept_

print("Transformation components:")
print("Coefficients:", coef)
print("Intercept:", intercept)

# New single coordinate from the beacon system
new_beacon_coord = np.array([15, 23])

transformed_coord = model.predict([new_beacon_coord])[0]


# Create a plot to visualize the points and transformation.
plt.figure(figsize=(10, 8))
plt.plot(
    beacon_coords[:, 0],
    beacon_coords[:, 1],
    marker="o",
    linestyle="-",
    color="blue",
    label="Path of Beacon",
)
plt.plot(
    agv_coords[:, 0],
    agv_coords[:, 1],
    marker="x",
    linestyle="-",
    color="red",
    label="Path of AGV",
)

# Plot the new beacon coordinate and its transformed counterpart as individual points.
plt.scatter(
    new_beacon_coord[0],
    new_beacon_coord[1],
    c="green",
    label="New Beacon Coord",
)
plt.scatter(
    transformed_coord[0],
    transformed_coord[1],
    c="purple",
    label="Transformed Coord in AGV system",
)

# Enhance the plot with appropriate titles and labels.
plt.title("Transformation of Coordinates")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.legend(loc="upper left")

# Display the plot.
plt.show()
