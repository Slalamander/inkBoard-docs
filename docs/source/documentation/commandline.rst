Command Line
==============

inkBoard provides a couple of useful command line commands.

Run the help function to get a description printed in your terminal:

.. code-block::

    inkBoard -h

inkBoard provides functionality to install configuration packages. These packages can be made via the designer.
By running the install command with a package file, the zip file is extracted, and the internal platforms and integrations present are copied to the correct folder within the inkBoard directory.
It will also take care of prompting you for any dependencies that need to be installed.

Running a specific configuration fill can be done with the ``run`` command.

.. code-block::

    inkBoard run <configuration.yaml>

The designer can be run without specifying a configuration file, although it optionally also takes that as an argument to immediately boot up a configuration.
If the designer is not installed, it will instead throw an error message.

.. code-block::

    inkBoard designer

.. code-block::

    inkBoard install <my-package.zip>

Installing dependencies for already installed integrations and platforms is also possible. Respectively:

.. code-block::

    inkBoard install integration <dummy_integration>

.. code-block::

    inkBoard install platform <dummy_platform>

The version command will print the current version of inkBoard, and of the designer if it is installed.

.. code-block::

    inkBoard version