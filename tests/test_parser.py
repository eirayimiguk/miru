import unittest

from miru.parser import Parser

class TestParser(unittest.TestCase):
    def test_novelai_diffusion_1(self):
        filename = "ocean, forest, mountain s-00001"
        expected_1 = "s-00001"
        expected_2 = [
            {"name": "ocean"},
            {"name": "forest"},
            {"name": "mountain"},
            {"name": "miru-parsed"}
        ]
        actual_1, actual_2 = Parser.novelai_diffusion(filename)
        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)

    def test_novelai_diffusion_2(self):
        filename = "{{{ocean}}}, (((forest))), mountain s-00001"
        expected_1 = "s-00001"
        expected_2 = [
            {"name": "ocean"},
            {"name": "forest"},
            {"name": "mountain"},
            {"name": "miru-parsed"}
        ]
        actual_1, actual_2 = Parser.novelai_diffusion(filename)
        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)

    def test_novelai_diffusion_3(self):
        filename = "{{{ocean}}},   (((forest))),   mountain,   s-00001"
        expected_1 = "s-00001"
        expected_2 = [
            {"name": "ocean"},
            {"name": "forest"},
            {"name": "mountain"},
            {"name": "miru-parsed"}
        ]
        actual_1, actual_2 = Parser.novelai_diffusion(filename)
        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)

    def test_novelai_diffusion_4(self):
        filename = "{{{ocean}}},   (((forest))),   mountain,  blue sky  s-00001"
        expected_1 = "s-00001"
        expected_2 = [
            {"name": "ocean"},
            {"name": "forest"},
            {"name": "mountain"},
            {"name": "blue sky"},
            {"name": "miru-parsed"}
        ]
        actual_1, actual_2 = Parser.novelai_diffusion(filename)
        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)

    def test_novelai_diffusion_5(self):
        filename = "{{{ocean}}},   (((forest))),   mountain,  blue  sky,    s-00001"
        expected_1 = "s-00001"
        expected_2 = [
            {"name": "ocean"},
            {"name": "forest"},
            {"name": "mountain"},
            {"name": "blue  sky"},
            {"name": "miru-parsed"}
        ]
        actual_1, actual_2 = Parser.novelai_diffusion(filename)
        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)

if __name__ == "__main__":
    unittest.main()
