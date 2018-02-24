import csv
import extract_params


class AnimalInfo:
    params = extract_params.extract_params()

    @staticmethod
    def extract_pure_data(filename):
        return [(1, 2)]

    @staticmethod
    def filter_data(filename):
        return [(1, 2)]

    @staticmethod
    def total_licks(data, time=-1):
        return time

    @staticmethod
    def create_bursts(data):
        return [data]

    @staticmethod
    def duration_of_licks(data):
        return 1

    @staticmethod
    def mean_number_of_bursts(bursts):
        return 1

    @staticmethod
    def mean_burst_size(bursts):
        return 1

    @staticmethod
    def get_duration(data):
        return 1

    @staticmethod
    def mean_burst_duration(bursts):
        return 1

    @staticmethod
    def get_mean_interlick_interval(data):
        return 1

    def __init__(self, filename, params):
        self.params = params
        self.name = filename

        self.pure_data = AnimalInfo.extract_pure_data(self.name)
        self.filtered_data = AnimalInfo.filter_data(self.name)
        self.bursts = AnimalInfo.create_bursts(self.filtered_data)

        self.create_session_info()

        self.session_info_lists = self.create_session_info()
        self.meal_info_lists = create_meal_info_lists()
        self.bin_info_lists = create_bin_info_lists()

    def create_session_info(self):
        return [
            ["Absolute total licks", AnimalInfo.total_licks(self.pure_data)],
            ["Total filtered licks", AnimalInfo.total_licks(self.filtered_data)],
            ["Latency to first lick", self.filtered_data[0][0]],
            ["First Burst Size", len(self.bursts[0])],
            ["First Burst Duration", AnimalInfo.duration_of_licks(self.bursts[0])],
            ["Total Licks in Minute One", AnimalInfo.total_licks(self.filtered_data, 60)],
            ["Mean Interlick Interval", AnimalInfo.get_mean_interlick_interval(self.filtered_data)],
            ["Mean Lick Duration", AnimalInfo.get_duration(self.filtered_data) / len(self.filtered_data)],
            ["Number of Bursts", len(self.bursts)],
            ["Mean Burst Size", AnimalInfo.mean_burst_size(self.bursts)],
            ["Mean Burst Duration", AnimalInfo.mean_burst_duration(self.bursts)]
            ]

    class Meal:
        def __init__(self, pure_data, latency_to_next):
            bursts = AnimalInfo.create_bursts(pure_data)
            self.total_licks = AnimalInfo.total_licks(pure_data)
            self.total_licks_in_minute = AnimalInfo.total_licks(pure_data, 60)
            self.total_licks_in_first_burst = AnimalInfo.total_licks(bursts[0], AnimalInfo.params.burst_criterion)
            self.total_duration = AnimalInfo.duration_of_licks(pure_data)
            self.mean_number_of_bursts = AnimalInfo.mean_number_of_bursts(bursts)
            self.mean_burst_size = AnimalInfo.mean_burst_size(bursts)
            self.mean_burst_duration = AnimalInfo.mean_burst_duration(bursts)
            self.latency_to_next = latency_to_next

    class Bins:
        def __init__(self, pure_data):
            bursts = AnimalInfo.create_bursts(pure_data)
            self.mean_interlick_interval = AnimalInfo.get_mean_interlick_interval(pure_data)
            self.mean_lick_duration = AnimalInfo.get_duration(pure_data) / len(pure_data)
            self.number_of_bursts = len(bursts)
            self.mean_burst_size = AnimalInfo.mean_burst_size(bursts)
            self.mean_burst_duration = AnimalInfo.mean_burst_duration(bursts)

    def create_meal_info_lists(self):
        return self.name

    def create_bin_info_lists(self):
        return self.name

    def output_data(self):
        with open(self.name, 'a') as csvfile:
            csvwriter = csv.writer(csvfile)

            csvwriter.writerow(self.name)
            csvwriter.writerow([])
            csvwriter.writerow(["Session:"])
            csvwriter.writerows(self.session_info_lists)  # Should be in form [["ABC", "DEF"], [...], ...]
            csvwriter.writerow([])
            csvwriter.writerow(["Meals:"])
            csvwriter.writerows(self.meal_info_lists)
            csvwriter.writerow([])
            csvwriter.writerow(["Bins:"])
            csvwriter.writerows(self.bin_info_lists)
            csvwriter.writerows([[], []])
