from biztest.interface.cmdb.cmdb_interface import monitor_check
import pytest


class TestCmdbInit:
    @pytest.mark.cmdb
    def test_cmdb_init(self):
        monitor_check()
