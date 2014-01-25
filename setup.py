from setuptools import setup, find_packages
import teslacoil

setup(
    name='django-teslacoil',
    version=teslacoil.__version__,
    packages=find_packages(exclude=['test_project']),
    url='https://github.com/celerityweb/django-teslacoil/',
    license='LGPL v3 - see LICENSE file',
    author='See AUTHORS file',
    description='TeslaCoil is a Django application to decouple the stock '
                'django.contrib.admin site into ReSTful APIs and to build '
                'UX-rich clients using popular Javascript MVC framework'
)
