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
| ``tray_size``   | int                            | Size in pixels of the taskbar/systemtray in which the icon is location                               | ``50``     |
+-----------------+--------------------------------+------------------------------------------------------------------------------------------------------+------------+
| ``menu_actions``| list                           | List of additional actions to add to the right click menu.                                           | ``[]``     |
|                 |                                | An empty entry creates a seperator line, otherwise each entry should have the keys                   |            |
|                 |                                | ``title``, which is the title for the action used in the menu,                                       |            |
|                 |                                | and ``action``, which is an ``actionentry`` pointing to what action to call.                         |            |
+-----------------+--------------------------------+------------------------------------------------------------------------------------------------------+------------+


Example
---------

.. code-block:: YAML

    system_tray:
      toolwindow: true
      tray_size: 47
      menu_actions:
        - title: Show Config
          action: show-config-file
        - title: Logs
          action:
            action: log-terminal
            data:
            level: DEBUG

