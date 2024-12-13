# Readme file for WebHooks

## What is WebHook?

There are various events generated in RainMaker, which are the result of the user actions
and messages which are transferred between the nodes and RainMaker. Some
examples of these events are - user associates a node or node status changes to online.

These events can be used by external third party systems, for further processing, e.g. Google
Voice Action or SalesForce, etc.

To facilitate the processing of these events by third party systems, RainMaker provides
support for WebHooks. Developers can extend the code for WebHooks and perform 
further actions, e.g. calling a REST API of some external system or maybe simply writing these
events into an AWS Simple Storage Service (S3) bucket.

You can develop your own WebHooks and deploy them in your AWS account, where Espressif’s
RainMaker is also deployed.

## How does a WebHook work?

A WebHook consists of an AWS Lambda function along with configuration files, which needs to be 
deployed in the AWS account.

Whenever a new event is generated, RainMaker publishes this event onto one of the pre-defined
AWS Simple Notification Service (SNS) topics. Every event type has a separate SNS topic
associated with it.

The lambda function, which is part of the WebHook, listens to the required SNS topics. When the
event occurs, the lambda function retrieves the payload for the event. It does the required
processing on the event payload and executes the required action, e.g. sending the event payload
to an external system or to storing it into S3, etc.

Whenever RainMaker generates any event (e.g. node is online), it needs to decide whether to process this event or not. 
Based on the configurations, RainMaker either sends the event to the SNS topic or may filter it out. 
There are three types of filter configurations - System level filter, User level filter and Node level filter. 
A generated event is eligible for some or all these filters.  
These are evaluated for filtering in the order: System > User > Node  
i.e. User level filter is checked only if System level filter is enabled.

The processing of these events can be enabled or disabled with the help of APIs.  

![RainMaker Webhook Architecture](pictures/RainmakerWebhookArch.png "RainMaker Webhook Architecture")  
*The above image describes the architecture of RainMaker's Webhook Framework.*

Here is the reference to the RainMaker WebHooks API - Refer [RainMaker API Documentation][swagger]

## Which events are currently supported by RainMaker?

### RainMaker currently supports the below events -

| Sr. No. |      RainMaker Event Name      |                Event Type                |                SNS Topic Name                 | Can be disabled for System | Can be disabled for User and Node |
| :-----: | :----------------------------: | :--------------------------------------: | :-------------------------------------------: | :------------------------: | :-------------------------------: |
|    1    |          Node Online           |       rmaker.event.node_connected        |       esp_rainmaker_sns_node_connected        |            Yes             |                Yes                |
|    2    |          Node Offline          |      rmaker.event.node_disconnected      |      esp_rainmaker_sns_node_disconnected      |            Yes             |                Yes                |
|    3    |     Add User Node sharing      |    rmaker.event.user_node_sharing_add    |    esp_rainmaker_sns_user_node_sharing_add    |            Yes             |                No                 |
|    4    |   Node Added to User Account   |       rmaker.event.user_node_added       |       esp_rainmaker_sns_user_node_added       |            Yes             |                No                 |
|    5    | Node Removed from User Account |      rmaker.event.user_node_removed      |      esp_rainmaker_sns_user_node_removed      |            Yes             |                No                 |
|    6    |    Node Parameters changed     |     rmaker.event.node_params_changed     |   esp_rainmaker_sns_node_parameter_modified   |            Yes             |                No                 |
|    7    |           Node Alert           |            rmaker.event.alert            |         esp_rainmaker_sns_node_alert          |            Yes             |                No                 |
|    8    |   Node Automation Triggered    |   rmaker.event.node_automation_trigger   |    esp_rainmaker_sns_automation_triggered     |            Yes             |                No                 |
|    9    |       Node group shared        | rmaker.event.user_node_group_sharing_add | esp_rainmaker_sns_user_node_group_sharing_add |            Yes             |                No                 |
|   10    |        Node group added        |    rmaker.event.user_node_group_added    |    esp_rainmaker_sns_user_node_group_added    |            Yes             |                No                 |
|   11    |       Node group removed       |   rmaker.event.user_node_group_removed   |   esp_rainmaker_sns_user_node_group_removed   |            Yes             |                No                 |
|   12    |   Node Registered to Account   |       rmaker.event.node_registered       |      esp_rainmaker_sns_node_registration      |             No             |                No                 |
|   13    |        Admin User Added        |      rmaker.event.admin_user_added       |      esp_rainmaker_sns_admin_user_added       |             No             |                No                 |
|   14    |         New Tags Added         |       rmaker.event.new_tags_added        |       esp_rainmaker_sns_new_tags_added        |             No             |                No                 |
|   15    |     Existing Tags Attached     |   rmaker.event.existing_tags_attached    |   esp_rainmaker_sns_existing_tags_attached    |             No             |                No                 |
|   16    |      Node Config changed       |     rmaker.event.node_config_changed     |    esp_rainmaker_sns_node_config_modified     |            Yes             |                Yes                |
|   17    |    User Node OTA triggered     |        rmaker.event.user_node_ota        |        esp_rainmaker_sns_user_node_ota        |            Yes             |                Yes                |
|   18    |        TimeSeries Data         |        rmaker.event.node_ts_data         |        esp_rainmaker_sns_node_ts_data         |            Yes             |                No                 |

