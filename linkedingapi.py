import requests

redirectURI = 'https://fixupe.com'
encoded_redirectURI = 'https%3A%2F%2Ffixupe.com'
clientId = '7836v8j0n81pz7'
clientSecret = 'nI8pyUEsOJXqS01Y'
response_type = 'code'

oauth_url = 'https://www.linkedin.com/oauth/v2/authorization?response_type=code&state=987654321&scope=w_member_social&client_id=7836v8j0n81pz7&redirect_uri=https://fixupe.com'
response = requests.post(oauth_url)
print(response)