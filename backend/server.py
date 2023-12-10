from flask import Flask, request, jsonify
from flask_cors import CORS
import pyterrier as pt
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import operator

app = Flask(__name__)
CORS(app)

df = pd.read_csv("backend/updatedGameQueries.csv")
print("Initial columns: ")
print(df.columns)
queryMatrix = pd.pivot_table(df, values="searches", index='query', columns="userid")
print("pivoted columns: ")
print(queryMatrix.columns)
queryMatrix = queryMatrix.fillna(0)

# Normalize the listen time by adjusting it around the mean for a user
queryNorm = queryMatrix.apply(lambda x: x - np.nanmean(x), axis=1)
queryNorm.head()
item_sim_df = pd.DataFrame(cosine_similarity(queryNorm,queryNorm),index=queryNorm.index,columns=queryNorm.index)

@app.route('/search', methods=['GET'])
def search():
    # Get the query from the request parameters
    query = request.args.get('query', '')
    queries, scores = recommendations(query)
    for x, y in zip(queries[:10], scores[:10]):
        print("{} with similarity of {}".format(x,y))
    formatted_query_results = [{"query": query, "score": score} for query, score in zip(queries, scores)]
    print("++++++++++++++++++++++++++++++++++++++++")
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
    
    return jsonify(response), jsonify(formatted_query_results)

def recommendations(queryID):
    matching_columns = [col for col in item_sim_df.columns if queryID.lower() in col.lower()]
    
    if not matching_columns:
        print("{} item not available".format(queryID))
        return None, None
    
    # Assuming there could be multiple matching columns, we take the first one
    query_column = matching_columns[0]

    simQueries = item_sim_df.sort_values(by=query_column, ascending=False).index[1:]
    simScores = item_sim_df.sort_values(by=query_column, ascending=False).loc[:, query_column].tolist()[1:]
    return simQueries, simScores

  
if __name__ == '__main__':
    # Run the Flask app on a specific port (e.g., 5000)
    app.run(port=5000, debug=True)



  
    # #single out the current user
    # user = [[14, 222, query, 14]]
    # userDf = pd.DataFrame(user, columns=['userid', 'query', 'searches'])
    # #calculate cosine similarity
    # otherUserDf = queryMatrix[queryMatrix.columns!=222]
    # similarities = cosine_similarity(userDf, otherUserDf)[0].tolist()
    # # Create list of indices of these users to get their data quick
    # indices = otherUserDf.index.tolist()
    # index_similarity = dict(zip(indices, similarities))
    # #Sort by similarity
    # index_similarity_sorted = sorted(index_similarity.items(), key=operator.itemgetter(1))
    # index_similarity_sorted.reverse() 
    # # grab top k users
    # top_users = index_similarity_sorted[:k]
    # sim_users = [u[0] for u in top_users]