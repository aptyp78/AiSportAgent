import { useState } from 'react';
import FileUpload from '../components/FileUpload';
import AnalysisResults from '../components/AnalysisResults';

const Home = () => {
  const [results, setResults] = useState(null);

  const handleResults = (data) => {
    setResults(data);
  };

  return (
    <div>
      <h1>FIT File Analyzer</h1>
      <FileUpload onResults={handleResults} />
      {results && <AnalysisResults results={results} />}
    </div>
  );
};

export default Home;