import extract_params
import csv


def extract_column_location_information(filename):
    with open(filename) as datafile:
        csv_reader = csv.reader(datafile)
        titles = csv_reader.next()
        for title in titles:
            title.strip()

        try:
            on_col = titles.index(params.on_column)
            off_col = titles.index(params.off_column)
        except ValueError:
            print "One of the columns you entered doesn't exist in the file {}\n" \
                  "Continuing to the next file...\n".format(filename)
            return None

        try:
            time_col = titles.index("Time")
        except ValueError:
            time_col = 7
            print "Assuming the 'time' column is the '{}' column...\n".format(titles[time_col])

        pure_data = []
        if on_col >= 0 and off_col >= 0 and time_col >= 0:
            for line in csv_reader:
                pure_data.append((
                    float(line[time_col]) * 1000,
                    float(line[on_col]),
                    float(line[off_col])
                ))

        return pure_data


def create_lick_time_pairs(pure_data):
    if not pure_data:
        return None
    i = 0
    time = 0
    on = 1
    off = 2
    lick_pairs = []
    while i <= len(pure_data) - 2:
        if pure_data[i][on] and pure_data[i+1][off]:
            lick_pairs.append((pure_data[i][time], pure_data[i+1][time]))
        i += 1
    return lick_pairs


def remove_false_pairs(lick_pairs, false_threshold):
    return [(start, stop) for start, stop in lick_pairs if stop - start > false_threshold]


params = extract_params.extract_params()
print params
for f in params.files:
    all_data = extract_column_location_information(f)
    lick_pairs = create_lick_time_pairs(all_data)
    lick_pairs_without_false = remove_false_pairs(lick_pairs, params.false_licks)
    
    print len(lick_pairs_without_false)











