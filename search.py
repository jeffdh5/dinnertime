import json
import oauth2
import urllib
import urllib2

def Search(host='api.yelp.com', path='/v2/search', url_params={'term':'bars', 'location':'san francisco', 'limit':1}, consumer_key='Ag5v1cO4xGtdPjP2A4m91g', consumer_secret='XKxecWJBM-at4X47JXv3IHImwYk', token='DRo0iJidHuW4y9s_qQjJnYGVXvvpsc9U', token_secret='4P4RfivcV5c9Ns8eCwCTanztHxY'):
  """Returns response for API request."""
  # Unsigned URL
  encoded_params = ''
  if url_params:
    encoded_params = urllib.urlencode(url_params)
  url = 'http://%s%s?%s' % (host, path, encoded_params)

  # Sign the URL
  consumer = oauth2.Consumer(consumer_key, consumer_secret)
  oauth_request = oauth2.Request('GET', url, {})
  oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                        'oauth_timestamp': oauth2.generate_timestamp(),
                        'oauth_token': token,
                        'oauth_consumer_key': consumer_key})

  token = oauth2.Token(token, token_secret)
  oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
  signed_url = oauth_request.to_url()

  # Connect
  try:
    conn = urllib2.urlopen(signed_url, None)
    try:
      response = json.loads(conn.read())
    finally:
      conn.close()
  except urllib2.HTTPError, error:
    response = json.loads(error.read())

  return response