from flask import Flask, request, Response, render_template
import ssh_client
import helpers
import json
import routers

app = Flask(__name__, static_url_path='/static')

# main route where we render the html
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# GET route in order to fetch the available routers for a given ASN
@app.route('/routers/<asn>', methods=['GET'])
def get_routers(asn):
  results = []
  for r in routers.routers_list:
    if r['asn'] == asn:
      # only return the address/hostname, the location and the OS type of the matching routers
      results.append(dict(name=r['address'][0],
                          location=r['location'],
                          type=r['type'])
      )
  return json.dumps(results)


# POST route in order to invoke the looking glass service
@app.route('/lg', methods=['POST'])
def lg():
    # get parameters from the request body
    req_data = request.get_json()
    # obtain the router object and the ready-to-enter command
    router, command = helpers.get_vars(req_data['router'], req_data['cmd'], req_data['ipprefix'])
    # instantiate our SSH_Client class
    client = ssh_client.SSH_Client(router)
    # run the command
    output_stream = client.run(command)
    # generator function
    def generate():
        for chunk in output_stream:
            yield chunk
        # close the underlaying transport session of the ssh client
        client.close()
    # each yield iteration  in generate() is sent directly to the browser
    return Response(generate())


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

