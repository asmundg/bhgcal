from setuptools import setup, find_packages

setup(name='bhgcal',
      packages=find_packages(),
      install_requires=['python-dateutil',
                        'requests'],
      entry_points=dict(console_scripts=['bhgcal=bhgcal:main']))
