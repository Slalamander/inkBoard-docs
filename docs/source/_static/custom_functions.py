"""A module with two small functions to use as examples for custom functions.

Use by requesting a function using 'custom:{function_name}'
"""

from typing import TYPE_CHECKING

from datetime import datetime as dt

from PythonScreenStackManager.elements import Button, PopupMenu, Icon, GridLayout
from PythonScreenStackManager.pssm.util import elementactionwrapper

from inkBoard import core as CORE

if TYPE_CHECKING:
    from PythonScreenStackManager.pssm_types import InteractEvent


def my_function(element: Button, interaction: "InteractEvent"):
    """A very basic custom function.

    Attach it as a tap_action to a Button element.
    When tapped, its text will to display the touched coordinates.
    """
    (x,y, _) = interaction
    element.update({"text": f"You touched coordinates {(x,y)}"})

@elementactionwrapper
def my_print_function():
    """A basic custom function using the `elementactionwrapper` decorator.
    
    It also shows how to interface  with the inkBoard core,
    which holds the core components for a running config.
    This includes, for example, the screen instance, a dict with all integrations,
    and as can be seen below, the device instance.
    """
    if CORE.device.has_feature("network"):
        network = CORE.device.network.SSID
        print(f"Connected to {network}")
    else:
        print("The device does not have the network feature :(")

def custom_trigger(trigger: "client.triggerDictType", client: "client.HAclient"):
    """A simple function to show how to work with trigger functions for home assistant entities.

    Parameters
    ----------
    trigger : client.triggerDictType
        The full element trigger. Contains the to_state, from_state, amongst others.
    client : client.HAclient
        The client object managing the connection to Home Assistant.
    """
    
    entity = trigger["entity_id"]
    new_state = trigger["to_state"]["state"]

    if trigger["from_state"] == None:
        ##from_state is none if the client connected, as it does not gather the previous state of the entity, just the current state.
        print(f"Entity {entity} is in state {new_state}")
    else:
        ##Although it prints it like this, keep in mind the function is triggered regardless of what triggered it.
        ##I.e. it can also be the case that the trigger was caused by an attribute changing.
        from_state = trigger["from_state"]["state"]

        popup: PopupMenu = CORE.screen.elementRegister["trigger-popup"]

        ##Since we call update later on, the title can be set like this.
        ##Otherwise, this can be done like this too, however, a call to update is required with updated=True passed.
        popup.title = trigger["to_state"]["attributes"].get("friendly_name","My Button")

        press_now = dt.fromisoformat(new_state)
        press_before = dt.fromisoformat(from_state)
        press_dt = press_now - press_before

        button_text = f"You pressed {entity} again after {press_dt.total_seconds()} seconds at {press_now}"
        buttonButton = Button(button_text, multiline=True)
        buttonIcon = Icon("mdi:gesture-tap-button", icon_color="homeassistant")

        subsc_num = len(client.stateDict)
        subscr_text = f"Subscribed to {subsc_num} entities"
        subscrButton = Button(subscr_text, multiline=True)
        subscrIcon = Icon("homeassistant", icon_color="homeassistant")

        menulayout = GridLayout([buttonIcon,buttonButton, subscrIcon, subscrButton], column_sizes=["r", "?"], columns=2, rows=None)

        popup.update({"menu_layout": menulayout})


        popup.show()

    return