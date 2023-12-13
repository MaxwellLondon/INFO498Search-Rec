import pandas as pd
import pyterrier as pt
import os

# Get the current working directory
current_directory = os.getcwd()

# Print the current working directory
# print("Current Directory:", current_directory)

if not pt.started():
    pt.init()

indexer = pt.TRECCollectionIndexer("./updated_polygon_index2", meta={"docno":300, "link":1024, "title":1024},meta_tags={"title":"title", "link":"link"})
indexref = indexer.index("INFO498Search-Rec/backend/updatedPolygon.trec")
index = pt.IndexFactory.of(indexref)

queries = pd.DataFrame([["q1","Pokemon"],["q2","Dragon"]],columns=["qid","query"])
tf_idf = pt.BatchRetrieve(index, wmodel="TF_IDF")
print(tf_idf.transform(queries))
print(index.getMetaIndex().getKeys())
print(index.getCollectionStatistics().toString())


