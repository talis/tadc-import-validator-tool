import time
import sys
import datetime
import os
from logbook import Logger, FileHandler, StreamHandler
from tadc_import_validator.csv_file_validator import CSVFileValidator
import argparse

__author__ = 'timhodson'

log = Logger("validate_csv_file")


def main():
    """
    The main routine which kicks everything off
    :return:
    """

    # register some logging handlers
    log_handler = FileHandler('/tmp/validate_csv_{}.log'.format(os.path.basename(time.strftime('%Y%m%d-%H%M%S'))),
                          mode='w', level='DEBUG', bubble=True)
    stdout_handler = StreamHandler(sys.stdout, level='INFO', bubble=True)

    # Setup the command line arguments
    flags = argparse.ArgumentParser(description="Tool to validate and fix errors in CSV files for TADC imports")
    flags.add_argument('csv_file', type=str, help="Path to a CSV file to validate")
    flags.add_argument('header_rows', type=str, help="Number of header rows")
    flags.add_argument('--fix-missing', '-f', action='store_true', help="Fix missing fields by inserting the value 'unknown'")
    args = flags.parse_args()

    with stdout_handler.applicationbound():
        with log_handler.applicationbound():
            start = time.time()
            log.info("starting at {}".format(time.strftime('%l:%M%p %Z on %b %d, %Y')))

            # if len(sys.argv) < 3:
            #     log.error("You need to specify the path to a CSV file and how many header rows are present")
            #     log.error("Usage: {} ./path/to/file.csv <numHeaderRows>".format(sys.argv[0]))
            #     exit(1)
            # else:
            #     filename = sys.argv[1]
            #     header_rows = sys.argv[2]

            with CSVFileValidator(
                    csv_file=args.csv_file,
                    header_rows=args.header_rows,
                    fix_missing=args.fix_missing) as validator:
                validator.validate_file()
                log.info("Running time: {}".format(str(datetime.timedelta(seconds=(round(time.time() - start, 3))))))

if __name__ == "__main__":
    main()