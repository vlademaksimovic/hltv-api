import logging
from flask import abort
import datetime

from src.utils import \
    get_attr, \
    get_tags, \
    get_text, \
    get_tag, \
    extract_digits, \
    sanity_check_integer, \
    sanity_check_string

logger = logging.getLogger(__name__)

URL = 'https://www.hltv.org'


def get(requester, limit=None, year=None, month=None):
    sanity_check_integer(limit, 'limit')
    sanity_check_integer(year, 'year')
    sanity_check_string(month, 'month')

    request_url = URL

    if year and month:
        year = int(year)
        month = month.lower()
        _sanity_check_year(year)
        _sanity_check_month(month)
        request_url = URL + ('/news/archive/%s/%s' % (year, month))

    if limit is None:
        limit = 0

    parsed_content = requester.request(request_url)
    news_items = parsed_content.find_all(
        'a', attrs={'class': 'newsline'}, limit=int(limit))
    news_urls = get_tags(parsed_content, 'a.newsline')

    if len(news_items) == 0 or len(news_urls) == 0:
        abort(502)  # Bad gateway

    return list(map(_parse_news_item, news_items, news_urls))


def _parse_news_item(news_item, news_url):
    try:
        title = get_text(news_item, 'div.newstext')
        url = URL + get_attr(news_url, 'href')

        country = get_tag(news_item, 'img.newsflag.flag')
        country = get_attr(country, 'title').lower()

        published_at = get_tag(news_item, 'div.newsrecent')
        comments = get_text(published_at.findNext('div'))
        comments = extract_digits(comments)
        published_at = get_text(published_at)

        return {
            'title': title,
            'news_url': url,
            'country': country,
            'published_at': published_at,
            'comments_count': int(comments),
        }

    except Exception:
        logger.error('#### START EXCEPTION ####')
        logger.exception(
            'Unable to parse news item with exception followed by HTML:')
        logger.error(news_item)
        logger.error('#### END EXCEPTION ####')

        abort(500)  # Internal server error


def _sanity_check_year(year):
    current_year = datetime.datetime.now().year
    if year < 2005 or year > current_year:
        abort(400, 'News for year [%i] is not available' % year)  # Bad request


def _sanity_check_month(month):
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
              'august', 'september', 'october', 'november', 'december']
    if month not in months:
        abort(400, 'Month [%s] does not exist' % month)  # Bad request
