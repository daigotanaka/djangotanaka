import csv
import datetime
from optparse import make_option
import re
from xml.dom import minidom

from django.core.management.base import BaseCommand

from core.models import Page


class Command(BaseCommand):
    args = "import filename --format=(wordpress|csv)"
    help = "Import pages"

    option_list = BaseCommand.option_list + (
        make_option(
            "--format",
            dest="format",
            default=None,
            help=""
        )
    )

    def handle(self, *args, **options):
        commands = {
            "worldpress": self.wordpress,
            "csv": self.csv
        }
        commands[options["format"]](args[0])

    def wordpress(self, filename):
        xmldoc = minidom.parse(filename)
        channel = xmldoc.getElementsByTagName("channel")
        items = channel[0].getElementsByTagName("item")
        item_count = 0
        for item in items:
            item_count += 1
            print item_count
            title = item.getElementsByTagName("title")[0].firstChild.nodeValue
            print title
            try:
                text = item.getElementsByTagName(
                    "content:encoded")[0].firstChild.nodeValue
            except AttributeError:
                continue
            text = text.replace("\n\n", "</p>\n<p>")
            text = re.sub(r"(</h[1-4]>)</p>", r"\1", text)
            text = re.sub(r"(</h[1-4]>)[\n]*([^<])", r"\1\n<p>\2", text)
            text = re.sub(r"<p>[\n]<p>", r"<p>", text)
            text = text.replace("</div></p>", "</div>")
            text = re.sub(r"<p>[\n]*<h", r"\n<h", text)
            text = "<h2>" + title + "</h2>\n<p>" + text + "</p>"
            try:
                created_at = datetime.datetime.strptime(
                    item.getElementsByTagName(
                        "wp:post_date_gmt"
                    )[0].firstChild.nodeValue, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                try:
                    created_at = datetime.datetime.strptime(
                        item.getElementsByTagName(
                            "wp:post_date"
                        )[0].firstChild.nodeValue, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    created_at = datetime.datetime.now()
            url = item.getElementsByTagName(
                "wp:post_id")[0].firstChild.nodeValue
            status = "private" if (item.getElementsByTagName(
                "wp:status")[0].firstChild.nodeValue == "draft") else "public"
            page = Page.objects.create(
                url=url,
                title=title,
                text=text,
                status=status)
            page.created_at = created_at
            page.save()
        return

    def csv(self, filename):
        # CSV import example
        item = 0
        with open(filename, "rU") as f:
            rows = csv.reader(f)
            for row in rows:
                if row[20] != "post" and row[20] != "page":
                    continue
                item += 1
                print item
                status = "private" if row[7] == "draft" else "public"
                created_at = datetime.datetime.strptime(
                    row[2], "%Y-%m-%d %H:%M:%S")
                modified_at = datetime.datetime.strptime(
                    row[14], "%Y-%m-%d %H:%M:%S")
                page = Page.objects.create(
                    url=str(item),
                    modified_at=modified_at,
                    title=row[5],
                    text=row[4],
                    status=status)
                page.created_at = created_at
                page.save()
