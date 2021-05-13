"""Test."""
import os
import unittest

from utils import db
from utils.flask import FlaskClient

from gig.ent_types import ENTITY_TYPE

N_SAMPLES = 5


SERVER_NAME, HOST, PORT = None, '127.0.0.1', 5001
# SERVER_NAME, HOST, PORT = 'gig', '0.0.0.0', 8080
# SERVER_NAME, HOST, PORT = 'gig', '18.209.43.63', 80

REGION_ID_SIZE_MAP = {
    'province': 1,
    'district': 2,
    'dsd': 4,
    'gnd': 7,
}


class TestGIGServer(unittest.TestCase):
    """Tests."""

    def setUp(self):
        """Setup."""
        if not SERVER_NAME:
            print('Starting flask...')
            os.system('./local_flask_start.sh &')
        self.__client = FlaskClient(SERVER_NAME, HOST, PORT)

    def tearDown(self):
        """Teardown."""
        if not SERVER_NAME:
            print('Stopping flask...')
            os.system('./local_flask_stop.sh')

    def test_entity(self):
        """Test."""
        entity = self.__client.run('entity', ['LK-11'])
        self.assertEqual(entity['name'], 'Colombo')

    def test_entity_ids(self):
        """Test."""
        entity_ids = self.__client.run('entity_ids', ['province'])\
            .get('entity_ids')
        self.assertEqual(len(entity_ids), 9)

    def test_ext_data(self):
        """Test."""
        entity_ids_map = {}
        for entity_type in ENTITY_TYPE.list():
            response = self.__client.run('entity_ids', [entity_type])
            entity_ids_map[entity_type] = response['entity_ids']

        for entity_type, entity_ids in entity_ids_map.items():
            subset_entity_ids = entity_ids[:N_SAMPLES]
            id_key = db.get_id_key(entity_type)

            for entity_id in subset_entity_ids:
                entity = self.__client.run('entity', [entity_id])
                self.assertEqual(entity[id_key], entity_id)

                if entity_type not in [
                    ENTITY_TYPE.ED,
                    ENTITY_TYPE.PD,
                    ENTITY_TYPE.PS,
                ]:
                    response = self.__client.run(
                        'ext_data',
                        ['census', 'total_population', entity_id],
                    )
                    self.assertTrue(
                        response[entity_id]['total_population'] >= 0,
                    )

    def test_nearby(self):
        """Test."""
        response = self.__client.run(
            'nearby',
            ['6.907560294565226,79.86413013335861'],  # Cinnamon Gaardens PS

        )
        nearby_entity_info_list = response['nearby_entity_info_list']
        first_entity = nearby_entity_info_list[0]['entity']
        self.assertEqual(first_entity['name'], 'Cinnamon Garden')

        # Not in Sri Lanka
        response = self.__client.run('nearby', ['20,70'])
        nearby_entity_info_list = response['nearby_entity_info_list']
        self.assertEqual(nearby_entity_info_list, [])


if __name__ == '__main__':
    unittest.main()
