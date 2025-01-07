Developing a Platform
=======================

.. py:module:: inkBoard.platforms

This section will go over the basics of developing a platform, and also try to set out the device model as well as possible.
It is somewhere in between a tutorial for creating your own custom device, and actual documentation, so I would advise keeping an implemented device model at hand for some decent comparisons.

Setting Up
------------

It is possible to use custom devices with inkBoard. 
Say you have created a custom device called ``my_device``.
In your configuration folder, create a new folder called ``my_device``.
To use that device, you can set the value of ``platform`` to ``./my_device``. The ``/`` tells inkBoard it should look for a custom device folder.
To get a custom device running, the folder should contains *at least* the following:

- An ``__init__.py`` file
- A ``device.py`` file 
- In ``device.py`` a ``Device`` class has to be defined, which should be based on :py:class:`inkBoard.platforms.BaseDevice`

When implementing features, the device should make use of the :py:class:`inkBoard.platforms.InkboardDeviceFeatures` named tuple to define them.
The internal names for the features are contained within :py:class:`inkBoard.platforms.FEATURES`, which can be passed to the DeviceFeatures as parameters.

When done, a platform.json file can be included, such that inkBoard can determine the packages required, as well as optional packages for optional features.
This allows other users to quickly install the new platform.

.. autoclass:: inkBoard.types.platformjson
    :no-index:
    :members:
    :exclude-members: __init__, __new__

The BaseDevice
----------------

The :py:class:`BaseDevice` is used as an abstract baseclass for setting up devices.
It ensures the basic functions required for an inkBoard device are present, and allows uniform validation for features.
implementing certain features like a backlight requires the respective baseclass. Other features, like rotation, may require a specific function to be defined.
Any function or property marked with *abstract* needs to be defined in the device class.

A good starting point when developing a device is to take a look at already implemented platforms. The ``desktop`` platform is relatively simple in its basics, and shows both how to develop a base device for ``PythonScreenStackManager`` and how to extend that device for inkBoard.

.. py:module: inkBoard.platforms.basedevice

.. autoclass-custom:: BaseDevice
    :members:
    :member-order: groupwise
    :inherited-members:

Implementing Features
------------------------

Implementing features differs a bit depending on the feature. Some features require a few functions, other require making use of a base class.

Interactive
~~~~~~~~~~~~~

To implement interactivity, mark the device with the :py:attr:`interactive feature <InkboardDeviceFeatures.FEATURE_INTERACTIVE>`.
When doing so, the screen will pass a ``touch_queue`` to the device's :py:meth:`event_bindings` function.
The device can put interaction events in this queue, and the screen will take care of dispatching it to the dashboard.

.. autoclass-custom:: PythonScreenStackManager.pssm_types.TouchEvent
    :members:
    :exclude-members: __init__, __new__, count, index
    
The touch events put into ``touch_type`` are dependent on the features of the device.
If it only has the :py:attr:`interactive feature <InkboardDeviceFeatures.FEATURE_INTERACTIVE>`, the device may only support dispatching taps, or may support dispatching long touches.
Anyhow, it will mean inkBoard does not dispatch any ``hold_release_action``.
The constants for these touch types are:

.. autodata:: PythonScreenStackManager.constants.TOUCH_TAP
    :no-index:

.. autodata:: PythonScreenStackManager.constants.TOUCH_LONG
    :no-index:

If the device supports the :py:attr:`press_release feature <InkboardDeviceFeatures.FEATURE_INTERACTIVE>`, the following constants should be used as touch types.
The screen takes care of categorising them as being a short press or a long one.

.. autodata:: PythonScreenStackManager.constants.TOUCH_PRESS
    :no-index:

.. autodata:: PythonScreenStackManager.constants.TOUCH_RELEASE
    :no-index:

Network
~~~~~~~~

This feature indicates that the device has an internet connection, and the baseclass is used to retrieve info on its connection.
It has two flavors, one for devices that just retrieve network info, and one for devices that can also control the connection state.

To implement the :py:attr:`connection feature <InkboardDeviceFeatures.FEATURE_NETWORK>` a device should make use of the :py:class:`network baseclass <PythonScreenStackManager.devices.Network>`.
It can be imported from ``inkBoard.platforms.basedevice`` as ``BaseNetwork``.

.. autoclass-custom:: PythonScreenStackManager.devices.Network
    :members:
    :member-order: groupwise
    :inherited-members:

The :py:class:`BaseConnectionNetwork <inkBoard.platforms.basedevice.BaseConnectionNetwork>` is used when a device has the :py:attr:`connection feature <InkboardDeviceFeatures.FEATURE_CONNECTION>`.
This feature extends the :py:attr:`connection feature <InkboardDeviceFeatures.FEATURE_NETWORK>` and provides functionality for a device to manage its network.

.. autoclass-custom:: inkBoard.platforms.basedevice.BaseConnectionNetwork
    :members:
    :member-order: groupwise
    :inherited-members:

Battery
~~~~~~~~

If a device implements the :py:attr:`battery feature <InkboardDeviceFeatures.FEATURE_BATTERY>`, the base battery class should be used.
It can be imported from ``inkBoard.platforms.basedevice`` as ``BaseBattery``, and should be able to retrieve the battery's state (``charging``, ``discharging`` and ``full``), and its charge level.

.. autoclass-custom:: PythonScreenStackManager.devices.Battery
    :members:
    :member-order: groupwise
    :inherited-members:

Backlight
~~~~~~~~~~~~

The :py:attr:`backlight feature <InkboardDeviceFeatures.FEATURE_BACKLIGHT>` is for devices that can control the backlight of the screen.
The name may be somewhat confusing, as this feature should also be used to, for example, control the screen's brightness.
inkBoard started on an E-Reader, which have often supply a backlight for the screen that can light it, and the name stuck (at least for now).

.. autoclass-custom:: PythonScreenStackManager.devices.Backlight
  :members:
  :member-order: groupwise
  :inherited-members:

Power
~~~~~~
The :py:attr:`power feature <InkboardDeviceFeatures.FEATURE_POWER>` requires the device to implement two functions:

- ``power_off``, to power off the device
- ``reboot``, to reboot the device

When validating the feature, inkBoard checks if these functions are redefined, or are still the same as the baseclass.

Resize & Rotation
~~~~~~~~~~~~~~~~~~~

The features for :py:attr:`resizing <InkboardDeviceFeatures.FEATURE_RESIZE>` and :py:attr:`rotation <InkboardDeviceFeatures.FEATURE_ROTATION>` work via the same principle.
Mainly since rotating the screen will likely mean the size of the screen has shifted as well.

A device is itself responsible to notice resizing, and to implement it. 
To make the screen handle the changed screen size, first the device must update the screenSize properties accordingly.
Then, the screen's resize function, :py:meth:`self.Screen._screen_resized` has to be called. This function is an async function, so it must be awaited.
Calling it allows the screen to take care of resizing all the elements.
However the device function must subsequently call :py:meth:`self.Screen.print_stack`, in order to print the dashboard again in the new size.

For rotation, the device must implement a :py:meth:`_rotate` function. The screen calls this function once the user requests a rotation.
Rotations are passed as a string value, as a :py:type:`rotation value <PythonScreenStackManager.pssm_types.RotationValues>`.
From there, the :py:meth:`_rotate` function should follow the same procedure as resizing.


