# EVM-GM Tool
Hi! I'm Manh. I'm a student at Ha Noi University of Sicence and Technology.
This is my graduation thesis project.
In this project I've researched about Project Managent method include: 

 - EVM (Earned Value Management)
 - GM (Growth Model) 

And then, I also researched about how to Combined EVM & GM in Software Project Management.

After about 9 month, this is my tool that I created to demo EVM-GM method.
Bellow is all step you need to do to set up tool.
## Enviroment
OS: Ubuntu 16.04
Language: Python
Framework: Django

## 1. Clone app project from github

    git clone https://github.com/manhnd1112/GR

Project will be cloned into **GR** folder, after clonning ended, go into **GR** folder by run the command bellow:

    cd GR
## 2. Install Apache2

    sudo apt-get install apache2
At the end of the installation process, Ubuntu 16.04 starts Apache. The web server should already be up and running.

We can check with the  `systemd`  init system to make sure the service is running by typing:

```
● apache2.service - LSB: Apache2 web server
   Loaded: loaded (/etc/init.d/apache2; bad; vendor preset: enabled)
  Drop-In: /lib/systemd/system/apache2.service.d
           └─apache2-systemd.conf
   Active: active (running) since Fri 2018-05-25 15:13:14 UTC; 15s ago
     Docs: man:systemd-sysv-generator(8)
   CGroup: /system.slice/apache2.service
           ├─9402 /usr/sbin/apache2 -k start
           ├─9405 /usr/sbin/apache2 -k start
           └─9406 /usr/sbin/apache2 -k start
May 25 15:13:13 gr-deploy systemd[1]: Starting LSB: Apache2 web server...
May 25 15:13:13 gr-deploy apache2[9367]:  * Starting Apache httpd web server apache2
May 25 15:13:14 gr-deploy apache2[9367]:  *
May 25 15:13:14 gr-deploy systemd[1]: Started LSB: Apache2 web server.
```

##  3. Mysql & Phpmyadmin
To install it, simply update the package index on your server and install the default package with `apt-get`

    sudo apt-get update
    sudo apt-get install mysql-server

Testing Mysql

    systemctl status mysql.service
You'll see output similar to the following:
```
● mysql.service - MySQL Community Server
   Loaded: loaded (/lib/systemd/system/mysql.service; enabled; vendor preset: en
   Active: active (running) since Wed 2016-11-23 21:21:25 UTC; 30min ago
 Main PID: 3754 (mysqld)
    Tasks: 28
   Memory: 142.3M
      CPU: 1.994s
   CGroup: /system.slice/mysql.service
           └─3754 /usr/sbin/mysqld
```
If MySQL isn't running, you can start it with `sudo systemctl start mysql`.

For an additional check, you can try connecting to the database using the  `mysqladmin`  tool, which is a client that lets you run administrative commands. For example, this command says to connect to MySQL as  **root**  (`-u root`), prompt for a password (`-p`), and return the version.

```
systemctl status mysql.service
```

You should see output similar to this:

Output

```
mysqladmin  Ver 8.42 Distrib 5.7.16, for Linux on x86_64
Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Server version      5.7.16-0ubuntu0.16.04.1
Protocol version    10
Connection      Localhost via UNIX socket
UNIX socket     /var/run/mysqld/mysqld.sock
Uptime:         30 min 54 sec

Threads: 1  Questions: 12  Slow queries: 0  Opens: 115  Flush tables: 1  Open tables: 34  Queries per second avg: 0.006
```
This means MySQL is up and running.
## 4. Install Phpmyadmin
We can install phpMyadmin by updating our local package index and then using the  `apt`  packaging system to pull down the files and install them on our system:
```
$ sudo apt-get update
$ sudo apt-get install phpmyadmin
```
Then you need to include PHPMyAdmin inside apache configuration.
```
$ sudo nano /etc/apache2/apache2.conf
```
After adding the above into file apache2 config, run following commands:
```
$ sudo ln -s /etc/phpmyadmin/apache.conf /etc/apache2/conf-available/phpmyadmin.conf
$ sudo a2enconf phpmyadmin.conf
$ sudo service apache2 reload
```
## 5. Install Python, packages & Django
### Install Python via commands:

    sudo add-apt-repository ppa:jonathonf/python-3.6
    sudo apt-get update
    sudo apt-get install python3.6
    
