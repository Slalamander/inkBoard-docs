Home Assistant Elements
==========================

Elements can be connected to the Home Assistant client by giving them an ``entity`` key in their config.
This signals to the client that it should update this element when the entity's state changes. Using ``state_styles`` and ``attribute_styles`` the properties of an element can be updated according to the entity's state.
:py:class:`Buttons <PythonScreenStackManager.elements.Button>` and :py:class:`Icons <PythonScreenStackManager.elements.Icon>` can be used with any element, with the latter showing the entity's state by default. If an element should reflect the state of an attribute instead, the ``entity_attribute`` key can be set.
:py:class:`Sliders <PythonScreenStackManager.elements.Slider>`, :py:class:`Counters <PythonScreenStackManager.elements.Counter>` and :py:class:`DropDowns <PythonScreenStackManager.elements.DropDown>` can also be used as is, although their entity's a limited to appropriate domains.

See :doc:`examples` for how to style elements using ``state_styles`` and ``attribute_styles``.


The client also supplies various elements itself, which make it a lot more convenient to implement certain entity types and control them.

.. py:module:: inkBoarddesigner.integrations.homeassistant_client.HAelements

.. auto-inkboardelement:: StateButton

.. auto-inkboardelement:: EntityTile

.. auto-inkboardelement:: PersonElement

.. auto-inkboardelement:: MediaPlayer

.. auto-inkboardelement:: WeatherElement

.. auto-inkboardelement:: WeatherForecast

.. auto-inkboardelement:: EntityTimer


.. also explain how to write a custom element/trigger function?