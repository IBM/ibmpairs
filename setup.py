#!/usr/bin/env python
from setuptools import setup

# define package version
version = '0.2.10'
# ... and record it for ibmpairs package
with open("ibmpairs/version.py", 'w') as f:
    f.write('# generated by setup.py\nversion = "{}"\n'.format(version))

def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except:
	    return 'sorry, no details available'

# read required packages
with open('requirements.txt') as f:
    reqPackList = [
        r.rstrip() for r in list(f)
        if '#' not in r
    ]
## optional packages
#   + [
#       'geopandas',
#       'geojson',
#       'gdal',
#   ]
with open('requirements-development.txt') as f:
    reqPackListDev = [
        r.rstrip() for r in list(f)
        if '#' not in r
    ]

setup(
    name='ibmpairs',
    version=version,
    description='open source Python modules for the IBM PAIRS Geoscope platform',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'License :: OSI Approved :: BSD License',
      'Programming Language :: Python :: 3',
      'Topic :: Scientific/Engineering :: GIS',
    ],
    keywords='IBM PAIRS GIS BigGeoData',
    url='https://ibmpairs.mybluemix.net',
    project_urls = {
        'Documentation': 'https://pairs.res.ibm.com/tutorial',
        'Source': 'https://github.com/ibm/ibmpairs',
        'Tracker': 'https://github.com/ibm/ibmpairs/issues',
    },
    author='Physical Analytics, IBM Research',
    author_email='pairs@us.ibm.com',
    maintainer='cmalbrec',
    license='BSD-Clause-3',
    packages=['ibmpairs','ibmpairs.external'],
    install_requires=reqPackList,
    test_suite='tests',
    tests_require=reqPackListDev,
    entry_points={
    },
    include_package_data=True,
    zip_safe=False,
)
