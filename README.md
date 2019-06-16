# yellscraper

Requires:
Requests
BeautifulSoup

pip install requests bs4


to use:

python YellScrapeV1.py


The Script Will Ask For Company Type.

This can be anything from partial match:

ltd

or full terms

car+wash

Notice all spaces replaced with +


This will search yell.com for all results for all the postcode districts withing the UK for the specified search term.

Only single user-agent set  and 30 second interval between post district.

***Future Plans

Increase anti-scrape detection
      for proxy in proxies
        for userAgent in userAgents
         ....

that sort of thing
***
