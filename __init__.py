"""
Search the Laravel Documentation
"""

from albert import Action, Item, QueryHandler, openUrl, info, debug
import os
import urllib.parse
from algoliasearch.search_client import SearchClient

md_iid = "0.5"
md_version = "0.4"
md_id = __name__
md_name = "Laravel"
md_docs = "https://laravel.com/docs/"
md_description = "Albert extension for quickly and easily searching the Laravel documentation"
md_url = "https://github.com/use-the-fork/albert-laravel-docs/issues"
md_maintainers = "@use-the-fork"
md_lib_dependencies = ["algoliasearch"]
md_trigger = "lv "



client = SearchClient.create("E3MIRNPJH5", "1fa3a8fec06eb1858d6ca137211225c0")
index = client.init_index("laravel")

GOOGLE_ICON_PATH = "{}/images/google.png".format(os.path.dirname(__file__))
ICON_PATH = "{}/images/icon.png".format(os.path.dirname(__file__))


class Plugin(QueryHandler):
    def id(self):
        return md_id

    def name(self):
        return md_name

    def description(self):
        return md_description

    def defaultTrigger(self):
        return md_trigger

    def getTitle(self, hierarchy):
        if hierarchy["lvl6"] is not None:
            return hierarchy["lvl6"]

        if hierarchy["lvl5"] is not None:
            return hierarchy["lvl5"]

        if hierarchy["lvl4"] is not None:
            return hierarchy["lvl4"]

        if hierarchy["lvl3"] is not None:
            return hierarchy["lvl3"]

        if hierarchy["lvl2"] is not None:
            return hierarchy["lvl2"]

        if hierarchy["lvl1"] is not None:
            return hierarchy["lvl1"]

        if hierarchy["lvl0"] is not None:
            return hierarchy["lvl0"]

        return None

    def getSubtitle(self, hierarchy):
        if hierarchy["lvl6"] is not None:
            return hierarchy["lvl5"]

        if hierarchy["lvl5"] is not None:
            return hierarchy["lvl4"]

        if hierarchy["lvl4"] is not None:
            return hierarchy["lvl3"]

        if hierarchy["lvl3"] is not None:
            return hierarchy["lvl2"]

        if hierarchy["lvl2"] is not None:
            return hierarchy["lvl1"]

        if hierarchy["lvl1"] is not None:
            return hierarchy["lvl0"]

        return None

    def handleQuery(self, query):
        items = []

        if not query.isValid:
            return

        if query.string.strip():

            search = index.search(
                query.string, {"facetFilters": "version:10.x", "hitsPerPage": 5, "highlightPreTag": "...", "highlightPostTag": "..."}
            )

            for hit in search["hits"]:

                title = self.getTitle(hit['hierarchy'])
                subtitle = self.getSubtitle(hit['hierarchy'])
                url = hit["url"]

                text = False
                try:
                    text = hit["_highlightResult"]["content"]["value"]
                except KeyError:
                    pass

                if text and subtitle:
                    title = "{} - {}".format(title, subtitle)
                    subtitle = text

                items.append(
                    Item(
                        id=f'{md_name}/{hit["objectID"]}',
                        icon=[ICON_PATH],
                        text=title,
                        subtext=subtitle if subtitle is not None else "",
                        actions=[
                            Action(
                                "Open",
                                'Open the {} Documentation'.format(md_name),
                                lambda u=url: openUrl(u)
                            )
                        ],
                    )
                )

            if len(items) == 0:
                term = "laravel {}".format(query.string)

                google = "https://www.google.com/search?q={}".format(
                    urllib.parse.quote(term)
                )

                items.append(
                    Item(
                        id=f'{md_name}/search_google',
                        icon=[GOOGLE_ICON_PATH],
                        text="Search Google",
                        subtext='No match found. Search Google for: "{}"'.format(term),
                        actions=[
                            Action(
                                "Open",
                                'No match found. Search Google',
                                lambda u=google: openUrl(u)
                            )
                        ],
                    )
                )

                items.append(
                    Item(
                        id=f'{md_name}/open_{md_name}_docs',
                        icon=[ICON_PATH],
                        text='Open {} Docs'.format(md_name),
                        subtext="No match found. Open {}".format(md_docs),
                        actions=[
                            Action(
                                "Open",
                                'Open the {} Documentation'.format(md_name.replace("https://", "")),
                                lambda u=md_docs: openUrl(u)
                            )
                        ],
                    )
                )

        query.add(items)
