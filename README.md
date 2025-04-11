# Space Exploration Missions Analyzer

A Python tool for analyzing space exploration missions from 1970-1999.

## Features

- Filter missions by prime number years
- Filter missions by years divisible by a specified number
- Filter by mission type, participating countries, success status, and scientific impact
- Generate summary statistics about filtered data
- Create visualizations of mission success rates by year

## Requirements

- Python 3.6+
- Required packages:
  - matplotlib
  - pytest (for running tests)

You can install the required packages using:

```bash
pip install matplotlib pytest
```

## Dataset

The project includes a dataset (`data.csv`) containing information about space exploration missions from 1970 to 1999. Each mission includes:

- Year
- Mission name
- Mission type (Lunar, Mars, Venus, etc.)
- Success status (boolean)
- Participating countries
- Scientific impact score (0-10)

## Usage

### Basic Usage

```bash
python analyze.py
```

This will display all missions in the dataset.

### Command-Line Arguments

The script supports several command-line arguments for filtering and analyzing the data:

- `-p, --prime`: Filter by prime number years
- `-a N, --divisible-by N`: Filter by years divisible by N
- `-t TYPE, --type TYPE`: Filter by mission type
- `-c COUNTRY, --country COUNTRY`: Filter by participating country
- `-s {true,false}, --success {true,false}`: Filter by success status
- `-i IMPACT, --impact IMPACT`: Filter by minimum scientific impact score
- `--summary`: Show summary statistics for the filtered results
- `--plot`: Generate a bar chart showing mission success rates by year
- `--plot-file FILENAME`: Save the plot to the specified file instead of displaying it
- `--data FILEPATH`: Specify a different data file to load (default: data.csv)

### Examples

Display only missions from prime number years:

```bash
python analyze.py --prime
```

Display missions from years divisible by 5:

```bash
python analyze.py -a 5
```

Display successful Mars missions:

```bash
python analyze.py -t Mars -s true
```

Display USSR missions with a scientific impact of at least 7:

```bash
python analyze.py -c USSR -i 7
```

Show all missions with summary statistics:

```bash
python analyze.py --summary
```

Generate a plot of mission success rates:

```bash
python analyze.py --plot
```

Combine multiple filters:

```bash
python analyze.py --prime -c USA --summary --plot
```

## Running Tests

To run the test suite:

```bash
pytest test_analyze.py
```

Or alternatively:

```bash
python test_analyze.py
``` 