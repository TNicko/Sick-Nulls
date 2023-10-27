import matplotlib.pyplot as plt
import numpy as np


def plot_transform_overlay(coords1: np.ndarray, coords2: np.ndarray) -> None:
    """
    Plot an overlay of two sets of coordinates.

    Args:
        coords1 (np.ndarray): First set of coordinates (e.g., actual path).
        coords2 (np.ndarray): Second set of coordinates (e.g., transformed path).
    """

    if coords1.ndim != 2 or coords2.ndim != 2:
        raise ValueError("Input coordinates must be 2-dimensional arrays.")

    # Create a plot to visualize the points and transformation.
    plt.figure(figsize=(10, 8))

    # Plotting the path of the AGV
    plt.plot(
        coords1[:, 0],
        coords1[:, 1],
        marker="x",
        linestyle="-",
        color="red",
        label="Path of AGV",
    )

    # Plotting the transformed path of the beacon based on the AGV's coordinate system
    plt.plot(
        coords2[:, 0],
        coords2[:, 1],
        marker="*",
        linestyle="-",
        color="green",
        label="Transformed Path of Beacon",
        alpha=0.6,
    )

    # Enhance the plot with appropriate titles, labels, and legend.
    plt.title("Transformation of Coordinates")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend(loc="upper right")

    # Display the plot.
    plt.show()


# The following is just an example of how to use this function with dummy data
if __name__ == "__main__":
    # Example data
    coords1 = np.array([[1, 2], [3, 4], [5, 6]])
    coords2 = np.array([[2, 3], [4, 5], [6, 7]])

    # Calling the function with example data
    plot_transform_overlay(coords1, coords2)