## About the sample WebHook Project

This project contains a sample WebHook - “HelloWorld Template”, which can be extended further
to develop a new WebHook. The code for this template is developed using Python language, but
you can select any other language (e.g. Java, Golang, etc.) which is supported by AWS Lambda. Read more [here][AWSLambdaDoc].

This WebHook listens to pre-configured SNS topics and prints the payload of the event into AWS CloudWatch Logs.

### Technologies which are required for developing a new WebHook

WebHooks can be developed using any programming language supported by AWS
Lambda - Python, Java, Golang, etc. Read more [here][AWSLambdaDoc].
Some basic experience with developing Lambda functions and knowledge about AWS CLI
will be helpful, for developing a WebHook.
The deployment of WebHooks is done using AWS Serverless Application Module (SAM)
and explained in the later sections of this document.
Reference Links - https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html


### Pre-requisites for Starting the WebHook deployment

You will need to install and configure the below frameworks on your host before you can start with the development of the WebHook.

- AWS CLI (Link - https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- After the AWS CLI is installed, Execute the below AWS CLI commands to configure the AWS credentials on your computer.

        $ aws configure

You will be prompted to enter AWS Access Key ID and AWS Secret Key ID.
After that, you will be prompted to enter your default AWS region (e.g. us-east-1)

Here is the link to configure the AWS credentials on your host using AWS access keys. (Link - https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)

- AWS SAM tool 
The steps to install and configure the AWS SAM tool are provided in the below Link - 
https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

- Python3.7 (Link- https://www.python.org/downloads/)
> You can use any supported python version. Accordingly, you just need to update the runtime field in template.yaml  
> To check the supported versions use `$ sam build --help` 


- Virtualenv (Link - https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#installing-virtualenv)

- You will need to have an S3 bucket, which will be used for packaging and uploading the build.
  You can use an existing S3 bucket or create a new unique bucket using the below Command.
    
        $ aws s3 mb s3://<S3-BUCKET>

- RainMaker is deployed into your AWS account and you have the credentials for the super admin user of your RainMaker deployment.

## Developing a new WebHook

After all the pre-requisites are satisfied, you will need to clone the Git repository for the sample
WebHook template.

**Step 1** Clone the sample WebHook repository

$ git clone https://github.com/espressif/esp-rainmaker-webhooks.git

**Step 2** Extend the code of the Lambda function

The code for the WebHooks Lambda function is in the hello_rainmaker/app.py file
This code currently prints the payload of the event generated in RainMaker in CloudWatch logs, but you can extend it further, as required.

**Step 3** Modify the SAM template file if required

The SAM Template is a yml file - WebHooksTemplatePython/template.yml

## Deploying the WebHooks

You can use either use a python virtual environment or your host's python environment.

For creating a Python Virtual environment,

**Step 1** Create a virtual environment venv.

This will create a local directory for creating a virtual environment which will contain all python, pip binaries, etc. Also, additional libraries can be installed in the virtual environment folder (after you activate this environment as in step 2).

    $ python3 -m virtualenv env -p <path to your python3.7 binary>


**Step 2** Activate the virtual environment using "source <virtual env folder created in step 1>/bin/activate”
e.g

    $  source env/bin/activate

**Step 3** Install required packages using the below commands

    $ cd WebHooksTemplatePython
    $ pip install -r hello_rainmaker/requirements.txt

**Step 4** Install additional libraries if required in your project. 
Update requirements.txt for additionally added libraries using pip freeze.

    $ pip freeze > hello_rainmaker/requirements.txt


**Step 5** Build the code

    $ sam build

**Step 6** Package and Deploy using the following commands. (Use previously used S3-BUCKET)

    $ sam package --template-file template.yaml --output-template-file template_package.yml --s3-bucket <S3-BUCKET>

> **Note** - Please use the below command for deploying your WebHook stack using `sam deploy` . Please note that, you will need to pass the values for parameters *--capabilities* and *--parameter-overrides StageName* as mentioned below. The value for the capabilities parameter to be used in this example is *CAPABILITY_NAMED_IAM* and for Stage name, you can use the values like dev or prod, etc. 

    $ sam deploy --template-file template_package.yml --stack-name HelloRainmaker --capabilities CAPABILITY_NAMED_IAM --parameter-overrides 'StageName=<STAGE-NAME>'

## Testing the WebHook event
After you login to RainMaker using your credentials, you will need to call the below APIs for configuring the WebHooks. 
You can make use of any REST client like Postman or you can use curl commands. 
You will first need to login to RainMaker from the REST client using your super admin credentials.
You will need to use the access token received in the Login response as the **Authorization** header to subsequent API calls.

> Please note all the following steps(1-5) are required. Currently, the supported API version is v1.

### 1. Login with User

API endpoint - < Base API URL > /v1/login

HTTP Method - POST

Request Body 

```
{
  "user_name": "<user_id>",
  "password": "<password>"
}
```

\*Login using superadmin credentials so that SYSTEM level filters may be enabled or disabled.  
Note - You will get **accesstoken** in the response to the above API Request. Use that in the header of the following API calls as `Authorization=<accesstoken>` 
### 2. Create the WebHooks Configuration

### Description -

API endpoint - < Base API URL >/{version}/admin/webhook_integration

HTTP Method - POST

Request Body
``` 
{
    "service_name": “<unique_name_of_the_webhook>”,
    "endpoint_name": “<end_point_name>”,
    “integration_enabled” : true
}
```

Note - This API needs to be called by the super admin user. This API creates the new WebHook into RainMaker. 

### 3. Adding System Filters

API endpoint - < Base API URL >/{version}/admin/event_filter

HTTP Method - POST

The following is a sample request payload for configuring a System Level Filter:

```
{
    "event_type" : "rmaker.event.node_connected",
    "entity_id" : "system.rmaker.event.node_connected",
    "entity_type" : "System",
    "enabled": true,
    “enabled_for_integrations” : [“<unique_name_of_the_webhook>”, “helloworldintegration”]
}
```

\*At least one webhook_integration must be added under `enabled_for_integrations` for webhook to be called.  
Note - This API needs to be called by the super admin user. This API enables the processing of the specific event in RainMaker, e.g. in this case, the Node connected event is enabled.  

### 4. Adding User-specific Filters

API endpoints:  
< Base API URL >/{version}/user/event_filter  
 **OR**  
< Base API URL >/{version}/admin/event_filter

HTTP Method - POST

Request Body

``` 
{
    "event_type" : "rmaker.event.node_connected",
    "entity_id" : "<user_id>",
    "entity_type" : "USER",
    "enabled": true,
    "enabled_for_integrations" : [“<unique_name_of_the_webhook>”, “helloworldintegration"]
}
``` 
\*At least one webhook_integration must be added under `enabled_for_integrations` for webhook to be called.  
Note - This API needs to be called by the end user or the super admin user. This API enables the processing of the event specific to the calling user. In this case, this API enables the node connected event for the user_id provided in the request body.

### 5. Adding Node-specific Filters

API endpoints:  
< Base API URL >/{version}/user/event_filter  
 **OR**  
< Base API URL >/{version}/admin/event_filter

HTTP Method - POST

Request Body

``` 
{
    "event_type" : "rmaker.event.node_connected",
    "entity_id" : "<node_id>",
    "entity_type" : "NODE",
    "enabled": true,
    "enabled_for_integrations" : [“<unique_name_of_the_webhook”, “helloworldintegration”]
}
``` 
\*At least one webhook_integration must be added under `enabled_for_integrations` for webhook to be called.  
Note - This API needs to be called by the end user or the super admin user. This API enables the processing of the event specific to the node. In this case, this API enables the node connected event for the node_id provided in the request body.

\*The webhook_integration API is an admin API  
\*The event_filter API is a user and admin API  

### Swagger File Path
[RainMaker Swagger API Documentation][swagger] 

### Testing the Node Online event

Step 1 - Connect the node to an MQTT broker using the ESP32 device or using a tool like MQTT.Fx

Step 2 - After the device is connected, check the logs in CloudWatch Logs for **HelloRainmakerFunction** lambda. The details about this event should be printed in the logs. e.g
```
{
    "EventVersion":"v1",
    "Id":"RainMakerEventId",
    "EventType":"rmaker.event.node_connected",
    "Timestamp":"<timestamp>",
    "Description":"<user_id>(User)'s (Node)thing3 disconnection status is false",
    "EventData":{
        "UserId":"<user_id>",
        "NodeId":"<node_id>",
        "Connected":true
    }
}
```

Step 3 - Disconnect the device

Step 4 - Disable the SYSTEM event filter for this node, using the REST API provided above.

Step 5 - Connect the node to the MQTT broker using an ESP32 device or using a tool like MQTT.Fx

Step 6 - After the device is connected, check the logs in CloudWatch Logs. There should not be
any log for this device.
> (To Watch logs go to AWS Services \> CloudWatch \> CloudWatch Logs \> Log groups \> /aws/lambda/HelloRainmakerFunction)


### How to trigger other events? (Assuming their filters are enabled)

1. Node Online:  
   Connect the node to an MQTT Broker. This could mean connecting an ESP32 device to power, or connecting a node using an MQTT Client like MQTT.Fx

2. Node Offline:  
   Disconnect the node from the MQTT Broker. This could mean disconnecting an ESP32 device from power, or disconnecting a node from an MQTT Client like MQTT.Fx

3. Add User Node sharing:  
   Share a node with a user:
   1. `PUT` Method at `{{base_url}}/v1/user/nodes/sharing/requests`:  

        ```
         {
             "nodes": [
                 "node_id"
             ],
             "user_name": "secondary user_name"
         }
         ```
   2. **Login as the shared User** and call the `PUT` Method at `{{base_url}}/v1/user/nodes/sharing/requests`:  

        ```
         {
             "accept": true,
             "request_id": "request_id_returned_in_last_call"
         }
        ```

4. Node Added to User Account: 
   1. Add a node through User-Node mapping:  
    `PUT` Method at `{{base_url}}/v1/user/nodes/mapping`   

        ```
        {
            "node_id": "<node_id>",
            "secret_key": "<sample_secret_key>",
            "operation": "add"
        }
        ```  
       Node should send the following payload to `node/<node_id>/user/mapping`:  

        ```
        {
            "node_id": "<node_id>",
            "user_id": "<user_id>",
            "secret_key": "<same_secret_key>"
         }
        ```  
   2. Receive a node through Node Sharing

5. Node Removed from User: 
   1. Remove User-Node mapping:  
    `PUT` Method at `{{base_url}}/v1/user/nodes/mapping`:  
    
       ```
        {
            "node_id": "<node_id>",
            "operation": "remove"
        }
        ```
   2. Removed a node received from Sharing

6. Node Parameters changed:  
    Node should update it's parameters.  
    It can send a similar payload to `node/<node_id>/params/local`:  
    ```
    {
        "Lightbulb": {
            "brightness": 0
        }
    }
    ```

7. Node Alert:  
    Node can send an alert(any JSON body) to `node/<node_id>/alert`

8. Node Automation Triggered:
   1.  Setup Node Automation Trigger:  
       `POST` Method at `{{base_url}}/v1/user/node_automation`: Refer [RainMaker API Documentation][swagger] 
    1. Trigger the Node Automation Condition:  
        For example, if trigger event is *Brightness equals 100*, then set Node Brightness to 100.

9.  Node group shared:  
    Share a node group with a secondary user:  
    1. `PUT` Method at `{{base_url}}/v1/user/node_group/sharing`:  

        ```  
        {
          "groups": [
              "group_id1"
          ],
          "user_name": "secondary user_name"
        }
        ```
    2. **Login to Secondary User**, and call `PUT` Method at `{{base_url}}/v1/user/node_group/sharing/requests`:  

        ```
        {
            "accept": true,  
            "request_id": "request_id_returned_in_last_call"
        }
        ```
10. Node group added:  
    When a Node Group is shared with another User, the receiving User will get a `rmaker.event.user_node_group_added` event.
11. Node group removed:  
    Delete a Node Group sharing.  
    `DELETE` Method at `{{base_url}}/v1/user/node_group/sharing?groups=<node_group_id>&user_name=<user_name>`:  Refer [RainMaker API Documentation][swagger] 
12. Node Registered to Account:  
    Use [Rainmaker Admin CLI][RainMakerAdminCLI] to generate and register nodes
13. Admin User Added:  
    Use [Rainmaker Admin CLI][RainMakerAdminCLI] to generate and register nodes
14. New Tags Added:  
    `PUT` Method at `{{base_url}}/v1/user/nodes?node_id=<node_id>` to add a new tag that is not attached before. Refer [RainMaker API Documentation][swagger]  
15. Existing Tags Attached:  
    `PUT` Method at `{{base_url}}/v1/user/nodes?node_id=<node_id>` to add a tag which was already attached elsewhere. Refer [RainMaker API Documentation][swagger]  
16. Node Config changed:  
    Publish a node's config to the MQTT topic `node/+/config` using an MQTT client. Refer [Sample config payload][SampleConfigPayload]    

[swagger]: http://swaggerapis.rainmaker.espressif.com
[AWSLambdaDoc]: https://aws.amazon.com/lambda/faqs/#:~:text=Q%3A%20What%20languages%20does%20AWS,our%20documentation%20on%20using%20Node
[RainMakerAdminCLI]: https://github.com/espressif/esp-rainmaker-admin-cli
[SampleConfigPayload]: https://rainmaker.espressif.com/docs/node-cloud-comm.html#appendix-sample-node-configuration
