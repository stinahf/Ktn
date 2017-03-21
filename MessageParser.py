import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history
        }

    def parse(self, payload):
        payload = json.loads(payload)

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            pass

    def parse_error(self, payload):
        error_parsed="<"+str(payload['timestamp'])+"> ERROR: "+payload['content']
        return error_parsed
    
    def parse_info(self, payload):
        info_parsed="<"+str(payload['timestamp'])+"> INFO: "+payload['content']
        return info_parsed

    def parse_message(self, payload)::
        message_parsed="<"+str(payload['timestamp'])+"> MESSAGE: "+payload['content']+": "payload['content']
        return message_parsed

    def parse_history(self, payload):
        history_parsed = "History: "

        for element in payload['content']:
            history_parsed += "<"+str(json.loads(element)['timestamp'])+"> "+json.loads(element)['sender']+": "json.loads(elements)['content'] +'\n'

        return history_parsed
     
