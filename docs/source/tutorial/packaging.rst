Packaging
==========

With a functional dashboard in place, it is time to ready ``tutorial.yaml`` to be deployed to a platform.
inkBoard supplies a (hopefully) convenient way to do this, by generating packages for the configuration file for the config's platform.
This is what the **Pack** button in the designer is for.

First off, the actual platform will need to be specified. Currently, the ``platform`` key under the ``device`` entry in the configuration is ``emulator``. 
This is value is meant as a placeholder, when you are simply designing a dashboard. It skips any validation checks for the device configuration as well.
For the tutorial, the ``desktop`` platform will be used.

The advantage of this platform is that functions basically the same as the designer itself, but just omits the user interface on the right.
When running it on the same platform (and in the same environment) as the designer installation, it also has access to the same resources. Meaning integrations present in the designer do not need to be installed seperately.

As the programme grows, and more platforms are added, it is likely that the types of packages will increase.


Installer Zip Package
-------------------------------
Currently, the Installer Zip Package is the only implemented package type. When you click the **Pack** button, you will be prompted to save a zip file.
inkBoard will create one with the supplied name, which contains a ``package.json`` file with information on the package (for example, inkBoard versions on which it was created).
This package contains the required yaml files from the base directory of the config, and the folders required for an inkBoard installation.

.. tip::
    If you want to include additional files with the package, like scripts, you can put them in the ``files`` folder. All contents are copied to the zip archive.



.. attention:: 
    It is not advised to install the zip package on the same machine as your designer installation.

    To run a configuration on there, run the install commands for platforms and integrations:

    .. code-block:: 
        
        inkBoard install platform desktop

    .. code-block:: 
        
        inkBoard install integrations <included integrations>
    
    |  
    |  In the future, this will be simplified to allow passing a configuration, such that only a single command will be needed.

