import json

# import requests


def lambda_handler(event, context):
    ''' 
        This lambda gets triggerred via SNS when the Rainmaker event is published on subscribed topic.
        This lambdap prints Rainmaker Event Received in SNS Message. 
        You can use this Rainmaker Event Information in your code.
        
        Rainmaker Event structure looks like following, e.g (Node Online Event)
        {
            "EventVersion":"v1",
            "Id":"RainmakeEventId",
            "EventType":"rmaker.event.node_connected",
            "Timestamp":"01-29-2021 04:32:27",
            "Description":"5c75d6be-4a95-4065-951b-9519664f6498(User)'s (Node)thing3 disconnection status is false",
            "EventData":{
                "UserId":"5c75d6be-4a95-4065-951b-9519664f6498",
                "NodeId":"thing3",
                "Connected":true
            }
        }
    '''
    print(json.loads( event['Records'][0]["Sns"]["Message"]))

