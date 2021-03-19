 #!/usr/bin/env python
"""This script is purely for testing purposes and will not form a part of the final product"""

import PySkiylia

import unittests

class TestMethods(unittests.TestCase):
    def test_add(self):
        self.assertEqual(PySkiylia.test(), "Completed")

if __name__ == "__main__":
    unittests.main()
