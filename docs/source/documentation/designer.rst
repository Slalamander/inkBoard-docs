.. raw:: html

   <div style="visibility: hidden;">

inkBoard Designer
==================

.. raw:: html

   </div>

.. image:: /_static/images/designer_logo.svg
    :alt: inkBoard designer logo

inkBoard also provides an interface to aid in designing dashboards.
It is mainly there to speed up the process, since it may not always be as easy to iterate over a dashboard configuration on platform.
To aid in accessibility, most widgets have tooltips explaining their use.

The designer is not only meant for designing however.
To keep the size the inkBoard library itself as small as possible, integrations and platforms are distributed with the designer.
inkBoard and the designer integrate quite smoothly, and if you do not want the hassle of packaging, copying and installing to a platform,
inkBoard accesses the designer integrations and platforms when indexing what is available.
Requirements for integrations and platforms are not preinstalled with the designer, however.
The appropriate install command still needs to be called, but again, the modules themselves can be located within the designer.

This documentation is currently very incomplete, but the designer still is as well.
As the designer is improved upon, this documentation will be as well.
For now, the figure and table from the tutorial are repeated below. 

.. figure:: /tutorial/images/light-ui-tutorial.png
   :figclass: light-only
   :align: center
   :alt: annotated designer interface in light mode

.. figure:: /tutorial/images/dark-ui-tutorial.png
   :figclass: dark-only
   :align: center
   :alt: annotated designer interface in light mode

.. csv-table:: Designer Interface Functions
   :file: /_static/uiexplainer.csv
   :widths: 10, 30, 60
   :header-rows: 1
   :name: ui-table