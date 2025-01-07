.. py:currentmodule:: PythonScreenStackManager.elements

Device Elements
================

Device elements are elements specifically meant to show the state of your device.
They update only when the variable they monitor has changed. 
The screen itself takes care of requesting the device to update features for the most part, which is done via ``poll_interval``.

.. auto-inkboardelement:: DeviceButton

.. auto-inkboardelement:: DeviceIcon

.. auto-inkboardelement:: BacklightSlider