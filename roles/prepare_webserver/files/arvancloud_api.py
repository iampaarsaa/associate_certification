import requests
import validators
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--sub",type=str, nargs="*",required=True)
parser.add_argument("--domain", type=str,required=True)
parser.add_argument("--key", type=str,required=True)
parser.add_argument("--ip", type=str,required=True)
args = parser.parse_args()


given_subdomains = args.sub
domain = args.domain
api_key = args.key
ip_address = args.ip


base_url = f"https://napi.arvancloud.ir/cdn/4.0/domains/{domain}/dns-records/"
request_headers = {
    "Authorization": f"apikey {api_key}",
    "Accept": "application/json",
}

def validate_argsformat():
    if not validators.ipv4(ip_address):
        print("ERROR MESSAGE: Ip's Format Is Not Valid")
        exit()
    if not validators.domain(domain):
        print("ERROR MESSAGE: Domain's Format Is Not Valid")
        exit()
    for each_subdomain in given_subdomains:
        if not each_subdomain.isalpha():
            print("ERROR MESSAGE: Subdomain's Format Is Not Valid")
        # full_domain = each_subdomain + "." + domain


def handle_errors(response):
    if not response.ok:
        print("ERROR CODE:", response.status_code)
        print("ERROR MESSAGE:", response.reason)
        exit()


def update_subdomain_records():
    validate_argsformat()
    subdomain_list=[]
    for each_given_subdomain in given_subdomains:
        subdomain_list.append({"name": each_given_subdomain, "id":""})

    list_response = requests.get(base_url, headers=request_headers, timeout=30)
    handle_errors(list_response)

    response_json = list_response.json()

    record_dict = {}
    for record in response_json["data"]:
        record_dict[record['name']] = record['id']

    for subdomain in subdomain_list:
        subdomain["id"] = record_dict.get(subdomain["name"])
        record_payload = {
            "value": [{"ip": ip_address}],
            "type": "a",
            "name": subdomain["name"],
            "ttl": 120,
            "cloud": False,
        }

        if not subdomain["id"]:
            add_response = requests.post(
                url=base_url, headers=request_headers, json=record_payload, timeout=30
            )
            handle_errors(add_response.json)
            continue

        record_url = base_url + subdomain["id"]
        update_response = requests.put(
            url=record_url, json=record_payload, headers=request_headers, timeout=30
        )
        handle_errors(update_response)


update_subdomain_records()