Now you have three Python versions, use `python` command for version 2.7, `python3`for version 3.5, and/or `python3.6` for version 3.6.1.
### Install pip (package management system)

    sudo  apt-get -y install python3-pip
	
### Install django
Go to project folder, type following commands to install django:

    cd GR
    sudo python3 setup.py install
Then, you can use bellow command to test for ensure django has been installed:

    django-admin.py --version
Above command will return lastest installed Django version.
## 6. Create database, config & run migration 
Use bellow command to log into mysql console:
```
mysql -u root -p
```
Then, you'll see output similar the following:
```
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 22
Server version: 5.7.22-0ubuntu0.16.04.1 (Ubuntu)
Copyright (c) 2000, 2018, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql>
```
In the console, run following commands to create & check database:
```
create database gr; # create new database with name 'gr'
show databases;     # check has database been created yet
exit; 				# exit mysql console
```
Next, we need to create file config `env.py` for tool by copy example file `env_example.py` :
```
$ cd GR/evm_gm_tool/evm_gm_tool/
$ cp env_example.py env.py
```
Then open file `env.py` and change file with server informations:
```
ENV_ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
ENV_DB_HOST = ''
ENV_DB_DATABASE = ''
ENV_DB_USERNAME = ''
ENV_DB_PASSWORD = ''
ENV_SERVER_IP = '127.0.0.1'
ENV_SERVER_PORT = '8000'
ENV_PAGE_LIMIT = 10
```
Next, we're going to install other packages:
```
# install "mysqlclient"
$ sudo apt-get install libmysqlclient-dev
$ pip3 install mysqlclient
# install "xlrd" module for read file excel
$ sudo pip3 install xlrd
# install "numpy" module 
$ sudo pip3 install numpy
# install "scipy" module
$ sudo pip3 install scipy
# install "Pillow" module
$ sudo pip3 install Pillow

```
Next, you need to run migration to create tables for database:
```
python3 manage.py migrate
```
## 7. Create super user for system
```
$ cd GR/evm_gm_tool/
$ python manage.py createsuperuser 
```
Then, you'll see output that require you enter super user informations:
```
Username (leave blank to use 'nguyendinhmanh11k58'): manhnd
Email address: nguyendinhmanh11k58@gmail.com
Password: 
Password (again): 
Superuser created successfully.
```
## 8. Run Tool
After finished all setting above, you can run tool.
You can run tool in local by following command:
```
$ python manage.py runserver --insecure
```
Or, if you deploy tool to a server (like aws ec2, google cloud, ...) you can run tool to allow access as global:
```
$ python manage.py runserver <internal_private_ip>:<port> --insecure
# something like:
# python manage.py runserver 10.xxx.0.x:8000 --insecure
```
Now, you can access to EVM-GM Tool.
## 9. Request A Demo
You can see my EVM-GM Tool demo by access here:
```
http://35.234.47.119:8000/
```
Then, login with following account info:

 - **Username:** guide
 - **Password:** 12345678

## Some screenshots of the EVM-GM Tool
#### Main Dashboard
![Main Dashboad](https://drive.google.com/uc?id=1s98isCZSTQqSPih0uZGnWbYOCfOiXh6j)

#### Project Dashboard
![Project dashboard](https://drive.google.com/uc?id=1aFVVnSe8lsQ_-nE5JrdXzJ2CoAFJaO9T)

#### Project Edit
![Project Edit](https://drive.google.com/uc?id=1_AvRqPvyR-Gr5aizBEwJD0Ax-_6zZSeU)

#### User Dashboard
![User dashboard](https://drive.google.com/uc?id=1lFn_DyLz9-DXuL5iFSxfPZqLnrgYLNAx)

#### Estimate At Complate
![Estimate](https://drive.google.com/uc?id=1ptqYB8YNOKBB0VKF4ZUh0v9TZfICdLvZ)

#### PE, MAPE
![mape](https://drive.google.com/uc?id=1oN3ec1fWczcvhzQYsqhk6Nhlt1IECm6h)

## Some info about author

 - Full Name: Nguyen Dinh Manh
 - Birthday: 11/12/1995
 - University: Ha Noi University of Sicence & Technology
 - Major: Software Development Engineer
 - Address: Nam Sach, Hai Duong, Viet Nam
