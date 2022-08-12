import os
import yaml
from tqdm import tqdm
from .benchmark_config import BenchmarkConfig
from .functional_validation_config import FunctionalValidationConfig


class Config:
    def __init__(self, log, model_cache_path_ = "", model_paths_cache_ = "", benchmark_config_ = None, func_val_config_ = None):
        self.log = log
        self.model_cache_path = model_cache_path_
        self.cache_models = False  # True - cache model paths into file
        self.benchmark_config = benchmark_config_
        self.func_val_config = func_val_config_
        self.model_caching = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cache.yml")

    @staticmethod
    def parse(config_path, log):
        if not os.path.exists(config_path):
            raise ValueError('Config file {} was not found!'.format(config_path))
        with open(config_path, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            config = Config(log)
            if 'model_cache_path' not in data:
                raise ValueError('\"model_cache_path\" was missed!')
            config.model_cache_path = data['model_cache_path']
            if 'benchmark' in data:
                config.benchmark_config = BenchmarkConfig.parse(data['benchmark'], log)
            if 'functional_validation' in data:
                config.func_val_config = FunctionalValidationConfig.parse(data['functional_validation'], log)
            return config

    def cache_models_to_config(self, model_path_list):
        self.log.info("Start saving to {}".format(self.model_caching))
        with open(self.model_caching, 'w') as out_file:
            yaml.safe_dump({'models': model_path_list}, out_file)
        self.log.info("End saving to {}".format(self.model_caching))

    @staticmethod
    def read_models_from_cache(path, log):
        log.info("Start reading from {}".format(path))
        with open(path, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            log.info("End reading from {}".format(path))
            return data['models']
        log.error("File {} was not opened".format(path))
        return None

    def get_model_path_list(self):
        if not self.cache_models and os.path.exists(self.model_caching):
            model_path_list = Config.read_models_from_cache(self.model_caching, self.log)
        else:
            self.log.info("Start scanning of {}".format(self.model_cache_path))
            model_dirs = [f.path for f in os.scandir(self.model_cache_path) if f.is_dir()]
            self.log.info("Count of model folders: {}".format(len(model_dirs)))
            model_path_list = []
            bar = tqdm(model_dirs)
            for model_dir in bar:
                self.log.debug("Start scanning of {}".format(model_dir))
                model_ir_paths = [os.path.join(dp, f) for dp, dn, filenames in os.walk(model_dir) for f in filenames if os.path.splitext(f)[-1] == '.xml']
                model_path_list.extend(model_ir_paths)
            bar.close()
            self.log.info("Count of models: {}".format(len(model_path_list)))
            self.log.info("End scanning of {}".format(self.model_cache_path))
            if self.cache_models:
                self.cache_models_to_config(model_path_list)
        return model_path_list
