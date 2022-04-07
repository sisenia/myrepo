from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from dnszone import DnsZone
import pymongo
import socket
import dns.resolver

client = pymongo.MongoClient("mongodb+srv://sherisenia:pa$$w0rd@cluster0.y4ewv.mongodb.net/test?retryWrites=true&w=majority")
db = client.test
collection = db.webusers_db

my_zone = DnsZone('clim.test', '192.168.37.135')

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('fqdn')
parser.add_argument('ipv4')
parser.add_argument('token')

class PostAddRecord(Resource):
  # curl http://192.168.37.127:5050/dns/addpost -d "fqdn=<fqdn>" -d "ipv4=<ipv4>" -X POST

  # JSON
  # curl -X POST http://127.0.0.1:5050/dns/addpost -H "Content-Type: application/json" -d '{"fqdn":"sundayyyy","ipv4":"2.3.5.5"}'
  def post(self):
    args = parser.parse_args()
    fqdn = str(args['fqdn']) + ".clim.test"
    ipv4 = args['ipv4']
    token = args['token']
    if dict(collection.find_one({"myuuid": args["token"]})):
      my_zone.update_address(fqdn, ipv4)
      return {'status_update': 'ok'}

    else:
      return {'status_update': 'not ok'}

    my_zone.add_address(fqdn, ipv4)
    return {'status_add': 'ok'}


class PostUpdateRecord(Resource):
  # curl http://192.168.37.127:5050/dns/updatepost -d "fqdn=<fqdn>" -d "ipv4=<ipv4>" -X POST
  def checkTokenDB(token):
    print(token_exists)
    return token_exists

  def post(self):
    args = parser.parse_args()
    fqdn = args['fqdn'] + ".clim.test"
    ipv4 = args['ipv4']
    print('token')
    token = args['token']

    try:
       if dict(collection.find_one({"myuuid": args["token"]})):
          my_zone.update_address(fqdn, ipv4)
          return {'status_update': 'ok'}

    except TypeError:
       return {'status_update': 'Token does not exist or Token is wrong !'}

class GetRecord(Resource):
  # curl http://192.168.37.127:5050/dns/put -d "fqdn=<fqdn>" -X PUT
  def put (self):
    args = parser.parse_args()
    fqdn = args['fqdn'] + ".clim.test"
    token = args['token']
    if dict(collection.find_one({"myuuid": args["token"]})):
      my_zone.update_address(fqdn, ipv4)
      return {'status_update': 'ok'}

    else:
      return {'status_update': 'not ok'}

    result = my_zone.check_address(fqdn)
    print(result)
    return {'status_ip': 'ok'}

class DelRecord(Resource):
  # curl http://192.168.37.127:5050/dns/del -d "fqdn=<fqdn>" -X DELETE
  def delete (self):
    args = parser.parse_args()
    fqdn = args['fqdn'] + ".clim.test"
    token = args['token']
    if dict(collection.find_one({"myuuid": args["token"]})):
      my_zone.update_address(fqdn, ipv4)
      return {'status_update': 'ok'}

    else:
      return {'status_update': 'not ok'}

    my_zone.clear_address(fqdn)
    return {'status_delete': 'ok'}

api.add_resource(PostAddRecord, '/dns/addpost')
api.add_resource(PostUpdateRecord, '/dns/updatepost')
api.add_resource(GetRecord, '/dns/put')
api.add_resource(DelRecord, '/dns/del')
print('ok')

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5050)
