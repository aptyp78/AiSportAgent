# Fit Analyzer Next.js Frontend

This project is a Next.js application designed to analyze FIT files. It allows users to upload FIT files and view the analysis results, including various metrics such as GPS coordinates, power, heart rate, cadence, elevation, pace, and running dynamics.

## Project Structure

The frontend of the application is organized as follows:

```
frontend
├── next.config.js        # Configuration settings for the Next.js application
├── package.json          # npm configuration file with dependencies and scripts
├── public                # Directory for static assets (images, icons, etc.)
├── README.md             # Documentation specific to the frontend
└── src                   # Source code for the application
    ├── pages             # Next.js pages
    │   ├── _app.tsx      # Custom App component for initializing pages
    │   └── index.tsx     # Main page with file upload and results display
    ├── components        # React components
    │   ├── FileUpload.tsx # Component for uploading FIT files
    │   └── AnalysisResults.tsx # Component for displaying analysis results
    └── styles            # Styles for the application
        └── globals.css    # Global CSS styles
```

## Getting Started

To get started with the frontend application, follow these steps:

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd fit-analyzer-next/frontend
   ```

2. **Install dependencies:**
   ```
   npm install
   ```

3. **Run the development server:**
   ```
   npm run dev
   ```

4. **Open your browser:**
   Navigate to `http://localhost:3000` to view the application.

## Features

- Upload FIT files for analysis.
- View analysis results in a user-friendly format.
- Responsive design for various devices.

## Deployment

This application is configured to be deployed on Vercel. Ensure that you have the necessary environment variables set up in your Vercel dashboard for the backend API.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.