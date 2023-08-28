from unittest.mock import patch, mock_open
from etf_performance.main import get_us_etfs


class TestGetUsEtfs:

    # Test that the function retrieves a list of US ETFs when the user chooses to open a file and the file exists
    def test_open_file_exists(self):
        # Mock the input method to simulate user choosing to open a file
        with patch('builtins.input', return_value='F'):
            # Mock the validate_file function to return a list of tickers
            with patch('main.validate_file', return_value=['EWZ', 'IWM', 'QQQ', 'SPY', 'XLF']):
                # Call the function under test
                result = get_us_etfs()
    
        # Assert that the result is the expected list of tickers
        assert result == ['EWZ', 'IWM', 'QQQ', 'SPY', 'XLF']

    # Test that the function returns a sorted list of tickers when the user chooses to write the list of ETFs and inputs a valid comma-separated list
    def test_valid_input(self):
        from unittest.mock import patch
        from io import StringIO
        from main import get_us_etfs

        # Mock user input
        with patch('sys.stdout', new=StringIO()) as fake_output, \
             patch('builtins.input', side_effect=['W','EWZ,IWM,QQQ,SPY,XLF']):
        
            expected_output = ['EWZ', 'IWM', 'QQQ', 'SPY', 'XLF']
            result = get_us_etfs()

            assert result == expected_output
            assert fake_output.getvalue() == ''

        # Mock user input with leading/trailing spaces
        with patch('sys.stdout', new=StringIO()) as fake_output, \
             patch('builtins.input', side_effect=['W','  EWZ , IWM , QQQ, SPY , XLF  ']):
        
            expected_output = ['EWZ', 'IWM', 'QQQ', 'SPY', 'XLF']
            result = get_us_etfs()

            assert result == expected_output
            assert fake_output.getvalue() == ''

        # Mock user input with mixed case tickers
        with patch('sys.stdout', new=StringIO()) as fake_output, \
             patch('builtins.input', side_effect=['W', 'ewz,IWM,qqq,SPY,xlf']):
        
            expected_output = ['EWZ', 'IWM', 'QQQ', 'SPY', 'XLF']
            result = get_us_etfs()

            assert result == expected_output
            assert fake_output.getvalue() == ''

   # Test that the function handles a FileNotFoundError when the user chooses to open a file and the file does not exist
    def test_file_not_found(self):
        from unittest.mock import patch
        from io import StringIO
        from main import get_us_etfs

        m = mock_open()
        m.side_effect = FileNotFoundError()

        # Mock user input
        with patch('builtins.open', m), \
            patch('sys.stdout', new=StringIO()) as fake_output, \
            patch('builtins.input', return_value='F'):

            result = get_us_etfs()

            assert result is None
            assert fake_output.getvalue() == 'Error: File not found!\n'

    # Test that the function handles duplicate tickers correctly when the user chooses to write the list of ETFs
    def test_duplicate_tickers(self):
        from unittest.mock import patch
        from io import StringIO
        from main import get_us_etfs

        # Mock user input with duplicate tickers
        with patch('sys.stdout', new=StringIO()) as fake_output, \
             patch('builtins.input', side_effect=['W', 'EWZ,EWZ,IWM,IWM,QQQ,SPY,SPY,XLF']):

            expected_output = ['EWZ', 'IWM', 'QQQ', 'SPY', 'XLF']
            result = get_us_etfs()

            assert result == expected_output
            assert fake_output.getvalue() == ''


    # Test that the function handles invalid input format correctly by displaying an error message and prompting the user again
    def test_invalid_input_format(self):
        from unittest.mock import patch
        from io import StringIO
        from main import get_us_etfs

        # Mock user input with invalid input format
        with patch('sys.stdout', new=StringIO()) as fake_output, \
             patch('builtins.input', return_value='X'):

            result = get_us_etfs()

            assert result is None
            assert fake_output.getvalue() == 'Invalid input format!\n'