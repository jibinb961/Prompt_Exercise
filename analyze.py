#!/usr/bin/env python3
"""
Space Exploration Missions Analyzer
This script analyzes space exploration missions from 1970-1999.
"""

import argparse
import csv
import math
import sys
from collections import Counter
import matplotlib.pyplot as plt
from pathlib import Path


def is_prime(num):
    """Check if a number is prime."""
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def is_divisible_by(num, divisor):
    """Check if a number is divisible by another number."""
    return num % divisor == 0


def load_data(file_path):
    """Load data from CSV file."""
    try:
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert string values to appropriate types
                row['year'] = int(row['year'])
                row['success'] = row['success'].lower() == 'true'
                row['scientific_impact'] = int(row['scientific_impact'])
                data.append(row)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)


def filter_by_prime_years(data):
    """Filter data to include only missions from prime number years."""
    return [row for row in data if is_prime(row['year'])]


def filter_by_divisible_years(data, divisor):
    """Filter data to include only missions from years divisible by divisor."""
    return [row for row in data if is_divisible_by(row['year'], divisor)]


def filter_by_column(data, column, value):
    """Filter data based on a column's value."""
    if column not in data[0].keys():
        print(f"Error: Column '{column}' not found in data.")
        return data
    
    # Handle different types of columns
    if column == 'success':
        value = value.lower() == 'true'
        return [row for row in data if row[column] == value]
    elif column == 'scientific_impact':
        try:
            threshold = int(value)
            return [row for row in data if row[column] >= threshold]
        except ValueError:
            print("Error: Scientific impact must be a number.")
            return data
    else:
        return [row for row in data if value.lower() in row[column].lower()]


def display_results(data, show_summary=False):
    """Display filtered results in a formatted way."""
    if not data:
        print("No missions match the specified criteria.")
        return

    # Print header
    print("\n{:<6} {:<25} {:<15} {:<8} {:<20} {:<10}".format(
        "Year", "Mission", "Type", "Success", "Countries", "Impact"
    ))
    print("-" * 85)

    # Print data rows
    for row in data:
        print("{:<6} {:<25} {:<15} {:<8} {:<20} {:<10}".format(
            row['year'],
            row['mission_name'],
            row['mission_type'],
            "✓" if row['success'] else "✗",
            row['participating_countries'],
            row['scientific_impact']
        ))
    
    # Show summary statistics if requested
    if show_summary:
        generate_summary(data)


def generate_summary(data):
    """Generate and display summary statistics from the data."""
    if not data:
        return
    
    print("\n=== Summary Statistics ===")
    
    # Mission count by year
    years = [row['year'] for row in data]
    year_counts = Counter(years)
    print(f"Total missions: {len(data)}")
    print(f"Years covered: {min(years)} to {max(years)}")
    
    # Success rate
    success_count = sum(1 for row in data if row['success'])
    success_rate = (success_count / len(data)) * 100
    print(f"Success rate: {success_rate:.1f}%")
    
    # Average scientific impact
    avg_impact = sum(row['scientific_impact'] for row in data) / len(data)
    print(f"Average scientific impact: {avg_impact:.1f}")
    
    # Mission types
    types = [row['mission_type'] for row in data]
    type_counts = Counter(types)
    print("\nMission types breakdown:")
    for mission_type, count in type_counts.most_common():
        print(f"  {mission_type}: {count} missions")
    
    # Countries
    countries = []
    for row in data:
        countries.extend(row['participating_countries'].split('/'))
    country_counts = Counter(countries)
    print("\nParticipating countries breakdown:")
    for country, count in country_counts.most_common():
        print(f"  {country}: {count} missions")


def plot_mission_success(data, output_file=None):
    """Generate a plot showing mission success rates by year."""
    if not data:
        return False
    
    # Group data by year
    years = sorted(set(row['year'] for row in data))
    success_by_year = {}
    total_by_year = {}
    
    for year in years:
        success_by_year[year] = 0
        total_by_year[year] = 0
    
    for row in data:
        year = row['year']
        total_by_year[year] += 1
        if row['success']:
            success_by_year[year] += 1
    
    # Calculate success rates
    years = list(total_by_year.keys())
    success_rates = [
        (success_by_year[year] / total_by_year[year]) * 100 
        if total_by_year[year] > 0 else 0 
        for year in years
    ]
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.bar(years, success_rates, color='steelblue')
    plt.axhline(y=sum(success_rates)/len(success_rates), color='r', linestyle='-', label='Average')
    plt.ylim(0, 105)
    plt.xlabel('Year')
    plt.ylabel('Success Rate (%)')
    plt.title('Space Mission Success Rate by Year (1970-1999)')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file)
        print(f"Plot saved to {output_file}")
        return True
    else:
        plt.show()
        return True


def main():
    """Main function to process command-line arguments and display results."""
    parser = argparse.ArgumentParser(description='Analyze space exploration missions data.')
    parser.add_argument('--data', type=str, default='data.csv',
                        help='Path to the CSV data file (default: data.csv)')
    parser.add_argument('-p', '--prime', action='store_true',
                        help='Filter missions by prime number years')
    parser.add_argument('-a', '--divisible-by', type=int, metavar='N',
                        help='Filter missions by years divisible by N')
    parser.add_argument('-t', '--type', type=str,
                        help='Filter missions by mission type')
    parser.add_argument('-c', '--country', type=str,
                        help='Filter missions by participating country')
    parser.add_argument('-s', '--success', type=str, choices=['true', 'false'],
                        help='Filter missions by success status')
    parser.add_argument('-i', '--impact', type=int,
                        help='Filter missions by minimum scientific impact')
    parser.add_argument('--summary', action='store_true',
                        help='Show summary statistics')
    parser.add_argument('--plot', action='store_true',
                        help='Generate a plot of mission success rates')
    parser.add_argument('--plot-file', type=str,
                        help='Save plot to specified file instead of displaying')
    
    args = parser.parse_args()
    
    # Load data
    data = load_data(args.data)
    
    # Apply filters
    filtered_data = data
    
    if args.prime:
        filtered_data = filter_by_prime_years(filtered_data)
    
    if args.divisible_by:
        filtered_data = filter_by_divisible_years(filtered_data, args.divisible_by)
    
    if args.type:
        filtered_data = filter_by_column(filtered_data, 'mission_type', args.type)
    
    if args.country:
        filtered_data = filter_by_column(filtered_data, 'participating_countries', args.country)
    
    if args.success:
        filtered_data = filter_by_column(filtered_data, 'success', args.success)
    
    if args.impact:
        filtered_data = filter_by_column(filtered_data, 'scientific_impact', str(args.impact))
    
    # Display results
    display_results(filtered_data, args.summary)
    
    # Generate plot if requested
    if args.plot or args.plot_file:
        plot_success = plot_mission_success(filtered_data, args.plot_file)
        if not plot_success:
            print("Not enough data to generate a plot.")


if __name__ == "__main__":
    main() 