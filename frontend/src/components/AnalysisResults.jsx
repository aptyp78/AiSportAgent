import React from 'react';

interface AnalysisResultsProps {
  results: any;
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ results }) => {
  if (!results) return null;

  // Если results - массив объектов, отображаем как таблицу
  if (Array.isArray(results)) {
    if (results.length === 0) return <div>Нет данных для отображения.</div>;
    const columns = Object.keys(results[0]);
    return (
      <table style={{ borderCollapse: 'collapse', width: '100%' }}>
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col} style={{ border: '1px solid #ccc', padding: '4px', background: '#f5f5f5' }}>
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {results.map((row: any, idx: number) => (
            <tr key={idx}>
              {columns.map((col) => (
                <td key={col} style={{ border: '1px solid #ccc', padding: '4px' }}>
                  {String(row[col])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  }

  // Если results - объект, отображаем ключ-значение
  if (typeof results === 'object') {
    return (
      <table style={{ borderCollapse: 'collapse', width: '100%' }}>
        <tbody>
          {Object.entries(results).map(([key, value]) => (
            <tr key={key}>
              <td style={{ border: '1px solid #ccc', padding: '4px', fontWeight: 'bold', background: '#f5f5f5' }}>{key}</td>
              <td style={{ border: '1px solid #ccc', padding: '4px' }}>
                {typeof value === 'object' ? JSON.stringify(value, null, 2) : String(value)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  }

  // Если results - что-то другое
  return <pre>{String(results)}</pre>;
};

export default AnalysisResults;