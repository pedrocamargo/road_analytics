.. _build_travel_model:

Travel model
============

* Congestion / interaction between demand and supply


Augmenting the road network model
_________________________________

Despite all the information contained in Open-Street maps, there are some pieces
of information that are incomplete and others that are simply missing and need
to augmented.

The often incomplete information regards the number of lanes and speed limits for
each one of the streets, while the information on actual link capacity is missing
from OSM, as it is an abstraction particular to the transport modelling world.

For this purpose, we augment the network with asserted values, which we list in
the :ref:`road_capacities` table


Customizing network assumptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
XXXXXXXXXXXXXXXXXX


Use Cases enabled:
~~~~~~~~~~~~~~~~~~

* Displaying general stats regarding link types and pavement surfaces

* Displaying specific stats for bridges, tolls, and tunnels and their link types
  and pavement surfaces

These use cases can be `visualized as well!
<https://nbviewer.org/github/pedrocamargo/road_analytics/blob/main/notebooks/use_cases/1.Descriptive_analytics.ipynb>`_

Building the travel demand model
--------------------------------

* personal auto-travel only

Trip generation
~~~~~~~~~~~~~~~

Trip distribution
~~~~~~~~~~~~~~~~~

Customizing model parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~