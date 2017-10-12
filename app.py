import os
import logging
import datetime
from flask import Flask, jsonify, make_response, request

from src import \
    requester, \
    rankings, \
    results, \
    matches, \
    news, \
    stats, \
    metrics

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

is_production = bool(os.environ.get('IS_PRODUCTION', default=False))


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(502)
def _handle_error(error):
    return make_response(jsonify({
        'error_msg': error.description,
        'error_code': int(error.code),
    }), error.code)


@app.route('/v1/rankings', methods=['GET'])
def _rankings():
    start = datetime.datetime.now()

    limit = request.args.get('limit')
    fetched_rankings = rankings.get(requester, limit)

    delta = _get_milliseconds_delta(start, end=datetime.datetime.now())
    metrics.log('rankings.latency', 'milliseconds', delta)
    metrics.log('rankings.count', 'counter', 1)

    return jsonify({
        'ranking': fetched_rankings,
        'count': len(fetched_rankings),
    })


@app.route('/v1/results', methods=['GET'])
def _results():
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    fetched_results = results.get(requester, limit, offset)

    return jsonify({
        'results': fetched_results,
        'count': len(fetched_results),
    })


@app.route('/v1/matches', methods=['GET'])
def _matches():
    limit = request.args.get('limit')
    filter = request.args.get('filter')
    fetched_results = matches.get(requester, filter, limit)

    upcoming_count = _get_count(fetched_results.get('upcoming'))
    live_count = _get_count(fetched_results.get('live'))

    return jsonify({
        'matches': fetched_results,
        'count': (upcoming_count + live_count),
    })


@app.route('/v1/news', methods=['GET'])
def _news():
    limit = request.args.get('limit')
    year = request.args.get('year')
    month = request.args.get('month')
    fetched_results = news.get(requester, limit, year, month)

    return jsonify({
        'news': fetched_results,
        'count': len(fetched_results),
    })


@app.route('/v1/stats', methods=['GET'])
def _stats():
    limit = request.args.get('limit')
    type = request.args.get('type')
    fetched_results = stats.get(requester, limit, type)

    players_count = _get_count(fetched_results.get('players'))
    teams_count = _get_count(fetched_results.get('teams'))

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


def _get_count(optional_array):
    return len(optional_array) if optional_array else 0


def _get_milliseconds_delta(start, end):
    """Assumes inputs are of type datetime.datetime"""
    return (end - start).microseconds / 1000


if __name__ == '__main__':
    # Flask server is only used during development
    if not is_production:
        app.run(debug=True, host='0.0.0.0', port=8000)
