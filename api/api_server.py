"""Script starts api server"""
from argparse import ArgumentParser
from wsgiref.simple_server import make_server
from api_handler import ApiHandler


if __name__ == '__main__':
    parser = ArgumentParser(description='Starts VM manager API server')
    parser.add_argument('-host', default='localhost')
    parser.add_argument('-port', type=int, default=8080)
    args = parser.parse_args()
    handler = ApiHandler()
    httpd = make_server(args.host, args.port, handler)
    print 'Started on http://%s:%s' % (args.host, args.port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
        exit()
