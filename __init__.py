"""Search the Laravel Documentation"""
from pathlib import Path

from albert import QueryHandler, Item

import os
import urllib.parse
import html
from algoliasearch.search_client import SearchClient

md_iid = "0.5"
md_version = "0.4"
md_id = __name__
md_name = "Laravel Docs"
md_description = "Albert extension for quickly and easily searching the Laravel documentation"
#md_license = "BSD-2"
#md_url = "https://url.com/to/upstream/sources/and/maybe/issues"
#md_maintainers = "@preferrablyYourGithubName"


client = SearchClient.create("8BB87I11DE", "8e1d446d61fce359f69cd7c8b86a50de")
index = client.init_index("docs")

# icon = "{}/icon.png".format(path.dirname(__file__))
# google_icon = "{}/google.png".format(path.dirname(__file__))
#

GOOGLE_ICON_PATH = str(Path(__file__).parent / 'google.png')
ICON_PATH = str(Path(__file__).parent / 'icon.png')

docs = "https://laravel.com/docs/"



class Plugin(QueryHandler):
    def id(self):
        return md_id

    def name(self):
        return md_name

    def description(self):
        return md_description

    def defaultTrigger(self):
        return "ld "

    def initialize(self):
        self.icon = [os.path.dirname(__file__) + "/icon.png"]

    def finalize(self):
        info('finalize')

    def getSubtitle(hit):
        if hit["h4"] is not None:
            return hit["h4"]

        if hit["h3"] is not None:
            return hit["h3"]

        if hit["h2"] is not None:
            return hit["h2"]

        return None
    def handleTriggerQuery(self, query):
        items = []

        if query.isTriggered:

            if not query.isValid:
                return

            if query.string.strip():
                search = index.search(
                    query.string, {"tagFilters": "master", "hitsPerPage": 5}
                )

                for hit in search["hits"]:

                    title = hit["h1"]
                    subtitle = self.getSubtitle(hit)
                    url = "{}{}".format(docs, hit["link"])

                    text = False
                    try:
                        text = hit["_highlightResult"]["content"]["value"]
                    except KeyError:
                        pass

                    if text and subtitle:
                        title = "{} - {}".format(title, subtitle)
                        subtitle = text

                    items.append(
                        {
                            'icon': ICON_PATH,
                            'text': html.unescape(title),
                            'subtext': html.unescape(subtitle if subtitle is not None else ""),
                            'actions': [UrlAction("Open in the Laravel Documentation", url)],
                        }
                    )

                if len(items) == 0:
                    term = "laravel {}".format(query.string)

                    google = "https://www.google.com/search?q={}".format(
                        urllib.parse.quote(term)
                    )

                    items.append(
                        {
                            'icon': GOOGLE_ICON_PATH,
                            'text': "Search Google",
                            'subtext': 'No match found. Search Google for: "{}"'.format(term),
                            'actions': [UrlAction("No match found. Search Google", google)],
                        }
                    )

                    items.append(
                        {
                            'icon': GOOGLE_ICON_PATH,
                            'text': "Open Docs",
                            'subtext': "No match found. Open laravel.com/docs...",
                            'actions': [UrlAction("Open the Laravel Documentation", docs)],
                        }
                    )

            else:
                items.append(
                    {
                        'icon': GOOGLE_ICON_PATH,
                        'text': "Open Docs",
                        'subtext': "Open laravel.com/docs....",
                        'actions': [UrlAction("Open the Laravel Documentation", docs)],
                    }
                )

        return items
