from data_loading import PortfolioAnalyzer
from data_analysis import DataAnalyzer
from reporting import ReportGenerator
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


def main():

    portfolio_analyzer = PortfolioAnalyzer()
    data_analyzer = DataAnalyzer(portfolio_analyzer.portfolio_data)
    report_generator = ReportGenerator()

    while True:
        print("\n=== Portfolio Analysis System ===")
        print("1. Import Portfolio Data")
        print("2. Analyze Changes")
        print("3. List Available Months")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ")

        try:
            if choice == "1":
                # Folder containing all Excel files
                folder_path = Path("..\data\mutual_fund_data")
                if not folder_path.exists():
                    print("Error: The folder 'mutual_fund_data' does not exist.")
                    return

                # Process all Excel files in the folder
                excel_files = list(folder_path.glob("ZN250 - Monthly Portfolio *.xlsx"))
                if not excel_files:
                    print("No Excel files found in the folder.")
                    return

                all_files_processed = True
                for file in excel_files:
                    # Extract `month_year` from the filename
                    parts = file.stem.split()  # Split by spaces
                    month_year = f"{parts[-2]} {parts[-1]}"  # Last two parts are the month and year

                    # Process the file
                    print(f"Processing file: {file.name}")
                    if not portfolio_analyzer.process_excel(str(file), month_year):
                        print(f"Failed to process file: {file.name}")
                        all_files_processed = False
                        break  # Stop processing further files if any failure occurs

                if all_files_processed:
                    print("All files processed successfully!")
                else:
                    print(
                        "Error: Some files failed to process. Please check the logs for details."
                    )

            elif choice == "2":
                if len(portfolio_analyzer.portfolio_data) < 2:
                    print("Please import at least two months of data first.")
                    continue

                print("\nAvailable months:")
                for month in sorted(portfolio_analyzer.portfolio_data.keys()):
                    print(f"- {month}")

                start_month = input("\nEnter start month: ")
                end_month = input("Enter end month: ")

                # Analyze range or single pair
                if start_month != end_month:
                    analysis = data_analyzer.analyze_changes_over_range(
                        start_month, end_month
                    )
                    if analysis:
                        report_generator.generate_reports(analysis, is_range=True)
                else:
                    analysis = data_analyzer.analyze_changes(start_month, end_month)
                    if analysis:
                        report_generator.generate_reports(analysis, is_range=False)

            elif choice == "3":
                print("\nAvailable months:")
                for month in sorted(portfolio_analyzer.portfolio_data.keys()):
                    print(f"- {month}")

            elif choice == "4":
                print("Thank you for using the Portfolio Analysis System!")
                break

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            logging.error(f"Error in main loop: {e}")
            print("An error occurred. Please check the logs for details.")


if __name__ == "__main__":
    main()
