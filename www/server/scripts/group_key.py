import squeakspace.common.util as ut
import squeakspace.common.util_http as ht
import squeakspace.server.db_sqlite3 as db
import squeakspace.common.squeak_ex as ex
import config


def post_handler(environ):

    query = ht.parse_post_request(environ)

    timestamp = ht.convert_int(ht.get_required(query, 'timestamp'), 'timestamp')
    node_name = ht.get_required(query, 'node_name')
    group_id = ht.get_required(query, 'group_id')
    owner_id = ht.get_required(query, 'owner_id')
    key_use = ht.get_required(query, 'key_use')
    key_type = ht.get_optional(query, 'key_type')
    pub_key = ht.get_optional(query, 'pub_key')
    public_key_hash = ht.get_required(query, 'public_key_hash')
    signature = ht.get_required(query, 'signature')

    conn = db.connect(config.db_path)
    try:
        c = db.cursor(conn)
        db.change_group_key(c, timestamp, node_name, group_id, owner_id, key_use, key_type, pub_key,
                               public_key_hash, signature)
        db.commit(conn)

        raise ht.ok_json({'status' : 'ok'})

    except ex.SqueakException as e:
        raise ht.convert_squeak_exception(e)

    finally:
        db.close(conn)


def get_handler(environ):

    query = ht.parse_get_request(environ)

    timestamp = ht.convert_int(ht.get_required(query, 'timestamp'), 'timestamp')
    node_name = ht.get_required(query, 'node_name')
    group_id = ht.get_required(query, 'group_id')
    owner_id = ht.get_required(query, 'owner_id')
    key_use = ht.get_required(query, 'key_use')
    public_key_hash = ht.get_required(query, 'public_key_hash')
    signature = ht.get_optional(query, 'signature')

    conn = db.connect(config.db_path)
    try:
        c = db.cursor(conn)
        group_key = db.read_group_key(c, timestamp, node_name, group_id, owner_id, key_use, public_key_hash, signature)

        raise ht.ok_json({'status' : 'ok', 'group_key' : group_key})

    except ex.SqueakException as e:
        raise ht.convert_squeak_exception(e)

    finally:
        db.close(conn)

def main_handler(environ):
    ht.dispatch_on_method(environ, {
            'POST' : post_handler,
            'GET' : get_handler})
            
def application(environ, start_response):
    return ht.respond_with_handler(environ, start_response, main_handler)
