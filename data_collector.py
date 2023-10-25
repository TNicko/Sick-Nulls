import os
import csv
from typing import Callable


def initialize_coordinates_file() -> Callable:
    folder_name = 'collected_data'
    csv_file = 'coordinates.csv'
    header = ['x1', 'y1', 'x2', 'y2']

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_path = os.path.join(folder_name, csv_file)

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

    def append_coordinates(x1, y1, x2, y2):
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([x1, y1, x2, y2])

    return append_coordinates

# Example usage within this module:
if __name__ == "__main__":
    append_coordinates = initialize_coordinates_file()
    append_coordinates(1.0, 2.0, 3.0, 4.0)
    append_coordinates(5.0, 6.0, 7.0, 8.0)