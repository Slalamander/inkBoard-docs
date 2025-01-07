
.. py:currentmodule:: PythonScreenStackManager.elements

Menu Elements
==============

Out of the box, inkBoard provides a few menus.
The StatusBar is the most prevalent one, as it the main way to actually access the other menus.
The idea of these menus is that they can be accessed via an icon in the statusbar.
The menus itself are limited to a single instance, meaning they do not need to be instantiated. Styling can be done via the ``element_properties`` in the statusbar.

.. auto-inkboardelement:: StatusBar

.. auto-inkboardelement:: DeviceMenu

.. auto-inkboardelement:: ScreenMenu