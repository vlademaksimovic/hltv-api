import os
import logging
from flask import Flask, abort, jsonify, make_response

from src import requester, rankings, results

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

is_production = bool(os.environ.get('IS_PRODUCTION', default=False))


@app.errorhandler(500)
@app.errorhandler(503)
def _handle_error(error):
    return make_response(jsonify({
        'error_msg': error.description,
        'error_code': str(error.code),
    }), error.code)


@app.route('/v1/rankings', methods=['GET'])
def _rankings():
    fetched_rankings = rankings.get(requester)

    if not fetched_rankings:
        abort(503)

    return jsonify({
        'ranking': fetched_rankings,
        'count': str(len(fetched_rankings)),
    })


@app.route('/v1/results', methods=['GET'])
def _results():
    fetched_results = results.get(requester)

    if not fetched_results:
        abort(503)

    return jsonify({
        'results': fetched_results,
        'count': str(len(fetched_results)),
    })


if __name__ == '__main__':
    app.run(debug=not is_production)
