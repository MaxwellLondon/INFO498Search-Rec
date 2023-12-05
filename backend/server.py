from flask import Flask, request, jsonify
from flask_cors import CORS
#import pyterrier as pt

app = Flask(__name__)
CORS(app)


@app.route('/search', methods=['GET'])
def search():
    # Get the query from the request parameters
    query = request.args.get('query', '')

    # Perform the search using PyTerrier

    # Dummy result
    results = [{'docid': '001', 'score': 0.9, 'content': 'Dummy document 1'},
               {'docid': '002', 'score': 0.8, 'content': 'Dummy document 2'}]

    # Format the results and send them to the front-end
    response = {'query': query, 'results': results}
    
    return jsonify(response)

# You can define more endpoints for recommendation, etc.

if __name__ == '__main__':
    # Run the Flask app on a specific port (e.g., 5000)
    app.run(port=5000, debug=True)
