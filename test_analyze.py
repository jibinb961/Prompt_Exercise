#!/usr/bin/env python3
"""
Unit tests for the Space Exploration Missions Analyzer
"""

import pytest
import os
import tempfile
import csv
from analyze import (
    is_prime,
    is_divisible_by,
    load_data,
    filter_by_prime_years,
    filter_by_divisible_years,
    filter_by_column
)


class TestPrimeFunctions:
    """Test cases for prime number functions."""

    def test_is_prime(self):
        """Test the is_prime function."""
        assert not is_prime(1)
        assert is_prime(2)
        assert is_prime(3)
        assert not is_prime(4)
        assert is_prime(5)
        assert not is_prime(6)
        assert is_prime(7)
        assert not is_prime(8)
        assert not is_prime(9)
        assert not is_prime(10)
        assert is_prime(11)
        assert is_prime(97)
        assert not is_prime(100)
        assert is_prime(1973)
        assert is_prime(1979)
        assert not is_prime(1980)


class TestDivisibilityFunctions:
    """Test cases for divisibility functions."""

    def test_is_divisible_by(self):
        """Test the is_divisible_by function."""
        assert is_divisible_by(10, 2)
        assert is_divisible_by(10, 5)
        assert not is_divisible_by(10, 3)
        assert is_divisible_by(1975, 5)
        assert not is_divisible_by(1979, 2)
        assert is_divisible_by(1980, 4)
        assert is_divisible_by(0, 5)
        
        # Test with edge cases
        with pytest.raises(ZeroDivisionError):
            is_divisible_by(10, 0)


@pytest.fixture
def sample_data_file():
    """Create a temporary sample data file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
        writer = csv.writer(tmp)
        writer.writerow(['year', 'mission_name', 'mission_type', 'success', 'participating_countries', 'scientific_impact'])
        writer.writerow(['1971', 'Mars 1', 'Mars', 'True', 'USSR', '5'])
        writer.writerow(['1972', 'Pioneer 10', 'Jupiter', 'True', 'USA', '8'])
        writer.writerow(['1973', 'Pioneer 11', 'Jupiter', 'True', 'USA', '7'])
        writer.writerow(['1975', 'Viking 1', 'Mars', 'True', 'USA', '9'])
        writer.writerow(['1977', 'Voyager 1', 'Outer Planets', 'True', 'USA', '10'])
        writer.writerow(['1980', 'Test Mission', 'Earth', 'False', 'USSR', '2'])
    
    filename = tmp.name
    yield filename
    # Clean up the temp file
    os.unlink(filename)


class TestDataProcessing:
    """Test cases for data processing functions."""

    def test_load_data(self, sample_data_file):
        """Test loading data from a CSV file."""
        data = load_data(sample_data_file)
        
        assert len(data) == 6
        assert data[0]['year'] == 1971
        assert data[0]['mission_name'] == 'Mars 1'
        assert data[0]['success'] is True
        assert data[0]['scientific_impact'] == 5
        
        assert data[5]['year'] == 1980
        assert data[5]['mission_name'] == 'Test Mission'
        assert data[5]['success'] is False

    def test_filter_by_prime_years(self, sample_data_file):
        """Test filtering data by prime years."""
        data = load_data(sample_data_file)
        filtered = filter_by_prime_years(data)
        
        # Years in the dataset: 1971, 1972, 1973, 1975, 1977, 1980
        # Of these, 1973 is prime (the others are not)
        assert len(filtered) == 1
        assert filtered[0]['year'] == 1973

    def test_filter_by_divisible_years(self, sample_data_file):
        """Test filtering data by years divisible by a number."""
        data = load_data(sample_data_file)
        
        # Years divisible by 2
        filtered = filter_by_divisible_years(data, 2)
        assert len(filtered) == 2
        assert filtered[0]['year'] == 1972
        assert filtered[1]['year'] == 1980
        
        # Years divisible by 5
        filtered = filter_by_divisible_years(data, 5)
        assert len(filtered) == 2  # Both 1975 and 1980 are divisible by 5
        years = [row['year'] for row in filtered]
        assert 1975 in years
        assert 1980 in years

    def test_filter_by_column(self, sample_data_file):
        """Test filtering data by column values."""
        data = load_data(sample_data_file)
        
        # Filter by mission type
        filtered = filter_by_column(data, 'mission_type', 'Mars')
        assert len(filtered) == 2
        assert filtered[0]['mission_name'] == 'Mars 1'
        assert filtered[1]['mission_name'] == 'Viking 1'
        
        # Filter by participating country
        filtered = filter_by_column(data, 'participating_countries', 'USSR')
        assert len(filtered) == 2
        assert filtered[0]['mission_name'] == 'Mars 1'
        assert filtered[1]['mission_name'] == 'Test Mission'
        
        # Filter by success status
        filtered = filter_by_column(data, 'success', 'false')
        assert len(filtered) == 1
        assert filtered[0]['mission_name'] == 'Test Mission'
        
        # Filter by scientific impact
        filtered = filter_by_column(data, 'scientific_impact', '8')
        assert len(filtered) == 3
        mission_names = [row['mission_name'] for row in filtered]
        assert 'Pioneer 10' in mission_names
        assert 'Viking 1' in mission_names
        assert 'Voyager 1' in mission_names


if __name__ == "__main__":
    pytest.main(["-v", __file__]) 