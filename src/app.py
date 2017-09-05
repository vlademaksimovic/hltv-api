import os
import logging
from flask import Flask, abort, jsonify
from src import requester, rankings, results

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

is_production = bool(os.environ.get('IS_PRODUCTION', default=False))


@app.route('/v1/rankings', methods=['GET'])
def _rankings():
    fetched_rankings = rankings.get(requester)

    if not fetched_rankings:
        abort(503)

    return jsonify({
        'ranking': fetched_rankings,
        'count': len(fetched_rankings),
    })


@app.route('/v1/results', methods=['GET'])
def _results():
    fetched_results = results.get(requester)

    if not fetched_results:
        abort(503)

    return jsonify({
        'results': fetched_results,
        'count': len(fetched_results),
    })


if __name__ == '__main__':
    app.run(debug=not is_production)
