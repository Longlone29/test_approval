import requests
import json
import os

receive_id = os.getenv("RECEIVE_ID")
authorization = os.getenv("AUTHORIZATION")
run_id = os.getenv("RUN_ID")
title = os.getenv("TITLE")

if not receive_id or not authorization or not run_id or not title:
  raise ValueError("RECEIVE_ID, AUTHORIZATION, RUN_ID, TITLE is not set")

# 替换为你的自定义机器人的 webhook 地址。
url = "https://open.larksuite.com/open-apis/im/v1/messages?receive_id_type=chat_id"
# 将消息卡片内容粘贴至此处。
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
card_json = card_json.replace("${{ github.run_id }}", run_id)
card_json = card_json.replace("${{ title }}", title)

body = json.dumps({"msg_type": "interactive", "content": card_json, "receive_id": receive_id})
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {authorization}"}
res = requests.post(url=url, data=body, headers=headers, timeout=10)
print(res.text)
