# PaymentAdmin

  This is a demo app of paynow.com for adding functionality
  through django admin page. This Project is used to create,
  add money and pay money to different user wallets.

# ADMIN CREDENTIALS

  One can login to admin page after taking dump of sql file to
  local database. 

  :-- One can create users using command
        python manage.py createsuperuser

  :-- By default one can access admin by using below
      credentials
          username --- shubh_travclan
          password --- shubh@9028

# Technology Stack

  Python == 3.6.8
  
  Django == 3.0.5 
  
  MySql == 5.7.29

# Installation

## Install OS (Ubuntu) Requirements

    sudo apt-get update
    sudo apt-get upgrade

## Clone Project

    git clone https://github.com/shubham1408/PaymentAdmin.git

## Setup your virtual environment and install requirements.

### Ubuntu/Mac setup

    python3 -m venv travenv
    source travenv/bin/activate
    pip3 install -r paynowdemo/requirements.txt
    

## MySQL (database) setup

    sudo apt-get install mysql-server
    mysql -u root -p (for Ubuntu, you might need to run it as sudo mysql -u root -p)
    create database travclandb;
    grant usage on *.* to myuser@localhost identified by 'mypasswd';
    grant all privileges on travclandb.* to myuser@localhost;

obtain a dump of the database (convodb.sql from paynowdemo/travclandb.sql) and then add it to your local MySQL server  (ensure that you run MySQL from the directory with the dump file):

    use travclandb;
    source travclandb.sql;

## Running Development Server

   python manage.py runserver


**Note:** Never forget to enable virtual environment (`source travenv/bin/activate`) before running the above commands and use settings accordingly.
