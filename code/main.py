#import pytest
from flask import Flask, render_template, request, make_response, session
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
import authomatic
import logging
import uuid
from config import CONFIG
import pymongo
import pprint
#from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, OperationFailure

client = pymongo.MongoClient("mongodb+srv://sherisenia:pa$$w0rd@cluster0.y4ewv.mongodb.net/test?retryWrites=true&w=majority")
db = client.test
collection = db.webusers_db



# Instantiate Authomatic.
authomatic = Authomatic(CONFIG, 'your secret string', report_errors=False)

app = Flask(__name__,template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    # We need response object for the WerkzeugAdapter.
    response = make_response()
    # Log the user in, pass it the adapter and the provider name.
    result = authomatic.login(WerkzeugAdapter(request, response), provider_name)
    # If there is no LoginResult object, the login procedure is still pending.
    if result:
        if result.user:
            # We need to update the user to get more info.
            result.user.update()
            result.user.myuuid = str(uuid.uuid4())


            user_exist = collection.find_one({"mail": result.user.email})
            if user_exist:
              result.user.myuuid = user_exist["myuuid"]
            else:
              dns = {"mail": result.user.email, "myuuid":result.user.myuuid}
              collection.insert_one(dns)



        # The rest happens inside the template.
#        POST  = [{
#            "_id": result.user.id,
 #           "name": result.user.name,
  #          "mail": result.user.email}]
   #     try:
    #       result = collection.insert_many(POST,ordered=False)

     #   except pymongo.errors.BulkWriteError as e:
      #     print(e.details['writeErrors'])

        return render_template('webpageoauth3.html', result=result)

    # Don't forget to return the response.
    return response

# Run the app on port 5000 on all interfaces, accepting only HTTPS connections
if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc', host='192.168.37.135', port=5000)
