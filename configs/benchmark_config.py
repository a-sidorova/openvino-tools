from .tool_config import ToolConfig


class BenchmarkConfig(ToolConfig):
    def __init__(self, log_, executor_ = "", time_ = 20, mode_ = "sync", device_ = 'CPU', \
            ignore_precision_ = [], needed_list_ = [], ignore_list_ = [], output_folder_ = ""):
        super().__init__(log_, device_, ignore_precision_, needed_list_, ignore_list_, output_folder_)
        self.time = time_
        self.executor = executor_
        self.mode = mode_

    @staticmethod
    def parse(data, log):
        if data is None:
            return None
        config = BenchmarkConfig(log)
        if 'time' in data:
            config.time = data['time']
        if 'mode' in data:
            config.mode = data['mode']
        if 'device' in data:
            config.device = data['device']
        if 'ignore_precision' in data:
            config.ignore_precision = data['ignore_precision']
        if 'needed_list' in data:
            config.needed_list = data['needed_list']
        if 'ignore_list' in data:
            config.ignore_list = data['ignore_list']
        if 'output_folder' not in data:
            raise ValueError('Parameter \"output_folder\" was missed for benchmark!')
        if 'executor' not in data:
            raise ValueError('Parameter \"executor\" was missed for benchmark!')
        config.output_folder = data['output_folder']
        config.executor = data['executor']
        return config
