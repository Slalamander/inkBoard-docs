Elements
=============

.. Make a custom directive to document elements

Elements are the bricks that make up a dashboard.
For an explantion of how to use them, refer to the :ref:`tutorial section on elements <tutorial/configuration:Elements>`.
All elements will be documented as below. Meaning they should give a quick explantion as to what they are, list the available shorthand functions, and all settable properties.
This is everything that should be required to use one in a YAML configuration, however if you want to use elements in custom functions, custom elements, or integrations, keep in mind this is not the full model.
For that, refer to the API reference (which I will link once I've made it).

Below is the base Element class. Every element is derived from it, so every action and property listed here is also available to other elements. Keep in mind though, usage may change for different elements.
This class **cannot** be used directly, it is not supposed to be. inkBoard will throw an error if it is specified as a ``type``.


.. auto-inkboardelement:: Element
    :summary-docstr:

.. auto-inkboardelement: Icon

    .. look at the code: need to make a custom property handler.
    .. see line 129

.. toctree::
    
    self
    icon
    baseelements

