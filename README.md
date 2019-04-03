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

## Configuring API Keys

Generate API keys with READ-WRITE available on the Adaptive Acceleration capability as described [here](https://control.akamai.com/dl/IDM/IAM/GUID-7A592469-DDDC-4705-A3FA-C89DCD15934E.html) 
and save them to your `~/.edgerc` file. Alternatively, you can also add the Adaptive Acceleration capability to your existing credentials. 


# Usage

Before you run the A2 reset command, you need to know the id of your property. That's exposed in the Akamai Control Center, on the _Automatic Push and Preconnect Policy_ page. 
To find it:

1. open your property on [control.akamai.com](https://control.akamai.com),
2. expand the _Related Apps_ dropdown and select _Automatic Push and Preconnect_,
3. click _Reset_ on the _Automatic Push and Preconnect Policy_ page,
4. the resulting dialog contains a sample command line that performs a reset for the property you are viewing. 

The command line is of the form `akamai a2 reset ###` where `###` is the property id. You can copy and paste the entire line into a terminal or script and run it:

```
akamai a2 reset 123456
```

If you want to check that the reset succeeded, use the exit code. 

## Exit Codes

The exit code is 0 on success, or 1 in case of an error returned by the [underlying API](https://developer.akamai.com/api/core_features/adaptive_acceleration/v1.html).

## Global Flags

- `--edgerc value` — Location of the credentials file (default: user's directory like "/Users/vzaytsev/.edgerc") [$AKAMAI_EDGERC]
- `--section value` — Section of the credentials file to use (default: "default") .
- `--debug` - `-d` - prints concise debug information about network endpoints
- `--verbose` - `-v` - prints network headers and other communication information
- `--help`, `-h` — Show help

The flags are passed to the `adaptive-acceleration` portion of the command-line: 

```
$ akamai a2 --section default -v reset 123456
Reset policy for: 123456
LOG: POST https://akab-cjzide3ie87zpaeu-ta8p6mb7deapdkpu.luna.akamaiapis.net/adaptive-acceleration/v1/properties/123456/reset 204
```

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
