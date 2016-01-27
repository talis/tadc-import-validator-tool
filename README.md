# TADC Import Validator

For use when preparing files for bulk import of requests into TADC.

TADC Import Validator takes a CSV file and validates that each row matches the validation used in TADC. This means that you can iteritavely test that a file is correct before atempting to upload into TADC.

## Installation

You can either install from source or using pip.

```(bash)
# using pip
pip install tadc-import-validator
```

```(bash)
# from source
cd tadc-import-validator-tool
python setup.py install
```

## Module

The import validator is created as a module so that you can use it's validation features in other code.

```(python)
# import the module
from tadc_import_validator.tadc_import_row import TADCImportRow

# instantiate a new import row
import_row = TADCImportRow()

# Either load the columns one by one - useful if you are building a row from some other data source.
import_row.add_data_to_column('A', hierarchy_data[0])
import_row.add_data_to_column('B', hierarchy_data[1])

# Or load the row from a list. This example loads and validates each row from a CSV reader.
with open(self.csv_file_name) as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',', dialect='excel', quotechar='"')
	row_counter = 0
	for row in csvreader:
		if row_counter >= self.header_rows:  # Skip header rows if necessary
			try:
				tadc_row = TADCImportRow()  # instatantiate a new row
				tadc_row.load(row)  # load the data into the row
				if tadc_row.is_valid():  # If the row is valid...
					log.info("row {} is valid".format(row_counter))
				else:
					log.error(u"row {} is not valid".format(row_counter))
					for error in tadc_row.get_errors():  # There may be many errors.
						log.error(u"column {}: {}".format(error['column'], error['message']))
					except Exception as e:
						log.error("{}".format(e.message))
		row_counter += 1
```

## Standalone Script

You can run the validator as a standalone package too The CSV reader code above is basically what we use to do this and this all gets picked up automatically so that you only have to do this:

**Note:** if you have installed using `pip` then you should already have `tadc-import-csv-validator` available to you. 

```(bash)
cd TADCImportValidator
python setup.py install

# And run as
# tadc-import-csv-validator <csvFilename> <numHeaderRows>
tadc-import-csv-validator path/to/file.csv 1
```

## Development

If you want to debug this script use the `develop` option to setup.py so that the modules are not linked to the precompiled egg but to your own version.
You can then use an IDE with python debugging and set breakpoints etc.

```(bash)
cd TADCImportVAlidator
python setup.py develop

# And run as
# tadc-import-csv-validator <csvFilename> <numHeaderRows>
tadc-import-csv-validator path/to/file.csv 1
```

