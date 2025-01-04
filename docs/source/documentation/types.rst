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

.. autoclass:: PSSMLayout

The internal representation of a layout in the base ``Layout`` element. Generally not required unless using the ``Layout`` element.

.. autoclass:: PSSMLayoutString

Indicates a layoutstring can be used. For example, a `tile_layout`.
**Quickly recap how these work here, or reference the tutorial**

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

These types usually mean an attribute requires some more configuration when used in the YAML configuration.

.. autoclass:: ElementActionType
    :no-index:
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

.. autoclass:: ElementActionFunction
    :exclude-members: __init__,  __new__
    :special-members: __call__

    

hello df