import csv
import extract_params
import os


# Constants
on = 1
off = 2
start = 0
stop = 1


class AnimalInfo:
    params = extract_params.extract_params()

    def __init__(self, filename):
        """Initialize the class so that the output function can use it"""
        self.name = filename

        self.pure_data = AnimalInfo.extract_pure_data(self.name)
        self.filtered_data = AnimalInfo.filter_false_licks(self.pure_data)
        self.filtered_data = AnimalInfo.filter_false_starts(self.filtered_data)
        if not self.filtered_data:
            raise ValueError("Data set empty after filtering. Tweak param_file.csv false lick/start settings.")
        self.bursts = AnimalInfo.create_bursts(self.filtered_data)

        self.session_info_lists = self.create_session_info()
        self.meal_info_lists = self.create_meal_info_lists()
        self.bin_info_lists = self.create_bin_info_lists()

    @staticmethod
    def extract_pure_data(name):
        """Simply extract the timestamp, on value, and off value for every column in the data"""

        def create_lick_time_pairs(pure_data):
            time = 0
            if not pure_data:
                return None
            i = 0

            lick_pairs = []
            while i <= len(pure_data) - 1:
                if pure_data[i][on] and pure_data[i + 1][off]:
                    lick_pairs.append((pure_data[i][time], pure_data[i + 1][time]))
                    i += 1
                i += 1
            return lick_pairs

        def extract_column_location_information(filename):
            with open(filename) as datafile:
                csv_reader = csv.reader(datafile)
                titles = csv_reader.next()
                for title in titles:
                    title.strip()

                try:
                    on_col = titles.index(AnimalInfo.params.on_column)
                    off_col = titles.index(AnimalInfo.params.off_column)
                except ValueError:
                    raise ValueError("One of the columns you entered doesn't exist in the file {x}\n"
                                     "Continuing to the next file...\n".format(x=filename))

                try:
                    time_col = titles.index("Time")
                except ValueError:
                    raise ValueError("Unable to find column labeled 'Time'")

                pure_data = []
                if on_col >= 0 and off_col >= 0 and time_col >= 0:
                    for line in csv_reader:
                        pure_data.append((
                            float(line[time_col]) * 1000,
                            float(line[on_col]),
                            float(line[off_col])
                        ))

                return pure_data

        return create_lick_time_pairs(extract_column_location_information(name))

    @staticmethod
    def filter_false_starts(pairs):
        """Filter the data by removing false start entries.

        If we define a window of X milliseconds and a threshold number of licks Y, then we can say our true
        data set begins when the subject has completed Y licks in the last X milliseconds. Filtering
        false starts means removing all intervals whose [start time, start_time+X] window produced less
        than Y licks. The filter algorithm is O(n^2) where n is the number of tuples in pairs. May
        be worth improving if the data sets get significantly larger.

        Parameters
        ----------
        pairs: list(tuple)
            List of lick start/end time pairs.

        Returns
        -------
        list(tuple)
            A list of lick start/end time pairs satisfying the filter.

        Raises
        ------
        ValueError
            If an empty pairs list is passed in as a parameter.
        """
        if not pairs:
            raise ValueError("filter_false_starts() error: invalid data")

        for i, lick_pair in enumerate(pairs):
            window_start_time = lick_pair[start]
            window_end_time = window_start_time + AnimalInfo.params.false_start_win_size
            lick_ctr = 0

            for p in pairs[i:]:
                if p[stop] <= window_end_time:
                    lick_ctr += 1
                if lick_ctr >= AnimalInfo.params.false_start_lick_thresh:
                    # Success, at least one interval was able to satisfy the filter conditions.
                    # All following intervals, including this one, represent valid lick data.
                    return pairs[i:]

        # Bad news, no interval has passed the filter.
        return None

    @staticmethod
    def filter_false_licks(pairs):
        """Filter the data by removing all false licks"""
        if not pairs:
            raise ValueError("Invalid data")

        to_remove = []
        for i in range(1, len(pairs)):
            if pairs[i][start] - pairs[i-1][stop] < AnimalInfo.params.false_licks:
                to_remove.append(i)

        count = 0
        for index in to_remove:
            pairs.pop(index-count)
            count += 1

        return pairs

    @staticmethod
    def total_licks(data, time=-1):
        """Find the total number of licks within a given time. If no time is given, just return the total number
        of licks"""
        if time < 0:
            return len(data)

        if not data:
            raise ValueError("Invalid data")

        start_time = data[0][start]
        return len([(beg, end) for beg, end in data if end < start_time + time])

    @staticmethod
    def create_bursts(pairs):
        """Separate the given pairs into bursts"""
        if not pairs:
            return []
        bursts = []
        burst = [pairs[0]]
        for i in range(1, len(pairs)):
            if pairs[i][start] - pairs[i - 1][stop] < AnimalInfo.params.pause_criterion:
                burst.append(pairs[i])
            else:
                bursts.append(burst)
                burst = [pairs[i]]

        if len(burst) != 0:
            bursts.append(burst)
        return bursts

    @staticmethod
    def mean_burst_size(bursts):
        """Return the mean burst size"""
        if not bursts:
            return 0
        size = 0.0
        for burst in bursts:
            size += len(burst)
        return size/len(bursts)

    @staticmethod
    def get_duration(data):
        if not data:
            return data
        """Return the duration of a given set of data"""
        return data[len(data) - 1][stop] - data[0][start]

    @staticmethod
    def mean_burst_duration(bursts):
        """Return the mean burst duration of a given set of bursts"""
        if not bursts:
            return 0
        durations = 0
        for burst in bursts:
            durations += AnimalInfo.get_duration(burst)
        return durations / len(bursts)

    @staticmethod
    def get_mean_interlick_interval(pairs):
        """Get the mean interval between each pair of licks"""
        if not pairs:
            return 0
        total_int = 0.0
        for i in range(1, len(pairs)):
            total_int += pairs[i][start] - pairs[i - 1][stop]
        return total_int / len(pairs)

    @staticmethod
    def get_mean_lick_duration(pairs):
        if not pairs:
            return 0
        total_int = 0.0
        for pair in pairs:
            total_int += pair[stop] - pair[start]
        return total_int / len(pairs)


    def create_session_info(self):
        """Create a list of information for the session"""
        return [
            ["Absolute total licks", AnimalInfo.total_licks(self.pure_data)],
            ["Total filtered licks", AnimalInfo.total_licks(self.filtered_data)],
            ["Latency to first lick", self.filtered_data[0][0]],
            ["First Burst Size", len(self.bursts[0])],
            ["First Burst Duration", AnimalInfo.get_duration(self.bursts[0])],
            ["Total Licks in Minute One", AnimalInfo.total_licks(self.filtered_data, 60000)],
            ["Mean Interlick Interval", AnimalInfo.get_mean_interlick_interval(self.filtered_data)],
            ["Mean Lick Duration", AnimalInfo.get_duration(self.filtered_data) / len(self.filtered_data)],
            ["Number of Bursts", len(self.bursts)],
            ["Mean Burst Size", AnimalInfo.mean_burst_size(self.bursts)],
            ["Mean Burst Duration", AnimalInfo.mean_burst_duration(self.bursts)]
            ]

    class Meal:
        """Class to hold meal data (does computations within initializer)"""
        def __init__(self, pure_data, latency_to_next):
            bursts = AnimalInfo.create_bursts(pure_data)
            self.total_licks = AnimalInfo.total_licks(pure_data)
            self.total_licks_in_minute = AnimalInfo.total_licks(pure_data, 60000)
            self.total_licks_in_first_burst = AnimalInfo.total_licks(bursts[0], AnimalInfo.params.pause_criterion)
            self.total_duration = AnimalInfo.get_duration(pure_data)
            self.number_of_bursts = len(bursts)
            self.mean_burst_size = AnimalInfo.mean_burst_size(bursts)
            self.mean_burst_duration = AnimalInfo.mean_burst_duration(bursts)
            self.latency_to_next = latency_to_next

    class Bins:
        """Class to hold bin data (does computations within initializer)"""
        def __init__(self, pure_data):
            bursts = AnimalInfo.create_bursts(pure_data)
            self.total_licks = len(pure_data)
            self.mean_interlick_interval = AnimalInfo.get_mean_interlick_interval(pure_data)
            self.mean_lick_duration = AnimalInfo.get_mean_lick_duration(pure_data)
            self.number_of_bursts = len(bursts)
            self.mean_burst_size = AnimalInfo.mean_burst_size(bursts)
            self.mean_burst_duration = AnimalInfo.mean_burst_duration(bursts)

    def create_meal_info_lists(self):
        """Create the output information for each meal"""
        def get_meals(pairs):
            """Creates meal groups of data"""
            all_meals = []
            single_meal = [pairs[0]]
            for i in range(1, len(pairs)):
                if pairs[i][start] - pairs[i - 1][stop] < AnimalInfo.params.meal_criterion:
                    single_meal.append(pairs[i])
                else:
                    all_meals.append(single_meal)
                    single_meal = [pairs[i]]
            return all_meals

        meals_data = get_meals(self.filtered_data)
        meals = []  # Holds meal objects
        if not meals_data:
            return meals
        for meal in range(0, len(meals_data)-1):
            # print meals_data[meal]
            latency = meals_data[meal+1][0][start] - meals_data[meal][len(meals_data[meal]) - 1][stop]
            meals.append(AnimalInfo.Meal(meals_data[meal], latency))
        meals.append(AnimalInfo.Meal(meals_data[len(meals_data)-1], 0))

        return [
            ["Meal: "] + ["Meal {x}".format(x=x) for x in range(1, len(meals)+1)],
            ["Total Licks"] + [m.total_licks for m in meals],
            ["Total Licks in Minute 1"] + [m.total_licks_in_minute for m in meals],
            ["Total Licks in Burst 1"] + [m.total_licks_in_first_burst for m in meals],
            ["Total Duration"] + [m.total_duration for m in meals],
            ["Number of Bursts"] + [m.number_of_bursts for m in meals],
            ["Mean Burst Size"] + [m.mean_burst_size for m in meals],
            ["Mean Burst Duration"] + [m.mean_burst_duration for m in meals],
            ["Latency to Next Meal"] + [m.latency_to_next for m in meals]
        ]

    def create_bin_info_lists(self):
        """Create the output information for each bin"""

        def get_bins(pairs):
            all_bins = []
            single_bin = []
            current_threshold = AnimalInfo.params.bins
            count = 0

            for pair in pairs:
                if pair[stop] <= current_threshold:
                    single_bin.append(pair)
                else:
                    all_bins.append(single_bin)
                    single_bin = [pair]
                    current_threshold += AnimalInfo.params.bins

            if single_bin:
                all_bins.append(single_bin)

            return all_bins
        bins_data = get_bins(self.filtered_data)
        bins = []
        for x in range(0, len(bins_data)):
            bins.append(AnimalInfo.Bins(bins_data[x]))

        return [
            ["Bin: "] + ["Bin {x}".format(x=x) for x in range(1, len(bins) + 1)],
            ["Total Filtered Licks: "] + [b.total_licks for b in bins],
            ["Mean Interlick Interval"] + [b.mean_interlick_interval for b in bins],
            ["Mean Lick Duration"] + [b.mean_lick_duration for b in bins],
            ["Number of Bursts"] + [b.number_of_bursts for b in bins],
            ["Mean Burst Size"] + [b.mean_burst_size for b in bins],
            ["Mean Burst Duration"] + [b.mean_burst_duration for b in bins],
        ]

    def output_data(self, output_file):
        """Use the output functions to create all necessary output information & write each them as rows to the file"""

        with open(output_file, 'ab') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([self.name])
            csv_writer.writerow([])

            csv_writer.writerow(["Session:"])
            csv_writer.writerows(self.session_info_lists)  # Should be in form [["ABC", "DEF"], [...], ...]
            csv_writer.writerow([])

            # csv_writer.writerow(["Meals:"])
            csv_writer.writerows(self.meal_info_lists)
            csv_writer.writerow([])

            # csv_writer.writerow(["Bins:"])
            csv_writer.writerows(self.bin_info_lists)
            csv_writer.writerows([[], []])


if os.path.exists("output.csv"):
    os.remove("output.csv")

for f in AnimalInfo.params.files:
    # try:
    AnimalInfo(f).output_data("output.csv")
    print AnimalInfo.params
    # except Exception as e:
    #     print e
    #     print "Invalid file: " + f
