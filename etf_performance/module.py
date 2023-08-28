from datetime import datetime, timedelta
from typing import Tuple

import holidays

from constants import NEGATIVE_ANSWERS, POSITIVE_ANSWERS


class BusinessDay:
    @staticmethod
    def next(dt: datetime) -> datetime:
        """
        Calculate the next business day relative to the given date.

        Parameters:
            dt (datetime): The input datetime object.

        Return:
            datetime: The next business day.
        """

        while dt.weekday() in holidays.WEEKEND or dt.date() in holidays.US():
            dt += timedelta(days=1)
        return dt

    @staticmethod
    def previous(dt: datetime) -> datetime:
        """
        Calculate the previous business day relative to the given date.

        Parameters:
            dt (datetime): The date to calculate the previous date from.

        Returns:
            datetime: The previous non-weekend and non-holiday date.
        """
        while dt.weekday() in holidays.WEEKEND or dt.date() in holidays.US():
            dt -= timedelta(days=1)
        return dt


class Period:
    @staticmethod
    def period_analyzed() -> Tuple[datetime, datetime]:
        """
        Analyze the period for performance.

        Return:
            tuple: A tuple containing the start date and end date of the analyzed period.

        Raise:
            ValueError: If the user inputs an invalid date format.

        """
        while True:
            try:
                performance_ytd = str(input('Performance YTD: (Y/N) ')).lower()
                try:
                    if performance_ytd in POSITIVE_ANSWERS:
                        start_date = datetime(
                            datetime.today().year, 1, 1
                        ).date()
                        end_date = datetime.today().date()
                        return start_date, end_date
                    else:
                        if performance_ytd in NEGATIVE_ANSWERS:
                            start_date = datetime.strptime(
                                input('Start date (dd/mm/yyyy): '), '%d/%m/%Y'
                            ).date()
                            end_date = datetime.strptime(
                                input('End date (dd/mm/yyyy): '), '%d/%m/%Y'
                            ).date()
                            if start_date < end_date:
                                return start_date, end_date
                            else:
                                print(
                                    'End date must be later than the start date.'
                                )
                except ValueError:
                    print('Invalid date format. It should be dd/mm/yyyy.')
            except ValueError:
                print('Invalid input format!')
