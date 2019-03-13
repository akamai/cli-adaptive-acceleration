import json
import requests
import sys
import os
from urllib import parse


def httpErrors(status_code, endpoint, result):
    """ Basic error handling """
    if not isinstance(result, list):
        details = result.get('detail') or result.get('details') or ""
    else:
        details = ""
    if status_code == 403:
        error_msg = "ERROR: Call to %s failed with a 403 result\n" % endpoint
        error_msg += "ERROR: This indicates a problem with authorization.\n"
        error_msg += "ERROR: Please ensure that the credentials you created for this script\n"
        error_msg += "ERROR: have the necessary permissions in the Luna portal.\n"
        error_msg += "ERROR: Problem details: %s\n" % details
        print(error_msg)
        exit(1)

    if status_code in [400, 401]:
        error_msg = "ERROR: Call to %s failed with a %s result\n" % (endpoint, status_code)
        error_msg += "ERROR: This indicates a problem with authentication or headers.\n"
        error_msg += "ERROR: Please ensure that the .edgerc file is formatted correctly.\n"
        error_msg += "ERROR: If you still have issues, please use gen_edgerc.py to generate the credentials\n"
        error_msg += "ERROR: Problem details: %s\n" % result
        print(error_msg)
        exit(1)

    if status_code in [404]:
        error_msg = "ERROR: Call to %s failed with a %s result\n" % (endpoint, status_code)
        error_msg += "ERROR: This means that the object does not exist as requested.\n"
        error_msg += "ERROR: Please ensure that the URL you're calling is valid and correctly formatted\n"
        error_msg += "ERROR: or look at other examples to make sure yours matches.\n"
        error_msg += "ERROR: Problem details: %s\n" % details
        print(error_msg)
        exit(1)

    error_string = None
    if "errorString" in result:
        if result["errorString"]:
            error_string = result["errorString"]
    else:
        for key in result:
            if type(key) is not str or isinstance(result, dict) or not isinstance(result[key], dict):
                continue
            if "errorString" in result[key] and type(result[key]["errorString"]) is str:
                error_string = result[key]["errorString"]
    if error_string:
        error_msg = "ERROR: Call caused a server fault.\n"
        error_msg += "ERROR: Please check the problem details for more information:\n"
        error_msg += "ERROR: Problem details: %s\n" % error_string
        print(error_msg)
        exit(1)
    return 0

def reset(session, baseurl, arlId, verbose):
    """ send reset OPEN API call """
    reset_url = parse.urljoin(baseurl, "/adaptive-acceleration/v1/properties/%s/reset" % arlId)
    resetResult = session.post(reset_url, '')
    status = resetResult.status_code
    if verbose:
        print("LOG: POST %s %s" % (reset_url, status))
    if status == 204:
        return 0
    if verbose:
        print(">>>\n" + json.dumps(resetResult.json(), indent=2) + "\n<<<\n")
    return httpErrors(resetResult.status_code, reset_url, resetResult.json())
