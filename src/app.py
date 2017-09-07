import os
import logging
from flask import Flask, abort, jsonify, make_response, request

from src import \
    requester, \
    rankings, \
    results, \
    matches

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

is_production = bool(os.environ.get('IS_PRODUCTION', default=False))


@app.errorhandler(500)
@app.errorhandler(502)
def _handle_error(error):
    return make_response(jsonify({
        'error_msg': error.description,
        'error_code': str(error.code),
    }), error.code)


@app.route('/v1/rankings', methods=['GET'])
def _rankings():
    fetched_rankings = rankings.get(requester)

    if not fetched_rankings:
        abort(502)

    return jsonify({
        'ranking': fetched_rankings,
        'count': str(len(fetched_rankings)),
    })


@app.route('/v1/results', methods=['GET'])
def _results():
    fetched_results = results.get(requester)

    if not fetched_results:
        abort(502)

    return jsonify({
        'results': fetched_results,
        'count': str(len(fetched_results)),
    })


@app.route('/v1/matches', methods=['GET'])
def _matches():
    match_filter = request.args.get('filter')
    fetched_results = matches.get(requester, match_filter)

    if not fetched_results:
        abort(502)  # Bad gateway

    return jsonify({
        'matches': fetched_results,
        'count': len(fetched_results),
    })


if __name__ == '__main__':
    app.run(debug=not is_production)
