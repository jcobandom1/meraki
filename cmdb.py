import meraki
import os
import json
import requests

base_url = "https://dev90052.service-now.com"
username = os.environ["SERVICENOW_USERNAME"]
password = os.environ["SERVICENOW_PASSWORD"]

def get_device_type(model):
    if model.startswith('MR'):
        return 'Router'
    elif model.startswith('MS'):
        return 'Switch'
    elif model.startswith('MX'):
        return 'Firewall'
    elif model.startswith('MV'):
        return 'Camera'
    else:
        return 'Meraki Device'

def get_api_url(device_type):
    if device_type == 'Router':
        return base_url + "/api/now/table/cmdb_ci_ip_router"
    elif device_type == 'Switch':
        return base_url + "/api/now/table/cmdb_ci_ip_switch"
    elif device_type == 'Firewall':
        return base_url + "/api/now/table/cmdb_ci_ip_firewall"
    else:
        return base_url + "/api/now/table/cmdb_ci_ip_device"
    
dashboard = meraki.DashboardAPI()

my_orgs = dashboard.organizations.getOrganizations()
org_id = my_orgs[0]['id']
my_devices = dashboard.organizations.getOrganizationDevices(organizationId=org_id)

headers = {
  "Content-Type": "application/json"
}
count = 0
for device in my_devices:
    serial = device.get('serial')
    ip = device.get('lanIp')
    model = device.get('model')
    device_type = get_device_type(model)
    mac = device.get('mac')
    payload = {
        "serial_number": serial,
        "ip_address": ip,
        "device_type": device_type,
        "manufacturer": "Cisco",
        "model_id": model,
        "short_description": "MAC Address: {}".format(mac),
        "name": "Meraki {}".format(model)
    }
    data = json.dumps(payload)
    url = get_api_url(device_type)
    response = requests.post(url, auth=(username, password), headers=headers, data=data)
    print("Actualizando equipo {} de tipo {} con número de serie {}".format(model, device_type, serial))
    count = count + 1
print("Se actualizaron {} equipos.".format(count))