from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from Mastermind import Mastermind
from itertools import product

class TestMastermindInit(TestCase):
    def test_default_init_for_r_4_t_6(self):
        r = 4
        t = 6
        m = Mastermind(r, t)
        self.assertEqual(m.r, r)
        self.assertEqual(m.t, t)
        self.assertEqual(m.guess, tuple(range(0, r)))
        self.assertEqual(m.resRange, {x for x in product(range(0, r+1), repeat=2) if x[1] <= x[0]})

    def test_default_init_for_r_5_t_10(self):
        r = 5
        t = 10
        m = Mastermind(r, t)
        self.assertEqual(m.r, r)
        self.assertEqual(m.t, t)
        self.assertEqual(m.guess, tuple(range(0, r)))
        self.assertEqual(m.resRange, {x for x in product(range(0, r+1), repeat=2) if x[1] <= x[0]})

class TestNextGuess(TestCase):
    def test_next_guess(self):
        with patch('Mastermind.Mastermind') as mock:
            m = mock.return_value
            m.guess = (0,1,2,3)
            self.assertEqual(m.nextGuess, m.guess)
    
# class TestGenTable(TestCase):
#     def test_default_full_for_r_4_t_6(self):
        
        
        
if __name__=="__main__":
    main()
