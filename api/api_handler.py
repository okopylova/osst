from webob import Request, Response
from webob import exc
from osst import vm_manager


# POST method used for other actions
_req_methods = {'list_all': 'GET',
                'create': 'PUT',
                'delete': 'DELETE'}


class ApiHandler(object):

    def __call__(self, environ, start_response):
        req = Request(environ)
        meth_name = req.path[req.path.rindex('/') + 1:]
        try:
            approved_method = _req_methods.get(meth_name, 'POST')
            if req.method != approved_method:
                raise exc.HTTPBadRequest('Incorrect method for %s, use %s' %
                                         (req.path, approved_method))
            if hasattr(vm_manager, meth_name):
                if(meth_name == 'list_all'):
                    resp = Response(', '.join(vm_manager.list_all()))
                else:
                    resp = Response(getattr(vm_manager, meth_name)(**req.json))
            else:
                raise exc.HTTPBadRequest('No such action %s' % req.path)
        except exc.HTTPException, e:
            resp = e
        except Exception, e:
            resp = exc.HTTPBadRequest(e.get_error_message())
        return resp(environ, start_response)
