import markdown2
import re

from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_page

from core.models import Page


def render_landing(request):
    old_page_id = request.GET.get("p", None)
    if old_page_id:
        try:
            page = Page.objects.get(slug=old_page_id)
            return HttpResponseRedirect("/p/%d" % page.id)
        except Page.DoesNotExist:
            raise Http404

    return render_page_by_slug(request, page_slug="landing", show_next_prev=False, discussion=False)


def render_page_by_slug(request, page_slug, show_next_prev=True, discussion=True):
    wo_html = re.sub(r"(.*)\.html$", r"\1", page_slug)
    if page_slug != wo_html:
        return HttpResponseRedirect("/%s" % wo_html)

    try:
        page = Page.objects.get(slug=page_slug)
    except Page.DoesNotExist:
        if page_slug == "landing":
            # Render hard coded backup
            return render_to_response("landing.html",
                context_instance=RequestContext(request))
        raise Http404
    return render_page_by_id(request, page.id, show_next_prev, discussion)


def is_markdown(content):
    markdown_header = "<!--markdown"
    if content[0:len(markdown_header)] == markdown_header:
        return True
    return False


def markdown(content):
    # TODO: Cache this!
    content = markdown2.markdown(
           content,
           extras=["code-friendly", "fenced-code-blocks", "footnotes", "wiki-tables"])
    return content


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
  .container h1 {
    display:none;
  }
  #banner {
    margin-top:-30px;
    margin-left:0px;
    margin-bottom:20px;
    padding: 0;
    width:100%%;
    background-size: 100%%;
    background-repeat: no-repeat;
    background-image: url(' %s ');
  }
  .byline {
    display:none;
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
        $('#banner').css('height', 'auto');
    } else {
        $('#banner').height($(window).height());
    }
    $(window).resize(function(){
        if ($(window).width() < 800) {
            $('#banner').css('height', 'auto');
            return;
        }
            $('#banner').height($(window).height());
    });
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
        carousel += """    <li data-target="#myCarousel" data-slide-to="%d"></li>
""" % i
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


def get_image_url(html):
    r = re.search("<img[^>]+src[ ]*=[ ]*[\'\"]([^\'\"]+)[\'\"].*>", html)
    try:
        url = r.group(1)
    except Exception:
        return settings.DEFAULT_IMAGE_URL
    return url


@cache_page(None)
def render_page_by_id(request, page_id, discussion=True, show_next_prev=True,
        template_name="page.html"):
    try:
        page = Page.objects.get(id=page_id)
    except Page.DoesNotExist:
        raise Http404

    if page.status != "public" and not request.user.is_staff:
        raise Http404

    content = page.body
    options = ""
    if is_markdown(content):
        content = markdown(content)
        options = content[0:content.find("-->")]

    image_url = get_image_url(content)

    page_head = page.head
    page_foot = page.foot
    exclude_first = 1
    if "black-background" in options:
        page_head += get_black_background_head()

    if "coverphoto" in options:
        page_head += get_coverphoto_head(image_url)
        page_foot += get_coverphoto_foot()
        exclude_first = 3

    if "carousel" in options:
        page_head += get_carousel_head()
        page_foot += get_carousel_foot()
        content = make_carousel_content(content, exclude_first)

    if request.user.is_staff:
        content += ("<div>Status: " + page.status + " <a href=\"/admin/core/page/" + str(page.id) +
            "\">Edit</a></div>")

    prev_page = None
    next_page = None
    if show_next_prev:
        pages = Page.objects.all() if request.user.is_staff else Page.objects.filter(status="public")
        pages = pages.exclude(slug="landing")
        prev_pages = pages.filter(created_at__lt=page.created_at).order_by(
            "-" + settings.ORDER_PAGES_BY)[:1]
        prev_page = prev_pages[0] if prev_pages else None
        next_pages = pages.filter(created_at__gt=page.created_at).order_by(
            settings.ORDER_PAGES_BY)[:1]
        next_page = next_pages[0] if next_pages else None

    context = {
        "title": page.title,
        "url": page.slug,
        "prev_page": prev_page,
        "next_page": next_page,
        "head": page_head,
        "main": content,
        "foot": page_foot,
        "created_at": page.created_at.date(),
        "modified_at": page.modified_at.date(),
        "image_url": image_url,
        "discussion": discussion
    }
    return render_to_response(template_name, context,
            context_instance=RequestContext(request))


def render_page_list(request, template_name="pages.html", content_type="application/xhtml+xml"):
    kwargs = {}
    if not request.user.is_staff:
        kwargs["status"] = "public"

    pages = Page.objects.exclude(title="").filter(**kwargs).order_by("-" + settings.ORDER_PAGES_BY)

    title = "blogs | " + settings.WEBSITE_TITLE
    context = {
        "title": title,
        "pages": pages
    }
    return render_to_response(template_name, context,
            context_instance=RequestContext(request))


def render_atom_xml(request, template_name="atom.xml", content_type="text/xml"):
    return render_page_list(request, template_name=template_name)
