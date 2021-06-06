"""Tests."""
import unittest
import gig_server


class TestGigServer(unittest.TestCase):
    """Tests."""

    def test_status(self):
        """Test."""
        status = gig_server.status()
        self.assertIn('server', status)

    def test_entities(self):
        """Test."""
        entities = gig_server.entities('LK')
        self.assertIn('LK', entities)

    def test_entity_ids(self):
        """Test."""
        province_ids = gig_server.entity_ids('province')['entity_ids']
        self.assertIn('LK-1', province_ids)

    def test_nearby(self):
        """Test."""
        nearby = gig_server.nearby('8,80')
        self.assertIn('nearby_entity_info_list', nearby)

    def test_ext_data(self):
        """Test."""
        ext_data = gig_server.ext_data('census', 'total_population', 'LK')
        self.assertIn('LK', ext_data)


if __name__ == '__main__':
    unittest.main()
