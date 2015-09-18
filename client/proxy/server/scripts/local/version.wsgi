import util as ut
import util_http as ht
import squeak_ex as ex
import config
import config_proto

def get_handler(environ):

    try:
        version = config_proto.version

        raise ht.ok_json({'status' : 'ok', 'version' : version})
        
    except ex.SqueakException as e:
        raise ht.convert_squeak_exception(e)


def main_handler(environ):
    ht.dispatch_on_method(environ, {
            'GET' : get_handler})

def application(environ, start_response):
    return ht.respond_with_handler(environ, start_response, main_handler)
