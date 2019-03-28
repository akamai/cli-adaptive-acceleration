# A2 - CLI

A command line interface for Akamai's Adaptive Acceleration offering. It allows you to reset the A2 Push and Preconnect 
optimizations manually. It can be used in continuous deployment environments where popular resources change often or 
quickly. 


## Install
First, install the [Akamai CLI](https://github.com/akamai/cli). Second, install the adaptive-acceleration CLI package with
 
```
akamai install adaptive-acceleration
```

# Setting Up

Before you can use the CLI, you need to install API keys and find the id of the property you wish to reset. 

## API Keys

Generate API keys with READ-WRITE available on the Adaptive Acceleration capability as described [here](https://control.akamai.com/dl/IDM/IAM/GUID-7A592469-DDDC-4705-A3FA-C89DCD15934E.html) 
and save them to your `~/.edgerc` file. Alternatively, you can also add the Adaptive Acceleration capability to your existing credentials. 

## Finding the Property Id with the CLI

Internally Adaptive Acceleration uses a PROPERTYID to track the property you are dealing with. These steps help you find the property and allow you to run a reset. 

1. Find your property in the Akamai Control Center.
2. In the header at the top of the page, open the dropdown titled with your name and select Profile. Control Center will show you a dialog with roles for your user. Close that, so you can see the Identity and Access Management UI beneath it. 
3. On the Users and API Clients tab, select the group dropdown that corresponds to your property. 
4. Click "New API client for me" - it can be found to the right of the group dropdown.
5. You will be shown a "New API client for" wizard. Hit "Next". 
6. You should see the "Access Level" page. Enter a client name and description. 
7. While you're still on the "Access Level" page, search for "property manager" in the filter box above the "API Service Name".
8. You should be shown a single entry named "Property Manager (PAPI)". Click the "Access Level" and select "READ-WRITE".
9. Hit the "Submit" button.
10. You should be shown the API client's information in the "Users and API Clients" tab. Click the button titled "New credential".
11. Copy the credential text out of the dialog, and paste it into ~/.edgerc, in a section named `default`.
12. Run `akamai property retrieve exact-name-of-your-property --section default`.
13. In the output, find the value of the `propertyId` field
   ```
   {
     "accountId": "act_B-M-1ZXZ3WU",
     "contractId": "ctr_M-1ZXZ3XD",
     "groupId": "grp_93848",
     "propertyId": "prp_459153",
   ```
   the property id is the numeric part of the value (ie, the part without the "prp_" prefix). In this case, it is 459153. Use that in the next section to replace PROPERTYID.

# Usage

To reset a policy, run

```
akamai a2 reset PROPERTYID
```

where PROPERTYID is the identifier you found in the previous section. 

## Global Flags
- `--edgerc value` — Location of the credentials file (default: user's directory like "/Users/vzaytsev/.edgerc") [$AKAMAI_EDGERC]
- `--section value` — Section of the credentials file to use (default: "default") .
- `--debug` - `-d` - prints debug information
- `--help`, `-h` — Show help


## Exit Codes

The exit code is 0 on success, or 1 in case of an error returned by the [underlying API](https://developer.akamai.com/api/core_features/adaptive_acceleration/v1.html).


## Errors

If the API key you provisioned does not have permission to reset the given property, you will get the following message:

```
$ akamai a2 reset 459153
Reset policy for: 459153
ERROR: Call to https://akab-xyz.luna.akamaiapis.net/adaptive-acceleration/v1/properties/359153/reset failed with a 403 result
ERROR: This indicates a problem with authorization.
ERROR: Please ensure that the credentials you created for this script
```

You can resolve this by editing the permissions of the credentials you created to ensure they include READ-WRITE permissiong on Adaptive Acceleration for your 
account. 
