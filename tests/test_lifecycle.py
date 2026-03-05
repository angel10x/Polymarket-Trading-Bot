import pytest
from unittest import TestCase
from unittest.mock import MagicMock

from poly_market_maker.lifecycle import Lifecycle


class TestLifecycle(TestCase):
    def setUp(self):
        self.counter = 0

    def test_init_lifecycle(self):
        lc = Lifecycle()

        def side_effect():
            self.counter += 1
            if self.counter >= 2:
                lifecycle.terminate()

        startup = MagicMock()
        callback = MagicMock(side_effect=side_effect)
        shutdown = MagicMock()

        with pytest.raises(SystemExit):
            with lc as lifecycle:
                lifecycle.on_startup(startup)
                lc.every(0.1, callback)
                lc.on_shutdown(shutdown)

        # assert relevant functions were called
        self.assertEqual(startup.call_count, 1)
        self.assertEqual(callback.call_count, 2)
        self.assertEqual(shutdown.call_count, 1)

        # assert state changes
        self.assertTrue(lc.terminated_internally)
        self.assertEqual(self.counter, 2)

    pass
