import csv
import sys


class Parameters:
    """Standardized to hold all parameters in milliseconds:
    false_licks, pause_criterion are provided in milliseconds by user
    meal_criterion, session_duration, are provided in seconds by user"""
    def __init__(self, folder, false_licks, pause_criterion, meal_criterion, session_duration, bins, on_column,
                 off_column):
        self.folder = folder.strip()
        self.false_licks = int(false_licks)
        self.pause_criterion = int(pause_criterion)
        self.meal_criterion = int(meal_criterion) * 1000
        self.session_duration = int(session_duration) * 1000
        self.bins = int(bins)
        self.on_column = on_column.strip()
        self.off_column = off_column.strip()

    def __str__(self):
        ret_string = "Folder with files     : {folder}\n" \
                     "False Licks (ms)      : {false_licks}\n" \
                     "Pause Criterion (ms)  : {pause_criterion}\n" \
                     "Meal Criterion (ms)   : {meal_criterion}\n" \
                     "Session Duration (ms) : {session_duration}\n" \
                     "Number of bins        : {bins}\n" \
                     "On Column             : {on_column}\n" \
                     "Off Column            : {off_column}\n"\
            .format(folder=self.folder, false_licks=self.false_licks, pause_criterion=self.pause_criterion,
                    meal_criterion=self.meal_criterion, session_duration=self.session_duration,
                    bins=self.bins, on_column=self.on_column, off_column=self.off_column)
        return ret_string


def extract_params():
    filename = "param_file.csv"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    try:
        with open(filename) as csvDataFile:
            csv_reader = csv.reader(csvDataFile)
            csv_reader.next()
            p = csv_reader.next()
            return Parameters(*p)

    except IOError:
        print "Error: File {} does not appear to exist.".format(filename)
        exit()
    except ValueError:
        print "Error: One or more of your parameter values is of an incorrect type. \n" \
              "It is likely that it is one of the criteria that are meant to be seconds, milliseconds, or an integer"
        exit()


print extract_params()
