import requests
import json

def check_inventory(product_id, zipcode):
    url = 'https://www.cvs.com/RETAGPV3/Inventory/V1/getStoreDetailsAndInventory'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=utf-8',
        'Origin': 'https://www.cvs.com',
        'Content-Length': '441',
        'Accept-Language': 'en-US,en;q=0.9',
        'Host': 'www.cvs.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15',
        'Referer': 'https://www.cvs.com/shop/abbott-binaxnow-covid-19-antigen-self-test-2-tests-for-serial-testing-prodid-550147',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    data = {
        'getStoreDetailsAndInventoryRequest': {
        'header': {
            'apiKey':'a2ff75c6-2da7-4299-929d-d670d827ab4a',
            'apiSecret':'a8df2d6e-b11c-4b73-8bd3-71afc2515dae',
            'appName':'CVS_WEB',
            'channelName':'WEB',
            'deviceType':'DESKTOP',
            'version':'1.0',
            'deviceToken':'device12345',
            'lineOfBusiness':'RETAIL',
            'responseFormat':'JSON',
            'securityType':'apiKey',
            'source':'CVS_WEB',
            'type':'rdp'
        },
        'productId':product_id,
        'geolatitude':'',
        'geolongitude':'',
        'addressLine':zipcode
        }
    }

    try:
        resp = requests.post(url, headers=headers, json=data)
    except requests.RequestException as e:
        raise SystemExit(e)

    resp_json = json.loads(resp.text)
    locs = resp_json['atgResponse']

    # Filter locations with inventory available
    filtered_locs = []
    for x in locs:
        if x['Qty'] > 0:
            filtered_locs.append(x)

    return filtered_locs


def main():
    with open('kits.json') as f:
        cfg = json.load(f)

    print('')
    for p in cfg['products']:
        print(f"{p['name']}\n=========")
        locs = check_inventory(p['product_id'], cfg['zip'])
        if len(locs) > 0:
            for v in locs:
                print(f"Found {v['Qty']} @ {v['storeAddress']} {v['City']} ({v['dt']} mi away)")
        else:
            print('N/A')
        print('\n')

if __name__ == '__main__':
    main()
