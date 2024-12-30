
:description: Learn how to design elements and dashboards in inkBoard

Designing
=========

With a :ref:`base configuration <tutorial-configuration>` written, it is time to actually utilise it as a dashboard.
More elements will be added, interactivity will be configured as well, and styling options will be explained.
First, a basic workflow for designing a dashboard will be gone through, after which those complexer features will be explained.

But first, start inkBoard designer by running this command. You should be greeted by the opening screen.

.. code-block:: console

    inkBoard designer

.. tip::
   
   You can open a configuration file immediately by running

   .. code-block:: console

      inkBoard designer path/to/configuration/file.yaml

.. figure:: images/designer-welcome-screen.png
   :figclass: light-only
   :align: center

.. figure:: images/designer-welcome-screen-dark.png
   :figclass: dark-only
   :align: center

The top four buttons are currently disabled, since there is no configuration selected.
You can toggle around the settings if you want though, although for now only the Dark Mode toggle will do something. 
Lets load the configuration from the previous section. Press the folder icon in the top right and open ``tutorial.yaml``.
If the configuration was setup correctly, you should see the dashboard below.

.. figure:: images/config-tutorial-dashboard.png
   :figclass: light-only
   :align: center

.. figure:: images/config-tutorial-dashboard-dark.png
   :figclass: dark-only
   :align: center

That is not very impressive yet, of course. Lets start with fixing up the current elements. Then, implement some interaction, and start adding more complex elements.

Design Workflow
----------------

inkBoard, and especially the designer, tries to make iterating over dashboard designs as smooth as possible. You may have already noticed the `Reload` button in the top right. It does exactly what you think, namely reloading the configuration.
Lets make some changes to the dashboard, and put it to use.

Styling a Button
~~~~~~~~~~~~~~~~

Start by making the ``Button`` a little more readable. Increase the font size by setting ``font_size`` and make the text bold by setting ``font``.

.. code-block::
  :caption: applying a custom font size to ``my-button``

  - type: Button
    id: my-button
    text: Hello World!
    font_color: white
    font_size: h
    font: default-bold

.. important::

   Like colors, fonts have shorthands available too. The base shorthand fonts are ``default``, ``default-regular``, ``default-bold``, ``header`` and ``clock``. Mainly, they map to some of the fonts integrated in the package.
   ``quicksand``, ``notosans`` and ``merriweather``. Integrations can add more shorthands too.
   A set of shorthand icons is available too, but they all map to mdi icons by default. The Home Assistant integration, for example, adds the ``homeassistant`` shorthand, which maps to the home assistant logo icon.

Press the reload button (Or F5 as a keyboard shortcut) to reload the config. As you'll see, maybe setting the font size to the full available height was a little much.
Instead, lets use the maximum possible font size for which the text will still fit. For that, use the ``fit_text`` key. When that is ``true``, the element will use the value of ``font_size`` as the minimum allowed font size. So, by setting it to 0, it can basically just fit the text to whatever value is necessary.
Reload the configuration, and indeed, it looks a lot better.

.. code-block:: 
  :caption: ``my-button`` with automatic font size
  
  - type: Button
    id: my-button
    text: Hello World!
    font_color: white
    font_size: 0
    fit_text: true
    font: default-bold

Styling an Icon
~~~~~~~~~~~~~~~

``my-icon`` and ``my-button`` are both still somewhat floating about on the dashboard. To seperate them a bit more, give ``my-icon`` its own background color.
This can be done by applying ``background_color``. If only the ``background_color`` property is set, the entire space of the element will be filled with said color.
In this case, that is a bit much, so to limit the background space, ``Icon`` elements can be given a ``background_shape`` property. A circle matches quite well with the round globe.

.. code-block::
  :caption: Applying a background to ``my-icon``

  - type: Icon
    id: my-icon
    icon: mdi:earth
    icon_color: white
    background_color: inkboard-light
    background_shape: circle

.. important::
   
   Not every element allows the use of ``background_shape`` (yet). For ``Button`` elements and base ``Layout`` elements, the radius property does allow using rounded corners.
   The advantage of them is that not the entire element's background is usually filled, but instead they use the space required to encompass the visible parts of the element.
   Currently, the following values for ``background_shape`` are implemented:
   
   - ``circle`` (``ImageDraw.pieslice``)
   - ``square`` (``ImageDraw.rectangle``)
   - ``rounded_square`` (``ImageDraw.rounded_rectangle``)
   - ``rounded_rectangle`` (``ImageDraw.rounded_rectangle``)
   - ``octagon`` (``ImageDraw.regular_polygon``)
   - ``hexagon`` (``ImageDraw.regular_polygon``)
   - ``none``, meaning background shape
   - ``ADVANCED``, allows for complicated usage
  
   By setting the ``shape_settings`` property, you can further configure how the shape is drawn.
   Every shape (except ``ADVANCED``) has default settings, but those can also be overwritten. 
   See the appropriate function in `Pillow's ImageDraw Module <https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html>`_. When using ``ADVANCED``, supply the ``method`` argument to ``shape_settings``, which has to be the string value of one of the methods of ``ImageDraw``.

