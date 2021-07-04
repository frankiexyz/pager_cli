"""Console script for pager_cli."""
import sys
import webbrowser
from pathlib import Path
from typing import Dict

import click
import requests
import strictyaml
from strictyaml import Map, Str, YAMLValidationError, load
from tabulate import tabulate
from yaspin import yaspin


URL = "https://api.pagerduty.com/incidents"


@yaspin(text="Loading...")
def fetch_open_incidents(userid: str, apikey: str) -> list[Dict[str, str]]:
    url = (
        f"{URL}?total=false&time_zone=UTC&statuses%5B%5D"
        f"=triggered&statuses%5B%5D=acknowledged&user_ids%5B%5D={userid}"
    )
    pageroutput = requests.get(
        url, headers={"authorization": f"Token token={apikey}"}
    ).json()
    output: list[Dict[str, str]] = []
    if not pageroutput.get("incidents", False):
        print("\n\U0001F9BE No active incident")
        return output
    for i in pageroutput["incidents"]:
        output.append(
            {
                "id": i["id"],
                "incident_number": i["incident_number"],
                "title": i["title"],
                "status": i["status"],
                "url": i["html_url"],
            }
        )
    return output


def fetch_config(config_path: str) -> strictyaml.representation.YAML:
    try:
        schema = Map({"userid": Str(), "apikey": Str()})
        config_raw = open(config_path).read()
        config = load(config_raw, schema)
    except YAMLValidationError as e:
        print(f"Configration file error: {repr(e)}")
        return None
    except FileNotFoundError as e:
        print(f"File not found: {repr(e)}")
        return None
    return config


@yaspin(text="Loading...")
def change_incident(incident: str, apikey: str, action: str) -> bool:
    if action == "ack":
        status = "acknowledged"
    else:
        status = "resolved"
    querystring = {
        "incidents": [
            {
                "id": incident,
                "type": "incident_reference",
                "status": status,
            },
        ]
    }

    headers = {
        "accept": "application/vnd.pagerduty+json;version=2",
        "content-type": "application/json",
        "from": "",
        "authorization": f"Token token={apikey}",
    }

    response = requests.put(URL, headers=headers, json=querystring).json()
    if action == "resolve" and response["incidents"][0]["status"] == "resolved":
        return True
    if action == "ack" and response["incidents"][0]["status"] == "acknowledged":
        return True
    return False


def execute(action: str, conf_path: str):
    config = fetch_config(conf_path)
    if config is None:
        print("Unable to load config")
        sys.exit(1)
    userid = config.get("userid")
    apikey = config.get("apikey")
    if action == "list":
        print(tabulate(fetch_open_incidents(userid, apikey)))
    elif action == "resolve":
        list_incidents = fetch_open_incidents(userid, apikey)
        print(tabulate(list_incidents))
        for i in list_incidents:
            if i['status'] != 'acknowledged':
                continue
            print(f"\U0001F3C3 trying to resolve {i['id']}...")
            if change_incident(i["id"], apikey, "resolve"):
                print(f"\U0001F44C resolved {i['id']}...")
            else:
                print(f"\U00011F44 fail to resolve {i['id']}...")
    elif action == "ack":
        list_incidents = fetch_open_incidents(userid, apikey)
        print(tabulate(list_incidents))
        for i in list_incidents:
            if i['status'] != 'triggered':
                continue
            print(f"\U0001F3C3 trying to ack {i['id']}...")
            if change_incident(i["id"], apikey, "ack"):
                print(f"\U0001F44C ack {i['id']}...")
                print(f"\U0001FA84 open incident {i['id']}")
                webbrowser.open(f"{i['url']}")
            else:
                print(f"\U00011F44E fail to ack {i['id']}...")


@click.command()
@click.option("--action", default="ack", help="Action list/ack/resolve")
@click.option(
    "--config",
    default=f"{Path.home()}/.pager_cli",
    help="config file default:~/.pager_cli",
)
def main(action, config):
    """Console script for pager_cli."""
    execute(action, config)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
