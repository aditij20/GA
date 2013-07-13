#
# Use OAUTH to access Twitter's live 1% stream of tweets
#  Write to STDOUT
#
import oauth2 as oauth
import urllib2 as urllib
import sys


#
# Get authorization using OAUTH. 
#
access_token_key    = "1408486478-YLXMB9oFiVYDMItD8iV5pGCp2XWJbh7vnKXNcjx"
access_token_secret = "MPDV3m2NJBRfspUp8YY3kpphp0kKMOeOJ5QLxjWb5s"

consumer_key        = "tU7FuiUiVNwTW03Yj11giA"
consumer_secret     = "hgTgyehPDlQeR9p5PuYMemkk5ttd62j2cb3qqcQxK8"

_debug = 0

oauth_token         = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer      = oauth.Consumer(key=consumer_key, secret=consumer_secret)
signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

# http_method = "GET"
http_method = "POST"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

#
# Construct, sign, and open a twitter request using the hard-coded credentials above.
#
def twitterreq(url, method, parameters):
  print "twitterreq ", parameters
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)
  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()


  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)
  return response

#
# Bounding box for contiguous US is:

def fetchsamples():
  url = "https://stream.twitter.com/1/statuses/sample.json"
  parameters={}
  parameters['locations'] = '-124.7625,24.5210,-66.9326,49.3845'
  
  try:
    response = twitterreq(url, "GET", parameters)
    for line in response:
      print line.strip()
  except:
    e = sys.exc_info()[0]
    print "Error with twitter request", url, "GET", parameters


if __name__ == '__main__':
  fetchsamples()