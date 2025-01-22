from datetime import datetime
import logging
from typing import Dict
from models import SecurityMetrics, SecurityChange, ChangeType


class DataAnalyzer:
    def __init__(self, portfolio_data: Dict):
        self.portfolio_data = portfolio_data

    def analyze_changes(self, start_month: str, end_month: str) -> Dict:
        try:
            if (
                start_month not in self.portfolio_data
                or end_month not in self.portfolio_data
            ):
                raise ValueError("Invalid months selected")

            start_data = self.portfolio_data[start_month]
            end_data = self.portfolio_data[end_month]

            analysis = {
                "metadata": {
                    "start_month": start_month,
                    "end_month": end_month,
                    "analysis_date": datetime.now().isoformat(),
                },
                "summary": {
                    "new_entries": 0,
                    "exits": 0,
                    "increases": 0,
                    "decreases": 0,
                    "no_change": 0,
                    "total_value_change": end_data["metadata"]["total_value"]
                    - start_data["metadata"]["total_value"],
                },
                "changes": {},
            }

            all_isins = set(start_data["securities"].keys()) | set(
                end_data["securities"].keys()
            )

            for isin in all_isins:
                start_security = start_data["securities"].get(isin)
                end_security = end_data["securities"].get(isin)

                if not start_security:
                    change = SecurityChange(
                        change_type=ChangeType.NEW_ENTRY,
                        old_metrics=None,
                        new_metrics=SecurityMetrics(**end_security["metrics"]),
                        percentage_change=100,
                        value_change=end_security["metrics"]["market_value"],
                    )
                    analysis["summary"]["new_entries"] += 1

                elif not end_security:
                    change = SecurityChange(
                        change_type=ChangeType.EXIT,
                        old_metrics=SecurityMetrics(**start_security["metrics"]),
                        new_metrics=None,
                        percentage_change=-100,
                        value_change=-start_security["metrics"]["market_value"],
                    )
                    analysis["summary"]["exits"] += 1

                else:
                    old_value = start_security["metrics"]["market_value"]
                    new_value = end_security["metrics"]["market_value"]
                    value_change = new_value - old_value
                    pct_change = (
                        (value_change / old_value * 100)
                        if old_value != 0
                        else float("inf")
                    )

                    if abs(pct_change) < 0.1:
                        change_type = ChangeType.NO_CHANGE
                        analysis["summary"]["no_change"] += 1
                    elif pct_change > 0:
                        change_type = ChangeType.INCREASED
                        analysis["summary"]["increases"] += 1
                    else:
                        change_type = ChangeType.DECREASED
                        analysis["summary"]["decreases"] += 1

                    change = SecurityChange(
                        change_type=change_type,
                        old_metrics=SecurityMetrics(**start_security["metrics"]),
                        new_metrics=SecurityMetrics(**end_security["metrics"]),
                        percentage_change=pct_change,
                        value_change=value_change,
                    )

                analysis["changes"][isin] = {
                    "name": (
                        end_security["name"] if end_security else start_security["name"]
                    ),
                    "change": change.__dict__,
                }

            return analysis

        except Exception as e:
            logging.error(f"Error analyzing changes: {e}")
            return None

    def analyze_changes_over_range(self, start_month: str, end_month: str) -> Dict:
        try:
            all_months = sorted(
                self.portfolio_data.keys(), key=lambda x: datetime.strptime(x, "%B %Y")
            )

            if start_month not in all_months or end_month not in all_months:
                raise ValueError("Invalid months selected.")

            start_index = all_months.index(start_month)
            end_index = all_months.index(end_month)

            if start_index >= end_index:
                raise ValueError("Start month must precede end month.")

            selected_months = all_months[start_index : end_index + 1]

            range_analysis = {
                "metadata": {
                    "start_month": start_month,
                    "end_month": end_month,
                    "analysis_date": datetime.now().isoformat(),
                },
                "monthly_changes": [],
                "summary": {
                    "new_entries": 0,
                    "exits": 0,
                    "increases": 0,
                    "decreases": 0,
                    "no_change": 0,
                    "total_value_change": 0,
                },
            }

            for i in range(len(selected_months) - 1):
                month1 = selected_months[i]
                month2 = selected_months[i + 1]
                month_analysis = self.analyze_changes(month1, month2)

                if month_analysis:
                    range_analysis["monthly_changes"].append(month_analysis)
                    for key in [
                        "new_entries",
                        "exits",
                        "increases",
                        "decreases",
                        "no_change",
                    ]:
                        range_analysis["summary"][key] += month_analysis["summary"][key]
                    range_analysis["summary"]["total_value_change"] += month_analysis[
                        "summary"
                    ]["total_value_change"]

            return range_analysis

        except Exception as e:
            logging.error(f"Error analyzing changes over range: {e}")
            return None
