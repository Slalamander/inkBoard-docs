Platforms
==========

.. py:currentmodule:: inkBoard.platforms

Platforms are defined under the ``device`` entry in your config.
The ``platform`` key is always required, as it indicates to inkBoard which device it should load in.


Features
-----------

To indicate to inkBoard what capabilities a device has, a feature class is implemented.
Some features may not do much (or are not fully implemented even).
Accessing features, for example for :doc:`/elements/device-elements`, can generally be done by specifying them with the ``FEATURE_`` prefix.
For example, :py:attr:`FEATURE_BACKLIGHT <InkboardDeviceFeatures.FEATURE_BACKLIGHT>` can be accessed via ``backlight``.

.. autoclass-custom:: InkboardDeviceFeatures
  :members:
  :inherited-members:
  :exclude-members: __init__, __new__, count, index
  :index-members:
  :summary-docstr:

.. toctree::
    :name: platformtree
    :hidden:

    desktop/index
    kobo/index
    Developing <developing>