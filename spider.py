import sys
import argparse
import time
import tracemalloc
import core


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('request',
                        type=str,
                        help='either load or get')
    parser.add_argument('url',
                        type=str,)
    parser.add_argument('--depth',
                        type=int,
                        required=False,
                        default=2,
                        help="depth for 'load' request")
    parser.add_argument('-n',
                        type=int,
                        required=False,
                        help="amount of urls in response to 'get' request")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.request != 'load' and args.request != 'get':
        print('request can be either load or get')
        sys.exit(0)
    if args.depth < 0:
        print('--depth should be non-negative')
        sys.exit(0)
    if args.n is None and args.request == 'get':
        print("Specify -n when request is 'load'")
        sys.exit(0)
    is_load_request = (args.request == 'load')
    start_time = time.time()
    tracemalloc.start()
    error, response = core.start(
        is_load_request,
        not is_load_request,
        args.url,
        args.n,
        args.depth,
    )
    current, peak = tracemalloc.get_traced_memory()
    end_time = time.time()
    if error:
        print('Error occurred while processing request')
        sys.exit(0)
    if is_load_request:
        print('ok, execution time: {0}s, peak memory usage {1} Mb'.format(end_time - start_time, peak / (1024 ** 2)))
    else:
        if error:
            print(error)
        if response:
            print([link.get_title() for link in response])


if __name__ == '__main__':
    main()
