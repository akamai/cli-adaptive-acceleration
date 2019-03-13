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

## API Keys

Generate API keys with READ-WRITE available on the Adaptive Acceleration capability as described [here](https://control.akamai.com/dl/IDM/IAM/GUID-7A592469-DDDC-4705-A3FA-C89DCD15934E.html) 
and save them to your `~/.edgerc` file. Alternatively, you can also add the Adaptive Acceleration capability to your existing credentials. 

## Finding the Property Id with Open APIs

Follow the steps on the [A2 Open API](https://developer.akamai.com/api/core_features/adaptive_acceleration/v1.html#gettingstarted) doc to find the property id.

## Finding the Property Id with the CLI

1. Find your property in luna.
2. Go to Your Name > Profile.
3. Select the Group for your property.
4. Click "Create new API client for me".
5. In the dialog, select the PAPI APIs with read/write credentials and the Adaptive Acceleration APIs with read/write. 
6. Create a new credential in the dialog. 
7. Copy the credential text out of the dialog, and paste it into ~/.edgerc, in a section named `default`.
8. Run `akamai property retrieve exact-name-of-your-property --section default`.
9. In the output, find the value of the `propertyId` field
   ```
   {
     "accountId": "act_B-M-1ZXZ3WU",
     "contractId": "ctr_M-1ZXZ3XD",
     "groupId": "grp_93848",
     "propertyId": "prp_459153",
   ```
   the property id is the numeric part of the value (ie, the part without the "prp_" prefix). In this case, it is 459153.

# Usage

To reset a policy, run

```
akamai adaptive-acceleration reset PROPERTYID
```

where PROPERTYID is the identifier you found in the previous section

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
