import { useState } from 'react';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/search?query=${query}`);
      const data = await response.json();
      setResults(data.results);
    } catch (error) {
      console.error('Error fetching search results:', error);
    }
  };

  return (
    <div>
      <h1>Search Endpoint Tester</h1>
      <div>
        <input
          type="text"
          placeholder="Enter your search query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>
      {results.length > 0 && (
        <div className="search-results">
          <h2>Search Results:</h2>
          <ul>
            {results.map((result) => (
              <li key={result.docid}>{result.content}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
