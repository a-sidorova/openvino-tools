import sys
import argparse

def build_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gold_file', help='Path to an gold file.', required=True, type=str, dest='gold_file')
    parser.add_argument('-c', '--check_file', help='Path to an file to check.', required=True, type=str, dest='check_file')
    parser.add_argument('-r', '--rate', help='Error rate', required=True, type=float, dest='error_rate')
    return parser


def get_values(file):
    with open(file) as f:
        next(f)
        array = []
        for line in f:
            array.append(float(line.split()[0]))
    return array


def compare(gold_values, check_values, error_rate):
    if (len(gold_values) != len(check_values)):
        print("[  ERROR  ] Count of gold values: {}".format(len(gold_values)))
        print("[  ERROR  ] Count of checking values: {}".format(len(check_values)))
        return -1, -1
    
    max_diff = 0
    error_values = {}
    for i in range(len(gold_values)):
        diff = abs(gold_values[i] - check_values[i])
        if (diff >= error_rate):
            error_values.update({i : [gold_values[i], check_values[i], diff]})
            if (diff > max_diff):
                max_diff = diff
    return error_values, max_diff

def print_results(values, max_diff, error_rate):
    if (len(values) == 0):
        print("[  SUCCESS  ] Error rate is passed. Max diff is {}".format(max_diff))
        return
    
    print("[  ERROR  ] THERE ARE PROBLEMS")
    for key, item in values.items():
        print("            Index {}: {} vs {}, diff: {}".format(key, item[0], item[1], item[2]))
    print("[  ERROR  ] Error rate is {} but max diff is {}".format(error_rate, max_diff))
    print("[  ERROR  ] Count of diffs: {} where count of values is {}".format(len(values.keys()), len(values)))


def main():
    print("[  START  ]")
    args = build_argparser().parse_args()
    gold_values = get_values(args.gold_file)
    check_values = get_values(args.check_file)
    values, max_diff = compare(gold_values, check_values, args.error_rate)
    if (values != -1):
        print_results(values, max_diff, args.error_rate)
    print("[   END   ]")


if __name__ == '__main__':
    sys.exit(main() or 0)
