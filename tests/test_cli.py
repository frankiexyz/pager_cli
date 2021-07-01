#!/usr/bin/env python

"""Tests for `pager_cli` package."""

from pager_cli import cli


URL = "https://api.pagerduty.com/incidents"


def test_fetch_open_incidents_empty(requests_mock):
    user_id = 'random-id'
    api_key = 'random-key'
    url = (
        f"{URL}?total=false&time_zone=UTC&statuses%5B%5D=triggered&statuses"
        f"%5B%5D=acknowledged&user_ids%5B%5D={user_id}"
    )
    requests_mock.get(
        url,
        headers={"authorization": f"Token token={api_key}"},
        json={'incidents': [], 'limit': 25, 'offset': 0, 'total': None, 'more': False},
    )
    resp = cli.fetch_open_incidents(user_id, api_key)
    assert resp == []


def test_fetch_open_incidents_list(requests_mock):
    output = {
        'incidents': [
            {
                'incident_number': 365456,
                'title': 'Customer Call',
                'description': 'Customer Call',
                'created_at': '2021-06-01T08:47:04Z',
                'status': 'acknowledged',
                'incident_key': None,
                'id': 'P9TETKK',
                'html_url': 'https://www.pagerduty.com/incidents/P9TETKK',
            }
        ]
    }
    user_id = 'random-id'
    api_key = 'random-key'
    url = (
        f"{URL}?total=false&time_zone=UTC&statuses%5B%5D=triggered&statuses"
        f"%5B%5D=acknowledged&user_ids%5B%5D={user_id}"
    )
    requests_mock.get(
        url,
        headers={"authorization": f"Token token={api_key}"},
        json=output,
    )
    resp = cli.fetch_open_incidents(user_id, api_key)
    assert resp == [
        {
            'id': 'P9TETKK',
            'incident_number': 365456,
            'title': 'Customer Call',
            'status': 'acknowledged',
            'url': 'https://www.pagerduty.com/incidents/P9TETKK',
        }
    ]


def test_fetch_open_incidents_resolve(requests_mock):
    output = '{"incidents": [{"incident_number": 365456, "title": "Customer Call", "description": "Customer Call", "created_at": "2021-06-01T08:47:04Z", "status": "acknowledged", "incident_key": null, "id": "P9TETKK", "html_url": "https://www.pagerduty.com/incidents/P9TETKK"}]}'
    user_id = 'random-id'
    api_key = 'random-key'

    headers = {
        "accept": "application/vnd.pagerduty+json;version=2",
        "content-type": "application/json",
        "from": "",
        "authorization": f"Token token={api_key}",
    }

    #    requests_mock.register_uri('PUT', URL, text=output)
    requests_mock.put(URL, headers=headers, text=output)
    resp = cli.change_incident(user_id, api_key, "ack")
    assert resp == True


def test_fetch_open_incidents_ack(requests_mock):
    output = '{"incidents": [{"incident_number": 365456, "title": "Customer Call", "description": "Customer Call", "created_at": "2021-06-01T08:47:04Z", "status": "resolved", "incident_key": null, "id": "P9TETKK", "html_url": "https://www.pagerduty.com/incidents/P9TETKK"}]}'
    user_id = 'random-id'
    api_key = 'random-key'

    headers = {
        "accept": "application/vnd.pagerduty+json;version=2",
        "content-type": "application/json",
        "from": "",
        "authorization": f"Token token={api_key}",
    }

    #    requests_mock.register_uri('PUT', URL, text=output)
    requests_mock.put(URL, headers=headers, text=output)
    resp = cli.change_incident(user_id, api_key, "resolve")
    assert resp == True
