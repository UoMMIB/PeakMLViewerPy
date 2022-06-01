from UI.MainView import MainView
from Data.DataAccess import DataAccess
import Logger as lg

def main():

    try:

        #Initialize logging session by creating log file.
        lg.initalise_logging_session()

        #Initialize data object
        data = DataAccess()

        #Creates main window
        MainView(data)

    except Exception as err:
        lg.log_error(f'An error occurred: {err}')

if __name__ == "__main__":
    main()
