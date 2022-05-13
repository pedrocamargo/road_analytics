# Geospatial Planning & Budgeting Platform Transport: Road Network Analytics

A set of Jupyter notebooks to support Road network analytics based on Open-Source and Open-Data
[Geospatial Planning & Budgeting Platform (GPBP) Transport sector use cases](https://docs.google.com/document/d/1AugI7_AiD2v-ES_actmseHsFMmi-oMdLxGF2YAcv5XY)

[FULL DOCUMENTATION IS AVAILABLE](https://pedrocamargo.github.io/road_analytics/), but a
quick preview of the facilities are provided below:

# Notebooks

The notebooks are divided in three separate groups, from building the analytics 
models from a variety of data sources to computing estimates of the impact of 
changes to the transportation network. 

## 1 Building the analytics model

Performs all the data import

### 1.1 Importing the OSM network

**In a nutshell**: Imports the OSM network into a computationally-efficient 
format

We can see the imported result on a browser 
[VISUALIZE IT! (it may take time to open)](https://nbviewer.org/github/pedrocamargo/road_analytics/blob/main/notebooks/1.Build_model_from_OSM.ipynb)

We can quickly compute network statistics at this point
[VISUALIZE IT!](https://nbviewer.org/github/pedrocamargo/road_analytics/blob/main/notebooks/use_cases/1.Descriptive_analytics.ipynb)

### 1.2 Importing Population data

**In a nutshell**: Imports population data from Raster format into a 
computationally-efficient and aggregated into customizable polygons

#### 1.2.1 Importing raw population data

**In a nutshell**: Imports population data from Raster format into 
a vector format

A heatmap shows the distribution of the population [VISUALIZE IT!](https://nbviewer.org/github/pedrocamargo/road_analytics/blob/main/notebooks/2.Vectorizing_population.ipynb)