Styling the StatusBar
~~~~~~~~~~~~~~~~~~~~~~

All that is left is to make the statusbar match the dashboard some more. First off, apply a bit of a margin on the top of it, such that the icons have a little more free space.
To keep the icons roughly the same size, increase its size too. By default, the statusbar gets 5% of the available space. Increase it to 7.5%.

.. code-block:: yaml
   :caption: Applying size and margins to the statusbar

   statusbar:
    outer_margins: [5, 10]
    size: "?*0.075"

To make the icons in the statusbar match ``my-icon``, the ``status_element_properties`` property can be used. This property applies the set properties to all the icons in the statusbar.
By setting the statusbar's ``foreground_color``, it is possible to use this value in child elements. By setting it to white, and subsequently setting ``icon_color`` to ``foreground``, the parent's ``foreground_color`` is used for the color value.
The same concept is used to set the ``background_color`` to the ``accent_color`` of the statusbar.

.. code-block:: yaml
   :caption: Editing the look of the status elements

   statusbar:
    outer_margins: [5, 10]
    size: "?*0.075"
    foreground_color: white
    accent_color: inkboard-light
    status_element_properties:
      icon_color: foreground
      background_color: accent
      background_shape: circle

.. important::

   Elements within layouts have access to the color properties of their parent layout. For example, an icon can take on its parent layout's ``background_color`` by setting ``icon_color`` to ``background``.
   Any color property of a layout is available as a shorthand as the name of that property minus the ``_color`` part. See the documentation for a specific element to see which color properties are available.

Finally, to make the clock's style match that of ``my-button``, a similar property will be used. Via ``element_properties``, certain layout type elements allow for styling elements within them.
This is mainly meant for layout elements with specific usage, like the ``Counter``, so more explanation to how they work will come later.
For now, the ``font_color`` is set to ``foreground`` as well, and the same font as ``my-button`` will be used.

.. code-block:: yaml
   :caption: Editing the look of the statusbar clock

   statusbar:
    outer_margins: [5, 10]
    size: "?*0.075"
    foreground_color: white
    accent_color: inkboard-light
    status_element_properties:
      icon_color: foreground
      background_color: accent
      background_shape: circle
   element_properties:
      clock:
        font_color: foreground
        font: default-bold

Continueing the Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you get the hang of styling elements, all those reloads and intermediate steps won't become as necessary. inkBoard tries to make its logs as usable as possible, especially for configuration errors, so if things don't work, keep an eye on that.
The dashboard resulting from all the steps in the previous section can be seen in the dropdown below.

.. dropdown::
   Resulting Dashboards

   .. carousel::
      :data-bs-interval: false

      .. figure:: images/tutorial-font-size-bad.png

         ..

         The font is a bit oversized

      .. figure:: images/tutorial-font-size-good.png

         ..

         ``fit_text`` fixes that

      .. figure:: images/tutorial-background-bad.png

         ..

         Fully applying a background color may be overdoing it somewhat

      .. figure:: images/tutorial-backgroundshape-good.png

         ..

         A ``background_shape`` looks more in place

      .. figure:: images/tutorial-statusbar-sizing.png

         ..

         A bit more space for the statusbar

      .. figure:: images/tutorial-styling-statuselements.png

         ..

         Styling the status elements

      .. figure:: images/tutorial-styling-clock.png

         ..

         Styling the statusbar clock

..

Designing a Dashboard
----------------------

Styling isn't all inkBoard can do. Nor are ``Icon`` and ``Button`` the only two available elements (as a matter of fact, a ``DigitalClock`` element has been styled too).
But to get a better feel for the more complex features, the dashboard needs more elements, those elements need to be configured, and stuff needs to actually work.

Element Actions
~~~~~~~~~~~~~~~~

Although inkBoard dashboards work fine with just displaying data, they are generally meant to be interactive.
By default, a couple of functions are available through the YAML syntax, which are referred to as `shorthand_functions`.
A few default ones are added, like ``quit`` and ``reload``, as well as some that depend on whether a platform supports certain features. For example, if a device supports the backlight feature, shorthands like ``backlight-toggle`` are also available.

Adding a shorthand to an element is quite simple. 
For example, adding ``reload`` to ``my-icon`` to reload the config on press is done by setting ``tap_action`` to ``reload``.
To add feedback on interaction, set ``show_feedback`` to ``true``.

.. code-block:: yaml
  :caption: Adding a ``tap_action`` to ``my-icon``

  - type: Icon
    id: my-icon
    icon: mdi:earth
    icon_color: white
    background_color: inkboard-light
    background_shape: circle
    show_feedback: true
    tap_action: reload

If you clicked around in the dashboard before, you may have noticed that the icons in the statusbar already are interactive, and open a menu when tapped on.
To explain how to mimick that behaviour, first add the ``popups`` entry, and make a ``PopupMenu`` element, which inherts from the base ``Popup`` element.

