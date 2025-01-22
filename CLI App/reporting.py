import logging
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict
from pathlib import Path

save_dir = Path("..\data\output_charts")
save_dir.mkdir(parents=True, exist_ok=True)


class ReportGenerator:

    def generate_reports(self, analysis: Dict, is_range: bool = False) -> list:
        """Generate detailed reports and visualizations."""
        try:
            print("\n=== Portfolio Analysis Report ===")
            if is_range:
                print(
                    f"Period: {analysis['metadata']['start_month']} to {analysis['metadata']['end_month']}"
                )
            else:
                print(
                    f"Period: {analysis['metadata']['start_month']} to {analysis['metadata']['end_month']}"
                )
            print("\nSummary:")
            print(f"New Entries: {analysis['summary']['new_entries']}")
            print(f"Exits: {analysis['summary']['exits']}")
            print(f"Increased Positions: {analysis['summary']['increases']}")
            print(f"Decreased Positions: {analysis['summary']['decreases']}")
            print(f"Unchanged Positions: {analysis['summary']['no_change']}")
            print(
                f"Total Value Change: ₹{analysis['summary']['total_value_change']:,.2f} Lakhs"
            )

            # Generate visualizations
            if is_range:
                chart_file_paths = []
                chart_file_paths += self._generate_range_charts(analysis)
            else:
                chart_file_paths += self._generate_charts(analysis)
            return chart_file_paths

        except Exception as e:
            logging.error(f"Error generating reports: {e}")
            return []

    def _generate_range_charts(self, analysis: Dict) -> list:
        """Generate charts for a multi-month range."""
        chart_file_paths = []
        chart_file_paths.append(self._generate_change_type_barchart(analysis))
        chart_file_paths.append(self._generate_portfolio_value_linechart(analysis))
        chart_file_paths.append(self._generate_correlation_heatmap(analysis))
        chart_file_paths.append(self._generate_stacked_area_chart(analysis))
        return chart_file_paths

    # Bar Chart: Monthly Summary of Change Types

    def _generate_change_type_barchart(self, analysis: Dict) -> str:
        """Generate a bar chart for monthly change type summary."""
        months = [
            month["metadata"]["end_month"] for month in analysis["monthly_changes"]
        ]
        new_entries = [
            month["summary"]["new_entries"] for month in analysis["monthly_changes"]
        ]
        exits = [month["summary"]["exits"] for month in analysis["monthly_changes"]]
        increases = [
            month["summary"]["increases"] for month in analysis["monthly_changes"]
        ]
        decreases = [
            month["summary"]["decreases"] for month in analysis["monthly_changes"]
        ]
        no_change = [
            month["summary"]["no_change"] for month in analysis["monthly_changes"]
        ]

        # Grouped Bar Chart
        x = np.arange(len(months))
        width = 0.15

        plt.figure(figsize=(12, 6))
        plt.bar(x - 2 * width, new_entries, width, label="New Entries")
        plt.bar(x - width, exits, width, label="Exits")
        plt.bar(x, increases, width, label="Increases")
        plt.bar(x + width, decreases, width, label="Decreases")
        plt.bar(x + 2 * width, no_change, width, label="No Change")

        plt.xlabel("Months")
        plt.ylabel("Count")
        plt.title("Monthly Summary of Change Types")
        plt.xticks(x, months, rotation=45)
        plt.legend()
        plt.tight_layout()

        chart_file = f"barchart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        chart_file_path = save_dir / chart_file
        plt.savefig(chart_file_path)
        plt.close()

        logging.info(f"Change type bar chart saved to {chart_file}")
        return str(chart_file_path)

    def _generate_portfolio_value_linechart(self, analysis: Dict) -> str:
        """Generate a line chart for portfolio value over time."""
        months = [
            month["metadata"]["end_month"] for month in analysis["monthly_changes"]
        ]
        total_values = [
            month["summary"]["total_value_change"]
            for month in analysis["monthly_changes"]
        ]

        plt.figure(figsize=(12, 6))
        plt.plot(months, total_values, marker="o", color="b", label="Portfolio Value")
        plt.title("Total Portfolio Value Over Time")
        plt.xlabel("Months")
        plt.ylabel("Portfolio Value (Lakhs)")
        plt.legend()
        plt.grid()
        plt.xticks(rotation=45)
        plt.tight_layout()

        chart_file = f"linechart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        chart_file_path = save_dir / chart_file
        plt.savefig(chart_file_path)
        plt.close()

        logging.info(f"Portfolio value line chart saved to {chart_file}")
        return str(chart_file_path)

    def _generate_correlation_heatmap(self, analysis: Dict) -> str:
        """Generate a heatmap of correlations between monthly changes."""
        change_types = ["new_entries", "exits", "increases", "decreases", "no_change"]
        data = {
            change_type: [
                month["summary"][change_type] for month in analysis["monthly_changes"]
            ]
            for change_type in change_types
        }

        # Create DataFrame for correlation calculation
        df = pd.DataFrame(data)
        correlation_matrix = df.corr()

        plt.figure(figsize=(8, 6))
        sns.heatmap(
            correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5
        )
        plt.title("Correlation Between Monthly Change Types")
        plt.tight_layout()

        chart_file = (
            f"correlation_heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
        chart_file_path = save_dir / chart_file
        plt.savefig(chart_file_path)
        plt.close()

        logging.info(f"Correlation heatmap saved to {chart_file}")
        return str(chart_file_path)

    def _generate_stacked_area_chart(self, analysis: Dict) -> str:
        """Generate a stacked area chart for change type contributions over time."""
        months = [
            month["metadata"]["end_month"] for month in analysis["monthly_changes"]
        ]
        new_entries = [
            month["summary"]["new_entries"] for month in analysis["monthly_changes"]
        ]
        exits = [month["summary"]["exits"] for month in analysis["monthly_changes"]]
        increases = [
            month["summary"]["increases"] for month in analysis["monthly_changes"]
        ]
        decreases = [
            month["summary"]["decreases"] for month in analysis["monthly_changes"]
        ]
        no_change = [
            month["summary"]["no_change"] for month in analysis["monthly_changes"]
        ]

        plt.figure(figsize=(12, 6))
        plt.stackplot(
            months,
            new_entries,
            exits,
            increases,
            decreases,
            no_change,
            labels=["New Entries", "Exits", "Increases", "Decreases", "No Change"],
            alpha=0.8,
        )
        plt.title("Change Type Contribution Over Time")
        plt.xlabel("Months")
        plt.ylabel("Count")
        plt.legend(loc="upper left")
        plt.xticks(rotation=45)
        plt.tight_layout()

        chart_file = (
            f"stacked_area_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
        chart_file_path = save_dir / chart_file
        plt.savefig(chart_file_path)
        plt.close()

        logging.info(f"Stacked area chart saved to {chart_file}")
        return str(chart_file_path)
