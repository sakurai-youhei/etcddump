import argparse
from os.path import basename
from sys import argv
from sys import version_info
from time import gmtime

from etcddump import operations


def version():
    try:
        from pkg_resources import get_distribution
        pkgver = get_distribution("etcddump").version
    except Exception:
        pkgver = '.'.join(map(str, gmtime()[:3]))

    return "{} v{} from {} (Python {}.{}.{})".format(
        basename(argv[0]), pkgver, __file__, *version_info[:3])


def main(**kw):
    parser = argparse.ArgumentParser(**kw)
    parser.add_argument('-f', '--file',
                        default=None,
                        help='File where the dump is located.')
    parser.add_argument('-v', '--version',
                        action='version',
                        version=version(),
                        help='Show version information.')
    parser.add_argument('-p', '--preserve-indexes',
                        dest='preserve_indexes',
                        action='store_true',
                        help='Try to keep the same indexes as before.')
    parser.add_argument('action',
                        help='What to do: dump or restore')
    parser.add_argument('url',
                        help='client url such as http://localhost:2379.')
    args = parser.parse_args()

    if args.action == 'dump':
        cl = operations.Dumper(url=args.url)
        cl.dump(filename=args.file)
    elif args.action == 'restore':
        cl = operations.Restorer(url=args.url)
        cl.restore(filename=args.file, preserve_indexes=args.preserve_indexes)
