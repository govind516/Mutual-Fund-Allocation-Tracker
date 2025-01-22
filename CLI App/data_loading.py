import json
from pathlib import Path
import pandas as pd
import logging
from datetime import datetime
from data_validation import DataValidator
from models import SecurityMetrics
from typing import Dict


class PortfolioAnalyzer:

    def __init__(self, data_dir: str = "..\data\portfolio_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.validator = DataValidator()
        self.portfolio_data: Dict[str, Dict] = self._load_all_data()

    def _load_all_data(self) -> Dict:
        """Load all JSON data files from the data directory"""
        data = {}
        for file in self.data_dir.glob("*.json"):
            try:
                with open(file, "r") as f:
                    month_data = json.load(f)
                    month = file.stem
                    data[month] = month_data
            except Exception as e:
                logging.error(f"Error loading {file}: {e}")
        return data

    def process_excel(self, file_path: str, month_year: str) -> bool:
        """Process an Excel file and store the data"""

        try:
            if not self.validator.validate_date(month_year):
                raise ValueError(f"Invalid date format: {month_year}")

            if not self.validator.validate_file(file_path):
                raise ValueError(f"Invalid file: {file_path}")

            # Read Excel file starting from row 8
            df = pd.read_excel(file_path, skiprows=7)

            # Clean and process data
            portfolio_data = df.iloc[:, [2, 3, 4, 5, 6, 7]].copy()
            portfolio_data.columns = [
                "Name",
                "ISIN",
                "Industry",
                "Quantity",
                "MarketValue",
                "NAV",
            ]
            portfolio_data = portfolio_data.dropna(subset=["ISIN"])

            # Convert numeric columns
            portfolio_data["Quantity"] = pd.to_numeric(
                portfolio_data["Quantity"], errors="coerce"
            )
            portfolio_data["MarketValue"] = pd.to_numeric(
                portfolio_data["MarketValue"], errors="coerce"
            )
            portfolio_data["NAV"] = (
                pd.to_numeric(portfolio_data["NAV"], errors="coerce") * 100
            )  # Convert to percentage

            # Create structured data
            processed_data = {
                "metadata": {
                    "date": month_year,
                    "total_securities": len(portfolio_data),
                    "total_value": float(portfolio_data["MarketValue"].sum()),
                    "processing_date": datetime.now().isoformat(),
                },
                "securities": {},
            }

            for _, row in portfolio_data.iterrows():
                security_data = {
                    "name": str(row["Name"]).strip(),
                    "industry": str(row["Industry"]).strip(),
                    "metrics": asdict(
                        SecurityMetrics(
                            quantity=float(row["Quantity"]),
                            market_value=float(row["MarketValue"]),
                            nav_percentage=float(row["NAV"]),
                            industry=str(row["Industry"]).strip(),
                        )
                    ),
                }
                processed_data["securities"][row["ISIN"]] = security_data

            # Save processed data
            output_file = self.data_dir / f"{month_year}.json"
            with open(output_file, "w") as f:
                json.dump(processed_data, f, indent=2)

            self.portfolio_data[month_year] = processed_data
            logging.info(f"Successfully processed data for {month_year}")
            return True

        except Exception as e:
            logging.error(f"Error processing Excel file: {e}")
            return False
