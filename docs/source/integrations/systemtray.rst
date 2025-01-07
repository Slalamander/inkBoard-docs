System Tray
============

The ``system_tray`` integration can be used to run inkBoard in the system tray, rather than from the taskbar.
It can only be used on the ``desktop`` platform.

Installation
--------------

Run the command to install the dependencies.

.. code-block:: console

    inkBoard install integration system_tray

Configuration
--------------

+-----------------+--------------------------------+------------------------------------------------------------------------------------------------------+------------+
| Option          | Type                           | Description                                                                                          | Default    |
+-----------------+--------------------------------+------------------------------------------------------------------------------------------------------+------------+
| ``icon``        | str , ``circle`` , ``droplet`` | The icon to show in the system tray. ``circle`` and ``droplet`` are variations of the inkBoard logo. | ``circle`` |
+-----------------+--------------------------------+------------------------------------------------------------------------------------------------------+------------+
| ``hide_window`` | bool                           | Hides the window from the taskbar when it is minimised                                               | ``false``  |
+-----------------+--------------------------------+------------------------------------------------------------------------------------------------------+------------+
| ``toolwindow``  | bool                           | Hides inkBoard from the taskbar entirely. It can be opened, minimised and closed via the tray icon.  | ``false``  |
+-----------------+--------------------------------+------------------------------------------------------------------------------------------------------+------------+

Example
---------

.. code-block:: YAML

    system_tray:
        toolwindow: true
