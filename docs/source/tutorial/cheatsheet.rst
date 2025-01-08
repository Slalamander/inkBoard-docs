
:description: A cheatsheet for important inkBoard concepts

.. highlight:: yaml

Cheatsheet
==========

In case you did not go through the full tutorial, or came back here for reference, this cheatsheet should quickly explain some important core concepts.

.. add: shorthand colors, duration stuff, dimensions, available background_shapes

.. grid:: 2
    :gutter: 3

    .. grid-item-card::  Elements

        Put elements on your dashboard to interact with.

        .. code-block:: yaml

            - type: Button
              text: Hello World!
              id: my-button

    .. grid-item-card:: Layouts

        Elements can be defined directly in layouts, or referenced via their ``id``.

        .. code-block:: yaml

            - type: GridLayout
              elements:
                - type: Button
                  text: Foo
                - my-button

    .. grid-item-card:: Dimensions

        Dimensions can often be set using strings, in order to use relative values.
        ``h`` and ``w`` for an element's height and width, ``H`` and ``W`` for the screen's height and width and
        and ``"?"`` in layouts to fill up available space.

    .. grid-item-card::  Colors

        You can define your own names for colors

        .. code-block:: yaml

            styles:
              shorthand_colors:
                inkboard: [19,54,91]

    .. grid-item-card:: Tile Layouts

        A ``tile_layout`` can be used to configure the placement of elements in a Tile.
        A ``","`` acts as a horizontal seperator, a ``";"`` as a vertical one.
        Encompassing elements within square brackets ``"["`` and ``"]"`` will put them in a sub layout.

        Use ``horizontal_sizes`` and ``vertical_sizes`` to size the tiles.
    
    .. grid-item-card:: Element Actions

        Properties like ``tap_action`` can be set using a dict. The ``data`` key defines arguments to pass to the called function,
        ``map`` defines attribute's who's value will be passed as arguments.

        Shorthand actions are available, and functions from other elements can be called via the ``element:`` identifier.

        .. code-block:: yaml

            tap_action:
              action: element:show-popup
              element_id: my-popup

    .. grid-item-card:: Durations

        Values typed with :py:class:`DurationType <PythonScreenStackManager.pssm_types.DurationType>`
        allow using strings like ``1h`` to set the duration, in addition to numerical values in seconds.

    .. grid-item-card:: ``element_properties``

        Tiles that have the ``element_properties`` property allow styling their child elements.
        Use the respective keys and under that define the properties for the element to set.





    .. grid-item-card:: Parent Colors

        Elements within layouts can use colors from their parent layout.
        Simply use the appropriate value when setting up a color.

        .. code-block:: yaml

            - type: TileLayout
              foreground_color: blue
              tile_layout: icon;text
              elements:
                icon:
                    - type: Icon
                      icon_color: foreground
                text:
                    - type: Button
                      font_color: foreground


    .. grid-item-card:: Substitutions

        Use substitutions to make references that can be changed easily.
        For example when trying to find a good color to use as a foreground.

        .. code-block:: yaml

            substitutions:
                a_color: yellow

            ...

            elements:
                - type: Button
                  font_color: ${a_color}
                - type: Icon
                  icon_color: ${a_color}

    .. grid-item-card:: Background Shapes

        Background shapes have a variety of options, like ``circle``, ``rounded_rectangle`` and ``octagon``.
        Using ``shape_settings`` they can be configured even more.
        Shapes are drawn using the `ImageDraw Module <https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html>`_ from Pillow.
