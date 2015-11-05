MHG-ERP
====================

# Environment
 * Please, execute this cmd: **sudo pip install -r requirements.txt**

# How to install

 1. create database in mysql: create database ERPSystem character SET utf8;
 1. sync database in project root path: python manage.py syncdb
 1. migrate database: python manage.py migrate
 1. test server : python manage.py runserver IP:PORT
 1. visit your web browser: IP:PORT

# Q&A
 1. When you login the website, you may meet the follow issue:
   **Site matching query does not exist**
   Solve: 
    * python manage.py shell 
    * from django.contrib.sites.models import Site
    * new_site = Site.objects.create(domain='foo.com', name='foo.com')



# How to deploy in production environment?
 1. Install necessary software
   * sudo apt-get install openssl libssl0.9.8 libssl-dev libpcre3 libpcre3-dev 
   * install nginx: download source code -> ./configure -> make -> sudo make install -> sudo /etc/init.d/nginx restart -> visit localhost in webbrowser
   * sudo apt-get install uwsgi uwsgi-core uwsgi-plugin-python
   * sudo pip install uwsgi
   * cd deploy -> sudo sh run.sh start|restart|stop|deploy|update
 2. Config your mysql server

# Lincenses
 This software uses GPLv3 lincense, SIE developer team own the copyright.

More information, you can visit our wiki pages.
