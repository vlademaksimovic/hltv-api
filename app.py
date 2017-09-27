import os
import logging
from flask import Flask, jsonify, make_response, request

from src import \
    requester, \
    rankings, \
    results, \
    matches, \
    news

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
    limit = request.args.get('limit')
    fetched_rankings = rankings.get(requester, limit)

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
    match_filter = request.args.get('filter')
    fetched_results = matches.get(requester, match_filter, limit)

    upcoming_matches_count = len(fetched_results.get('upcoming')) \
        if fetched_results.get('upcoming') else 0
    live_matches_count = len(fetched_results.get('live')) \
        if fetched_results.get('live') else 0

    return jsonify({
        'matches': fetched_results,
        'count': (upcoming_matches_count + live_matches_count),
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


if __name__ == '__main__':
    # Flask server is only used during development
    if not is_production:
        app.run(debug=True, host='0.0.0.0', port=8000)
