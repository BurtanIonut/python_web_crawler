Python Web Crawler

I implemented a simple web crawler that writes to a file all the links that lead to html files for an initial URL, given by the user. The links are limited to containing the domain name and the top level domain of the user given URL.

I implemented a few methods to work with files, it the file_handling.py source

I implemented a Crawled class that takes care of converting file contents to a set and vice-versa. The Crawler is also responsible for managing the set contents based on the crawled links. Also, the Crawler initialises the Spider and gives it links to crawl.

I implemented a Spider class that takes a base link and gets all the links on the given page as long as the page is a html file, then returns the set with the crawled links.

The main source holds the code that gets the input from the user (the base URL) and initialises the Crawler.

I have several ISSUES with the code, as described in the sources:

Most importantly: The code can greatly benefit from using paralelisation,
the Crawler should be able to run multiple Spiders at once.
Other issues include:
When to write to files, because the sets holding the links keep growing
and the time it would take to rewrite the files increses. I have
to keep in mind that the program might crash and the data in the sets can get lost.
Therefore I cannot update the files just once at the end of the crawling process, the
updates have to be done periodically, but just how perodically....?
Errors from reading certain links:
I have to find some documentation or some sort of way to identify when and why certain
errors arise.