#!/usr/bin/env python
from distutils.core import setup


setup(name='postcalc',
        version='0.1',
        url='https://github.com/temaput/postcalc',
        author="Artem Putilov",
        author_email="putilkin@gmail.com",
        description="calculate russian post delivery fee",
        long_description=open('README.md').read(),
        keywords="Russianpost, delivery, tarifs",
        license='BSD',
        py_modules=['tarifcalc'],
        # package_data={'drawinvoice': ['fonts/*.ttf']},
        requires=['httplib2'],
        # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=['Environment :: Commercial',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: Unix',
            'Programming Language :: Python']
        )

