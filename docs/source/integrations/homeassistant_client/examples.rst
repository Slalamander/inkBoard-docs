Examples
==========

A fully working example for the Home Assistant integration can already be found in the designer repo.
See the ``homeassistant_example.yaml`` in the `example folder <https://github.com/Slalamander/inkBoarddesigner/tree/main/examples>`_.
To get that example working, you will also need to fill out the entries in ``ha_substitutions.yaml``, following the directions in the comments.
The configuration will automatically use those substitutions in the config.

Below are some examples from that file with a little more explanation than what is in the file.
The substitution entities have also been changed for generic entity ids.

Calling Service Actions
--------------------------

Various elements will be set a ``tap_action`` to call predefined service when given an entity and no ``tap_action`` is set yet.
For example, the ``Icon`` in the next section will already be configured to toggle ``light.livingroom``.
However, it may be desirable to call a service action from other elements, or call a different service action from an element.
This can be done via the shorthand ``call-service-action``.
The ``data`` key of the action can then be set to the same yaml you'd use to call the service action from Home Assistant.
The example below will allow a ``Button`` connected to a temperature sensor to toggle the livingroom light when tapped.

.. code-block:: yaml

    - type: Button
      entity: sensor.temperature
      tap_action:
        action: call-service-action
        data:
          action: light.toggle
          target:
            entity_id: light.livingroom

State Styles
-------------

The ``state_styles`` is relatively straight forward.
If the entity's state changed, these keys can be matched to a state, and the element's properties will change accordingly.
If the element has an ``entity_attribute`` set, the state is considered to be the value of that attribute.
It can be used to show the state of a light, for example.

.. code-block:: yaml

    - type: Icon
      background_color: black
      background_shape: circle
      entity: light.livingroom
      state_styles:
        "on":
          icon: mdi:lightbulb
          icon_color: white
        "off":
          icon: mdi:lightbulb-off
          icon_color: gray

``state_styles`` can also be made conditional by setting ``state_conditionals`` to ``true``.
In here, ``state`` is the variable matching the value of the entities state or linked attribute.

.. code-block:: yaml

    - type: Button
      entity: input_number.counter
      id: button-style
      state_conditionals: true
      state_styles:
        "default": "Eh"
        "state > 2": "That's Something"
        "state < -2": "This is even less than eh"

Attribute Styles
-----------------

``attribute_styles`` are similar to ``state_styles``, just a lot more flexible (and consequently, more complex to use).
They are applied in order, so if multiple conditions evaluate to ``true``, the properties that are updated will take on the last value from a ``true`` condition.
The styles are supplied as a list. The ``attribute`` key specifies the entity's attribute to check, with ``state`` being a special value to use the state instead of an attribute.
Under the ``states`` key, you can define a list of conditions that will be checked, via the same logic as the ``state_styles`` example above.
An ``else`` key can also be provided, which specifies the element properties to apply if none of the conditions evaluate to ``true``.

.. code-block:: yaml

    - type: Button
      entity: weather.home
      state_conditionals: true
      attribute_styles:
        - attribute: temperature
          states:
            - state: state > 19
              properties:
                background_color: green
            - state: state < 7.5
              properties:
                background_color: gray
          else:
            background_color: white
        - attribute: state
          states:
            - state: "'rain' in state"
              properties:
                font_color: steelblue
            - state: "'sun' in state"
              properties:
                font_color: yellow
          else:
            font_color: black

Trigger Functions
------------------

Currently it is not possible yet to give elements a custom trigger function, however entities can be given one.
A trigger function takes two arguments, a ``trigger``, which is a dict holder the trigger data, and the ``client``, which is the object managing the connection to Home Assistant.
The example below will simply print the last time a button was pressed when inkBoard starts.
However, in the full example file, this example is expanded upon to also allow showing a popup when the button is pressed.
In general, I would advise taking a look at the full example, as it shows a lot of the API features not available in the YAML config.

.. code-block:: yaml

    entities:
      - entity_id: input_button.my_button
          trigger_functions:
            - function: custom:custom_trigger
              call_on_connect: true


.. code-block:: python

    from inkBoarddesigner.integrations.homeassistant_client import client

    def custom_trigger(trigger: "client.triggerDictType", client: "client.HAclient"):
        """A simple function to show how to work with trigger functions for home assistant entities.
        """
        
        entity = trigger["entity_id"]
        new_state = trigger["to_state"]["state"]

        if trigger["from_state"] == None:
            ##from_state is none if the client connected, as it does not gather the previous state of the entity,
            ## just the current state.
            print(f"Entity {entity} is in state {new_state}")

.. tip::
    If you want to access the state of other entities, you can use ``client.stateDict``, which is a dict the ids of all subscribed entities and their last received state.

As a quick reference, here is the full ``custom_trigger`` function from ``custom_functions.py``.

.. literalinclude:: /_static/custom_functions.py
    :language: python
    :caption: A custom trigger to open a popup
    :linenos:
    :start-at: def custom_trigger
    :end-at: return

Custom Element
-----------------

Custom elements can be made similarly as via regular custom elements.
It is useful to import the ``HAElement`` as a baseclass, as it provides the functionality for the ``entity`` property, ``state_styles``, etc.
Otherwise, the element needs to be given a ``trigger_function`` in addition to the usual required methods.
