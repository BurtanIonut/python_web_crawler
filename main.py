from crawler import *
import requests


# get a valid url as input
def get_valid_url():
    while True:
        print "Enter a valid url e.g <http://MY_SITE.com> or <http://www.MY_SITE.ro>"
        try:
            url_ = str(raw_input())
        except ValueError:
            print "Enter a valid address"
        else:
            try:
                # check if we get a valid page from the url
                page_ = requests.get(url_)
            except (requests.exceptions.ConnectionError, requests.exceptions.MissingSchema):
                print "Cannot connect, would you like to enter a new URL? y/n"
                try:
                    opt = str(raw_input())
                except ValueError:
                    print "Crawler Shutting down"
                    return False
                else:
                    if opt == "y":
                        continue
                    else:
                        print "Crawler Shutting down"
                        return False
            else:
                return page_, url_


if __name__ == "__main__":

    page, url = get_valid_url()
    print "Url is valid, page found"
    if page:
        print "Initiating crawler"
        crawler = Crawler(url)
        crawler.start()
    else:
        # ISSUE: if the requests.get() call succedes, but still returns an empty page
        # it happened on few sites, i have to get more insight into this problem
        print "Cannot establish a connection :("