.. code-block:: yaml
   :caption: Making a ``Popup`` element

   popups:
      - type: PopupMenu
        id: my-popup
        title: "Hello World!"
        menu_layout:
          type: GridLayout
          elements:
            - type: Button
              text: Again!
              id: my-popup-button

.. important::
   
   ``Popup`` elements are simply ``Layout`` elements with added functionality to print them on top of whatever is currently on screen, and determine their size and position more directly.

This is a very simple element, but if you reload the dashboard, it does not appear. To make that happen, it has to be shown somehow.
To do so, the ``show`` shorthand function of ``my-popup`` can be linked to the ``tap_action`` of ``my-icon``. 
For this, the shorthand function identifier ``element:`` needs to be used, and the appropriate ``element_id`` needs to be set for the ``tap_action``.

.. code-block:: yaml
  :caption: Linking an element action to the ``tap_action`` of ``my-icon``

  - type: Icon
    id: my-icon
    icon: mdi:earth
    icon_color: white
    background_color: inkboard-light
    background_shape: circle
    show_feedback: true
    tap_action:
      action: element:show-popup
      element_id: my-popup

When tapping ``my-icon`` now, ``my-popup`` appears! The syntax for ``elementactions`` is the same for interaction actions, for example ``tap_action`` and ``hold_action``,
but ``elementactions`` can also be used with certain elements to automate them. In general, this goes for element properties starting with ``on_``.
To show this off, add a ``Counter`` and a ``Slider`` element to your dashboard. Don't forget to update ``my-layout`` and add them.

.. code-block:: yaml
  :caption: Creating a ``Slider`` and a ``Counter``

  - type: Counter
    id: my-counter
    minimum: -10
    maximum: 10
    foreground_color: foreground
    on_count:
      action: element:set-position
      element_id: my-slider

  - type: Slider
    id: my-slider
    minimum: -10
    maximum: 10
    color: accent
    thumb_color: foreground
    on_position_set:
      action: element:set-value
      element_id: my-counter

.. hint::
  .. dropdown::
    ``my-slider`` and ``my-counter`` do not show up

    .. code-block:: yaml
      :caption: edit ``my-layout`` to add the new elements

      - type: GridLayout
        foreground_color: white
        accent_color: inkboard-light
        rows: 2
        columns: 2
        column_sizes: [w/4, "?"]
        id: my-layout
        elements:
          - my-icon
          - my-button
          - my-counter
          - my-slider

When changing the value of ``my-counter``, ``my-slider`` updates to reflect that value too, and the same happens vice-versa.
``element_actions`` are more powerful than just calling some functions, however. Using the ``data`` and ``map`` keys, it possible to pass parameters to the called functions.
To do so, update ``my-counter`` such that the text of ``my-button`` is changed whenever its value changes. This can be done via the ``data`` key, since the text is a value that does not change.
``my-slider`` will update the the text of ``my-button`` to the current slider position. Since this means a value is mapped to a property of the element, the ``map`` key is used. The ``position`` property of the slider is the current value of the slider, so the ``text`` key under ``map`` should have the value ``position``.

.. attention::
  If you pass any parameters that a function does not accept, an error will be thrown and the function will not be called.

.. code-block:: yaml
  :caption: Using the ``data`` and ``map`` key in an ``elementaction``

  - type: Counter
    id: my-counter
    minimum: -10
    maximum: 10
    foreground_color: foreground
    on_count:
      action: element:update
      element_id: my-button
      data:
        text: Count me in!

  - type: Slider
    id: my-slider
    minimum: -10
    maximum: 10
    color: accent
    thumb_color: foreground
    on_position_set:
      action: element:update
      element_id: my-button
      map:
        text: position

Interacting with the two elements should now change the text displayed on ``my-button``. The shorthand function ``element:update`` updates the element's properties to the values passed via ``data`` and ``map``, and is available for any element.
The previous example, that linked the values of ``my-counter`` and ``my-slider``, can also be achieved by using the ``element:update`` shorthand. If you want to experiment more with ``elementactions``, try getting that to work, for example.

For available ``elementactions``, take a look at the documentation for the elements. The same goes for available shorthand actions. 

.. important::

  ``elementactions`` can be defined to call a function or do something when they are interacted with. Certain elements also have actions that allow automation, for example when their value changes.
  Look for element properties that end on ``_action`` for interactable actions, and properties that start with ``on_`` for automation actions.

  The ``data`` key for an ``elementaction`` can be used to pass directly defined values to the called function. This always happens by passing the value as a keyword, so be careful to check if the called function accepts said keyword.
  ``map`` functions similar to ``data``. However, instead of passing a defined value, it maps the value of the key to the value of the matching property of the element.


.. add carouself with the popup being shown, and the three states of updating the button.

Tiles
~~~~~~~

.. 1. improve font_size
.. 2. fix clock font color
.. 3. Background + shape for the button and the icon.
.. 4. improve statusbar -> give statusbar some margin by default
.. 5. improve cog icon to wifi signal? to explain the element_properties -> may already be done within the clock.

.. don't forget to talk about the interface as well.
.. When done with the entire documentation, maybe make the element names :ref:`Layout` or something.