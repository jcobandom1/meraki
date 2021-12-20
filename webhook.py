from webexteamssdk import WebexTeamsAPI
from flask import Flask, request

app = Flask(__name__)
api = WebexTeamsAPI()
room_id = "Y2lzY29zcGFyazovL3VzL1JPT00vYzg2ZjljMDAtNTY5Yi0xMWVjLThjNmUtYjE2MmM5MjUxYmVl"

message = '''
# Alerta de Meraki
## Tipo de alerta: {alert_type}
El dispositvo **{device}** de la red **{network}** superó el umbral de **{threshold} MB** con una utilización de **{usage} MB**, Mac address **{macaddress}** , serial **{serial}**.
'''

@app.route('/meraki', methods=['POST'])
def webhook():
    data = request.get_json()
    alert_type = data['alertType']
    threshold = int(data['alertData']['usageThreshold'])
    threshold = threshold//1000000
    usage = int(data['alertData']['kbTotal'])
    usage = usage//1000000
    network = data['networkName']
    device = data['deviceName']
    macaddress = data['deviceMac']
    serial = data['deviceSerial']
    
    api.messages.create(roomId=room_id, 
                        markdown=message.format(alert_type=alert_type, 
                                                device=device, 
                                                network=network, 
                                                threshold=threshold, 
                                                usage=usage))
    
    return "Success"

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8085)