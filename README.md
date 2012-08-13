# Python-AppDotNet

## Quick HOWTO:

* Install the dependencies (see top of appdotnet.py)
* Create a app.net client app.
* Use "x-appdotnethelper:///" as the Callback URL.
* Call appdotnet.py with the client id

	# python appdotnet.py authenticate <client_id>

* This will open your web browser at a "x-appdotnethelper:///" url take note of the access token.

	# python appdotnet.py set-accesstoken <access_token>
	
* You should be good now, fetch the last batch of global posts

	# python global
