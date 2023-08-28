# ETF Performance Analyzer

A tool to analyze the performance of various ETFs based on historical data.

![image](https://github.com/rodrigofmcarvalho/etf_performance/assets/96849660/b492fec8-58cb-4e99-969e-1f454403e29b)

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Configuration](#configuration)
    - [Constants](#constants)
- [Component Description](#component-description)
- [Contributing](#contributing)
- [License](#license)

## Features

- Retrieve a list of US ETFs based on user input.
- Analyze the performance of ETFs over a specified period.
- Calculate and display the best performing funds.
- Visualize ETF performance with plots.

## Prerequisites

- Python 3.10+
- Poetry for dependency management.

## Usage

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd etf_performance
   ```

2. Install Poetry if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install the required packages using Poetry:
   ```bash
   poetry install
   ```

4. Run the main script using Poetry:
   ```bash
   poetry run python main.py
   ```

## Configuration

Make sure to update the constant.py file according to your needs.

### Constants

- `ETF_FILE_PATH`: Path to the file containing the list of ETFs.
- `POSITIVE_ANSWERS`: Acceptable positive answers.
- `NEGATIVE_ANSWERS`: Acceptable negative answers.
- `OPEN_FILE_ANSWERS`: Acceptable answers for opening a file.
- `WRITE_ANSWERS`: Acceptable answers for writing the list of ETFs.

## Component Description

- **BusinessDay**: Class to calculate the next and previous business days.
- **Period**: Class to determine the period for performance.
- **get_us_etfs**: Function to retrieve a list of US ETFs.
- **validate_file**: Function to validate and read the ETF file.
- **get_etf_historical_data**: Function to retrieve historical data for a specific ETF.
- **process_etfs**: Function to generate historical data for a list of ETFs.
- **plot_etf_performance**: Function to plot ETF performance.
- **normalize_etf_data**: Function to normalize ETF data.
- **get_best_funds_data**: Function to calculate the best funds data.

## Contributing

1. Fork the repository.
2. Create a new branch for your features or bug fixes.
3. Commit your changes and push to your fork.
4. Open a pull request from your fork to the main repository.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Autor

Rodrigo Carvalho
