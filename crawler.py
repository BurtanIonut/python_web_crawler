from spider import *
from file_handling import *
import urlparse


class Crawler:

    def __init__(self, url):
        # this is the url, given as input from the user
        self.url = url
        # this is the domain name + top domain
        self.base_url = url.split("/")[2]
        # this is the path to the queued links
        self.path_queue = self.base_url + "/" + "queue"
        # this is the path to the crawled links
        self.path_crawled = self.base_url + "/" + "crawled"
        self.set_queue = set()
        self.set_crawled = set()
        self.set_in_progress = set()
        self.spider = Spider()

    def create_new_crawl(self):
        create_folder(self.base_url)
        create_file(self.base_url + "/" + "queue")
        create_file(self.base_url + "/" + "crawled")

    # this is used to limit the span of urls to the ones that have the domain name
    # and top domain of the base url in them
    def drop(self, to_queue_):
        aux_set_queue = set()
        for i in to_queue_:
            domain = urlparse.urljoin(i, '/')
            if domain.__contains__(self.base_url):
                aux_set_queue.add(i)
        return aux_set_queue

    # ISSUE: it is really slow to crawl all the links with just one spider
    # will have to try a multi-threaded approach
    def release_spider(self, link_):
        return self.spider.crawl(link_)

    # this method inserts the base link into the file with queued links
    # basically it provides the starting point of the program
    def init_queue(self):
        with open(self.path_queue, 'w') as w:
            w.write(self.url)

    # ISSUE: i use this to periodically update the files with the
    # crawled and queued links, i have a feeling this is not the best
    # approach, will look into it
    def update_files(self):
        print "Updating files..."
        overwrite_file(self.path_queue)
        overwrite_file(self.path_crawled)
        set_to_file(self.set_queue, self.path_queue)
        set_to_file(self.set_crawled, self.path_crawled)

    def start(self):
        update_timer = 0
        print("Creating new project, if it does not already exist")
        self.create_new_crawl()
        # if the files with the queued and crawled links are empty,
        # i have to provide a starting point by writing the initial url into
        # the queue file
        if os.path.isfile(self.path_queue) and os.path.isfile(self.path_crawled):
            if os.stat(self.path_queue).st_size == 0 and os.stat(self.path_crawled).st_size == 0:
                self.init_queue()
        self.set_queue = file_to_set(self.path_queue)
        self.set_crawled = file_to_set(self.path_crawled)
        print "Started crawling..."
        while self.set_queue:
            # ISSUE: like i said on the update_files method,
            # i believe this file management part can be improved
            if update_timer >= 1000:
                self.update_files()
                update_timer = 0
            crt_link = self.set_queue.pop()
            if crt_link not in self.set_crawled:
                # some information to give a bit of feedback on that is
                # is going on while the spider crawls
                print("Spider crawling { " + crt_link + " }")
                print "CRAWLED LINKS: " + str(len(self.set_crawled))
                print "QUEUED LINKS: " + str(len(self.set_queue))
                # this call is what gets the spider to start crawling
                to_queue = self.release_spider(crt_link)
                # check if the spider returned any number of links
                if to_queue:
                    # if the spider returned a non zero number of
                    # crawled links, then the queue set is updated
                    # with the links that are in the base url's scope,
                    # see drop method
                    update_timer += len(to_queue)
                    to_queue = self.drop(to_queue)
                    self.set_queue.update(to_queue)
                    # update the crawled set with the current crawled link
                    self.set_crawled.add(crt_link)
                else:
                    # if the spider returned no links, i only
                    # set the link the link the spider worked on as crawled
                    self.set_crawled.add(crt_link)
        self.update_files()
        print "Finished crawling... :)"
