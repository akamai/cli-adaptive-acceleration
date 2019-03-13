""" Copyright 2017 Akamai Technologies, Inc. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.

 You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import sys
import os
import argparse
import logging
from configparser import ConfigParser
import http.client as http_client

logger = logging.getLogger(__name__)

def get_prog_name():
    prog = os.path.basename(sys.argv[0])
    if os.getenv("AKAMAI_CLI"):
        prog = "akamai adaptive-acceleration"
    return prog


class EdgeGridConfig():

    parser = argparse.ArgumentParser(description='Process command line options.', prog=get_prog_name(), usage="akamai adaptive-acceleration [--edgerc credentials_file] [--section credentials_file_section] [-d] [-v] reset propertyId")

    def __init__(self, config_values, configuration, flags=None):
        subparsers = self.parser.add_subparsers(help='command help', dest="command")
        reset_parser = subparsers.add_parser("reset", help="[propertyId] reset A2 Push and Preconnect policy for the properyId. propertyId argument is mandatory")
        reset_parser.add_argument('propertyId', help="id of the property to be reset. This argument is mandarory.", metavar='propertyId',  type=int, action='store')

        self.parser.add_argument('--verbose', '-v', default=False, action='count', help=' verbose mode')
        self.parser.add_argument('--debug', '-d', default=False, action='count', help='debug mode (prints HTTP headers)')
        self.parser.add_argument('--edgerc', default='~/.edgerc', metavar='credentials_file', help='location of the credentials file (default is ~/.edgerc)')
        self.parser.add_argument('--section', default='default', metavar='credentials_file_section', action='store', help=' credentials file Section\'s name to use')

        if flags:
            for argument in flags.keys():
                self.parser.add_argument('--' + argument, action=flags[argument])

        arguments = {}
        for argument in config_values:
            if config_values[argument]:
                if config_values[argument] == "False" or config_values[argument] == "True":
                    self.parser.add_argument('--' + argument, action='count')
                self.parser.add_argument('--' + argument)
                arguments[argument] = config_values[argument]

        try:
            args = self.parser.parse_args()
        except:
            exit(1)

        arguments = vars(args)

        if not ('command' in arguments and arguments["command"]) :
            print("ERROR: missing adaptive-acceleration command. %s" % self.parser.format_usage())
            exit(1)

        if not ('propertyId' in arguments and arguments["propertyId"]) :
            print("ERROR: missing mandatory propertyId argument for the reset command")
            exit(1)

        if arguments['debug']:
            http_client.HTTPConnection.debuglevel = 1
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

        if "section" in arguments and arguments["section"]:
            configuration = arguments["section"]

        arguments["edgerc"] = os.path.expanduser(arguments["edgerc"])

        if os.path.isfile(arguments["edgerc"]):
            config = ConfigParser()
            config.read_file(open(arguments["edgerc"]))
            if not config.has_section(configuration):
                err_msg = "ERROR: No section named %s was found in your %s file\n" % (configuration, arguments["edgerc"])
                err_msg += "ERROR: Please generate credentials for the script functionality\n"
                err_msg += "ERROR: and run 'python gen_edgerc.py %s' to generate the credential file\n" % configuration
                print( err_msg )
                exit(1)
            for key, value in config.items(configuration):
                # ConfigParser lowercases magically
                if key not in arguments or arguments[key] is None:
                    arguments[key] = value
                else:
                    print("Missing configuration file.  Run python gen_edgerc.py to get your credentials file set up once you've provisioned credentials in LUNA.")
                    return None

        for option in arguments:
            setattr(self, option, arguments[option])
