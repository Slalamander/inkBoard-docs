
Customising
============

.. highlight:: python

inkBoard also allows adding custom elements and functions relatively easily.
Both can be parsed, in the appropriate places, using the ``custom:`` identifier.
This page is a small reference on writing your own custom elements and functions.
As a reference, these files are included in the `example configuration <https://github.com/Slalamander/inkBoarddesigner/tree/main/examples>`_ in the designer repo.
For this part of the tutorial, some experience with coding in Python can be useful to fully understand what is going on.

Custom Functions
-----------------

To get started, in the folder where your configuration file is located, navigate to ``custom/functions``.
You can create these folder if they do not exist yet.
In the functions folder, create a new file ``custom_functions.py``.

Lets start of with importing the necessary modules.
From ``PythonScreenStackManager.elements``, the elements that will be used within functions are imported.
From ``PythonScreenStackManager.pssm.util``, the ``elementactionwrapper`` is imported.
This is a decorator that can be used to easily allow functions to be used as element actions, without requiring the parameters that are usually passed.

In line 8, the inkBoard ``core`` object is imported. This object holds all objects of the current running configuration, like ``CORE.screen``, ``CORE.device`` and ``CORE.config``.
Type hinting is in place, so getting information on the objects attached to it is relatively straight forward with an IDE.

Lastly, under ``TYPE_CHECKING``, a few modules are *"imported"* for type hinting.
This generally makes it a bit easier to code functions, since it makes it easier for an IDE to show what properties, functions and the like are available for an object.
Keep in mind that imports under ``TYPE_CHECKING`` must be wrapped in quotation marks when referencing them.

.. literalinclude:: /_static/custom_functions.py
    :caption: Importing inkBoard modules and required modules
    :linenos:
    :start-at: import
    :end-before: def
    :emphasize-lines: 5,6, 8

.. note::
    Chances are PythonScreenStackManager will change its name to be more convenient to include and reference in the documentation.

First off, make a function that will update a button to show the coordinates you tapped on.
The coordinates can be extracted from the :py:class:`InteractEvent <PythonScreenStackManager.pssm_types.InteractEvent>`.
Subsequently, call ``element.update`` to update the element that was tapped on.
The ``update`` function takes a dict under ``updateAttributes``, which indicates which properties to update to what value.
By giving it a ``text`` key, the element's ``text`` property will be updated to the new value.

.. literalinclude:: /_static/custom_functions.py
    :caption: A custom function to show tap coordinates
    :linenos:
    :start-at: def
    :end-at: element.update

.. tip::
    Custom functions can also be async (preferably so, even). The screen takes care that functions do not block the event loop.
    Some base functions, like ``update`` also have async equivalents, like ``async_update``.

To now assign the function to an element, we can set the ``tap_action`` of ``my-button`` to ``custom:my_function``.
When running the config, you will see that ``my-button`` now shows the coordinates when you tap it.

.. code-block:: yaml

      - type: Button
        id: my-button
        text: Hello World!
        font_color: white
        font_size: 0
        fit_text: true
        font: default-bold
        tap_action: custom:my_function

The ``elementactionwrapper`` may be useful if you want to use a certain function in multiple places, or for multiple purposes.
It catches out the element and interactevent from the function call, and subsequently calls the function with everything else.
For now, a simple function that prints the network the device is currently connected to will suffice.
The network can be accessed from the ``CORE`` object, via the ``device`` attribute.
Be aware that accessing the network is only available on devices that have that feature.

.. literalinclude:: /_static/custom_functions.py
    :caption: Using an ``elementactionwrapper``
    :linenos:
    :start-at: @element
    :end-at: print("The device

Assigning it to an element can be used in the same way as ``my_function``.

.. important::
    Custom functions can be defined in python files and modules in the ``custom/functions`` folder.
    inkBoard collects all functions from all files, as well as functions in the ``__init__.py`` file in modules.
    Custom functions can be used by calling them via the identifier ``custom:``

Custom Elements
-----------------
