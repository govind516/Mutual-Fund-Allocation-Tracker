# Portfolio Analysis System

The **Portfolio Analysis System** is a comprehensive tool designed to analyze portfolio data over time, visualize trends, and generate detailed reports. It includes a command-line application (`CLI App`) and a Streamlit-based web interface for an interactive user experience.

## Features

1. **Data Import**:  
   - Supports importing multiple months of portfolio data from `.xlsx` files.
   - Automatically processes and organizes data for analysis.

2. **Data Analysis**:  
   - Compares portfolio data across months to identify:
     - New entries
     - Exits
     - Position increases
     - Position decreases
     - Unchanged positions
   - Summarizes total value changes over time.

3. **Report Generation**:  
   - Generates visualizations such as bar charts, line charts, heatmaps, and stacked area charts.
   - Saves charts in the `data/output_charts` directory for easy access.
   - Supports both single-month and multi-month range analysis.

4. **Interactive Web App**:  
   - User-friendly interface built with **Streamlit**.
   - Options for importing data, analyzing changes, and generating reports.
   - Visualizes results directly in the app.

---

## Directory Structure

```plaintext
├── CLI App
│   ├── app.py                 # CLI for running the application
│   ├── data_analysis.py       # Logic for analyzing portfolio data
│   ├── data_loading.py        # Handles data loading and processing
│   ├── data_validation.py     # Validates data consistency
│   ├── models.py              # Defines data models
│   ├── reporting.py           # Handles report generation and visualizations
│   ├── streamlit_app.py       # Streamlit web app for interactive use
├── data
│   ├── mutual_fund_data       # Raw mutual fund data
│   ├── output_charts          # Generated charts for reports
│   ├── portfolio_data         # Processed portfolio data files
├── venv
│   ├── ...                    # Virtual environment files
└── .gitignore                 # Files and directories to ignore in Git
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/govind516/Mutual-Fund-Allocation-Tracker/
   cd Mutual-Fund-Allocation-Tracker
   ```

2. Activate the virtual environment:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Unix/MacOS:**
     ```bash
     source venv/bin/activate
     ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
---

## Usage

### Web Interface
1. Run the Streamlit app:
   ```bash
   cd "CLI App"
   streamlit run streamlit_app.py
   ```
2. Open the provided local URL in your browser.

3. Use the sidebar to navigate through the app:
   - **Import Data**: Upload `.xlsx` files for portfolio analysis.
   - **Analyze Changes**: View summarized changes between selected months.
   - **Generate Reports**: Generate detailed reports with visualizations.

![image](https://github.com/user-attachments/assets/d59cfd66-e58d-45e5-8067-770422cdc746)

### CLI Usage
1. Navigate to the `CLI App` directory:
   ```bash
   cd "CLI App"
   ```
2. Run the CLI tool:
   ```bash
   python app.py
   ```

---

## Output Charts

Generated charts are stored in the `data/output_charts` directory and include:
- **Bar Chart**: Monthly summary of change types.
- **Line Chart**: Portfolio value over time.
- **Heatmap**: Correlations between change types.
- **Stacked Area Chart**: Contributions of each change type over time.

---

## Technologies Used

- **Python**: Core programming language.
- **Pandas**: Data manipulation and analysis.
- **Matplotlib & Seaborn**: Data visualization.
- **Streamlit**: Interactive web app framework.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature/fix:
3. Commit your changes:
4. Push your branch:
5. Create a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).
