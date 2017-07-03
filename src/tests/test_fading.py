import unittest
import numpy as np

from channel.fading import Fading


class FadingTest(unittest.TestCase):
    def setUp(self):
        doppler_freq = 100
        m = 10
        k = 2
        time = 1e-3
        self.fading = Fading(doppler_freq, m, k, time)

    def test_fading(self):
        # Error margin
        error = 1e-5
        signal_in = np.array([0-1j, 1+0j, 0+1j, -1+0j])
        signal_faded = self.fading.propagate(signal_in)
        self.assertFalse(np.allclose(np.real(signal_in), np.real(signal_faded), atol=error))
        self.assertFalse(np.allclose(np.imag(signal_in), np.imag(signal_faded), atol=error))
        signal_after_remove_fading = signal_faded/self.fading.get_fading()
        self.assertTrue(np.allclose(np.real(signal_in), np.real(signal_after_remove_fading), atol=error))
        self.assertTrue(np.allclose(np.imag(signal_in), np.imag(signal_after_remove_fading), atol=error))

if __name__ == '__main__':
    unittest.main()
