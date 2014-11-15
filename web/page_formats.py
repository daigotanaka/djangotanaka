import re

from django.conf import settings


def get_image_url(html):
    r = re.search("<img[^>]+src[ ]*=[ ]*[\'\"]([^\'\"]+)[\'\"].*>", html)
    try:
        url = r.group(1)
    except Exception:
        return settings.DEFAULT_IMAGE_URL
    return url


def get_video_url(html):
    r = re.search("covervideo[ ]*=[ ]*[\'\"]([^\'\"]+)[\'\"]", html)
    try:
        url = r.group(1)
    except Exception:
        return None
    return url


def get_black_background_head():
    return """
<style>
body {
    background-color: black;
    color: white;
}

#banner a {
color: white;
}
</style>
"""


def get_coverphoto_head(image_url):
    return """
<style>
#main p:first-of-type {
  display: none;
}
@media (min-width: 800px){
  body, html {
    width: 100%%;
    height: 100%%;
  }
  .container {
    width: 100%%;
    margin: 0;
  }
  #banner {
    opacity: 0;
    -webkit-animation: smooth 5s ease-out;
    -moz-animation: smooth 5s ease-out;
    -o-animation: smooth 5s ease-out;
    -ms-animation: smooth 5s ease-out;
    animation: smooth 5s ease-out;
  }
  @-webkit-keyframes smooth {
      0%% { opacity: 1;}
      100%% { opacity: 0;}
  }
  #cover_content {
    margin-top:-30px;
    margin-left:0px;
    margin-bottom:20px;
    padding: 0;
    width:100%%;
    background-size: 100%%;
    background-repeat: no-repeat;
    background-image: url(' %s ');
  }
  #content {
    border: none;
    margin: 0 auto;
    float: none;
  }
  #main p:nth-of-type(2) {
    display: none;
  }
}
</style>
""" % image_url


def get_coverphoto_foot():
    return """
<script>
$(function(){
    if ($(window).width() < 800) {
        $('#cover_content').css('height', 'auto');
    } else {
        $('#cover_content').height($(window).height());
    }
    $(window).resize(function(){
        if ($(window).width() < 800) {
            $('#cover_content').css('height', 'auto');
            return;
        }
            $('#cover_content').height($(window).height());
    });
});
</script>
"""


def get_covervideo_head():
    return """
<style>
@media (min-width: 800px){
  body, html {
    width: 100%%;
    height: 100%%;
  }
  .container {
    width: 100%%;
    margin: 0;
  }
  #banner {
    position: absolute;
    top: 100px;
    opacity: 0;
    -webkit-animation: smooth 5s ease-out;
    -moz-animation: smooth 5s ease-out;
    -o-animation: smooth 5s ease-out;
    -ms-animation: smooth 5s ease-out;
    animation: smooth 5s ease-out;
  }
  @-webkit-keyframes smooth {
      0%% { opacity: 1;}
      100%% { opacity: 0;}
  }
  #cover_content {
    margin-top:-30px;
    margin-left:0px;
    margin-bottom:20px;
    padding: 0;
    width:100%%;
  }
  #cover_content video {
    right: 0;
    bottom: 0;
    min-width: 100%;
    min-height: 100%;
    width: auto;
    height: auto;
  }
  #content {
    border: none;
    margin: 0 auto;
    float: none;
  }
  #main p:first-of-type {
    display: none;
  }
}
@media (max-width: 800px){
  #cover_content {
    display: none;
  }
}
</style>
"""


def get_covervideo_foot():
    return """
<script>
$(function(){
  if ($(window).width() < 800) return;
  var vid=$("#cover_content video").get(0);
  //try to force it to start automatically after a few secs
  setTimeout(function(){
    $("body").one("touchstart load",function(){
    vid.play();
    }).trigger("load");
  },0);
});
</script>
"""


def get_carousel_head():
    return """
<link href="/static/css/carousel.css" rel="stylesheet">
"""


def get_carousel_foot():
    return """
<script>
    !function ($) {
        $(function(){
            $('#myCarousel').carousel({
                interval: 5000
            })
        })
    }(window.jQuery)
</script>
"""


def make_carousel_content(content, exclude_first=1):
    content = content.replace("<p>", "").replace("</p>", "<!--cd-->")
    items = content.strip().split("<!--cd-->")
    items = items[0:-1]
    if len(items) < 1:
        return content

    carousel = """
<!-- Carousel
================================================== -->
<div id="myCarousel" class="carousel slide">
  <ol class="carousel-indicators">
    <li data-target="#myCarousel" data-slide-to="0" class="active"></li>
"""
    for i in range(1, len(items) - exclude_first):
        carousel += '    <li data-target="#myCarousel" data-slide-to="%d">' % i
        carousel += "</li>"
    carousel += """  </ol>
  <div class="carousel-inner">
"""
    count = 0
    status = " active"
    before_carousel = ""
    for item in items:
        count += 1
        if count <= exclude_first:
            before_carousel += """
<p>
%s
</p>
""" % item
            continue
        carousel += """    <div class="item%s">
      %s
    </div>
""" % (status, item)
        status = ""
    carousel += """
  </div>
</div><!-- /.carousel -->
"""
    return before_carousel + carousel


def get_cover_video_block(video_url, poster_url):
    return """<video autoplay control loop muted poster="%s" class="full_screen_video" >
<source src="%s" type="video/mp4">
</video>
""" % (poster_url, video_url)
