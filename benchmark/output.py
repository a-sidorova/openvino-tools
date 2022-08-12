import csv
from os import stat


class Output:
    def __init__(self, log, path):
        self.log = log
        self.path = path

    def create_table_row(self, status, model, device, mode, latency, fps, note):
        return '{0};{1};{2};{3};{4};{5};{6}'.format(status, model, device, mode, latency, fps, note)

    def create_table(self):
        self.log.debug("Create table {}".format(self.path))
        HEADERS = 'Status;Topology;Device;Mode;Latency;FPS;Note;'
        with open(self.path, 'w') as table:
            table.write(HEADERS + '\n')
            table.close()

    def add_row_to_table(self, model, path):
        status, api, d, latency, fps, note = Output.parse(path)
        report_row = self.create_table_row(status, model, d, api, latency, fps, note)
        with open(self.path, 'a') as table:
            table.write(report_row + '\n')
            table.close()

    @staticmethod
    def parse(path):
        with open(path, 'r') as file:
            lines = [line.rstrip('\n')[:-1] for line in file]
            status = "SUCCESS"
            note = ""
            latency = -1
            fps = -1
            for line in lines:
                if "api;" in line:
                    api = line.split(";")[-1]
                elif "d;" == line[:2]:
                    d = line.split(";")[-1]
                elif "Median latency (ms);" in line:
                    latency = line.split(";")[-1]
                elif "throughput;" in line:
                    fps = line.split(";")[-1]
                elif "error;" in line:
                    status = "ERROR"
                    note = line.split(";")[-1]
                    break
            return status, api, d, latency, fps, note

