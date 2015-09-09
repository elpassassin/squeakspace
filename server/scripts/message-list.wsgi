import util as ut
import util_http as ht
import db_sqlite3 as db
import squeak_ex as ex
import config

def get_handler(environ):

    query = ht.parse_get_request(environ)

    timestamp = ht.convert_int(ht.get_required(query, 'timestamp'), 'timestamp')
    node_name = ht.get_required(query, 'node_name')
    user_id = ht.get_required(query, 'user_id')
    start_time = ht.convert_int(ht.get_optional(query, 'start_time'), 'start_time')
    end_time = ht.convert_int(ht.get_optional(query, 'end_time'), 'end_time')
    max_records = ht.convert_int(ht.get_optional(query, 'max_records'), 'max_records')
    order = ht.get_optional(query, 'order')
    public_key_hash = ht.get_required(query, 'public_key_hash')
    signature = ht.get_required(query, 'signature')

    conn = db.connect(config.db_path)
    try:
        c = db.cursor(conn)
        message_list = db.read_message_list(c, timestamp, node_name, user_id, start_time, end_time,
                                            max_records, order, public_key_hash, signature)

        raise ht.ok_json({'status' : 'ok', 'message_list' : message_list})

    except ex.SqueakException as e:
        raise ht.convert_squeak_exception(e)

    finally:
        db.close(conn)



def main_handler(environ):
    ht.dispatch_on_method(environ, {'GET' : get_handler})

def application(environ, start_response):
    return ht.respond_with_handler(environ, start_response, main_handler)

