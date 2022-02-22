"""Base Integration for Cortex XSOAR (aka Demisto)

This is an empty Integration with some basic structure according
to the code conventions.

MAKE SURE YOU REVIEW/REPLACE ALL THE COMMENTS MARKED AS "TODO"

Developer Documentation: https://xsoar.pan.dev/docs/welcome
Code Conventions: https://xsoar.pan.dev/docs/integrations/code-conventions
Linting: https://xsoar.pan.dev/docs/integrations/linting

This is an empty structure file. Check an example at;
https://github.com/demisto/content/blob/master/Packs/HelloWorld/Integrations/HelloWorld/HelloWorld.py

"""
import ast
import demistomock as demisto
from CommonServerPython import *  # noqa # pylint: disable=unused-wildcard-import
from CommonServerUserPython import *  # noqa
from datetime import datetime
from dateutil import parser

import requests
import traceback
from typing import Dict, Any

# Disable insecure warnings
requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member


''' CONSTANTS '''

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'  # ISO8601 format with UTC, default in XSOAR
PP_TOKEN = demisto.params().get('credentials',None)
HEADER = {'Authorization': f'Token {PP_TOKEN}'}
API_MAX_LOOPS = demisto.params().get('api_loops',1)
''' CLIENT CLASS '''
class Client(BaseClient):
    """Client class to interact with the service API

    This Client implements API calls, and does not contain any XSOAR logic.
    Should only do requests and return data.
    It inherits from BaseClient defined in CommonServer Python.
    Most calls use _http_request() that handles proxy, SSL verification, etc.
    For this  implementation, no special attributes defined
    """
    
    # TODO: REMOVE the following dummy function:
    def baseintegration_dummy(self, dummy: str) -> Dict[str, str]:
        """Returns a simple python dict with the information provided
        in the input (dummy).

        :type dummy: ``str``
        :param dummy: string to add in the dummy dict that is returned

        :return: dict as {"dummy": dummy}
        :rtype: ``str``
        """

        return {"dummy": dummy}
    # TODO: ADD HERE THE FUNCTIONS TO INTERACT WITH YOUR PRODUCT API


''' HELPER FUNCTIONS '''

# TODO: ADD HERE ANY HELPER FUNCTION YOU MIGHT NEED (if any)

''' COMMAND FUNCTIONS '''


def test_module(client: Client) -> str:
    """Tests API connectivity and authentication'

    Returning 'ok' indicates that the integration works like it is supposed to.
    Connection to the service is successful.
    Raises exceptions if something goes wrong.

    :type client: ``Client``
    :param Client: client to use

    :return: 'ok' if test passed, anything else will fail the test.
    :rtype: ``str``
    """

    message: str = ''
    try:
        # TODO: ADD HERE some code to test connectivity and authentication to your service.
        # This  should validate all the inputs given in the integration configuration panel,
        # either manually or by using an API that uses them.
        message = 'ok'
        demisto.info("Line 91")
        demisto.info(HEADER)
        base_url = urljoin(demisto.params()['url'], 'api/v1')
        demisto.info(urljoin(base_url,'/scans/list'))
        res= client._http_request(
        method='GET',
        url_suffix='/scans/list',
        headers=HEADER,
        )
        if res:
            message="ok"
        demisto.info("Get Response")
        demisto.info(res)


    except requests.exceptions.HTTPEror as err:
        if 400 <= res.status_code < 500:
            return_error('Invalid token')
        else:
            return_error(err)
    except Exception as err:
        return_error(err)        
    except DemistoException as e:
        if 'Forbidden' in str(e) or 'Authorization' in str(e):  # TODO: make sure you capture authentication errors
            message = 'Authorization Error: make sure API Key is correctly set'
        else:
            raise e
    return message


# TODO: REMOVE the following dummy command function
def AddBlackWhitelist(client: Client, args: Dict[str, Any],ListType)-> CommandResults:
    DicForParams={"email":"address","url":"prefix","ip":"ip"}
    Type = args.get('target_type', None)
    if not Type:
        raise ValueError('target_type not specified')
    Value = args.get('target_value', None)
    if not Value:
        raise ValueError('Value not specified')
    Name = args.get('created_by', None)
    if not Name:
        raise ValueError('Name not specified')
    DicForParams[Type.lower()]
    try:
        demisto.info("Before response")
        res= client._http_request(
        method='POST',
        url_suffix=f'/{ListType}/{Type}/',
        json_data={"created_by":Name,DicForParams[Type.lower()]:Value},
        headers=HEADER,
        )
        demisto.info("After response")
        demisto.info(res)
        if ListType=="blacklist":
            return CommandResults(
            outputs_prefix='PP-Blacklist',
            outputs_key_field='id',
            outputs=res)
        return CommandResults(
            outputs_prefix='PP-Whitelist',
            outputs_key_field='id',
            outputs=res)    
    except DemistoException as e:
        demisto.info(e)    

