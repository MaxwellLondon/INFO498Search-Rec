import { useState } from 'react';
import './App.css'; // Include your custom styles
import 'bootstrap/dist/css/bootstrap.min.css'; // Include Bootstrap styles
import { FaFolder, FaSearch } from 'react-icons/fa'; // Import icons

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [recommendations, setRecommendations] = useState([]);

  const handleSearch = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/search?query=${query}`);
      const data = await response.json();

      // Extracting the top 10 results and recommendations from the JSON object
      const topResults = data.results.slice(0, 10).map(result => result.docno);
      const topRecommendations = data.recs.slice(0, 10).map(rec => rec.query);

      // Setting the results and recommendations in the state
      setResults(topResults);
      setRecommendations(topRecommendations);
    } catch (error) {
      console.error('Error fetching search results:', error);
    }
  };

  return (
    <div className="container-fluid h-100">
      {/* Top Sidebar */}
      <div className="row bg-dark text-white p-3">
        <div className="col">
          <span className="h2">🔍 Search App</span>
        </div>
      </div>

      {/* Main Content */}
      <div className="row mt-4 h-100">
        {/* Left Sidebar */}
        <div className="col-2 bg-light p-3">
          {/* Folder Icon */}
          <div className="text-center">
            <FaFolder size={40} color="#007BFF" />
            <p className="mt-2">Sidebar Content</p>
          </div>
        </div>

        {/* Main Content Area */}
        <div className="col-10 d-flex flex-column">
          <h1 className="mb-4">Search Endpoint Tester</h1>

          <div className="input-group mb-3">
            <input
              type="text"
              className="form-control form-control-lg"
              placeholder="Enter your search query"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <div className="input-group-append">
              <button className="btn btn-primary btn-lg" onClick={handleSearch}>
                <FaSearch /> Search
              </button>
            </div>
          </div>

          {results.length > 0 && (
            <div className="search-results mt-4">
              <h2>Search Results:</h2>
              <table className="table table-bordered table-hover">
                <thead className="thead-dark">
                  <tr>
                    <th scope="col">#</th>
                    <th scope="col">Document Number</th>
                  </tr>
                </thead>
                <tbody>
                  {results.map((result, index) => (
                    <tr key={result}>
                      <th scope="row">{index + 1}</th>
                      <td>{result}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {recommendations.length > 0 && (
            <div className="recommendations mt-4">
              <h2>Recommendations:</h2>
              <table className="table table-bordered table-hover">
                <thead className="thead-dark">
                  <tr>
                    <th scope="col">#</th>
                    <th scope="col">Recommendation</th>
                  </tr>
                </thead>
                <tbody>
                  {recommendations.map((rec, index) => (
                    <tr key={index}>
                      <th scope="row">{index + 1}</th>
                      <td>{rec}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
