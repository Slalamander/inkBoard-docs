Types
=======

.. currentmodule:: PythonScreenStackManager.pssm_types

The documentation will likely contain typehints to various types used internally in the code.
Any types that are relevant when writing a configuration file will be noted here, as well as a couple of hints that may be useful when writing custom functions.

Direct types mean they are an alias for more complex types, like the :py:class:`PSSMdimension` indicating DimensionStrings can be used, for example.
`class` types mean they can be configured further.

A quick refresher on how Python types relate to YAML syntax:

.. code-block:: yaml

    dict:
        value1: 1
        value2: hi
    list:
        quick_list: [1, 2, 3]
        long_list:
            - 1
            - 2
            - 3
    tuple: same as list

For the default values of element properties, you will often see these denoted via ``{}`` for a dict, and ``[]`` or ``()`` for a list.

.. include: durationtype, areatype? ##colorproperty etc?

Shorthand Types
-----------------------

.. currentmodule:: PythonScreenStackManager.pssm_types


These types are used as shorthands to quickly note the use of a certain variable.


.. autoclass:: ColorType


This type indicates a value expect a valid color. This means it can be *anything* that inkBoard considers a valid color value, and can thus also be a self defined shorthand, for example.

.. autoclass: DurationType

Denotes durations are accepted. Either a float or integer, which is the direct value in seconds, or a duration string.

.. autoclass:: PSSMdimension

Any kind of acceptable dimension, meaning either an integer or float (which translates directly to the number of pixels), or a dimensional string

.. autoclass:: PSSMarea

The format in which pssm defines element areas.

.. autoclass:: PSSMLayout

The internal representation of a layout in the base ``Layout`` element. Generally not required unless using the ``Layout`` element.

.. autoclass:: PSSMLayoutString

Indicates a layoutstring can be used. For example, a `tile_layout`. See the :ref:`Tile tutorial<tutorial/designing:Tiles>`.

.. autoclass:: DurationType

Used for properties that describe durations. A DurationType can be passed as a ``float`` (i.e. 1.5), ``int`` (i.e. 2) or a duration string i.e. (``2min``).
Unless stated otherwise, ``float`` and ``int`` values are equivalent to the amount of seconds.

.. autoclass:: RotationValues

Type hint for rotation values that can be set via strings. Mainly useful for devices where a screen rotation can be set.
Allowed values and their corresponding value in degrees are:

- ``UR`` :  0°
- ``CW`` : 90°
- ``UD`` : 180°
- ``CCW`` : 270°

.. autoclass:: BadgeLocationType

Shorthand values for placing badges. Currently only in use for ``Icon`` elements.

- ``UR`` :  Upper Right
- ``LR`` : Lower Right
- ``UL`` : Upper Left
- ``LL`` : Lower Left

Configuration Types
--------------------

These types usually mean an attribute requires some more configuration when used in the YAML configuration,
like aditional keys.

.. autoclass-custom:: ElementActionType
    :members:
    :exclude-members: __init__,  __new__

in YAML syntax:

.. code-block:: yaml

    element_action:
        action: my-action
        data:
            value: 1
        map:
            value_2: attribute

Advanced Types
---------------

These are types you may not run into directly, especially when just using YAML.
However they are useful when writing custom functions or elements and the like.

.. autoclass-custom:: ElementActionFunction
    :exclude-members: __init__,  __new__
    :special-members: __call__

.. autoclass-custom:: InteractEvent
    :members:
    :exclude-members: __init__,  __new__

Decorators
~~~~~~~~~~~~

Some decorators are included which can make the creation of custom functions and elements more convenient.
They can be imported from ``PythonScreenStackManager.pssm.util``.

.. py:module:: PythonScreenStackManager.pssm.util

.. autodecorator:: colorproperty

.. autoattribute:: colorproperty.NOT_NONE
    :annotation:

    | Used to indicate a colorproperty is not allowed to have ``None`` as a value.
    | Use via ``@colorproperty.NOT_NONE``

.. autodecorator:: elementaction

.. autodecorator:: elementactionwrapper

.. autoattribute:: elementactionwrapper.method
    :annotation:

    | Decorator wrapper for functions that are methods, as to not catch out the first argument (for example ``self``).
    | Use via ``@elementactionwrapper.method``
