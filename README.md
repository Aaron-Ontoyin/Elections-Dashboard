# Elections Dashboard

## Overview

The Elections Dashboard is a Streamlit-based application designed to visualize election data. It allows users to select specific years, parties, and methods to analyze and display the top polling stations based on various criteria.

## Features

- **Year Selection**: Users can select one or more years to filter the data.
- **Party Selection**: Users can choose a political party to analyze.
- **Top N Selection**: Users can specify the number of top polling stations to display.
- **Method Selection**: Users can choose the method for ranking polling stations:
  - **Local Fraction**: Top N stations with the highest fraction of votes for the party in those respective stations.
  - **Global Fraction**: Top N stations with the highest fraction of votes for the party across all stations.
  - **Number**: Top N stations with the highest number of votes for the party.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Aaron-Ontoyin/Elections-Dashboard.git
   cd Elections-Dashboard
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```sh
   streamlit run app.py
   ```

2. Open your web browser and go to `http://localhost:8501` to access the dashboard.

## Example

1. Select the party from the dropdown menu.
2. Choose the years you want to analyze.
3. Specify the number of top polling stations (N).
4. Select the method for ranking the polling stations.
5. The dashboard will display the results based on your selections.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [`LICENSE`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fc%3A%2FUsers%2FHP%2FDocuments%2FLab%2FOn_It%2FElections-Dashboard%2FLICENSE%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "c:\Users\HP\Documents\Lab\On_It\Elections-Dashboard\LICENSE") file for details.

## Contact

For any questions or suggestions, please open an issue in the repository.