import matplotlib.pyplot as plt
from uuid import uuid4

class TimeSeriesPlotterManager:
    def __init__(self, keys = []) -> None:
        self.keys = keys
        for key in keys:
            setattr(self, key, TimeSeriesPlotter(key))

    def get(self, key):
        return getattr(self, key)

    def add(self, key, series_name, time, value):
        getattr(self, key).add(series_name, time, value)

    def show(self):
        for key in self.keys:
            getattr(self, key).show()

class TimeSeriesPlotter:
    def __init__(self, name) -> None:
        """
        Initializes the TimeSeriesPlotter class with an empty dictionary to store time series data.
        The dictionary structure is now {series_name: {'times': [int], 'values': [float]}}.
        """
        self.time_series_data = {}
        self.name = name

    def add(self, series_name, time, value):
        """
        Adds a data point to the specified time series. If the series does not exist, it creates a new one.
        Each data point consists of a time (integer) and a corresponding value (float).

        Args:
        - series_name (str): The name of the time series to which the data point should be added.
        - time (int): An integer representing the time of the data point.
        - value (float): The value of the data point.
        """
        if series_name not in self.time_series_data:
            self.time_series_data[series_name] = {'times': [], 'values': []}
        self.time_series_data[series_name]['times'].append(time)
        self.time_series_data[series_name]['values'].append(value)

    def show(self, uuid=None):
        """
        Plots all time series stored in the dictionary. Each series is plotted with its times on the x-axis
        and its values on the y-axis. Each series is connected by lines and is labeled with its series name.
        """
        plt.figure(figsize=(50, 30))
        
        for series_name, data in self.time_series_data.items():
            plt.plot(data['times'], data['values'], '-o', label=series_name, markersize=4)
        
        plt.title('Time Series Data', fontsize=50)  # Adjusted title size
        plt.xlabel('Time', fontsize=40)  # Adjusted xlabel size
        plt.ylabel(self.name, fontsize=40)  # Adjusted ylabel size
        plt.xticks(fontsize=30)  # Adjusted xticks size
        plt.yticks(fontsize=30)  # Adjusted yticks size
        plt.legend(fontsize=40)  # Adjusted legend size
        if uuid is None:
          uuid = str(uuid4())
        print(f"/app/cache/worldgen/{self.name}-{uuid}.png")
        plt.savefig(f"/app/cache/worldgen/{self.name}-{uuid}.png")

