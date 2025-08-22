import requests
import json
import os

receive_id = os.getenv("RECEIVE_ID")
run_id = os.getenv("RUN_ID")
title = os.getenv("TITLE")
app_id = os.getenv("APP_ID")
app_secret = os.getenv("APP_SECRET")

if not receive_id or not run_id or not title or not app_id or not app_secret:
  raise ValueError("RECEIVE_ID, RUN_ID, TITLE, APP_ID, APP_SECRET is not set")

# 获取 access_token
def get_access_token():
  url = f"https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
  body = json.dumps({"app_id": app_id, "app_secret": app_secret})
  res = requests.post(url=url, data=body, timeout=10)
  if res.status_code != 200:
    raise ValueError(f"get access_token failed, status_code: {res.status_code}, response: {res.text}")

  return res.json()["tenant_access_token"]

access_token = get_access_token()

url = "https://open.larksuite.com/open-apis/im/v1/messages?receive_id_type=chat_id"
card_json = '''
{
  "config": {
    "wide_screen_mode": true,
    "update_multi": true
  },
  "elements": [
    {
      "tag": "action",
      "actions": [
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "通过"
          },
          "type": "primary",
          "value": {
            "action": "approve",
            "title": "${{ title }}",
            "run_id": "${{ github.run_id }}"
          }
        },
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "拒绝"
          },
          "type": "danger",
          "value": {
            "value": {
              "action": "reject",
              "title": "${{ title }}",
              "run_id": "${{ github.run_id }}"
            }
          }
        }
      ]
    }
  ],
  "header": {
    "template": "blue",
    "title": {
      "content": "${{ title }}",
      "tag": "plain_text"
    }
  }
}
'''
card_json = card_json.replace("${{ title }}", title)
card_json = card_json.replace("${{ github.run_id }}", run_id)

body = json.dumps({"msg_type": "interactive", "content": card_json, "receive_id": receive_id})
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
res = requests.post(url=url, data=body, headers=headers, timeout=10)
print(res.text)
