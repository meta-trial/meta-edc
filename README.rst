meta-edc
--------


Metformin Treatment for Diabetes Prevention in Africa: META Trial


TASO, MRC/UVRI/LSHTM, NIMR – TZ and Liverpool School of Tropical Medicine (ISRCTN76157257)


http://www.isrctn.com/ISRCTN76157257



Installation
------------

To setup and run a test server locally

You'll need mysql.

.. code-block:: bash

  mysql -Bse 'create database meta character set utf8;'

.. code-block:: bash

  conda create -n edc python=3.7
  conda activate edc
  mkdir ~/projects
  cd projects
  https://github.com/meta-trial/meta-edc.git
  cd ~/projects/meta-edc
  git checkout master
  cp .env.tests .env
  
Edit the environment file to include your mysql password in the ``DATABASE_URL``

.. code-block:: bash

  cd ~/projects/meta-edc
  git checkout master
  mysql://user:password@127.0.0.1:3306/meta
    
Continue with the installation

.. code-block:: bash
  cd ~/projects/meta-edc
  git checkout master
  pip install .
  pip install -U -r requirements/stable-v0.1.10.txt
  python manage.py migrate
  python manage.py import_randomization_list
  python manage.py import_holidays
  python manage.py createsuperuser
  python manage.py runserver
