import os
import logging
import datetime
from flask import Flask, jsonify, make_response, request, send_from_directory

from src.utils import \
    get_count, \
    get_milliseconds_delta

from src import \
    requester, \
    rankings, \
    results, \
    matches, \
    news, \
    stats, \
    metrics

STATIC_FOLDER = 'src/resources'
app = Flask(__name__, static_folder=STATIC_FOLDER)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

is_production = bool(os.environ.get('IS_PRODUCTION', default=False))


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(502)
def _handle_error(error):
    metrics.log('errors.count', 'counter', 1)
    metrics.log('errors.code', 'code', int(error.code))
    return make_response(jsonify({
        'error_msg': error.description,
        'error_code': int(error.code),
    }), error.code)


@app.route('/v1/rankings', methods=['GET'])
def _rankings():
    start = datetime.datetime.now()

    limit = request.args.get('limit')
    fetched_rankings = rankings.get(requester, limit)

    delta = get_milliseconds_delta(start, end=datetime.datetime.now())
    metrics.log('rankings.latency', 'milliseconds', delta)
    metrics.log('rankings.count', 'counter', 1)

    return jsonify({
        'rankings': fetched_rankings,
        'count': len(fetched_rankings),
    })


@app.route('/v1/results', methods=['GET'])
def _results():
    start = datetime.datetime.now()

    limit = request.args.get('limit')
    offset = request.args.get('offset')
    fetched_results = results.get(requester, limit, offset)

    delta = get_milliseconds_delta(start, end=datetime.datetime.now())
    metrics.log('results.latency', 'milliseconds', delta)
    metrics.log('results.count', 'counter', 1)

    return jsonify({
        'results': fetched_results,
        'count': len(fetched_results),
    })


@app.route('/v1/matches', methods=['GET'])
def _matches():
    start = datetime.datetime.now()

    limit = request.args.get('limit')
    filter = request.args.get('filter')
    fetched_results = matches.get(requester, filter, limit)

    upcoming_count = get_count(fetched_results.get('upcoming'))
    live_count = get_count(fetched_results.get('live'))

    delta = get_milliseconds_delta(start, end=datetime.datetime.now())
    metrics.log('matches.latency', 'milliseconds', delta)
    metrics.log('matches.count', 'counter', 1)

    return jsonify({
        'matches': fetched_results,
        'count': (upcoming_count + live_count),
    })


@app.route('/v1/news', methods=['GET'])
def _news():
    start = datetime.datetime.now()

    limit = request.args.get('limit')
    year = request.args.get('year')
    month = request.args.get('month')
    fetched_results = news.get(requester, limit, year, month)

    delta = get_milliseconds_delta(start, end=datetime.datetime.now())
    metrics.log('news.latency', 'milliseconds', delta)
    metrics.log('news.count', 'counter', 1)

    return jsonify({
        'news': fetched_results,
        'count': len(fetched_results),
    })


@app.route('/v1/stats', methods=['GET'])
def _stats():
    start = datetime.datetime.now()

    limit = request.args.get('limit')
    type = request.args.get('type')
    fetched_results = stats.get(requester, limit, type)

    players_count = get_count(fetched_results.get('players'))
    teams_count = get_count(fetched_results.get('teams'))

    delta = get_milliseconds_delta(start, end=datetime.datetime.now())
    metrics.log('stats.latency', 'milliseconds', delta)
    metrics.log('stats.count', 'counter', 1)

    return jsonify({
        'stats': fetched_results,
        'count': (players_count + teams_count),
    })


@app.route('/', methods=['GET'])
def _index():
    return jsonify({
        'author': 'Simon Egersand',
        'author_url': 'https://github.com/simeg',
        'base_url': 'http://hltv-api.herokuapp.com',
        'project_name': 'HLTV API',
        'project_url': 'https://github.com/simeg/hltv-api',
        'latest_version': 1,
    })


@app.route('/robots.txt', methods=['GET'])
@app.route('/sitemap.xml', methods=['GET'])
def _robots():
    return send_from_directory(app.static_folder, request.path[1:])


if __name__ == '__main__':
    # Flask server is only used during development
    if not is_production:
        app.run(debug=True, host='0.0.0.0', port=8000)
