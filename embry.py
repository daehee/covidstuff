"""
https://embrywomenshealth.com/testing-blitz/
"""
import requests
import json
from urllib.parse import unquote
from datetime import datetime, timedelta

# Filter times between 8AM and 9PM
valid_time_start = datetime.strptime('08:00' , '%H:%M')
valid_time_end = datetime.strptime('21:00', '%H:%M')

now = datetime.now()
start_date = now.strftime('%Y-%m-%d')
next_week = now + timedelta(days=7)
end_date = next_week.strftime('%Y-%m-%d')
start_date_time = now.strftime('%Y-%m-%d %H:%M')

def get_appts(dept_id, appt_type_id):
    url = 'https://ytvorydlwnfwhc7l7vcw4yxo5y.appsync-api.us-east-1.amazonaws.com/graphql'
    headers = {
        'origin': 'https://app.backstagemedical.co',
        'X-Api-Key': 'da2-oevatclh6vfzrjexqfegdx5ugi'
    }
    data = {
      'operationName': 'listApptOpenSlotswithproviderandappointtype',
      'variables': {
        'practiceid': 9567,
        'offset':0,
        'pageSize':6000,
        'startDate': start_date,
        'endDate': end_date,
        'departmentid': dept_id,
        'appointmenttypeid': appt_type_id,
        'startDatetime': start_date_time
        },
      'query': 'query listApptOpenSlotswithproviderandappointtype($offset: Int!, $pageSize: Int!, $practiceid: Int!, $startDate: AWSDate, $endDate: AWSDate, $startDatetime: String, $departmentid: Int!, $providerid: Int, $appointmenttypeid: Int) {\n  listApptOpenSlotswithproviderandappointtype(offset: $offset, pageSize: $pageSize, practiceid: $practiceid, startDate: $startDate, endDate: $endDate, startDatetime: $startDatetime, departmentid: $departmentid, providerid: $providerid, appointmenttypeid: $appointmenttypeid) {\n    apptopenslot {\n      appointment_open_slot_id\n      practiceid\n      date\n      appointmentid\n      departmentid\n      departmentid\n      localproviderid\n      appointmenttype\n      providerid\n      starttime\n      duration\n      appointmenttypeid\n      patientappointmenttypename\n      createdat\n      updatedat\n      __typename\n    }\n    totalcount\n    __typename\n  }\n}\n'
    }
    resp = requests.post(url, json=data, headers=headers)
    resp_json = json.loads(resp.text)
    appts = resp_json['data']['listApptOpenSlotswithproviderandappointtype']['apptopenslot']
    filtered_appts = []
    for x in appts:
        dt = datetime.strptime(x['starttime'], '%H:%M:%S')
        if valid_time_start < dt < valid_time_end:
            filtered_appts.append(x)
    return filtered_appts

def main():
    with open('embry.json') as f:
        locs = json.load(f)

    print('')
    for v in locs:
        appts = get_appts(v['dept_id'], v['appt_type_id'])

        appt_site = unquote(appts[0]['appointmenttype'])
        print(f"{appt_site}: {v['name']}")

        book_url = f"https://app.backstagemedical.co/widgets/#/schedule-appointment?pId=9567&providerId=131&typeId={v['appt_type_id']}"
        book_url_now = book_url + '&autoschedule=1'
        book_url_later = book_url + '&autoschedule=0'
        print(f'Book now: {book_url_now}')
        print(f'Book later: {book_url_later}')

        print('First available:')
        for v in range(0,5):
            print(f"{appts[v]['date']} {appts[v]['starttime']}")

        print('')

if __name__ == '__main__':
    main()
