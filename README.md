# Python-AppDotNet

## Quick HOWTO:

* Install the dependencies (see top of appdotnet.py)
* Create a app.net client app.
* Use "x-appdotnethelper:///" as the Callback URL.
* Call appdotnet.py with the client id

	$ python appdotnet.py authenticate <client_id>

* This will try to open your web browser at a "x-appdotnethelper:///#access_token=xxxxxxx" url take note of the access token.

	$ python appdotnet.py accesstoken <access_token>
	
* You should be good now, fetch the last batch of global posts

	$ python global
