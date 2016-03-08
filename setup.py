from setuptools import setup, find_packages

__author__ = 'timhodson'

setup(name='tadc_import_validator',
      version='0.1.1',
      description='Validates CSV files for use in Talis Aspire Digitised Content data imports',
      url='http://talis.com',
      author='Talis Education Ltd',
      author_email='tgh@talis.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'unicodecsv',
          'logbook',
          'datetime',
      ],
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Development Status :: 4 - Beta',
          'Environment :: Other Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Text Processing',
          'Natural Language :: English',
      ],
      entry_points={
          'console_scripts': ['tadc-import-csv-validator=tadc_import_validator.command_line:main'],
      },
      zip_safe=False)
