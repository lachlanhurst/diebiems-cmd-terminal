#
# Unit tests
#

import unittest

from dbmscommand.interface import _parse_cellslikeresponse

cellsresponse = """-----   Cell voltages   -----
Cell voltage 0           : 3.381V
Cell voltage 1           : 3.385V
Cell voltage 2           : 3.387V
Cell voltage 3           : 3.382V
Cell voltage 4           : 3.385V
Cell voltage 5           : 3.382V
Cell voltage 6           : 3.387V
Cell voltage 7           : 3.385V
Cell voltage 8           : 3.385V
Cell voltage 9           : 3.387V
Cell voltage10           : 3.385V
Cell voltage11           : 3.382V
Cell voltage high       : 3.387V
Cell voltage low        : 3.381V
Cell voltage average  : 3.385V
Cell voltage mismatch : 0.006V
----- End Cell voltages -----"""

statusresponse = """-----Battery Pack Status-----
Pack voltage          : 40.59V
Pack current          : 2.35A
State of charge       : 77.8%
Remaining capacity    : 3.74Ah
Operational state     : Charging
Load voltage          : 0.00V
Cell voltage high     : 3.388V
Cell voltage low      : 3.381V
Cell voltage average  : 3.385V
Cell voltage mismatch : 0.007V
Discharge enabled     : False
Charge enabled        : True
---End Battery Pack Status---"""


class InterfaceTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_cells_response(self):
        parseddata = _parse_cellslikeresponse(cellsresponse)

        cell0label, cell0voltage = parseddata[0]
        assert cell0label == "Cell voltage 0"
        assert cell0voltage == "3.381"

        cell5label, cell5voltage = parseddata[5]
        assert cell5label == "Cell voltage 5"
        assert cell5voltage == "3.382"

    def test_parse_status_response(self):
        parseddata = _parse_cellslikeresponse(statusresponse)

        packvoltagelabel, packvoltage = parseddata[0]
        assert packvoltagelabel == "Pack voltage"
        assert packvoltage == "40.59"

        # Remaining capacity    : 3.74Ah
        rclabel, rc = parseddata[3]
        assert rclabel == "Remaining capacity"
        assert rc == "3.74"

        opstatelabel, opstate = parseddata[4]
        assert opstatelabel == "Operational state"
        assert opstate == "Charging"


if __name__ == "__main__":
    unittest.main() # run all tests
