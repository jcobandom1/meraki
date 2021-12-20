from webexteamssdk import WebexTeamsAPI
from flask import Flask, request
import meraki

app = Flask(__name__)
api = WebexTeamsAPI()
dashboard = meraki.DashboardAPI()
my_orgs = dashboard.organizations.getOrganizations()
org_id = my_orgs[0]['id']

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
            param = message[1]

            if command == "serial":
                serial = param
                my_devices = dashboard.organizations.getOrganizationDevices(organizationId=org_id)
                requested_device = None
                for device in my_devices:
                    if device["serial"] == serial:
                        requested_device = device
                if requested_device is not None:
                    mac = device["mac"]
                    model = device["model"]
                    url = device["url"]
                    message = "El dispositivo solitado es modelo **{model}** con dirección mac **{mac}** y el url de administración es {url}"
                    api.messages.create(roomId = room_id, markdown=message.format(mac=mac, model=model, url=url))
                else:
                    api.messages.create(roomId = room_id, text="No se encontró un dispositivo con ese número de serie")
    
    return "Success"

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8085)