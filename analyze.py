import extract_params
import csv


time = 0
on = 1
off = 2
start = 0
stop = 1


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

    lick_pairs = []
    while i <= len(pure_data) - 1:
        if pure_data[i][on] and pure_data[i+1][off]:
            lick_pairs.append((pure_data[i][time], pure_data[i+1][time]))
        i += 1
    return lick_pairs


def remove_false_pairs(pairs, false_threshold):
    return [(beg, end) for beg, end in pairs if end - beg > false_threshold]


def get_latency_to_first_lick(pairs):
    return pairs[0][0]


def get_bursts(pairs, pause_threshold):
    bursts = []
    burst = [pairs[0]]
    for i in range(1, len(pairs)):
        if pairs[i][start] - pairs[i-1][stop] < pause_threshold:
            burst.append(pairs[i])
        else:
            bursts.append(burst)
            burst = [pairs[i]]
    return bursts


def get_meals(bursts, meal_threshold):
    meals = []
    meal = [bursts[0]]
    for i in range(1, len(bursts)):
        if bursts[i][0][start] - bursts[i-1][len(bursts[i-1]-1)][stop] < meal_threshold:
            meal += bursts[i]
        else:
            meals.append(meal)
            meal = [bursts[i]]
    return meals


def get_duration_of(pairs):
    return pairs[len(pairs)-1][stop] - pairs[0][start]


params = extract_params.extract_params()
print params
for f in params.files:
    all_data = extract_column_location_information(f)
    lick_pairs = create_lick_time_pairs(all_data)
    lick_pairs_without_false = remove_false_pairs(lick_pairs, params.false_licks)
    print len(lick_pairs_without_false)











