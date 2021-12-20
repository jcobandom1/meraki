from webexteamssdk import WebexTeamsAPI
from flask import Flask, request
import meraki

app = Flask(__name__)
api = WebexTeamsAPI()
dashboard = meraki.DashboardAPI()

@app.route('/webhook', methods=['POST'])
def webhook():
    me = api.people.me()
    data = request.get_json()
    person_id = data['data']['personId']
    
    if person_id != me.id:
        person = api.people.get(person_id)
        domain = person.emails[0].split("@")[1]
        if domain == "bancobcr.com" or domain == "altus.cr":
            message_id = data['data']['id']
            room_id = data['data']['roomId']
            message = api.messages.get(message_id)
            message = message.text.split("/")
            message = message[1]
            message = message.split()
            command = message[0]

            if command == "orgs":
                webex_msg = "Usted tiene a su cargo las siguientes organizaciones Meraki:"
                org_list = ""
                my_orgs = dashboard.organizations.getOrganizations()
                for org in my_orgs:
                    id = org["id"]
                    name = org["name"]
                    org_list = org_list + "\n* {name}: {id}".format(name=name, id=id)
                webex_msg = webex_msg + org_list
                api.messages.create(roomId = room_id, markdown=webex_msg)
            elif command == "networks":
                org_id = message[1]
                webex_msg = "La organización contiene las siguientes redes:"
                network_list = ""
                my_networks = dashboard.organizations.getOrganizationNetworks(org_id)
                for network in my_networks:
                    id = network["id"]
                    name = network["name"]
                    network_list = network_list + "\n* {name}: {id}".format(name=name, id=id)
                webex_msg = webex_msg + network_list
                api.messages.create(roomId = room_id, markdown=webex_msg)
            elif command == "devices":
                network_id = message[1]
                webex_msg = "La red contiene los siguientes dispositivos:"
                device_list = ""
                my_devices = dashboard.networks.getNetworkDevices(network_id)
                for device in my_devices:
                    model = device["model"]
                    serial = device["serial"]
                    device_list = device_list + "\n* Modelo: {model}, Serial: {serial}".format(model=model, serial=serial)
                webex_msg = webex_msg + device_list
                api.messages.create(roomId = room_id, markdown=webex_msg)
            
    return "Success"

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8085)