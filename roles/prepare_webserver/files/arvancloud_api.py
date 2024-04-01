import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--wpdomain", type=str)
parser.add_argument("--regdomain", type=str)
parser.add_argument("--rootdomain", type=str)
parser.add_argument("--apikey", type=str)
parser.add_argument("--ansiblehost", type=str)
args = parser.parse_args()

wp_domain = args.wpdomain
reg_domain = args.regdomain
root_domain = args.rootdomain
api_key = args.apikey
ansible_host = args.ansiblehost

base_url = f"https://napi.arvancloud.ir/cdn/4.0/domains/{root_domain}/dns-records/"
request_headers = {
    "Authorization": f"apikey {api_key}",
    "Accept": "application/json",
}


def error_handling(response):
    if response.status_code >= 400:
        print("ERROR CODE:", response.status_code)
        print("ERROR MESSAGE:", response.text)
        exit()


def update_subdomain_records():
    subdomain_list = [{"name": wp_domain, "id": ""}, {"name": reg_domain, "id": ""}]

    get_response = requests.get(base_url, headers=request_headers, timeout=30)
    error_handling(get_response)

    response_json = get_response.json()

    record_dict = {}
    for record in response_json["data"]:
        record_name = record["name"]
        record_id = record["id"]
        record_dict[record_name] = record_id

    for subdomain in subdomain_list:
        subdomain["id"] = record_dict.get(subdomain["name"])

        record_url = base_url + subdomain["id"]
        record_payload = {
            "value": [{"ip": ansible_host}],
            "type": "a",
            "name": subdomain["name"],
            "ttl": 120,
            "cloud": False,
        }
        if not subdomain["id"]:
            post_response = requests.post(
                url=base_url, headers=request_headers, json=record_payload, timeout=30
            )
            error_handling(post_response)
            break
        put_response = requests.put(
            url=record_url, json=record_payload, headers=request_headers, timeout=30
        )
        error_handling(put_response)


update_subdomain_records()
