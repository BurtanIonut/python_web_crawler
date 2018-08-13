from bs4 import BeautifulSoup
import urlparse
import requests

# ISSUE: this a list of url string endings, i have to make additional checks because
# some links that point to files actually have the Content-type "html/text" and
# in the header of the page and get passed as html files
checks = [".mp3", ".pdf", ".mp4", ".odp", ".zip", ".png", ".tar.gz"]


class Spider:
    def __init__(self):
        self.link = ""
        self.base_url = ""

    # this is the method used to crawl a page
    def crawl(self, link):
        self.link = link
        self.base_url = self.link.split("/")[2]
        return self.get_links()

    # uses the list of string suffixes above to do additional checks
    def check_additionally(self):
        for i in checks:
            if self.link.endswith(i):
                return False
        return True

    # this method gathers all the links from a given page
    # without links that are equal to the initial link
    def get_links(self):
        to_queue = set()
        try:
            head = requests.head(self.link)
        except:
            return False
        else:
            try:
                # ISSUE: i got this error on a site, so i use a catch for it
                # until i better understand what happened
                headers = head.headers["Content-type"]
            except KeyError:
                print "KeyError: content-type :("
                return to_queue
            else:
                # this if statement should check if the page is an actual html file
                # still, some links that point to file downloads, pdfs or other,
                # pass this check, therefore i use the check_additionally() method
                if "text/html" in headers:
                    if self.check_additionally():
                        page = requests.get(self.link)
                        try:
                            soup = BeautifulSoup(page.text, "html.parser")
                        except MemoryError:
                            # ISSUE: got this problem on a site
                            # i have to look into this
                            print "Memory error :("
                            return to_queue
                        else:
                            for link_ in soup.findAll('a'):
                                to_add = urlparse.urljoin(self.base_url, link_.get('href'))
                                # make sure we don't check the initial link again
                                if to_add.startswith(("https://", "http://")) and to_add != self.link:
                                    to_queue.add(to_add)
                            if not to_queue:
                                # if there are no links on the current page
                                print "SPIDER: nothing to be done for " + "{ " + self.link + " }"
                    else:
                        # if the html file check passes but check_additionally() fails
                        print "SPIDER: not HTML file " + "{ " + self.link + " }"
                else:
                    # if the html file check passes
                    print "SPIDER: not HTML file " + "{ " + self.link + " }"
                return to_queue
