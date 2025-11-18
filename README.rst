|pypi| |actions| |codecov| |downloads| |clinicedc|

META EDC
========

Metformin treatment in Africa - META

* https://www.ucl.ac.uk/global-health/research/z-research/respond-africa/metformin-treatment-africa-meta
* https://www.inteafrica.org/related-projects/meta-trial/
* https://www.lstmed.ac.uk/research/departments/international-public-health/respond-africa/meta
* http://www.isrctn.com/ISRCTN76157257

py 3.12+ / DJ 5.2 using the `Clinic EDC <https://github.com/clinicedc/edc>`_ framework

This codebase is used for two randomized clinical trials:

____

META PHASE II:

(final version `0.1.77 <https://github.com/meta-trial/meta-edc/tree/0.1.77>`_)

Metformin Treatment for Diabetes Prevention in Africa: META Trial
TASO, MRC/UVRI/LSHTM, NIMR – TZ and Liverpool School of Tropical Medicine (ISRCTN76157257)
http://www.isrctn.com/ISRCTN76157257

____

META PHASE III:

A randomised placebo-controlled double-blind phase III trial to determine the effects of metformin versus placebo on the incidence of diabetes in HIV-infected persons with pre-diabetes in Tanzania.

Liverpool School of Tropical Medicine

EDCTP grant number: RIA2018CO-2513

Trial registration: ISCRTN 77382043

https://ico.org.uk/ESDWebPages/Entry/Z4763134

____

See also https://github.com/clinicedc/edc

|django|

Installation
------------

As of version 1.1.10, we are building and deploying with `uv <https://docs.astral.sh/uv>`_.

Here we assume you have your DB setup and already have your ``.env`` file.

First-time install
++++++++++++++++++

Assuming you are logged into the account ``myaccount``:

.. code-block:: bash

    mkdir -p ~/.etc/meta && \
    mkdir ~/edc && \
    cd ~/edc && \
    uv venv && \
    uv pip install -U meta-edc==1.5.2 && \
    wget https://raw.githubusercontent.com/meta-trial/meta-edc/1.5.2/manage.py && \
    uv pip freeze | grep meta-edc

Copy your ``.env`` file to ``~/.etc``.

Place this at or near the end of your ``.bashrc``:

.. code-block:: bash

    # >>> EDC using uv >>>
    export DJANGO_SETTINGS_MODULE=meta_edc.settings.uat
    export META_PHASE=3
    export DJANGO_BASE_DIR=/home/myaccount/edc
    export DJANGO_ENV_DIR=/home/myaccount/.etc/
    cd ~/edc
    source .venv/bin/activate
    export PATH="/home/myaccount/edc:$PATH"
    # <<< EDC using uv <<<

Source ``.bashrc`` and run ``manage.py check``.

.. code-block:: bash

    source ~/.bashrc && \
    cd ~/edc && \
    python manage.py check

If all is OK, run ``migrate``:

    Explicitly specify the settings file when using ``migrate``.

    * live: ``--settings=meta_edc.settings.live``
    * uat: ``--settings=meta_edc.settings.uat``
    * debug:  ``--settings=meta_edc.settings.debug``


.. code-block:: bash

    cd ~/edc && \
    python manage.py migrate --settings=meta_edc.settings.live

Update an existing install
++++++++++++++++++++++++++

From the above example:

.. code-block:: bash

    cd ~/edc && \
    uv venv --clear && \
    uv pip install -U meta-edc==1.5.2 && \
    wget -O manage.py https://raw.githubusercontent.com/meta-trial/meta-edc/1.1.10/manage.py && \
    uv pip freeze | grep meta-edc && \
    python manage.py check

If all is OK, run ``migrate``

.. code-block:: bash

    cd ~/edc && \
    python manage.py migrate --settings=meta_edc.settings.live



.. |pypi| image:: https://img.shields.io/pypi/v/meta-edc.svg
    :target: https://pypi.python.org/pypi/meta-edc

.. |actions| image:: https://github.com/meta-trial/meta-edc/actions/workflows/build.yml/badge.svg
  :target: https://github.com/meta-trial/meta-edc/actions/workflows/build.yml

.. |codecov| image:: https://codecov.io/gh/meta-trial/meta-edc/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/meta-trial/meta-edc

.. |downloads| image:: https://pepy.tech/badge/meta-edc
   :target: https://pepy.tech/project/meta-edc

.. |django| image:: https://www.djangoproject.com/m/img/badges/djangomade124x25.gif
   :target: http://www.djangoproject.com/
   :alt: Made with Django

.. |clinicedc| image:: https://img.shields.io/badge/framework-Clinic_EDC-green
   :alt:Made with clinicedc
   :target: https://github.com/clinicedc
