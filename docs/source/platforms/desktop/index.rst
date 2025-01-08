Desktop
========

The ``desktop`` platform can be used to have an inkBoard dashboard on your platform.
It's base features should work on any system that supports Python's standard UI interface (and Pillow).

Its features are relatively configurable, and can be fiddled with as you desire.
optionally, ``pywifi`` can be installed to implement the ``connection`` feature.

Due to limitations with how windows handles taskbar icons, when running as is, a python icon will show in the taskbar rather than the inkBoard icon.
This can only be prevented by packaging inkBoard into its own executable, instead of it being a simple python package.
This functionality may come in a future version, but for now, if that icon in the taskbar bugs you, the :doc:`/integrations/system_tray` integration can be used to have inkBoard show in the system tray, rather than the taskbar.


.. toctree::
    :hidden:

    self
    readme-page