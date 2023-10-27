# AGV Localization - SICK Hackathon Project

This repository hosts the code for our AGV (Automated Guided Vehicles) Localization solution, developed during the [SICK Hackathon](https://www.sick.com/) on October 24-26. Our approach enhances AGV navigation by ensuring precise location tracking and orientation awareness.

## Overview

Our strategy improves AGV localization through:

1. **Location Identification:** We triangulate the AGV's position using SICK beacons, akin to GPS technology.
2. **Orientation Awareness:** AGVs undertake a 'spin test,' employing LiDAR to match real-time environmental scans with internal maps, verifying their directional stance.

## Implementation

The codebase encompasses:

- UWB beacon interactions for precise localization.
- Control algorithms directing AGVs' orientation maneuvers.
- LiDAR data integration and MQTT communications handling.

## Contributions

Initiated as a collaborative venture at the SICK Hackathon.

Contributors:

- [Nickolai Tchesnokov](https://github.com/TNicko)
- [Arkadiusz Podkowa](https://github.com/czuhajster)
- [André Pinho](https://github.com/p1nho)
- [Walter Niinimäki](https://github.com/WalterNi)
- [Ayman Ali](https://github.com/aym183)

## Acknowledgments

Special thanks to [SICK](https://www.sick.com/) for fostering innovation at their hackathon event and [Safelog](https://www.safelog.de/en/) for providing their AGV.
