import sys
import argparse
import logging as log
from configs.config import Config
from benchmark.benchmark import Benchmark


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str, dest='config_path', help='Path to configuration file', required=True)
    parser.add_argument('-t', '--type', type=str, dest='type', help='Type of validation', choices=['benchmark'], required=True)
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', required=False)
    return parser


def get_validation_tool(type, config, model_paths, log):
    if type == 'benchmark':
        return Benchmark(config.benchmark_config, model_paths, log)


def main():
    args = build_parser().parse_args()
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.DEBUG if args.verbose else log.INFO,
        stream=sys.stdout
    )
    try:
        log.info('Start script execution...')
        config = Config.parse(args.config_path, log)
        models = config.get_model_path_list()
        tool = get_validation_tool(args.type, config, models, log)
        tool.run()
        log.info('Finish script execution...')
    except Exception as ex:
        log.error(str(ex))
        sys.exit(1)

if __name__ == '__main__':
    sys.exit(main() or 0)
