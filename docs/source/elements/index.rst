Elements
=============

.. somehow include the line element somewhere lol

.. py:currentmodule:: PythonScreenStackManager.elements

Elements are the bricks that make up a dashboard.
For an explantion of how to use them, refer to the :ref:`tutorial section on elements <tutorial/configuration:Elements>`.
All elements will be documented as below. Meaning they should give a quick explantion as to what they are, list the available shorthand functions, and all settable properties.
This is everything that should be required to use one in a YAML configuration, however if you want to use elements in custom functions, custom elements, or integrations, keep in mind this is not the full model.
For that, refer to the API reference (which I will link once I've made it).

All elements have their configurable properties listed in three ways, depending on how much info you need.
The *Full* tab gives all information on a property, meaning its typing, documentation string and default value.
The *Compact* tab lists the typing and default value of a property.
The *List* tab provides a consice list with the default value and a summary of the property.

Below is the base Element class. Every element is derived from it, so every action and property listed here is also available to other elements. Keep in mind though, usage may change for different elements.
This class **cannot** be used directly, it is not supposed to be. inkBoard will throw an error if it is specified as a ``type``.

For the moment, images to show off the elements are not included yet. However, the example ``configuration.yaml`` in the inkBoarddesigner repo shows off all elements. You can run it if you want a preview at hand.

.. auto-inkboardelement:: Element
    :summary-docstr:


.. toctree::
    :hidden:
    
    button
    icon
    tile
    sliders
    checkboxes
    clocks
    counter
    dropdown
    layouts
    popups
    menus
    device-elements
    baseelements

