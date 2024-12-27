

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

    You can add your own shorthand colors via the ``styles`` entry. Any color that can be parsed by the color parser is valid, but it is advised to either use RGB(A) values or simply add other names for css colors.
    
    .. code-block:: yaml

        styles:
          shorthand_colors:
            my-color: orange

    
    The color parser uses the `Pillow color module <https://pillow.readthedocs.io/en/stable/reference/ImageColor.html#module-PIL.ImageColor>`_. For a full list of color names, `this <https://stackoverflow.com/a/54165440>`_ stackoverflow answer gives a nice overview.


The configuration of ``minimum_hold_time`` means that instead of half a second, a touch will be considered as being held after a full second.
inkBoard supports parsing simple textual durations to the appropriate amount of seconds. These types of entry also accept numerical value.

Dashboard Entries
---------------------

These entries setup your actual dashboard (aside from anything under the screen entry). They hold configurations for all the elements that are present on a dashboard.

*Wait...* what are elements? Think of elements as fullfilling roles similar to cards on Home Assistant dashboards, or widgets on your phones home screen. They are not exactly the same however. Elements in inkBoard are the name for any type of "widget".
There are various types of elements. A few basic ones, and some that can hold other elements, for example. But a lot of elements derive from each other, or contain instances of other elements.
So keep an eye out for the elements an element inherits from. To give an example, all elements allow a ``background_color`` to be set, since they all inherit from the base element. This will not be repeated for each class, hence it is important to keep it in mind.
And also keep in mind which elements are contained within an element you're adding, since those, generally, can all be styled seperately as well. 

Strictly speaking, no entries are required. However, to actually get a dashboard up and running, you will need to at least have a few elements defined. inkBoard will also need to know how to setup the dashboard via them.
If you define none of these, you will simply get an empty dashboard.

Elements
~~~~~~~~

The ``elements`` entry is the most general dashboard entry. It can hold the configuration for any kind of element. Lets start with making two simple elements. 
A ``Button`` element, which are elements that shows some text, and an ``Icon`` element, which shows an icon. To start, add the ``elements`` entry to your configuration.
For any element you add, the type of element is identified by the ``type`` key. Any element can also be given a custom ``id``. This makes it easy to reference them in actions, or other elements for example.

Start with defining the ``Button`` under ``elements``. Since multiple elements can be defined under the ``elements`` entry, put them in a list. For a ``Button``, the text to write is defined under the ``text`` key, for the tutorial it will be set to `Hello World!`.
To make the text readable, specify the ``font_color`` as white.

For the ``Icon``, the process is similar. Since it is a different kind of Element, the options are different however. An ``icon`` needs to be specified so it knows what icon needs to be shown. inkBoard supports the `Material Design Icons <https://pictogrammers.com/library/mdi/>`_ library. They are identified by prefixing an icon via ``mdi:``.
For the tutorial, an icon of the earth will be used by setting ``icon`` to `mdi:earth`. The color of the icon can be set via ``icon_color``. 

.. tip::
  
  If you are using VSCode as your IDE, the `VSCode Material Design Icons Intellisens extension <https://marketplace.visualstudio.com/items?itemName=lukas-tr.materialdesignicons-intellisense>`_ makes finding icons a lot easier, and omits the need to go to external websites to find one.



The ``elements`` entry should now look like like below. The ``id`` can be set however you want, however, the given values will be used to reference the elements later.

.. code-block:: yaml

  elements:
    - type: Button
      id: my-button
      text: Hello World!
      font_color: white

    - type: Icon
      id: my-icon
      icon: mdi:earth
      icon_color: white


Layouts
~~~~~~~

As mentioned, there are elements that can hold other elements. These types of elements are all based on the ``Layout`` element. That does not neccesarrily mean they are to be used as such, as certain elements function via other elements held within their base layout.
Under the ``layouts`` entry you can configure various layouts. Any element defined directly under this must be a type of ``Layout`` element, otherwise it will not pas validation. 

For now, lets keep to the basics, and simply add ``my-button`` and ``my-icon`` to a layout element. The ``GridLayout`` element is probably the easiest element to work with in the YAML syntax. It places all elements added to it in a grid, which can have its rows and columns set. However, it also allows for automatically setting the required amounts of columns or rows to fit in all added elements.
For a ``GridLayout``, the elements can be added under ``elements``, and the elements to add can be directly referenced via their ``id``. As will be shown later, it is also possible to directly define elements within other elements.

Considering the ``Icon`` will always be square, the ``Button`` needs more width to decently fit within the layout.
For ``GridLayouts``, these can be set for rows and columns by setting ``row_sizes`` and ``column_sizes`` respectively. Say, the ``Icon`` will get about a quarter of the available width, and the ``Button`` will be given the rest.
For this, the ``column_sizes`` can be set to ``[w/4, "?"]``. This introduces another important concept, ``DimensionStrings``. Generally, whereever dimensions are required, these strings can be used to calculate variable values. Integer values are also possible, but will translate directly into a pixel value.
By setting the first column size to ``w/4``, the element will give that column a size that equals a quarter of its own width. The second column is given the value ``"?"``. The ``"?"`` is a sort of placeholder value. They are mainly used in layouts, where there total weight is accumulated, and subsequently divided.
For example, in this case, setting ``column_sizes`` to ``["?*0.25", "?*0.75"]`` or ``["?", "?*3"]`` will yield the same results. For the former, the total weight of ``"?"`` equals one, and the first column is given 25% of that, and the second one gets 75%. The same goes for the latter.

The ``layouts`` entry should now look like below.

.. code-block:: yaml

  layouts:
    - type: GridLayout
      id: my-layout
      rows: 1
      columns: 2
      column_sizes: ["w/4", "?"]
      elements:
        - my-button
        - my-icon 


Main Tabs & Statusbar
~~~~~~~~~~~~~~~~~~~~~~~~

The ``main_tabs`` entry is meant as the main ``Layout`` element in your dashboard. 
It configures a ``TabPages`` element directly, and inkBoard will put it as the topmost element, optionally together with a ``StatusBar``.
The ``statusbar`` entry configures a ``StatusBar`` element directly. These elements fullfill a somewhat similar role to the android statusbar. It shows various ``Icon`` elements meant to display information on the current state of the dashboard.
The icons are added via inkBoard or integrations, so there is no need to worry about that. Both will, for now, be added with a minimum configuration. All that will be altered, is hiding the navigation bar from the ``TabPages`` since there is only one view for the moment. This is done via the ``hide_navigation_bar`` key. 
``my-layout`` still needs to be added to the ``TabPages`` element in order for it to actually appear on the screen though. This is done under ``tabs`` key. Each tab needs an element defined, and be given a name such that they can be identified easily.

This part of your configuration should look like below now.

.. code-block:: yaml

  statusbar:

  main_tabs:
    hide_navigation_bar: true
    tabs:
      - element: my-layout
        name: My Layout


The Base Configuration
-----------------------

This should leave you with a very basic configuration file. If followed correctly, your ``tutorial.yaml`` file should look like :ref:`this <tutorial-configuration>`. 
The :doc:`next section <designing>` will go further in depth, utilising the designer and designing more complex elements.

.. dropdown::
  **Tutorial/tutorial.yaml**

  .. literalinclude:: /_static/tutorial-configuration.yaml
    :linenos:
    :caption: tutorial.yaml
    :name: tutorial-configuration


.. maybe give each entry its own subsection -> idk gotta stay focused on the tutorial part of this.? or at least the big ones. Also don't forget to mention i.e. tap_actions and stuff. -> will do that in design

