from PyStrong.HomogenousType import check_container


class TestCheckContainer(unittest.TestCase):
    def test_correct_elements(self):
        """
        Container only has integer values
        """

        __container: list[int] = [
            1, 2, 3, 4, 5, 6, 7
        ]
        _type, status, position = check_container(__container, int)
        self.assertTrue(
            (_type == int) and
            (status == True) and
            (position == -1)
        )

    def test_incorrect_elements(self):
        """
        Container where first element is a `str`
        """
        __container: list[int] = [
            '1', 2, 3, 4, 5, 6, 7
        ]

        _type, status, position = check_container(__container, int)
        self.assertFalse(
            (_type == int) and
            (status == True) and
            (position == -1)
        )
        self.assertTrue(
            (_type == str) and
            (status == False) and
            (position == 0)
        )

    def test_empty(self):
        """
        Check the container if empty
        """

        __container: list[int] = []
        _type, status, position = check_container(__container, int)
        self.assertTrue(
            (_type == int) and
            (status == True) and
            (position == -1)
        )

    def test_non_iterable(self):
        """
        Give a non-container like object
        """

        __container: bool = False
        with self.assertRaises(ValueError):
            _ = check_container(__container, bool)
