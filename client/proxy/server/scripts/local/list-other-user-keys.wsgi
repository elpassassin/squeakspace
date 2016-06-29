import util as ut
import util_http as ht
import db_sqlite3 as db
import squeak_ex as ex
import config


def get_handler(environ):

    query = ht.parse_get_request(environ)
    cookies = ht.parse_cookies(environ)

    user_id = ht.get_required_cookie(cookies, 'user_id')
    session_id = ht.get_required_cookie(cookies, 'session_id')

    other_user_id = ht.get_optional(query, 'other_user_id')
    node_name = ht.get_optional(query, 'node_name')

    conn = db.connect(config.db_path)
    try:
        c = db.cursor(conn)
        keys = db.list_other_user_keys(c, user_id, session_id, other_user_id, node_name)

        raise ht.ok_json({'status' : 'ok', 'keys' : keys})
        
    except ex.SqueakException as e:
        raise ht.convert_squeak_exception(e)

    finally:
        db.close(conn)

def main_handler(environ):
    ht.dispatch_on_method(environ, {
            'GET' : get_handler})

def application(environ, start_response):
    return ht.respond_with_handler(environ, start_response, main_handler)
