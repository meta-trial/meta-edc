|pypi| |actions| |codecov| |downloads|


META Edc
--------

This codebase is used for two randomized clinical trials:

____

META PHASE II:

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

To setup and run a test server locally

You'll need mysql. Create the database

.. code-block:: bash

  mysql -Bse 'create database meta character set utf8;'


Create a virtualenv, clone the main repo and checkout master

.. code-block:: bash

  conda create -n edc python=3.7
  conda activate edc


Clone the main repo and checkout master

.. code-block:: bash

  mkdir ~/projects
  cd projects
  https://github.com/meta-trial/meta-edc.git
  cd ~/projects/meta-edc
  git checkout master


Copy the test environment file

.. code-block:: bash

  cd ~/projects/meta-edc
  git checkout master
  cp .env.tests .env


Edit the environment file (.env) to include your mysql password in the ``DATABASE_URL``.

.. code-block:: bash

  # look for and update this line
  DATABASE_URL=mysql://user:password@127.0.0.1:3306/meta


Continue with the installation

.. code-block:: bash

  cd ~/projects/meta-edc
  git checkout master
  pip install .
  pip install -U -r requirements/stable-v0.1.10.txt
  python manage.py migrate
  python manage.py import_randomization_list
  python manage.py import_holidays


Create a user and start up `runserver`

.. code-block:: bash

  cd ~/projects/meta-edc
  git checkout master
  python manage.py createsuperuser
  python manage.py runserver


Login::

  localhost:8000


Once logged in, go to you user account and update your group memberships. As a power user add yourself to the following

* ACCOUNT_MANAGER
* ADMINISTRATION
* AE
* AE_REVIEW
* CLINIC
* DATA_MANAGER
* DATA_QUERY
* EVERYONE
* EXPORT
* LAB
* LAB_VIEW
* PHARMACY
* PII
* RANDO
* REVIEW
* SCREENING
* TMG
* UNBLINDING_REQUESTORS
* UNBLINDING_REVIEWERS


.. |pypi| image:: https://img.shields.io/pypi/v/meta-edc.svg
    :target: https://pypi.python.org/pypi/meta-edc

.. |actions| image:: https://github.com/meta-trial/meta-edc/workflows/build/badge.svg?branch=develop
  :target: https://github.com/meta-trial/meta-edc/actions?query=workflow:build

.. |codecov| image:: https://codecov.io/gh/meta-trial/meta-edc/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/meta-trial/meta-edc

.. |downloads| image:: https://pepy.tech/badge/meta-edc
   :target: https://pepy.tech/project/meta-edc

.. |django| image:: https://www.djangoproject.com/m/img/badges/djangomade124x25.gif
   :target: http://www.djangoproject.com/
   :alt: Made with Django
