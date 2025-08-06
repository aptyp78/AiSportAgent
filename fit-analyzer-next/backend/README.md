# Fit Analyzer Backend

This is the backend component of the Fit Analyzer project, which is designed to analyze FIT files uploaded by users. The backend is built using Python and Flask, and it utilizes the `fitparse` library to extract relevant data from the FIT files.

## Project Structure

- `app.py`: The main entry point for the Flask application. This file handles file uploads and processes the FIT files.
- `requirements.txt`: This file lists the Python dependencies required for the backend, including Flask and fitparse.

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd fit-analyzer-next/backend
   ```

2. **Create a Virtual Environment**
   It is recommended to create a virtual environment to manage dependencies.
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   Install the required Python packages using pip.
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   Start the Flask server.
   ```bash
   python app.py
   ```

## API Endpoints

- **POST /upload**
  - Description: Upload a FIT file for analysis.
  - Request: A multipart/form-data request containing the FIT file.
  - Response: A JSON object with the analysis results, including:
    - GPS coordinates
    - Power
    - Heart Rate
    - Cadence
    - Elevation
    - Pace
    - Running Dynamics (ground contact time, vertical oscillation)

## Usage

Once the backend is running, the frontend application can be used to upload FIT files and display the analysis results. Ensure that the frontend is configured to point to the correct backend URL.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.