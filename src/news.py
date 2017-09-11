import logging
from flask import abort

from src.utils import \
    sanity_check_integer, \
    get_tags, \
    get_text, \
    get_tag, \
    extract_digits

logger = logging.getLogger(__name__)

URL = 'https://www.hltv.org'


def get(requester, limit=None, year=None, month=None):
    sanity_check_integer(limit, 'limit')
    sanity_check_integer(year, 'year')
    sanity_check_integer(month, 'month')

    if limit is None:
        limit = 0

    parsed_content = requester.request(URL)
    news_items = parsed_content.find_all(
        'a', attrs={'class': 'newsline'}, limit=int(limit))
    news_urls = get_tags(parsed_content, 'a.newsline')

    if len(news_items) == 0 or len(news_urls) == 0:
        abort(502)  # Bad gateway

    return list(map(_parse_news_item, news_items, news_urls))


def _parse_news_item(news_item, news_url):
    try:
        title = get_text(news_item, 'div.newstext')
        url = URL + news_url.get('href')

        country = get_tag(news_item, 'img.newsflag.flag')
        country = country.get('title').lower()

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
