# GEDTM30

## Overview

GEDTM30 is a **global 1-arc-second (~30m) Digital Terrain Model (DTM)** built using a machine-learning-based data fusion approach. This dataset was generated using a global-to-local random forest model trained on ICEsat-2 and GEDI data, leveraging almost 30 billion of the highest-quality elevation points. 

GEDTM30 is also used to generate 15 land surface parameters at six scales (30, 60, 120, 240, 480 and 960m), covering aspects of topographic position, light and shadow, landform characteristics, and hydrology. A publication describing methods used has been submitted to PeerJ and is in review. The repository demonstrates the modeling and parametrization. 

## Data Components

1. **GEDTM30: Terrain Height Prediction**

Represents terrain height values, scaled by a factor of 10x.

2. **Uncertainty Map of Terrain Prediction**

Represents the uncertainty in the terrain height prediction, derived from the standard deviation of individual trees' predictions., scaled by a factor of 100x.

3. **15 land surface parameters**

Produced by DTM parametrization, representing different terrain features. Metadata of each parameter is currently stored at [scale.csv](parametrization/scaling.csv). The optimized [Equi7](https://github.com/TUW-GEO/Equi7Grid) tiling system for parameterization is currently stored at [equi7_tiles](parametrization/equi7_tiles)

![Alt text](img/landing.jpg)

## Usage

This dataset is designed for researchers, developers, and professionals working in earth sciences, GIS, and remote sensing. It can be integrated into various geospatial analysis workflows to enhance terrain representation and modeling accuracy. This dataset covers the entire world and is well-suited for applications in:

- Topography

- Hydrology

- Geomorphometry

- Others

## Getting Started

- Access and test the model and parametrization, please clone this repository:

```
git clone https://github.com/openlandmap/GEDTM30.git
```

- Download the data set from Zenodo (10.5281/zenodo.14900180)


## Citation

If you use this dataset in your research or application, please cite:
```
@dataset{GEDTM30,
  author = {update required},
  title = {update required},
  year = {update required},
  url = {update required}
}
```
## License

This dataset is released under fully open license [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.en). 

## Contact

For any questions or contributions, feel free to open an issue or reach out via [yu-feng.ho@opengeohub.org].

