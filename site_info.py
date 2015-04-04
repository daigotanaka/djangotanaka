# My settings
WEBSITE_URL = "http://0.0.0.0:5000"
WEBSITE_TITLE = "My Site Name"
WEBSITE_BYLINE = "Something more to say"
DEFAULT_IMAGE_URL = WEBSITE_URL + "/static/img/thumbnail.jpg"

ORDER_PAGES_BY = "created_at"

DISQUS_HANDLE = ""

# Could change it to http://feeds.feedburner.com/your_handle
FEED_URL = WEBSITE_URL + "/atom_xml/"

GOOGLE_ANALYTICS_DOMAIN = WEBSITE_URL[7:].replace("www.", "")
GOOGLE_ANALYTICS_ID = ""
