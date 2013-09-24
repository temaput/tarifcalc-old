#!/usr/bin/env python
from setuptools import setup


setup(name='tarifcalc',
        version='0.1',
        py_modules=['tarifcalc'],
        setup_requires=['httplib2'],
        include_package_data=False,
        # package_data={'drawinvoice': ['fonts/*.ttf']},
        url='https://github.com/temaput/postcalc',
        author="Artem Putilov",
        author_email="putilkin@gmail.com",
        description="calculate russian post delivery fee",
        long_description=open('README.md').read(),
        keywords="Russianpost, delivery, tarifs",
        license='BSD',
        # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=['Environment :: Commercial',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: Unix',
            'Programming Language :: Python']
        )

