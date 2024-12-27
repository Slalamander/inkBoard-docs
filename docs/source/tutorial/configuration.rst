

Configuration
=============

To get started with writing a dashboard configuration file, first make a new folder in the inkBoard folder called ``Tutorial``. Make a new file in it called ``tutorial.yaml``, which will hold a very simple dashboard that will be run at the end of this tutorial.
There will be a distinction between :ref:`Configuration Entries` and :ref:`Dashboard Entries`, which respectively affect the base configuration and the dashboard configuration.

Those familiar with Home Assistant or ESPHome should find the YAML syntax (somewhat) familiar. If you have not use used YAML before, take a look at, for example, `the Home Assistant tutorial <https://www.home-assistant.io/docs/configuration/yaml/>`_.

.. tip::

    The ``!secret`` and ``!include`` constructors work the same as for Home Assistant and ESPHome,
    meaning the use of a ``secrets.yaml`` file, or including yaml configurations from other files, is also possible.

Configuration Entries
---------------------

These are base entries to run your dashboard. If inkBoard cannot validate these entries, it will not continue to validating your dashboard entries, and, as such, inkBoard will not run.
This also includes gathering integrations included in the configuration, and having their entries validated.

Required Entries
~~~~~~~~~~~~~~~~

There are two required entries in the config files that do not directly have to do with designing the dashboard.

The ``inkBoard`` entry is a base entry to configure some behaviour of inkBoard. It can largely be left alone for now, all that will be done for now is set a name for the project.

.. code-block:: yaml

    inkBoard:
      name: inkBoard Tutorial

The ``device`` entry is dependent on the platform that runs the dashboard. For now, it will set it to ``emulator``, a generic device, which is only available in the designer.

.. code-block:: yaml

    device:
      platform: emulator

Optional Entries
~~~~~~~~~~~~~~~~

These entries do not need to be present for the configuration to run.
Ignoring any added by integrations, they are ``logger``, ``folders``, ``designer`` and ``screen``.
The former 3 can be considered advanced features, and for general use (or beginners), their base configurations should be sufficient.

The ``screen`` entry handles the setup of the screen, which is the Python class that handles the logic for printing to the device, processing interactions, and getting device states. If that means nothing to you, that is fine, as understanding that sentence is not required for configuring the screen entry.
Lets say the default background picture is too messy for your dashboard, and maybe think the general time for a long touch is too short. That can be configured by changing the ``screen`` entry.

.. code-block:: yaml

    screen:
      background: inkboard
      minimum_hold_time: 1s

Instead of a background picture, the inkBoard theme color will be used. Although inkboard is not an actual supported shorthand css color, there is support for adding custom colors, called shorthand colors. The inkBoard themed colors ``inkboard``, ``inkboard-light``, ``inkboard-gray`` and ``inkboard-dark`` are available by default. Integrations also support adding their own colors. For example, the Home Assistant branded blue color is added as a shorthand by the Home Assistant integration.

.. tip::

    You can add your own shorthand colors via the ``styles`` entry. Any color that can be parsed by the color parser is valid, but it is advised to either use RGB(A) values or simply rename css colors.

    .. code-block:: yaml

        styles:
          shorthand_colors:
            my-color: orange


The configuration of ``minimum_hold_time`` means that instead of half a second, a touch will be considered as being held after a full second.
inkBoard supports parsing simple textual durations to the appropriate amount of seconds. These types of entry also accept numerical value.

Dashboard Entries
---------------------

These entries setup your actual dashboard (aside from anything under the screen entry). They hold configurations for all the elements that are present on a dashboard.

*Wait...* what are elements? Think of elements as fullfilling roles similar to cards on Home Assistant dashboards, or widgets on your phones home screen. They are not exactly the same however. Elements in inkBoard are the name for any type of "widget".
There are various types of elements. A few basic ones, and some that can hold other elements, for example. But a lot of elements derive from each other, or contain instances of other elements.
So keep an eye out for the elements an element inherits from. To give an example, all elements allow a ``background_color`` to be set, since they all inherit from the base element. This will not be repeated for each class, hence it is important to keep it in mind.
And also keep in mind which elements are contained within an element you're adding, since those, generally, can all be styled seperately as well. 

The next section will go more in depth with element types and styling them.

.. maybe give each entry its own subsection -> idk gotta stay focused on the tutorial part of this.? or at least the big ones. Also don't forget to mention i.e. tap_actions and stuff.

