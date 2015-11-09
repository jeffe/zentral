import json
import requests
from .base import BaseAction
from zentral.conf import contact_groups

API_ENDPOINT = "https://api.twilio.com/2010-04-01/"


class Action(BaseAction):
    def __init__(self, config_d):
        super(Action, self).__init__(config_d)
        self.auth = (config_d['account_sid'], config_d['auth_token'])
        self.url = "{api_endpoint}Accounts/{account_sid}/Messages".format(api_endpoint=API_ENDPOINT,
                                                                          account_sid=config_d['account_sid'])

    def trigger(self, event, action_config_d):
        action_config_d = action_config_d or {}
        args = {'Body': '\n\n'.join([event.get_notification_subject(), event.get_notification_body()])}
        for group_name in action_config_d['groups']:
            for contact_d in contact_groups[group_name]:
                cell_number = contact_d.get('cell', None)
                if cell_number:
                    args['To'] =  cell_number
                    requests.post(self.url, data=args, auth=self.auth)
