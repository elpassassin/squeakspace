import squeakspace.common.util as ut
import squeakspace.common.util_http as ht
import squeakspace.proxy.server.db_sqlite3 as db
import squeakspace.common.squeak_ex as ex
import config

def get_handler(environ):

    query = ht.parse_get_request(environ)

    action = ht.get_required(query, 'action')

    conn = db.connect(config.db_path)
    try:
        c = db.cursor(conn)

        if action == 'database':
            database = db.dump_local_database(c)
            raise ht.ok_json({'status' : 'ok', 'database' : database})

        else:
            raise ht.BadFieldResponse('action', action)
        
    except ex.SqueakException as e:
        raise ht.convert_squeak_exception(e)

    finally:
        db.close(conn)



def main_handler(environ):
    ht.dispatch_on_method(environ, {
            'GET' : get_handler})

def application(environ, start_response):
    return ht.respond_with_handler(environ, start_response, main_handler)