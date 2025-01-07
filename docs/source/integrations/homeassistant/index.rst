Home Assistant
=================

The Home Assistant integration enables an inkBoard dashboard to function as a Home Assistant dashboard.
It connects to the websocket api, meaning the dashboard stays up to the date with your house as long as it stays connected.

Installation
--------------

Run the command to install the dependencies.

.. code-block:: console

    inkBoard install integration homeassistant_client

Configuration
--------------

It is configured under the ``home_assistant`` entry, and requires the following two options to connect:

- ``url``: The url to your Home Assistant server. Requires the port as well when connecting internally. For example ``101.0.0.0:8123``
- ``token``: A long lived api token to authenticate with the server. 
   - The token can be acquired by going to your server's frontend, then to your profile. 
     Under the security tab, at the bottom, you will see the *Long-lived access tokens*. Create a token (give it a recognisable name) and copy it to use with your config.

.. attention::
    Be careful with both your instance's url, and **especially** your access token.
    They can be used to gain full access to your house.
    Always put them in a ``secrets.yaml`` file, and reference them via the ``!secrets`` directive, so you're sure you don't accidentally share them somewhere.
    If you do accidentally compromise it, the token can be deleted on the same page as where you got it.

Aside from the ``home_assistant`` entry, the integration also allows usage of two other entries.

- ``entities`` can be used to subscribe to more entities than just those assigned to elements. It can also be used to run functions when an entity's state changes by supplying ``trigger_functions``.
- ``service_actions`` can be used to define service action calls with data, can be useful if you are calling a service in multiple places.

It also adds the shorthand function ``call-service-action``, which can be used to, for example, toggle a light by tapping an element.

.. This is done via a ``trigger_function``, which can also be set to a shorthand function -> not sure if custom trigger functions are implemented rn?

Below is a small basic config for the integration, although both the ``entities`` and ``service_actions`` key are not mandatory.

.. code-block:: yaml

    home_assistant:
      url: !secret ha_url
      token: !secret api_token

    entities:
      - entity_id: input_button.my_button
          trigger_functions:
            - function: custom:custom_trigger
              call_on_connect: true
    
    service_actions:
      my_action:
        action: light.toggle
        target:
          entity_id: climate.radiator




.. toctree::
    :hidden:

    Elements <elements>
    examples