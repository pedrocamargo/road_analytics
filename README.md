# Geospatial Planning & Budgeting Platform Transport: Road Network Analytics

A set of Jupyter notebooks to support Road network analytics based on Open-Source and Open-Data
[Geospatial Planning & Budgeting Platform (GPBP) Transport sector use cases](https://docs.google.com/document/d/1AugI7_AiD2v-ES_actmseHsFMmi-oMdLxGF2YAcv5XY)

# Notebooks

In order to enable non-technical experts to utilize this tool, we have set it as a sequence of Jupyter notebooks that 
implement the analyses and analysis frameworks described in the GPBP documentation.

These Jupyter Notebooks can be run locally or in the Cloud (we recommend using [SaturnCloud](https://saturncloud.io/), 
although Google Colab should be powerful enough for very small countries), and we provide the documentation for running it
in both the SaturnCloud and locally [TODO].

## 1. Building the road network model from Open-Street Maps

The first step in the analytics setup process is the development of the Road Network model from OSM data. 

This step includes the following sub-steps:

* Downloading and interpreting (parsing) the OSM network
* Downloading the country borders from Open-Street Maps
* Making sure that only links from within the country borders are kept in the model
* Veryfing if the network is a routable by computing a path through the network
* Print general stats regarding link types and pavement surfaces
* Print specific stats for bridges, tolls, and tunnels and their link types and pavement surfaces

[Visualize the notebook! (it may take time to open)](https://nbviewer.org/github/pedrocamargo/road_analytics/blob/main/notebooks/1.Build_model_from_OSM.ipynb)


## 2. Population vectorization


## 3. Creating zoning
