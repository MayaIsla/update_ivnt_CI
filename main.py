import requests
import base64
from openpyxl import load_workbook
import pandas as pd
from datetime import datetime, date
import json
import os

pd.options.display.max_colwidth = 1000
pd.set_option('display.float_format', lambda x: '%.3f' % x)

datetime_Format = "{:%Y-%m-%d}".format(datetime.now())

with open('C:/ivnt_encode.txt', 'rb') as ivnt_key:
  coded_string_ivnt = ivnt_key.read()
ivnt_api__Key = base64.b64decode(coded_string_ivnt).decode('utf-8')

api_uri = "https://tenant.saasit.com/api/odata/businessobject/CIs"
iv_auth_header = {'Authorization': ivnt_api__Key}

newpath = "C:/Logs"

original_df = pd.read_csv("C:/IMEI.csv", index_col=False)
df = original_df.drop(["Suspend Date", "Primary Number Y or N", "Designated Employee"], axis=1)

for row in df.itertuples():
   ivnt_phone_model = (row.Model)
   print(row)
   ivnt_phone_number = (row.Number)
   ivnt_loginID = (row.ADID)
   ivnt_IMEI = (row.IMEI)

   ivnt_get_phone = "https://tenant.saasit.com/api/odata/businessobject/CIs?$search=" + ivnt_IMEI
   request_ivnt_phone_exists = requests.get(url = ivnt_get_phone, headers=iv_auth_header)
   if request_ivnt_phone_exists.status_code == 204: #204 no content - means phone doesn't exist
      body_response = str('{"MACAddress": ' + '"' + ivnt_phone_number + '","Name":' + '"' +  ivnt_IMEI + '","SerialNumber":' + '"' + ivnt_phone_number + '","LoginName":' + '"' + ivnt_loginID + '","Status": "Assigned",' + '"ivnt_AssetSubtype": "Mobile Phone' +  '","CIType": "ivnt_Infrastructure"' + ',"Model":' + '"' + ivnt_phone_model+ '"' +"}")
      update_CI = requests.post(url=api_uri, data= body_response, headers=iv_auth_header)
      #print(update_CI)
   else:
      if request_ivnt_phone_exists.status_code == 200:
          request_iv_get_recID_text = request_ivnt_phone_exists.text
          json_RecID = json.loads(request_iv_get_recID_text)

          for i in json_RecID['value']:
              ivnt_ci_RecId = (i['RecId'])
          
          ivnt_ci_mod_url = "https://tenant.saasit.com/api/odata/businessobject/CIs('" + ivnt_ci_RecId + "')"
          body_response = str('{"MACAddress": ' + '"' + ivnt_phone_number + '","Name":' + '"' +  ivnt_IMEI + '","SerialNumber":' + '"' + ivnt_phone_number + '","LoginName":' + '"' + ivnt_loginID + '","Status": "Assigned",' + '"ivnt_AssetSubtype": "Mobile Phone' +  '","CIType": "ivnt_Infrastructure"' + ',"Model":' + '"' + ivnt_phone_model+ '"' +"}")
          update_existing_CI = requests.put(url=ivnt_ci_mod_url, data= body_response, headers=iv_auth_header)
          #print(update_existing_CI)

      else: 
         #print("No 200 or 204 error please look at transcript.")
         ivnt_phone_model = (row.Model)
         ivnt_phone_number = (row.Number)
         ivnt_loginID = (row.ADID)
         ivnt_IMEI = (row.IMEI)

         ivnt_get_phone = "https://tenant.saasit.com/api/odata/businessobject/CIs?$search=" + ivnt_IMEI
         request_ivnt_phone_exists = requests.get(url = ivnt_get_phone, headers=iv_auth_header)
         text_CSV =  request_ivnt_phone_exists.text
         with open("C:/Logs/file.csv","w") as file:
            file.write(text_CSV + "\n")

      
   #body_response = str('{"MACAddress": ' + '"' + ivnt_phone_number + '","Name":' + '"' +  ivnt_IMEI + '","SerialNumber":' + '"' + ivnt_phone_number + '","LoginName":' + '"' + ivnt_loginID + '","Status": "Assigned",' + '"ivnt_AssetSubtype": "Mobile Phone' +  '","CIType": "ivnt_Infrastructure"' + ',"Model":' + '"' + ivnt_phone_model+ '"' +"}")
   #update_CI = requests.post(url=api_uri, data= body_response, headers=iv_auth_header)
   #print(update_CI.text)
