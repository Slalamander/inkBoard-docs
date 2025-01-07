Kobo
======

The ``kobo`` platform is what inkBoard was originally developed for.
The basics were provided by the `PythonScreenStackManager Package <https://github.com/Mavireck/Python-Screen-Stack-Manager>`_
and from there things got rather out of hand on my end.

The platform implements the following features:

- ``backlight``
- ``battery``
- ``network``
- ``interactive``
- ``rotation``
- ``auto_start``
- ``power``

And optionally also provides the ``connection`` feature.

Currently, is has been tested and confirmed to work on these devices:

- Kobo Glo HD
- Kobo Glo (Technically a Tolino Shine running on Kobo Firmware)

The basis for printing is the `fbink library <https://github.com/NiLuJe/FBInk/tree/master>`_ by NiLuJe.
This means inkBoard should be able to run on any device that can install that package and its included python package.
Certain features are linked via the filesystem however, so it could be that they do not link up on other devices.
That will be updated as more devices are tested.

The fbink library is also available for kindle. I have still not managed to get my hands on one however, so I have not tested with it.
If you happen to do so, please let me know if it works! I suspect a few things may be different, but who knows, it might work out of the box.

.. toctree::
    :hidden:

    self
    readme-page