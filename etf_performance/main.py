import logging
import sys
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

from constants import ETF_FILE_PATH, OPEN_FILE_ANSWERS, WRITE_ANSWERS
from module import Period

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.ERROR)


def get_us_etfs() -> List[str]:
    """
    Retrieve a list of US ETFs based on the user's input method.

    Return:
        List[str]: A list of US ETF tickers.
    """
    while True:
        input_method = input(
            'Do you want to open an file or write the list of ETFs? (F/W) '
        )
        if input_method in OPEN_FILE_ANSWERS:
            try:
                tickers = validate_file()
                tickers = list(set(tickers))
                tickers.sort()
                return tickers
            except FileNotFoundError:
                print('Error: File not found!')
                break
        elif input_method in WRITE_ANSWERS:
            tickers = [
                ticker.strip().upper()
                for ticker in input(
                    'Insert the list of ETFs separated by commas: '
                ).split(',')
            ]
            tickers = list(set(tickers))
            tickers.sort()
            return tickers
        else:
            print('Invalid input format!')
            break


def validate_file() -> List[str]:
    """
    Read the contents of a file located at `ETF_FILE_PATH` and returns a list of tickers.

    Return:
    List[str]: A list of tickers read from the file.
    """
    with open(ETF_FILE_PATH, 'r') as file:
        tickers = [line.strip() for line in file.readlines()]
        return tickers


def get_etf_historical_data(
    ticker: str, start_date: str, end_date: str
) -> pd.Series:
    """
    Retrieve historical data for a specific ETF.

    Parameters:
        ticker (str): The ticker symbol of the ETF.
        start_date (str): The start date of the historical data in the format "YYYY-MM-DD".
        end_date (str): The end date of the historical data in the format "YYYY-MM-DD".

    Return:
        pandas.Series: The closing prices of the ETF for the specified date range.

    Raise:
        Exception: If there is an error retrieving the data.
    """
    try:
        return yf.download(
            ticker, start=start_date, end=end_date, progress=False
        )['Close']
    except Exception as e:
        if 'No timezone found, symbol may be delisted' in str(e):
            raise Exception(
                f'Failed to download data for {ticker}. The symbol may be delisted.'
            )
        else:
            raise Exception(
                f'Failed to download data for {ticker}. Reason: {e}'
            )


def process_etfs(
    tickers: List[str], start_date: str, end_date: str
) -> pd.DataFrame:
    """
    Generate historical data for a list of ETFs.

    Parameters:
        tickers (list): A list of ticker symbols for the ETFs.
        start_date (str): The start date for the historical data in the format 'YYYY-MM-DD'.
        end_date (str): The end date for the historical data in the format 'YYYY-MM-DD'.

    Return:
        pd.DataFrame: A DataFrame containing the historical data for the ETFs.
    """
    etf_historical_data = pd.DataFrame(
        index=pd.date_range(start=start_date, end=end_date, freq='D')
    )
    tickers_not_found = []
    for ticker in tickers:
        try:
            etf_historical_data[ticker] = get_etf_historical_data(
                ticker, start_date, end_date
            )
        except Exception:
            tickers_not_found.append(ticker)
    return etf_historical_data


def plot_etf_performance(data: pd.DataFrame) -> None:
    """
    Plot the performance of an ETF based on the given data.

    Parameters:
        data (pd.DataFrame): The data containing the performance of the ETF.

    Return:
        None
    """
    plt.plot(data)
    plt.legend(data.columns, loc='upper left')
    plt.ylabel('Performance(%)')
    plt.xticks(rotation=45)

    for column in data.columns:
        x = data.index[-1]
        y = data[column].iloc[-1]
        plt.scatter(x, y, color='blue' if y >= 0 else 'red')
        plt.annotate(
            f'{y:.2f}%',
            (x, y),
            textcoords='offset points',
            xytext=(0, 10),
            ha='center',
        )

    plt.gca().yaxis.set_major_formatter(
        plt.matplotlib.ticker.PercentFormatter()
    )
    plt.tight_layout()
    plt.show()


def normalize_etf_data(
    etf_historical_data: pd.DataFrame,
) -> Optional[pd.DataFrame]:
    """
    Calculate the normalized ETF data.

    Parameters:
        etf_historical_data (pd.DataFrame): The historical data for the ETF.

    Return:
        Optional[pd.DataFrame]: The normalized ETF data, or None if no valid data is found.
    """
    if etf_historical_data.empty:
        print('No valid ETF data found. Exiting.')
        return None
    return etf_historical_data / etf_historical_data.iloc[0]


def get_best_funds_data(
    etf_historical_data_normalized: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Calculate the best funds data based on the given ETF historical data.

    Parameters:
        etf_historical_data_normalized (pd.DataFrame): A normalized DataFrame containing the ETF historical data.

    Return:
        Tuple[pd.DataFrame, pd.DataFrame]: A tuple containing two DataFrames:
            - best_funds: A DataFrame containing the performance (%) of the best funds.
            - best_funds_historical_data: A DataFrame containing the historical data of the best funds.
    """
    best_funds = pd.DataFrame()
    best_funds['Performance(%)'] = (
        etf_historical_data_normalized.iloc[-1].sort_values(ascending=False)
        - 1
    ) * 100
    best_funds = best_funds.round(1)
    best_funds_historical_data = etf_historical_data_normalized.loc[
        :, etf_historical_data_normalized.columns.isin(list(best_funds.index))
    ]
    return best_funds, (best_funds_historical_data - 1) * 100


def main():
    tickers = get_us_etfs()
    start_date, end_date = Period.period_analyzed()
    etf_historical_data = process_etfs(tickers, start_date, end_date)
    etf_historical_data.dropna(axis='index', how='all', inplace=True)
    etf_historical_data.dropna(axis='columns', how='all', inplace=True)

    etf_historical_data_normalized = normalize_etf_data(etf_historical_data)

    if etf_historical_data_normalized is not None:
        best_funds, best_funds_historical_data = get_best_funds_data(
            etf_historical_data_normalized
        )
        print(best_funds)
        plot_etf_performance(best_funds_historical_data)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n\nGracefully exiting application...\n\n\n')
        sys.exit(0)
