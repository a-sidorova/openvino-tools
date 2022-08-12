import abc


class ToolConfig(metaclass=abc.ABCMeta):
    def __init__(self, log_, device_ = 'CPU', ignore_precision_ = [], needed_list_ = [], ignore_list_ = [], output_folder_ = ""):
        self.log = log_
        self.device = device_
        self.ignore_precision = ignore_precision_
        self.needed_list = needed_list_
        self.ignore_list = ignore_list_
        self.output_folder = output_folder_
