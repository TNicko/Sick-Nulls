import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pickle

# Historical data points
beacon_coords = np.array(
    [[52.47, -6.98], [52.68, -3.53], [48.67, -6.98], [52.68, -7.97]]
)
agv_coords = np.array(
    [[5.94, 3.67], [9.31, 3.41], [5.02, 7.00], [5.008, 2.998]]
)

# Test points
beacon_test_coord = np.array([[52.68, -7.97], [48.66, -7.03], [52.64, -8.1]])
agv_test_coord = np.array([[5.008, 2.998], [5.034, 6.991], [5.008, 3.002]])

# Fit the model with the historical data
model = LinearRegression().fit(beacon_coords, agv_coords)


def save_model(model):
    filename = "model/linear_regression_model.sav"
    pickle.dump(model, open(filename, "wb"))


save_model(model)
# Coefficients and intercept from the model
coef = model.coef_
intercept = model.intercept_

# print("Transformation components:")
# print("Coefficients:", coef)
# print("Intercept:", intercept)

# Calculate the transformed coordinates of the beacons based on the model
transformed_beacon_coords = model.predict(beacon_coords)

# PREDICTION
predicted_coord = model.predict(beacon_test_coord)
print(predicted_coord)

# Create a plot to visualize the points and transformation.
plt.figure(figsize=(10, 8))

# Plotting the original paths of the beacon and the AGV
# plt.plot(
# beacon_coords[:, 0],
# beacon_coords[:, 1],
# marker="o",
# linestyle="-",
# color="blue",
# label="Path of Beacon",
# )
plt.plot(
    agv_coords[:, 0],
    agv_coords[:, 1],
    marker="x",
    linestyle="-",
    color="red",
    label="Path of AGV",
)

# Plotting the transformed path of the beacon based on the AGV's coordinate system
plt.plot(
    transformed_beacon_coords[:, 0],
    transformed_beacon_coords[:, 1],
    marker="*",
    linestyle="-",
    color="green",
    label="Transformed Path of Beacon",
    alpha=0.6,
)
plt.scatter(
    predicted_coord[:, 0],
    predicted_coord[:, 1],
    c="purple",
    marker="o",
    s=100,
    label="Predicted point",
)
plt.scatter(
    agv_test_coord[:, 0],
    agv_test_coord[:, 1],
    c="pink",
    marker="o",
    s=100,
    label="Actual point",
)


# Enhance the plot with appropriate titles, labels, and legend.
plt.title("Transformation of Coordinates")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.legend(loc="upper right")

# Display the plot.
plt.show()
