import util as ut
import util_http as ht
import db_sqlite3 as db

def get_handler(environ):
    global counter

    query = ht.parse_get_request(environ)

    node_name = ht.get_required(query, 'node_name')

    version = db.read_version(node_name)

    raise ht.ok_json(
            {'status' : 'ok',
             'version' : version})

def main_handler(environ):
    ht.dispatch_on_method(environ, {'GET' : get_handler})

def application(environ, start_response):
    return ht.respond_with_handler(environ, start_response, main_handler)
