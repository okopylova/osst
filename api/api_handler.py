from webob import Request, Response
from webob import exc
from osst import vm_manager


class APIHandler(object):

    def __call__(self, environ, start_response):
        req = Request(environ)
        action = req.path.strip('/').replace('/', '_') + '_' + req.method
        try:
            if hasattr(self, action):
                resp = getattr(self, action)(req)
            else:
                resp = exc.HTTPBadRequest('Incorrect path or method')
        except exc.HTTPException as e:
            resp = e
        except ValueError:
            resp = exc.HTTPBadRequest('Incorrect data for request')
        except Exception as e:
            resp = exc.HTTPServerError(e.message)
        return resp(environ, start_response)

    def api_v1_list_all_GET(self, req):
        return Response(', '.join(vm_manager.list_all()))

    def api_v1_create_PUT(self, req):
        return Response(vm_manager.create(**req.json))

    def api_v1_delete_DELETE(self, req):
        return Response(vm_manager.delete(**req.json))

    def api_v1_reboot_POST(self, req):
        return Response(vm_manager.reboot(**req.json))

    def api_v1_power_on_POST(self, req):
        return Response(vm_manager.power_on(**req.json))

    def api_v1_power_off_POST(self, req):
        return Response(vm_manager.power_off(**req.json))
