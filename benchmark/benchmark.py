import os
import sys
import subprocess
from datetime import datetime
from tqdm import tqdm
from tool import Tool
from .output import Output


class Benchmark(Tool):
    def __init__(self, config, model_paths, log):
        super().__init__(config, model_paths, log)
    
    def create_command_line(self, model, script_dir, log_file):
        command_line = '{} -m {} -d {} -t {} -api {} --report_type no_counters --report_folder {} >> {}'.format(
            self.config.executor, model, self.config.device, self.config.time, self.config.mode, script_dir, log_file
        )
        self.log.debug("Command line: {}".format(command_line))
        return command_line
    
    def run(self):
        self.log.info("Start benchmark")
        script_dir = os.path.dirname(os.path.realpath(__file__))
        report_file = os.path.join(script_dir, "benchmark_report.csv")

        date = datetime.now()
        date_str = date.strftime("%Y%m%d_%H_%M")
        output_handler = Output(self.log, os.path.join(self.config.output_folder, "benchmark_report_{}.csv".format(date_str)))
        output_handler.create_table()
        bar = tqdm(self.model_paths)
        for model in bar:
            self.log.debug("Start benchmark of {}".format(model))
            log_file = os.path.join(script_dir, "benchmark_report_{}.log".format(date_str))
            command_line = self.create_command_line(model, script_dir, log_file)
            p = subprocess.Popen(command_line, stdout=subprocess.PIPE, shell=True)
            p.communicate()
            p.wait()
            self.log.debug("End benchmark of {}".format(model))
            output_handler.add_row_to_table(model, report_file)
            self.log.debug("Added results of benchmark of {}".format(model))
        bar.close()
        self.log.info("End benchmark")
