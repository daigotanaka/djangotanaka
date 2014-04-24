from site_info import *

def global_vars(context):
    return {
        "WEBSITE_TITLE": WEBSITE_TITLE,
        "WEBSITE_URL": WEBSITE_URL,
        "WEBSITE_BYLINE": WEBSITE_BYLINE,
        "DISQUS_HANDLE": DISQUS_HANDLE,
        "FEED_URL": FEED_URL,
        "GOOGLE_ANALYTICS_ID": GOOGLE_ANALYTICS_ID,
        "GOOGLE_ANALYTICS_DOMAIN": GOOGLE_ANALYTICS_DOMAIN
    }
