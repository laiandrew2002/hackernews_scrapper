import requests
from bs4 import BeautifulSoup
import pprint

# res = requests.get("https://news.ycombinator.com/news")
# soup = BeautifulSoup(res.text, "html.parser")
# links = soup.select(".storylink")
# # votes = soup.select(".score")
# subtext = soup.select(".subtext")

def hackernews_five_page_url():
  hackernewsUrlP1 = "https://news.ycombinator.com/news"
  hackernewsList = [hackernewsUrlP1]
  for i in range(4):
    hackernewsPage = hackernewsUrlP1 + f"?p={i+2}"
    hackernewsList.append(hackernewsPage)
  return hackernewsList


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


if __name__ == "__main__":
  hackernews_page_list = hackernews_five_page_url()
  # loop the page url and pass into hackernews_scrapping and then unpack them
  finalNewsList = [news for url in hackernews_page_list for news in hackernews_scrapping(url)]
  sortedNews = sort_stories_by_votes(finalNewsList)
  pprint.pprint(sortedNews)
