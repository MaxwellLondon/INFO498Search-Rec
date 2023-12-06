from flask import Flask, request, jsonify
from flask_cors import CORS
import pyterrier as pt
import pandas as pd

app = Flask(__name__)
CORS(app)


@app.route('/search', methods=['GET'])
def search():
    # Get the query from the request parameters
    query = request.args.get('query', '')

    # Perform the search using PyTerrier

    if not pt.started():
        pt.init()

    index = pt.IndexFactory.of("./backend/polygon_index2")

    lm = pt.BatchRetrieve(index, wmodel="Hiemstra_LM")

    results_df = lm.transform(query)

    # Extract the top 10 results
    top_results = results_df.head(10)

     # Format the top results into a list of dictionaries
    formatted_results = []
    for index, row in top_results.iterrows():
        result_dict = {
            'docid': str(row['docid']),
            'rank': int(row['rank']),
            'score': float(row['score']),
            'docno': str(row['docno']),
        }
        formatted_results.append(result_dict)

    # Format the results and send them to the front-end
    response = {'query': query, 'results': formatted_results}
    
    return jsonify(response)


# You can define more endpoints for recommendation, etc.

if __name__ == '__main__':
    # Run the Flask app on a specific port (e.g., 5000)
    app.run(port=5000, debug=True)
