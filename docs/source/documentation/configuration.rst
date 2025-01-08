inkBoard Configuration
========================

.. entries to explain here:
.. inkBoard, logger, screen, small bit on the device

These entries are provided by a base inkBoard installation. More may be added by integrations or even platforms.

Base Entries
---------------

The entries explained here below can be considered the basic entries.


``inkBoard``
~~~~~~~~~~~~~~~~~

The ``inkBoard`` entry configures some general settings for the dashboard. It is required.

.. currentmodule:: inkBoard.configuration.types

.. autoclass:: InkboardEntry
   :members:
   :no-index:
   :exclude-members: __init__

.. for screen: omit the device entry. Should be fine?
    Also should NOT show the members, just the doc string really


``device``
~~~~~~~~~~~~~~~~~

The ``device`` entry is used to setup the device and platform. It is required.
The ``platform`` key is required. Otherwise, see the documentation for the platform for the available options.

.. autoclass:: DeviceEntry
   :members:
   :no-index:
   :exclude-members: __init__

``screen``
~~~~~~~~~~~~~~~~~

The ``screen`` entry is used to set up the screen instance, which manages the dashboard. It is required.

.. autoclass:: ScreenEntry
   :members:
   :no-index:
   :exclude-members: __init__


``logger``
~~~~~~~~~~~~~~~~~

The ``logger`` entry can be used to setup the logging interfaces of inkBoard. It is not required.

.. autoclass:: LoggerEntry
   :members:
   :no-index:
   :exclude-members: __init__

``substitutions``
~~~~~~~~~~~~~~~~~~~~

The ``substitutions`` entry can be used to implement substitution in the configuration. It is not required.
A substitution can be used later on in the config by referencing it via ``${my_substitution}``

Example:

.. code-block:: yaml
   
   substitutions:
      my_substitution: "Hello World!"

   elements:
      - type: Button
        text: ${my_substitution}



``designer``
~~~~~~~~~~~~~~~~~

The ``designer`` entry can be used to configure specific settings when using the designer. It is not required.

.. autoclass:: DesignerEntry
   :members:
   :no-index:
   :exclude-members: __init__


Dashboard Entries
-------------------

Dashboard entries are read out at a later point than the base entries.
They are all used to define the elements and configure the last bits of the dashboard.

``elements``
~~~~~~~~~~~~~~~~~

Under ``elements``, any kind of element can be defined. They are only validated for being an actual element.

``layouts``
~~~~~~~~~~~~~~~~~

Under ``layouts``, inkBoard validates elements under this entry to be based on the :py:class:`Layout <PythonScreenStackManager.elements.Layout>` element.
This helps in keeping your configuration organised by seperating single elements from their layout containers.

``popups``
~~~~~~~~~~~~~~~~~

Under ``popups``, inkBoard validates that elements defined within are based on the :py:class:`Popup <PythonScreenStackManager.elements.Popup>` element.
Also an entry to keep things organised.

``statusbar``
~~~~~~~~~~~~~~~~~

``statusbar`` is used to setup the :py:class:`StatusBar <PythonScreenStackManager.elements.StatusBar>` element on the main dashboard element.
Aside from the properties of a StatusBar, this entry also allows the keys ``size`` and ``location``.
It is not required, if the entry is not in the config, no StatusBar will be added.

- ``size`` (:py:class:`DimensionString <PythonScreenStackManager.pssm_types.PSSMdimension>`): specifies the size of the statusbar.
- ``location`` (``top``, ``bottom``, ``left``, ``right``): specifies the location of the StatusBar with respect to the ``main_tabs``.

If not specified, the ``orientation`` property is automatically set based on the value of ``location``.

``main_tabs``
~~~~~~~~~~~~~~~~~

``main_tabs`` is used to setup a :py:class:`TabPages <PythonScreenStackManager.elements.TabPages>` element that can be used to navigate through your dashboard.
Under it you can simply setup all the properties for a :py:class:`TabPages <PythonScreenStackManager.elements.TabPages>` element without specifying ``type``.

Unless otherwise specified under the ``main_element`` key of ``inkBoard``, this element will be used as the main element.
If not overwritten in the element's config, it can be accessed via the element id ``inkboard-main-tab-pages``.
