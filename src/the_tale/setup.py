# coding: utf-8
import re
import json
import setuptools



with open('./the_tale/meta_config.json') as f:
    config = json.loads(f.read())
    VERSION = re.search('((\d+\.?)+)', config['version']).group(0)


setuptools.setup(
    name='TheTale',
    version=VERSION,
    description='Zero Player Game with indirect character controll',
    long_description = 'Zero Player Game with indirect character controll',
    url='https://github.com/Tiendil/the-tale',
    author='Aleksey Yeletsky <Tiendil>',
    author_email='a.eletsky@gmail.com',
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'Topic :: Games/Entertainment',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',

        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',

        'Natural Language :: English',
        'Natural Language :: Russian'],
    keywords=['gamedev', 'the-tale', 'game development', 'zpg', 'zero player game'],
    packages=setuptools.find_packages(),
    install_requires=['psycopg2==2.6.2',
                      'kombu==4.0.0',
                      'postmarkup==1.2.2',
                      'Markdown==2.6.7',
                      'xlrd==1.0.0',
                      'MarkupSafe==0.23',
                      'boto3==1.4.1',
                      'unicodecsv==0.14.1',
                      'django-redis==4.5.0',
                      'psutil==4.4.2'],

    include_package_data=True,
    test_suite = 'tests' )
