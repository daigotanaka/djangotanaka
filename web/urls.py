from django.conf.urls import patterns, url

from views import (render_atom_xml, render_landing, render_page_by_id,
    render_page_by_slug, render_page_list)


urlpatterns = patterns("",
    url(r"^$", render_landing, name="landing"),
    url(r"^blogs/$", render_page_list, name="page_list"),
    url(r"^atom_xml/$", render_atom_xml, name="atom_xml"),
    url(r"^p/(?P<page_id>.*)/$", render_page_by_id, name="page_by_id"),
    url(r"^(?P<page_slug>.*)/$", render_page_by_slug, name="page_by_slug")
    # url(r"^accounts/", include(accounts_urls)),
)
