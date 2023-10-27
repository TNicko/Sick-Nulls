import numpy as np
from sklearn.linear_model import LinearRegression
import pickle
import plots
from typing import List, Tuple, Any

# Type aliases
Coordinate = Tuple[float, float]
Coordinates = List[Coordinate]

BEACON_COORDS = np.array(
    [[52.47, -6.98], [52.68, -3.53], [48.67, -6.98], [52.68, -7.97]]
)
AGV_COORDS = np.array(
    [[5.94, 3.67], [9.31, 3.41], [5.02, 7.00], [5.008, 2.998]]
)
MODEL_PATH = "model/model.sav"


def build_model(
    beacon_coords: Coordinates, agv_coords: Coordinates, model_path: str
) -> None:
    """Train and save the linear regression model."""
    model = LinearRegression().fit(
        np.array(beacon_coords), np.array(agv_coords)
    )
    with open(model_path, "wb") as file:
        pickle.dump(model, file)


def load_model(model_path: str) -> Any:
    """Load the trained model from the file."""
    with open(model_path, "rb") as file:
        return pickle.load(file)


def predict_coordinates(model: Any, beacon_coords: Coordinates) -> np.ndarray:
    """Predict AGV coordinates based on beacon coordinates."""
    return model.predict(np.array(beacon_coords))


if __name__ == "__main__":
    model = load_model(MODEL_PATH)
    predictions = predict_coordinates(model, BEACON_COORDS)

    # Plotting the predictions against actual data
    plots.plot_transform_overlay(AGV_COORDS, predictions)
