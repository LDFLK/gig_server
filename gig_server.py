"""GIGServer."""
import logging
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from waitress import serve

from utils.sysx import log_metrics
import gig.ents
import gig.nearby
import gig.ext_data

DEFAULT_CACHE_TIMEOUT = 120
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

# ----------------------------------------------------------------
# Handlers
# ----------------------------------------------------------------


@app.route('/status')
@cache.cached(timeout=DEFAULT_CACHE_TIMEOUT)
def status():
    """Index."""
    data = log_metrics()
    data['server'] = 'gig_server'
    return data


@app.route('/entities/<string:entity_ids_str>')
@cache.cached(timeout=DEFAULT_CACHE_TIMEOUT)
def entities(entity_ids_str):
    """Get entity."""
    _entity_ids = entity_ids_str.split(';')
    return gig.ents.multiget_entities(_entity_ids)


@app.route('/entity_ids/<string:entity_type>')
@cache.cached(timeout=DEFAULT_CACHE_TIMEOUT)
def entity_ids(entity_type):
    """Get entity IDs."""
    return {
        'entity_ids': gig.ents.get_entity_ids(entity_type),
    }


@app.route('/nearby/<string:latlng_str>')
@cache.cached(timeout=DEFAULT_CACHE_TIMEOUT)
def nearby(latlng_str):
    """Get places near latlng."""
    lat, _, lng = latlng_str.partition(',')
    lat_lng = (float)(lat), (float)(lng)
    return {
        'nearby_entity_info_list': gig.nearby.get_nearby_entities(lat_lng),
    }


@app.route(
    '/ext_data/<string:data_group>/<string:table_id>/<string:entity_id>'
)
@cache.cached(timeout=DEFAULT_CACHE_TIMEOUT)
def ext_data(data_group, table_id, entity_id):
    """Get extended data."""
    return gig.ext_data.get_table_data(data_group, table_id, [entity_id])


if __name__ == '__main__':
    PORT = 4001
    HOST = '0.0.0.0'
    logging.info('Starting gig_server on %s:%d...', HOST, PORT)
    serve(
        app,
        host=HOST,
        port=PORT,
        threads=8,
    )
