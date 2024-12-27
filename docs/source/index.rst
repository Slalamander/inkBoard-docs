.. inkBoard documentation master file, created by
   sphinx-quickstart on Tue Dec 24 13:36:32 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

:layout: landing
:description: Landing page for inkBoard.

.. image:: /_static/images/logo.svg

inkBoard aims to provide a unified way of creating dashboards for various uses, on various devices. 
The dashboards are entirely image based, meaning all that is needed to make it work is a way to print pixels onto a screen using Python.
inkBoard takes care of building your dashboard from the configuration, integrating extensions and platforms, and making it all easy to share with your own devices, or others online.
To aid in designing dashboards, inkBoard also provides a seperate designer package, allowing dashboards to made outside of any device limitations (except those of the PC it is running on).

.. container:: buttons

   `Docs </install/>`_
   `inkBoard <https://github.com/Slalamander/inkBoard>`_
   `inkBoard Designer <https://github.com/Slalamander/inkBoarddesigner>`_
   `PythonScreenStackManager <https://github.com/Slalamander/PythonScreenStackManager>`_


.. grid:: 1 1 2 3
    :gutter: 2
    :padding: 0
    :class-row: surface

    .. grid-item-card::  :material-regular:`invert_colors;2em;sd-text-primary` Image Based

        As long as it can run Python and print images, it can display inkBoard dashboards (performance not guaranteed).

    .. grid-item-card::  :material-regular:`notes;2em;sd-text-primary` YAML Configured

        Dashboards can be configured entirely within YAML. Python experience is not required, just some comfort with using the command line.

    .. grid-item-card:: :material-regular:`brush;2em;sd-text-primary` Emulate and Design

        A UI interface to ease the design process and provide options to emulate the platform of your dashboard.

    .. grid-item-card::  :material-regular:`apps;2em;sd-text-primary` Integrate and Extend
        
        Extend your dashboard's capabilities with various integrations, or use your own custom functions and elements.


    .. grid-item-card:: :material-regular:`home;2em;sd-text-primary` Home Assistant Inspired
        :link: /customisation/colors/

        Inspired by, and written for, Home Assistant, inkBoard's syntax is similar to that of Home Assistant's yaml dashboards, with a mixture of ESPHome thrown in too.

    .. grid-item-card:: :material-regular:`folder;2em;sd-text-primary` Package, Install, Run
        :link: /extensions/nbsphinx/

        Package any configuration you made, including any required integrations and platforms. Easily install every requirement via the command line, and run your new dashboard.
        


It is build on `PythonScreenStackManager <https://github.com/Slalamander/PythonScreenStackManager>`_ as the dashboarding backend, so everything  

It includes a dashboarding system that is build entirely on `Pillow <https://pillow.readthedocs.io/en/stable/?badge=latest#>`_,
Don't put this here, too technical

Add your content using ``reStructuredText`` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.

.. toctree::
    :caption: Tutorial
    :name: tutorialtree
    :hidden:

    tutorial/index
    tutorial/installation
    tutorial/configuration

.. toctree::
   :maxdepth: 2
   :caption: Contents:

