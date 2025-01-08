Layouts
========

.. py:currentmodule:: PythonScreenStackManager.elements

Layouts form containers to hold other elements. 
Keep in mind that, although the base element :py:class:`Layout` can be used in YAML, and is not as user friendly to use with it.

.. auto-inkboardelement:: Layout
    :summary-docstr:


.. auto-inkboardelement:: TileLayout

.. auto-inkboardelement:: GridLayout

.. auto-inkboardelement:: TabPages

Useful Elements
-----------------------

The elements below are not a type of :py:class:`Layout` per se, but they are mainly useful within one, and not so much on their own.
I also don't know where else to put them really.

The navigation bar of a :py:class:`TabPages` element is build up of :py:class:`NavigationTile` elements.

.. auto-inkboardelement:: NavigationTile
    :ignore-required:

If you want to seperate elements within layouts, the :py:class:`Line` element can be used.

.. auto-inkboardelement:: Line