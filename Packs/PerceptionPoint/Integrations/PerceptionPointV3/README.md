[Enter a comprehensive, yet concise, description of what the integration does, what use cases it is designed for, etc.]
This integration was integrated and tested with version 1.0 of PerceptionPointV3

Some changes have been made that might affect your existing content. 
If you are upgrading from a previous of this integration, see [Breaking Changes](#breaking-changes-from-the-previous-version-of-this-integration-perceptionpointv3).

## Configure PerceptionPointV3 on Cortex XSOAR

1. Navigate to **Settings** > **Integrations** > **Servers & Services**.
2. Search for PerceptionPointV3.
3. Click **Add instance** to create and configure a new integration instance.

    | **Parameter** | **Description** | **Required** |
    | --- | --- | --- |
    | Your server URL |  | True |
    | Token to use Perception Point's API | The API Key to use for connection | True |
    | Fetch incidents |  | False |
    | Incidents Fetch Interval |  | False |
    | Incident type |  | False |
    | Trust any certificate (not secure) |  | False |
    | Use system proxy settings |  | False |

4. Click **Test** to validate the URLs, token, and connection.
## Commands
You can execute these commands from the Cortex XSOAR CLI, as part of an automation, or in a playbook.
After you successfully execute a command, a DBot message appears in the War Room with the command details.
### pp-add-blacklist
***
This commands adds a record to the blacklist.
A record can be:
1. email address or entire domains can be added (without @)
2. url - for example 
 


#### Base Command

`pp-add-blacklist`
#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| target_type | Enter the type of target(email,url,ip). | Required | 
| target_value | Enter the blacklist object value | Required | 
| created_by | Enter your name. | Required | 


#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| PP-Blacklist.Output | String | \[Enter a description of the data returned in this output.\] | 


#### Command Example
``` ```

#### Human Readable Output



### pp-release-email
***
This commands releases a mail that is in quarantine


#### Base Command

`pp-release-email`
#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| scan_id | Enter the scan id to release. | Required | 
| should_mark_as_clean | Set to True if you want to release a mail without marking the scan as clean. | Optional | 


#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| PP-ReleaseMail.Output | String | \[Enter a description of the data returned in this output.\] | 


#### Command Example
``` ```

#### Human Readable Output



### pp-add-whitelist
***
This commands adds a record to the whitelist


#### Base Command

`pp-add-whitelist`
#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| target_type | Enter the type of target(email,url,ip). | Required | 
| target_value | Enter the whitelist object value | Required | 
| created_by | Enter your name. | Required | 


#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| PP-Whitelist.Output | String | \[Enter a description of the data returned in this output.\] | 


#### Command Example
``` ```

#### Human Readable Output



## Breaking changes from the previous version of this integration - PerceptionPointV3
%%pull incidents, add to the blacklist and whitelist, request investigation%%
The following sections list the changes in this version.

### Commands
#### The following commands were removed in this version:
* *commandName* - this command was replaced by XXX.
* *commandName* - this command was replaced by XXX.

### Arguments
#### The following arguments were removed in this version:

In the *commandName* command:
* *argumentName* - this argument was replaced by XXX.
* *argumentName* - this argument was replaced by XXX.

#### The behavior of the following arguments was changed:

In the *commandName* command:
* *argumentName* - is now required.
* *argumentName* - supports now comma separated values.

### Outputs
#### The following outputs were removed in this version:

In the *commandName* command:
* *outputPath* - this output was replaced by XXX.
* *outputPath* - this output was replaced by XXX.

In the *commandName* command:
* *outputPath* - this output was replaced by XXX.
* *outputPath* - this output was replaced by XXX.

## Additional Considerations for this version
%%None%%
* Insert any API changes, any behavioral changes, limitations, or restrictions that would be new to this version.
