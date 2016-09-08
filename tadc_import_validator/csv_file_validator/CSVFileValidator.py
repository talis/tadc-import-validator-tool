import os
import unicodecsv as csv
from logbook import Logger
from ..tadc_import_row import TADCImportRow
from collections import OrderedDict

__author__ = 'timhodson'

log = Logger('CSVFileValidator')


class CSVFileValidator:
    """
    Validates a CSV File presented as a TADC Import data file.
    """

    def __init__(self, csv_file, output_dir, old_date_format, header_rows=2, fix_missing=False):
        self.csv_file_name = csv_file
        log.info("Processing File: {}".format(self.csv_file_name))
        self.header_rows = int(header_rows)
        log.info("Expecting {} header rows".format(self.header_rows))
        self.old_date_format = old_date_format
        self.fix_missing = fix_missing
        self.fixed_output_dir = output_dir
        self.fixed_filename = None
        self.fixed_csv_writer = None
        self.fixed_fp = None
        if self.fix_missing:
            log.info("Will fix missing values".format(self.header_rows))
            self.init_fixed_file()
        self.error_summary = OrderedDict()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.fixed_fp:
            self.fixed_fp.close()
        return self

    def validate_file(self):
        """
        Read all rows of a CSV file and output a message about whether is is valid or not.
        :return:
        """

        with open(self.csv_file_name) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', dialect='excel', quotechar='"')
            row_counter = 0
            for row in csvreader:
                if row_counter >= self.header_rows:
                    try:
                        tadc_row = TADCImportRow(old_date_format=self.old_date_format, fix_missing=self.fix_missing)
                        tadc_row.load(row)
                        if tadc_row.is_valid():
                            log.info("row {} is valid".format(row_counter))
                            if self.fix_missing:
                                log.debug("Write output for row {} to fix file".format(row_counter))
                                # output the row to a fixed file.
                                self.write_fixed_file(tadc_row)
                        else:
                            log.error(u"row {} is not valid".format(row_counter))
                            for error in tadc_row.get_errors():
                                self.add_error_summary(row_counter, error)
                                log.error(u"column {}: {}".format(error['column'], error['message']))
                    except Exception as e:
                        log.error("{}".format(e.message))
                row_counter += 1
            self.print_error_summary()

    def add_error_summary(self, row, error):
        error_column = error['column']
        error_message = error['message']
        if not self.error_summary.get(row):
            self.error_summary[row] = {}
        if not self.error_summary[row].get(error_column):
            self.error_summary[row][error_column] = error_message

    def print_error_summary(self):
        error_rows = len(self.error_summary)
        error_count = 0
        column_error_summary = {}
        if error_rows > 0:
            log.info("Errors were found for the following columns")
            for row, columns in self.error_summary.iteritems():
                for column in columns:
                    error_count += 1
                    if column_error_summary.get(column):
                        column_error_summary[column] += 1
                    else:
                        column_error_summary[column] = 1
                    # rows are zero counted so fix with a +1 for humans to read.
                    log.info("Row {} column {} : {}".format(row + 1, column, columns[column]))

            log.info("Summary: There were {} errors found in {} rows".format(error_count, error_rows))
            for column in column_error_summary:
                log.info(" - Column {} had {} errors".format(column, column_error_summary[column]))
        else:
            log.info("No errors found. Woohoo!")

    def init_fixed_file(self):
        split_orig_filename = os.path.splitext(self.csv_file_name)
        new_name = os.path.join(self.fixed_output_dir,
                                "{}.fixed{}".format(split_orig_filename[0], split_orig_filename[1]))
        self.fixed_filename = os.path.realpath(new_name)
        self.fixed_fp = open(self.fixed_filename, 'a')
        self.fixed_csv_writer = csv.writer(self.fixed_fp, delimiter=',', dialect='excel', quotechar='"')

    def write_fixed_file(self, row):
        self.fixed_csv_writer.writerow(row.output_for_csv())

    def get_fixed_filename(self):
        return self.fixed_filename
