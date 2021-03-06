import re

from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from core.models import Page
from core.rutils import is_rmarkdown, rmarkdown_page
from core.utils import is_markdown, markdown_page
from page_formats import (
    get_cover_video_block, get_image_url, get_black_background_head,
    get_coverphoto_head, get_coverphoto_foot,
    get_covervideo_head, get_covervideo_foot,
    get_carousel_head, get_carousel_foot, get_video_url, make_carousel_content)


def render_500(request):
    response = render_to_response('500.html', {},
            context_instance=RequestContext(request))
    response.status_code = 500
    return response


def render_landing(request):
    old_page_id = request.GET.get("p", None)
    if old_page_id:
        try:
            page = Page.objects.get(slug=old_page_id)
            return HttpResponseRedirect("/p/%d" % page.id)
        except Page.DoesNotExist:
            raise Http404

    return render_page_by_slug(request, page_slug="landing",
                               show_next_prev=False, discussion=False)


def render_page_by_slug(request, page_slug, show_next_prev=True,
                        discussion=True):
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

    if is_rmarkdown(content):
        # It should not use page_id as a kwarg to keep the cache key consistent
        content = rmarkdown_page(page_id, clear_cache=False)
    elif is_markdown(content):
        content = markdown_page(page_id, clear_cache=False)
        options = content[0:content.find("-->")]

    try:
        content = content.decode("utf-8")
    except UnicodeEncodeError:
        pass  # Taking a chance here. Let it fail later if it does.

    image_url = get_image_url(content)
    cover_content = ""
    page_head = page.head
    page_foot = page.foot
    exclude_first = 1
    custom_css = None
    if "custom-css" in options:
        try:
            custom_css = re.match(r".* (.*\.css)", options).group(1)
        except:
            custom_css = None

    if "black-background" in options:
        page_head += get_black_background_head()

    if "coverphoto" in options:
        page_head += get_coverphoto_head(image_url)
        page_foot += get_coverphoto_foot()
        exclude_first = 3

    if "covervideo" in options:
        page_head += get_covervideo_head()
        page_foot += get_covervideo_foot()
        exclude_first = 2
        video_url = get_video_url(content)
        cover_content = get_cover_video_block(video_url)

    if "carousel" in options:
        page_head += get_carousel_head()
        page_foot += get_carousel_foot()
        content = make_carousel_content(content, exclude_first)

    if request.user.is_staff:
        content += ("<div>Status: " + page.status +
                    " <a href=\"/admin/core/page/" + str(page.id) +
                    "\">Edit</a></div>")

    prev_page = None
    next_page = None
    if show_next_prev:
        if request.user.is_staff:
            pages = Page.objects.all()
        else:
            pages = Page.objects.filter(status="public")
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
        "custom_css": custom_css,
        "cover_content": cover_content,
        "main": content,
        "foot": page_foot,
        "created_at": page.created_at.date(),
        "modified_at": page.modified_at.date(),
        "image_url": image_url,
        "discussion": discussion
    }
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))


def render_page_list(request, template_name="pages.html",
                     content_type="application/xhtml+xml"):
    kwargs = {}
    if not request.user.is_staff:
        kwargs["status"] = "public"

    pages = Page.objects.exclude(title="").filter(**kwargs).order_by(
        "-" + settings.ORDER_PAGES_BY)

    title = "blogs | " + settings.WEBSITE_TITLE
    context = {
        "title": title,
        "pages": pages
    }
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))


def render_atom_xml(request, template_name="atom.xml",
                    content_type="text/xml"):
    return render_page_list(request, template_name=template_name)
