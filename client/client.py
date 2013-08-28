'''Client for osst VM manager API'''
import argparse
import urllib2
import json


def build_json(**kwargs):
    return json.dumps(kwargs)


def requester(host, port, action, json=None, method=None):
    '''Send requests for VM manager API functions and
    output result on screen'''

    url = 'http://%s:%d/api/v1/%s' % (host, port, action)
    req = urllib2.Request(url, json)
    if method:  # if method is undefined, POST used by default
        req.get_method = lambda: method
    try:
        print urllib2.urlopen(req).read()
    except urllib2.HTTPError, e:
        print e.read()


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('-host', default='localhost')
    parser.add_argument('-port', type=int, default=8080)
    subparsers = parser.add_subparsers()
    for act in ['create', 'power_on', 'reboot', 'power_off', 'delete']:
        subparser = subparsers.add_parser(act)
        subparser.add_argument('-vmname', required=True)
        subparser.set_defaults(action=act)
    subparser = subparsers.add_parser('list_all')
    subparser.set_defaults(action='list_all')
    args = parser.parse_args()
    http_methods = {'list_all': 'GET', 'create': 'PUT', 'delete': 'DELETE'}
    requester(args.host, args.port, args.action,
              build_json(vmname=args.vmname)
              if hasattr(args, 'vmname') else None,
              http_methods.get(args.action))


if __name__ == '__main__':
    main()
