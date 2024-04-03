from collections import defaultdict
import requests
import validators
import argparse


def is_args_valid(domain: str, subdomains: list[str], ip: str) -> bool:
    if not validators.ipv4(ip):
        print("ERROR MESSAGE: Ip's Format Is Not Valid")
        return False
    if not validators.domain(domain):
        print("ERROR MESSAGE: Domain's Format Is Not Valid")
        return False
    for subdomain in subdomains:
        if not subdomain.isalnum():
            print("ERROR MESSAGE: Subdomain's Format Is Not Valid")
            return False
    return True


def exit_on_errors(response):
    if not response.ok:
        print("ERROR CODE:", response.status_code)
        print("ERROR MESSAGE:", response.json()["message"])
        exit()


def update_subdomain_records(domain: str, subdomains: list[str], ip: str, api_key: str):
    if not is_args_valid(domain, subdomains, ip):
        return 0

    base_url = f"https://napi.arvancloud.ir/cdn/4.0/domains/{domain}/dns-records/"
    request_headers = {
        "Authorization": f"apikey {api_key}",
        "Accept": "application/json",
    }

    list_response = requests.get(base_url, headers=request_headers, timeout=30)

    exit_on_errors(list_response)

    records = list_response.json()
    records_by_name = defaultdict(str)

    for record in records["data"]:
        records_by_name[record["name"]] = record["id"]

    for subdomain in subdomains:
        record_payload = {
            "value": [{"ip": ip}],
            "type": "a",
            "name": subdomain,
            "ttl": 120,
            "cloud": False,
        }

        record_id = records_by_name[subdomain]

        if not record_id:
            add_response = requests.post(
                url=base_url, headers=request_headers, json=record_payload, timeout=30
            )
            exit_on_errors(add_response)
            continue

        record_url = base_url + record_id
        update_response = requests.put(
            url=record_url, json=record_payload, headers=request_headers, timeout=30
        )
        exit_on_errors(update_response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--subdomain", type=str, nargs="+", required=True)
    parser.add_argument("--domain", type=str, required=True)
    parser.add_argument("--apikey", type=str, required=True)
    parser.add_argument("--ip", type=str, required=True)

    args = parser.parse_args()
    update_subdomain_records(args.domain, args.subdomain, args.ip, args.apikey)
