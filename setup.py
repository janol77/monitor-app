from setuptools import find_packages, setup

setup(name="Monitor-app",
      version = "0.1",
      description = "Monitor-app",
      author = "Alejandro Medina",
      platforms = ["any"],
      license = "GPLv3",
      include_package_data=True,
      packages = find_packages(),
      install_requires = ["Flask==0.11.1",
                          "mongoengine==0.10.6",
                          "flask-mongoengine==0.8",
                          "Flask-Login==0.4.0",
                          "gunicorn==19.6.0",
                          "pyquery==1.2.17",
                          "Flask-WTF==0.13.1",
                          "Flask-Principal==0.4.0",
                          "unittest2==1.1.0",
                          "simplejson==3.10.0",
                          "Flask-Script==2.0.5"],
      )