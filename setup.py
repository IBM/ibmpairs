from setuptools import setup

def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except:
	    return 'sorry, no details available'

setup(
    name='ibmpairs',
    version='0.0.3',
    description='open source Python modules for the IBM PAIRS Geoscope platform',
    long_description=readme(),
    classifiers=[
      'Development Status :: 3 - Alpha',
      'License :: OSI Approved :: BSD',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 3',
      'Topic :: Scientific/Engineering :: GIS',
    ],
    keywords='IBM PAIRS GIS BigGeoData',
    url='http://github.com/ibm/ibmpairs',
    author='Physical Analytics, IBM Research',
    author_email='pairs@us.ibm.com',
    license='BSD-Clause-3',
    packages=['ibmpairs'],
    install_requires=[
        'numpy',
        'Pillow>=1.6',
        'pandas',
        'future',
        'requests>=2.4',
        'shapely',
## optional packages
#        'geopandas',
#        'geojson',
#        'gdal',
    ],
    test_suite='tests',
    tests_require=[],
    entry_points={
    },
    include_package_data=True,
    zip_safe=False,
)
