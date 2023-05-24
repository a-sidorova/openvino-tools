import os
import sys
import math
import traceback
import argparse
import logging as log


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--reference',
                        help='Path to a blob file with a reference values.',
                        required=True,
                        type=str,
                        dest='reference')
    parser.add_argument('-t', '--target',
                        help='Path to a blob file with a target values.',
                        required=True,
                        type=str,
                        dest='target')
    parser.add_argument('--rel_threshold',
                        help='Relative threshold.',
                        required=False,
                        default=0.0001,
                        type=str,
                        dest='rel_threshold')
    parser.add_argument('--abs_threshold',
                        help='Absolute threshold.',
                        required=False,
                        default=10e-6,
                        type=str,
                        dest='abs_threshold')
    parser.add_argument('--all_values',
                        help='Print all incompantible values.',
                        action='store_true',
                        dest='all')

    args = parser.parse_args()

    return args


def read(path):
    log.info(f'Reading of file {path}')
    if os.path.exists(path) and os.path.isfile(path):
        values = []
        with open(path, "r") as f:
            values = f.readlines()
        # skip first line since there is blob information
        return values[1:]
    else:
        raise Exception(f'Incorrect path {path}')


def comparison(reference_values, target_values, rel_threshold, abs_threshold, all=False):
    reference_size = len(reference_values)
    target_size = len(target_values)
    if (reference_size != target_size):
        raise Exception(f'Incorrect count of reference and target values: {reference_size} vs {target_size}')

    print_error = True
    rel_count, rel_max = 0, 0
    abs_count, abs_max = 0, 0

    for i in range(reference_size):
        lhs = float(reference_values[i])
        rhs = float(target_values[i])
        if math.isnan(lhs) or math.isnan(rhs):
            log.info(f'{i}: There is NAN values: {lhs} vs {rhs}')
            print_error = False
            continue
        error = False
        abs = math.fabs(lhs - rhs)
        rel = abs / lhs if lhs != 0 else 0
        if abs > abs_threshold:
            abs_count += 1
            abs_max = max(abs, abs_max)
            error = True
        if rel > rel_threshold:
            rel_count += 1
            rel_max = max(rel, rel_max)
            error = True
        if error and (print_error or all):
            log.info(f'{i}: Abs threshold: {abs}, Relative threshold: {rel}, Values: {lhs} vs {rhs}')
            print_error = False
    log.info(f'Max Abs Threshold: {abs_max}, Count: {abs_count}')
    log.info(f'Max Rel Threshold: {rel_max}, Count: {rel_count}')


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout,
    )
    args = cli_argument_parser()
    try:
        log.info(f'Absolute threshold: {args.abs_threshold}')
        log.info(f'Relative threshold: {args.rel_threshold}')

        reference_values = read(args.reference)
        target_values = read(args.target)
        comparison(reference_values, target_values, args.rel_threshold, args.abs_threshold, args.all)

    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
