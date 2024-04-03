from collections import defaultdict
import requests
import validators
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--subdomain", type=str, nargs="*", required=True)
parser.add_argument("--domain", type=str, required=True)
parser.add_argument("--apikey", type=str, required=True)
parser.add_argument("--ip", type=str, required=True)
args = parser.parse_args()


subdomains_list = args.subdomain
domain = args.domain
api_key = args.apikey
ip_address = args.ip


def validate_argsformat():
    if not validators.ipv4(ip_address):
        print("ERROR MESSAGE: Ip's Format Is Not Valid")
        return False
    if not validators.domain(domain):
        print("ERROR MESSAGE: Domain's Format Is Not Valid")
        return False
    for subdomain in subdomains_list:
        if not subdomain.isalnum():
            print("ERROR MESSAGE: Subdomain's Format Is Not Valid")
            return False
    return True


def handle_response(response):
    if not response.ok:
        print("ERROR CODE:", response.status_code)
        print("ERROR MESSAGE:", response.json()["message"])
        return False
    return True

def update_subdomain_records():
    validation_result = validate_argsformat()
    if not validation_result:
        return 0

    base_url = f"https://napi.arvancloud.ir/cdn/4.0/domains/{domain}/dns-records/"
    request_headers = {
        "Authorization": f"apikey {api_key}",
        "Accept": "application/json",
    }
    subdomains_dict = defaultdict(str)

    list_response = requests.get(base_url, headers=request_headers, timeout=30)
    request_result = handle_response(list_response)
    if not request_result:
        return 0

    record_list = list_response.json()

    for record in record_list["data"]:
        subdomains_dict[record["name"]] = record["id"]

    for subdomain in subdomains_list:
        record_payload = {
            "value": [{"ip": ip_address}],
            "type": "a",
            "name": subdomain,
            "ttl": 120,
            "cloud": False,
        }

        subdomain_id = subdomains_dict[subdomain]

        if not subdomain_id:
            add_response = requests.post(
                url=base_url, headers=request_headers, json=record_payload, timeout=30
            )
            handle_response(add_response)
            continue

        record_url = base_url + subdomain_id
        update_response = requests.put(
            url=record_url, json=record_payload, headers=request_headers, timeout=30
        )
        handle_response(update_response)


update_subdomain_records()
