import requests
from bs4 import BeautifulSoup
import pprint

hackernewsUrlP1 = "https://news.ycombinator.com/news"
hackernewsUrlP2 = hackernewsUrlP1 + "?p=2"
# res = requests.get("https://news.ycombinator.com/news")
# soup = BeautifulSoup(res.text, "html.parser")
# links = soup.select(".storylink")
# # votes = soup.select(".score")
# subtext = soup.select(".subtext")

def sort_stories_by_votes(hnlist):
  return sorted(hnlist, key=lambda k: k["votes"], reverse=True)


def create_custom_hn(links, subtext):
  hn = []
  for ind, item in enumerate(links):
    title = item.getText()
    href = item.get("href", None)
    vote = subtext[ind].select(".score")
    if len(vote):
      point = int(vote[0].getText().replace(" points", ""))
      if point > 99:
        hn.append({
          "title": title,
          "link": href,
          "votes": point
        })
  return hn


def hackernews_scrapping(url):
  res = requests.get(url)
  soup = BeautifulSoup(res.text, "html.parser")
  links = soup.select(".storylink")
  subtext = soup.select(".subtext")

  news = create_custom_hn(links, subtext)
  return news

newslist1 = hackernews_scrapping(hackernewsUrlP1)
newslist2 = hackernews_scrapping(hackernewsUrlP2)
sortedNews = sort_stories_by_votes(newslist1 + newslist2)

pprint.pprint(sortedNews)