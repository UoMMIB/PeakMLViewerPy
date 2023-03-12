from UI.MainView import MainView
from Data.DataAccess import DataAccess
import Logger as lg
import argparse

def main():

    try:

        parser = argparse.ArgumentParser()
        parser.add_argument('-p','--peakml')
        parser.add_argument('-a','--annotation_params')
        args = parser.parse_args()

        #Initialize logging session by creating log file.
        lg.initalise_logging_session()

        #Initialize data object
        data = DataAccess()

        #Creates main window
        MainView(data, args.peakml, args.annotation_params)

    except Exception as err:
        lg.log_error(f'An error occurred: {err}')

if __name__ == "__main__":
    main()
