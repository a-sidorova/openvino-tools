import os
import sys
import argparse
import traceback
import logging as log


SUPPORTED_PRECISIONS = set(['FP32', 'FP16', 'INT8'])


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--model_dir',
                        help='Path to a directory that contains models.',
                        required=True,
                        type=str,
                        dest='model_dir')
    parser.add_argument('-c', '--cache_file',
                        help='Path to a result file with cached model list.',
                        required=True,
                        type=str,
                        dest='cache_file')
    parser.add_argument('--precisions',
                        help='List of precision.',
                        required=False,
                        default=['FP32'],
                        type=str,
                        nargs='+',
                        dest='precisions')
    parser.add_argument('--filter',
                        help='Filter model name.',
                        required=False,
                        default=[],
                        type=str,
                        nargs='+',
                        dest='filter')

    args = parser.parse_args()
    
    if not os.path.isdir(args.model_dir):
            raise Exception(f'Incorrect path to model cache directory {args.model_dir}')

    if os.path.exists(args.cache_file):
        raise Exception(f'The file with name {args.cache_file} is already existed')

    if len(set(args.precisions).difference(SUPPORTED_PRECISIONS)) != 0:
        raise Exception(f'Supported precisions: {SUPPORTED_PRECISIONS}')

    return args


def filter_path(precision):
    if precision == 'FP32':
        return '/FP32/1/'
    if precision == 'FP16':
        return '/FP16/1/'
    if precision == 'INT8':
        return '/FP16/INT8/1/'


def load_models(model_dir, precisions, filter):
    log.info(f'Reading of models from directory {model_dir} has been started')
    models = []
    for dp, dn, filenames in os.walk(model_dir):
        for prc in precisions:
            filtered_path = filter_path(prc)
            if filtered_path in dp:
                for f in filenames:
                    if os.path.splitext(f)[1] == '.xml':
                        models.append(os.path.join(dp, f) + '\n')
                        log.debug(f'The model {os.path.join(dp, f)} has been loaded')

    if len(filter) == 0:
        return models

    log.info(f'Filtering of models by {filter} has been started')
    filtered_models = []
    for model in models:
        for model_filter in filter:
            if model_filter in model:
                filtered_models.append(model)
                break
    return filtered_models


def cache(models, cache_file):
    with open(cache_file, 'w') as f:
        for model in models:
            f.write(model)

    status = os.path.isfile(cache_file) and os.stat(cache_file).st_size > 0
    return status


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout,
    )
    args = cli_argument_parser()
    try:
        model_list = load_models(args.model_dir, args.precisions, args.filter)
        status = cache(model_list, args.cache_file)

        if status:
            log.info(f'Cached file {args.cache_file} has been successfully created')
        else:
            raise Exception(f'Cached file {args.cache_file} creation is failed')

    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
