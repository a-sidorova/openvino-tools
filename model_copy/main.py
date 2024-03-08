import os
import sys
import argparse
import traceback
import subprocess
import logging as log
from threading import Timer


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--cache_file',
                        help='Path to a cache file that contains models.',
                        required=True,
                        type=str,
                        dest='cache_file')
    parser.add_argument('-src',
                        help='Source directory.',
                        required=True,
                        type=str,
                        dest='src_dir')
    parser.add_argument('-dst',
                        help='Destination directory.',
                        required=True,
                        type=str,
                        dest='dst_dir')

    args = parser.parse_args()
    
    if not os.path.isdir(args.src_dir):
        raise Exception(f'Incorrect path to src model directory {args.src_dir}')

    if not os.path.exists(args.cache_file):
        raise Exception(f'The file with name {args.cache_file} has not been found!')

    return args


def load_from_cache(file):
    with open(file, "r") as f:
        content_list = f.readlines()
    return content_list


def update_path(full_path, src_dir, dst_dir):
    return full_path.replace(src_dir, dst_dir)


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.DEBUG,
        stream=sys.stdout,
    )
    args = cli_argument_parser()
    try:
        model_list = load_from_cache(args.cache_file)
        for model in model_list:
            model_dir_path = os.path.dirname(model)
            new_model_dir_path = update_path(model_dir_path, args.src_dir, args.dst_dir)
            command_line = f"sudo mkdir -p {new_model_dir_path} && sudo cp -r {model_dir_path}/* {new_model_dir_path}"
            process = subprocess.Popen(command_line, env=os.environ.copy(), shell=True, stdout=subprocess.PIPE, universal_newlines=True)
            timer = Timer(300, process.kill)
            try:
                timer.start()
                out, _ = process.communicate()
            finally:
                timer.cancel()

            new_model_path = update_path(model, args.src_dir, args.dst_dir)
            if os.path.exists(new_model_path):
                log.debug(f'The model {new_model_path} has been successfully copied')
            else:
                log.warning(f'The model {new_model_path} has not been copied')

    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
