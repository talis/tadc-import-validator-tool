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

    # Setup the command line arguments
    flags = argparse.ArgumentParser(description="Tool to validate and fix errors in CSV files for TADC imports")
    flags.add_argument('csv_file', type=str, help="Path to a CSV file to validate")
    flags.add_argument('header_rows', type=str, help="Number of header rows")
    flags.add_argument('--fix-missing', '-f', action='store_true', help="Fix missing fields by inserting the value 'unknown'")
    flags.add_argument('--output-dir', '-o', type=str, help='Where to put output files', default=os.getcwd())
    flags.add_argument('--log-dir', '-l', type=str, help='Where to put log files', default='/tmp')
    flags.add_argument('--log-level', type=str, help='Choose a log level', default='INFO')
    flags.add_argument('--old-date-format', type=str, help="the format of dates that will be fixed", default='%d/%m/%Y')
    args = flags.parse_args()

    log_filename = os.path.join(
            args.log_dir,
            'tadc_import_validator_{}.log'.format(os.path.basename(time.strftime('%Y%m%d-%H%M%S')))
        )

    # register some logging handlers
    log_handler = FileHandler(
        log_filename,
        mode='w',
        level=args.log_level,
        bubble=True
    )
    stdout_handler = StreamHandler(sys.stdout, level=args.log_level, bubble=True)

    with stdout_handler.applicationbound():
        with log_handler.applicationbound():
            log.info("Arguments: {}".format(args))
            start = time.time()
            log.info("starting at {}".format(time.strftime('%l:%M%p %Z on %b %d, %Y')))

            with CSVFileValidator(
                    csv_file=args.csv_file,
                    header_rows=args.header_rows,
                    output_dir=args.output_dir,
                    old_date_format=args.old_date_format,
                    fix_missing=args.fix_missing) as validator:
                validator.validate_file()
                log.info("Running time: {}".format(str(datetime.timedelta(seconds=(round(time.time() - start, 3))))))
                log.info("Log written to {}:".format(log_filename))
                log.info("Fixed data is in: {}".format(validator.get_fixed_filename()))

if __name__ == "__main__":
    main()
