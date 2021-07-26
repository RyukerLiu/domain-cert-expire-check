import ssl
import OpenSSL
import datetime
import pytz
import requests
import json
import os


def main():
    warning_days = 30

    domains = ['www.omnisegment.com', "www.omnibpm.com", "omni.ag"]

    now = datetime.datetime.now(datetime.timezone.utc)

    content = ''

    for domain in domains:
        not_afger_datetime = get_SSL_Expiry_Date(domain, 443)
        days_to_expired = (not_afger_datetime - now).days

        if days_to_expired < warning_days:
            alert = 'Warning!!!!!!'
        else:
            alert = ''

        content += f'domain: {domain}\n' \
                   f'expired_time: {not_afger_datetime}\n' \
                   f'days to expired: {days_to_expired}\n' \
                   f'{alert}\n' \
                   f'\n'


    SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
    url = SLACK_WEBHOOK_URL

    data = {
        'text': content
        
    }
    payload=json.dumps(data)
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def get_SSL_Expiry_Date(host, port):
    cert = ssl.get_server_certificate((host, port))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    not_after = x509.get_notAfter()
    not_afger_datetime = datetime.datetime.strptime(not_after.decode('ascii'), '%Y%m%d%H%M%SZ')
    not_afger_datetime = pytz.UTC.localize(not_afger_datetime)
    taipei = pytz.timezone('Asia/Taipei')
    not_afger_datetime = not_afger_datetime.astimezone(taipei)
    return not_afger_datetime


if __name__ == '__main__':
    main()