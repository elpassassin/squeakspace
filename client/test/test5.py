#!/usr/bin/python

import json
import httplib as ht

import client_path
import client as cl
import util as ut
import client_types as tp

import test_params


conn = ht.HTTPConnection(test_params.server_address, test_params.server_port)
client = cl.Client(conn, test_params.node_name)

key_type = test_params.key_type
key_parameters = {'name_real' : 'Alf',
                  'name_email' : 'alf@example.com',
                  'key_type' : 'RSA',
                  'key_length' : 1024,
                  'key_usage' : 'cert',
                  'subkey_type' : 'RSA',
                  'subkey_length' : 1024,
                  'subkey_usage' : 'encrypt,sign,auth'}

Alf = tp.User('Alf',
        key=ut.createPrivateKey(key_type, key_parameters),
        revoke_date=None,
        default_mail_access='allow',
        when_mail_exhausted='block',
        quota_size=100*1024*1024,
        mail_quota_size=10*1024*1024,
        user_class=None,
        auth_token=None)


resp = Alf.create(client)
assert(resp['status'] == 'ok')

print (client.send_debug({'action' : 'database'}))
client.assert_integrity(True)

mess = 'This is a test'
(resp, gen) = client.send_message(
        to_user=Alf.user_id,
        to_user_key_hash=Alf.key.public_key_hash,
        from_user=None,
        from_key=None,
        message=mess,
        proof_of_work_args=json.dumps({'algorithm':'dummy','level':2}))

assert(resp['status'] == 'ok')
mess_id = gen[0]
client.assert_integrity(True)


resp = client.read_message(Alf.user_id, mess_id, Alf.key)
assert(resp['status'] == 'ok')
message = resp['message']
assert(message['message'] == mess)
assert(message['message_id'] == mess_id)

client.assert_integrity(True)

resp = client.delete_message(Alf.user_id, mess_id, Alf.key)
assert(resp['status'] == 'ok')
client.assert_integrity(True)

resp = Alf.delete(client)
assert(resp['status'] == 'ok')

client.assert_db_empty()
client.assert_integrity(True)

