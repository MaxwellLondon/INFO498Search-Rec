from flask import Flask, request, jsonify
from flask_cors import CORS
import pyterrier as pt
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import atexit

df = pd.read_csv("INFO498Search-Rec/backend/updatedGameQueries.csv")
print(df)
app = Flask(__name__)
CORS(app)

def save_df_to_csv():
    global df
    print(df.tail())
    df.to_csv("./backend.csv", index=False)
    print("DataFrame saved to CSV")

atexit.register(save_df_to_csv)


@app.route('/search', methods=['GET'])
def search():
    # Get the query from the request parameters

    query = request.args.get('query', '')
    global df  # Assuming you want to use the global df variable
    if query not in df['query'].values:
        # Add a new query row using pd.concat() only if it's not a duplicate
        new_row = pd.DataFrame({'query': [query]})
        df = pd.concat([df, new_row], ignore_index=True)

    print(len(df))
    rec_dict = recommendations(query)
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
    response = {'query': query, 'results': formatted_results, 'recs': rec_dict}
    
    return jsonify(response)

def recommendations(query):
    global df
    # Create a CountVectorizer to convert text data to a matrix of token counts
    vectorizer = CountVectorizer()
    
    # Fit and transform the stored queries
    stored_queries_matrix = vectorizer.fit_transform(df['query'])
    
    # Transform the given query
    given_query_matrix = vectorizer.transform([query])

    # Calculate cosine similarity
    cosine_sim = cosine_similarity(stored_queries_matrix, given_query_matrix)

    # Get the similarity scores for each stored query
    similarity_scores = cosine_sim.flatten()

    # Add the similarity scores to the DataFrame
    df['CosineSimilarity'] = similarity_scores

    # Sort the DataFrame based on similarity scores in descending order
    sorted_df = df.sort_values(by='CosineSimilarity', ascending=False)
    
    # Remove rows with identical queries to the search input
    sorted_df = sorted_df[sorted_df['query'] != query]

    # Extract the top results
    top_results = sorted_df[['query', 'CosineSimilarity']].head(10)
  
    top_results['Rank'] = range(1, len(top_results) + 1)  # Add a new 'Rank' field
    # Convert the DataFrame to a dictionary
    top_results_dict = top_results.to_dict(orient='records')

    return top_results_dict

  
if __name__ == '__main__':
    # Run the Flask app on a specific port (e.g., 5000)
    app.run(port=5000, debug=True)