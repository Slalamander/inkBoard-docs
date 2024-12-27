Installation
=============

If you do not have Python installed yet, you can follow the the `ESPHome tutorial <https://esphome.io/guides/installing_esphome>`_. Make sure you install Python 3.9 (i.e. do not install the newest version). Simply follow the tutorial up to the point of installing ESPHome.
If you already have Python installed, I would advice to check the version. As of now, I can only confirm inkBoard to run on Python 3.9.

Make a folder somewhere to store all your configurations in a centralised location (not required, but I would recommand it). Open a terminal in that folder (On windows, right click and select *open in terminal*, on Linux, copy the path to the folder, open a terminal and use :code:`cd /the/path/to/inkboardfolder`).

In this folder, create a virtual environment to hold your inkBoard installation. This will help keep your Python installation clean, and makes restarting with a clean inkBoard installation easier.
Run this in the terminal to set up the virtual environment:

.. code-block:: console
    
    python3.9 -m venv .venv

Activate the virtual environment so inkBoard will be installed in it:

.. tab-set::
    :sync-group: commandline-code

    .. tab-item:: Windows
        :sync: windows

        .. code-block:: console
    
            ./.venv/Scripts/activate

    .. tab-item:: Linux
        :sync: linux

        .. code-block:: console

            source ./.venv/bin/activate

Next, install inkBoard Designer. This takes care of installing all dependencies and sets up an entry point, so activating the virtual environment afterwards should be taken care of by it.

.. code-block:: console

    pip install inkBoarddesigner

If everything went correct, you should now be able to run the version command, and get an output.

.. code-block:: console

    inkBoard version

Which should output something akin to this:

.. code-block:: console

    >>> inkBoard Version: 0.2.7
    >>> inkBoard designer Version: 0.2.0

.. note::
    
    If you want to start the designer, you can run the command below. However, the tutorial will first get started on writing a runnable configuration file.

    .. code-block:: console

        inkBoard designer