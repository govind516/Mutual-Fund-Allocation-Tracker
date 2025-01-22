import streamlit as st
from data_loading import PortfolioAnalyzer
from data_analysis import DataAnalyzer
from reporting import ReportGenerator
from pathlib import Path

# Initialize classes
portfolio_analyzer = PortfolioAnalyzer()
data_analyzer = DataAnalyzer(portfolio_analyzer.portfolio_data)
report_generator = ReportGenerator()

# Title of the app
st.title("Portfolio Analysis System")

# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox(
    "Select an option", ["Import Data", "Analyze Changes", "Generate Reports"]
)

if option == "Import Data":
    st.header("Import Portfolio Data")
    uploaded_files = st.file_uploader(
        "Choose Excel files", accept_multiple_files=True, type=["xlsx"]
    )
    if st.button("Process Files"):
        for uploaded_file in uploaded_files:
            # Process each uploaded file
            month_year = (
                uploaded_file.name.split()[-2] + " " + uploaded_file.name.split()[-1]
            )
            if portfolio_analyzer.process_excel(uploaded_file, month_year):
                st.success(f"Processed {uploaded_file.name} successfully!")
            else:
                st.error(f"Failed to process {uploaded_file.name}.")

elif option == "Analyze Changes":
    st.header("Analyze Changes")

    if len(portfolio_analyzer.portfolio_data) < 2:
        st.warning("Please import at least two months of data first.")
    else:
        start_month = st.selectbox(
            "Select Start Month", list(portfolio_analyzer.portfolio_data.keys())
        )
        end_month = st.selectbox(
            "Select End Month", list(portfolio_analyzer.portfolio_data.keys())
        )

        if st.button("Analyze"):
            if start_month != end_month:
                analysis = data_analyzer.analyze_changes_over_range(
                    start_month, end_month
                )
                if analysis:
                    st.success("Analysis over range completed successfully.")

                    # Displaying summary in text format
                    summary = analysis.get("summary", {})
                    st.subheader("Summary")
                    st.write(f"New Entries: {summary.get('new_entries', 0)}")
                    st.write(f"Exits: {summary.get('exits', 0)}")
                    st.write(f"Increases: {summary.get('increases', 0)}")
                    st.write(f"Decreases: {summary.get('decreases', 0)}")
                    st.write(f"No Change: {summary.get('no_change', 0)}")
                    st.write(
                        f"Total Value Change: {summary.get('total_value_change', 0)} Lakhs"
                    )

                    # Optionally display monthly changes as a table
                    # st.subheader("Monthly Changes")
                    # st.table(analysis.get("monthly_changes", []))
                else:
                    st.error("No analysis results found for the selected range.")
            else:
                analysis = data_analyzer.analyze_changes(start_month, end_month)
                if analysis:
                    st.success(
                        "Analysis for the selected month completed successfully."
                    )

                    # Displaying summary in text format
                    summary = analysis.get("summary", {})
                    st.subheader("Summary")
                    st.write(f"New Entries: {summary.get('new_entries', 0)}")
                    st.write(f"Exits: {summary.get('exits', 0)}")
                    st.write(f"Increases: {summary.get('increases', 0)}")
                    st.write(f"Decreases: {summary.get('decreases', 0)}")
                    st.write(f"No Change: {summary.get('no_change', 0)}")
                    st.write(
                        f"Total Value Change: {summary.get('total_value_change', 0)}"
                    )
                else:
                    st.error("No analysis results found for the selected month.")

elif option == "Generate Reports":
    st.header("Generate Reports")

    if len(portfolio_analyzer.portfolio_data) < 2:
        st.warning("Please import at least two months of data first.")
    else:
        start_month = st.selectbox(
            "Select Start Month", list(portfolio_analyzer.portfolio_data.keys())
        )
        end_month = st.selectbox(
            "Select End Month", list(portfolio_analyzer.portfolio_data.keys())
        )

        if st.button("Generate Report"):
            if start_month != end_month:
                analysis = data_analyzer.analyze_changes_over_range(
                    start_month, end_month
                )
                if analysis:
                    chart_files = report_generator.generate_reports(
                        analysis, is_range=True
                    )
                    st.success("Report generated for range.")
                    st.subheader("Generated Report")
                    for chart_file in chart_files:
                        st.image(
                            chart_file,
                            caption=f"Chart: {Path(chart_file).stem}",
                            use_column_width=True,
                        )
                else:
                    st.error("Unable to generate report for the selected range.")
            else:
                analysis = data_analyzer.analyze_changes(start_month, end_month)
                if analysis:
                    chart_files = report_generator.generate_reports(
                        analysis, is_range=True
                    )
                    st.success("Report generated for the selected month.")
                    st.subheader("Generated Report")
                    for chart_file in chart_files:
                        st.image(
                            chart_file,
                            caption=f"Chart: {Path(chart_file).stem}",
                            use_column_width=True,
                        )
                else:
                    st.error("Unable to generate report for the selected month.")
