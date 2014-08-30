import os
import argparse

from ..slave import Slave
from ..env import WmtEnvironment


class EnsureHttps(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import urlparse
        o = urlparse.urlsplit(values)
        url = urlparse.urlunsplit(('https', o.netloc, o.path, '', ''))
        setattr(namespace, self.dest, url)


def main():
    import argparse
    import traceback

    parser = argparse.ArgumentParser()
    parser.add_argument('id', help='run ID')
    parser.add_argument('--server-url',
                        default='https://csdms.colorado.edu/wmt/api-dev',
                        help='URL of WMT server')
                        #action=EnsureHttps, help='URL of WMT server')
    parser.add_argument('--exec-dir', default=os.path.expanduser('~/.wmt'),
                        help='path to execution directory')
    #parser.add_argument('--env', default=os.path.join(_WMT_ETC, 'environ.yaml'),
    #                    help='path to environment file')
    parser.add_argument('--config', default=None,
                        help='WMT site configuration file')
    parser.add_argument('--show-env', action='store_true',
                        help='print execution environment and exit')
    args = parser.parse_args()

    env = WmtEnvironment.from_config(args.config)

    if args.show_env:
        print str(env)
        return

    slave = Slave(args.server_url, env=env.env)

    try:
        _ = slave.start_task(args.id, dir=args.exec_dir, env=env.env)
    #except TaskError as error:
    #    slave.report_error(args.id, str(error))
    #    print error
    except Exception as error:
        slave.report_error(args.id, traceback.format_exc())
        print traceback.format_exc()
    else:
        slave.report_success(
            args.id, 'simulation is complete and available for pickup)')
        print 'success'
