import React from 'react';

interface AnalysisResult {
  gpsAvailable: boolean;
  power: number | null;
  heartRate: number | null;
  cadence: number | null;
  elevation: number | null;
  pace: number | null;
  runningDynamics: {
    groundContactTime: number | null;
    verticalOscillation: number | null;
  } | null;
}

interface AnalysisResultsProps {
  results: AnalysisResult | null;
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ results }) => {
  if (!results) {
    return <div>No analysis results available.</div>;
  }

  return (
    <div>
      <h2>Analysis Results</h2>
      <table>
        <thead>
          <tr>
            <th>Data Point</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>GPS Available</td>
            <td>{results.gpsAvailable ? 'Yes' : 'No'}</td>
          </tr>
          <tr>
            <td>Power</td>
            <td>{results.power !== null ? results.power : 'N/A'}</td>
          </tr>
          <tr>
            <td>Heart Rate</td>
            <td>{results.heartRate !== null ? results.heartRate : 'N/A'}</td>
          </tr>
          <tr>
            <td>Cadence</td>
            <td>{results.cadence !== null ? results.cadence : 'N/A'}</td>
          </tr>
          <tr>
            <td>Elevation</td>
            <td>{results.elevation !== null ? results.elevation : 'N/A'}</td>
          </tr>
          <tr>
            <td>Pace</td>
            <td>{results.pace !== null ? results.pace : 'N/A'}</td>
          </tr>
          <tr>
            <td>Ground Contact Time</td>
            <td>{results.runningDynamics?.groundContactTime !== null ? results.runningDynamics.groundContactTime : 'N/A'}</td>
          </tr>
          <tr>
            <td>Vertical Oscillation</td>
            <td>{results.runningDynamics?.verticalOscillation !== null ? results.runningDynamics.verticalOscillation : 'N/A'}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default AnalysisResults;