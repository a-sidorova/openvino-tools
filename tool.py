import abc


class Tool(metaclass=abc.ABCMeta):
    def __init__(self, config, model_paths, log):
        self.log = log
        self.config = config
        self.model_paths = self.model_filter(model_paths)
    
    def precision_filter(self, model_paths):
        self.log.info("Start model filtering by precision...")
        models = model_paths
        for ignored_precision in self.config.ignore_precision:
           for path in model_paths:
               if ignored_precision in path:
                   models.remove(path)
        self.log.info("End model filtering by precision...")
        return models
            
    
    def model_filter(self, model_paths):
        self.log.info("Start model filtering by name...")
        models = []
        if self.config.needed_list:
            for needed_model in self.config.needed_list:
                needed_paths = [path for path in model_paths if needed_model in path]
                if len(needed_paths) == 0:
                    self.log.info("Model <{}> is not in cache".format(needed_model))
                models.extend(needed_paths)
        elif self.config.ignore_list:
            models = model_paths
            for ignored_model in self.config.ignore_list:
                for path in model_paths:
                    if ignored_model in path:
                        models.remove(path)
        else:
            models = model_paths
        self.log.info("End model filtering by name...")
        return self.precision_filter(models)


    def run(self):
        pass