def ReleaseMail(client: Client, args: Dict[str, Any])-> CommandResults:
    mark_clean = demisto.params().get('should_mark_as_clean', True)
    demisto.info("Mark Clean")
    demisto.info(mark_clean)
    ScanID = args.get('scan_id')
    if not ScanID:
        raise ValueError('scan id not specified')
    try:
        res= client._http_request(
        method='GET',
        url_suffix=f'/quarantine/release/{ScanID}/?should_mark_as_clean={mark_clean}',
        headers=HEADER,
        )
        demisto.info("After response")
        return CommandResults(
        outputs_prefix='PP-ReleaseMail',
        outputs=res,
    )
    except DemistoException as e:
        demisto.info(e)    
def fetch_incidents(client: Client, args: Dict[str, Any]):
    last_run_str = str(demisto.getLastRun())
    my_dict = ast.literal_eval(last_run_str)
    demisto.info("last_run_str" +last_run_str)
    try:
        if "start" in str(my_dict):
            timestamp=str(my_dict['start'])
        else:
            demisto.info("no start val")
            day_ago = str(datetime.now() - timedelta(days=1))
            tmp=day_ago.replace(' ','T').partition(".")[0] #needs date to be in format of 2018-11-06T08:56:41, using partition to get rid of .3211 for example
            timestamp=date_to_timestamp(tmp)/1000 #for our api time needs to be a 10 digits timestamp and not 13.
            demisto.info(timestamp)
    except DemistoException as e :
        demisto.info(e)    
    try:
        #return 20 incidents each time, once everything works well i will change to 200 as recommended in the docs, it is just passing another parameter to our api. 
        res= client._http_request(
        method='GET',
        url_suffix=f'/scans/list/',
        params={"verbose_verdict":"MAL","start":timestamp,"limit":50},
        headers=HEADER,
        resp_type='json'
        )
        incidents = []
        incident_results=res["results"]
        for event in incident_results:
            t=event['created_at']+"+02:00"
            demisto.info("line 205")
            demisto.info(t)
            event.pop('attachment', None)
            incident = {
            'name': event['id'],
            'occurred': t,
            'rawJSON': json.dumps(event)
            }
            incidents.append(incident)
        last_scan_date=incidents[-1]['occurred']
        partitioned_string = last_scan_date.partition('.')
        date_timestamp=date_to_timestamp(partitioned_string[0])
        ten_digits=int(date_timestamp)/1000
        demisto.setLastRun({
            'start':int(round(ten_digits))#13 digits timestamp --> 10 digits timestamp
            })
        demisto.incidents(incidents)
    except DemistoException as e:
        demisto.info(e) 



''' MAIN FUNCTION '''


def main() -> None:
    """main function, parses params and runs command functions

    :return:
    :rtype:
    """

    # TODO: make sure you properly handle authentication
    # api_key = demisto.params().get('credentials', {}).get('password')

    # get the service API url
    base_url = urljoin(demisto.params()['url'], 'api/v1')
    demisto.info(base_url)
    # if your Client class inherits from BaseClient, SSL verification is
    # handled out of the box by it, just pass ``verify_certificate`` to
    # the Client constructor
    verify_certificate = not demisto.params().get('insecure', False)

    # if your Client class inherits from BaseClient, system proxy is handled
    # out of the box by it, just pass ``proxy`` to the Client constructor
    proxy = demisto.params().get('proxy', False)
    demisto.info(HEADER)

    demisto.debug(f'Command being called is {demisto.command()}')
    try:

        # TODO: Make sure you add the proper headers for authentication
        # (i.e. "Authorization": {api key})
        headers: Dict = {}

        client = Client(
            base_url=base_url,
            verify=verify_certificate,
            headers=HEADER,
            proxy=proxy)

        if demisto.command() == 'test-module':
            # This is the call made when pressing the integration Test button.
            result = test_module(client)
            return_results(result)

        # TODO: REMOVE the following dummy command case:
        elif demisto.command() == 'pp-add-blacklist':
            return_results(AddBlackWhitelist(client, demisto.args(),"blacklist"))
        elif demisto.command() == 'pp-add-whitelist':
            return_results(AddBlackWhitelist(client, demisto.args(),"whitelist"))
        # TODO: ADD command cases for the commands you will implement
        elif demisto.command() == 'pp-release-email':
            return_results(ReleaseMail(client, demisto.args()))
        elif demisto.command() == 'fetch-incidents':
            fetch_incidents(client,demisto.args())    
    except Exception as e:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f'Failed to execute {demisto.command()} command.\nError:\n{str(e)}')


''' ENTRY POINT '''


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()