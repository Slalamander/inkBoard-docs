inkBoard Configuration
========================

.. entries to explain here:
.. inkBoard, logger, screen, small bit on the device

The entries explained here below can be considered the basic entries.

inkBoard
------------

The ``inkBoard`` entry configures some general settings for the dashboard. It is required.

.. currentmodule:: inkBoard.configuration.types

.. autoclass:: InkboardEntry
   :members:
   :no-index:
   :exclude-members: __init__

.. for screen: omit the device entry. Should be fine?
    Also should NOT show the members, just the doc string really


device
---------

The ``device`` entry is used to setup the device and platform. It is required.
The ``platform`` key is required. Otherwise, see the documentation for the platform for the available options.

.. autoclass:: DeviceEntry
   :members:
   :no-index:
   :exclude-members: __init__

screen
-------

The ``screen`` entry is used to set up the screen instance, which manages the dashboard. It is required.

.. autoclass:: ScreenEntry
   :members:
   :no-index:
   :exclude-members: __init__


logger
-------

The ``logger`` entry can be used to setup the logging interfaces of inkBoard. It is not required.

.. autoclass:: LoggerEntry
   :members:
   :no-index:
   :exclude-members: __init__

substitutions
---------------

The ``substitutions`` entry can be used to implement substitution in the configuration. It is not required.
A substitution can be used later on in the config by referencing it via ``${my_substitution}``

Example:
.. code-block:: YAML
   
   substitutions:
      my_substitution: "Hello World!"

   elements:
      - type: Button


``designer``
-------------

The ``designer`` entry can be used to configure specific settings when using the designer. It is not required.

.. autoclass:: DesignerEntry
   :members:
   :no-index:
   :exclude-members: __init__