import pandas as pd
import pyterrier as pt

if not pt.started():
    pt.init()

indexer = pt.TRECCollectionIndexer("./polygon_index2", meta={"docno":300,"title":1024},meta_tags={"title":"title"})
indexref = indexer.index("./polygon.trec")
index = pt.IndexFactory.of(indexref)
# print(index.getCollectionStatistics().toString())

queries = pd.DataFrame([["q1","Pokemon"],["q2","Dragon"]],columns=["qid","query"])
tf_idf = pt.BatchRetrieve(index, wmodel="TF_IDF")
print(tf_idf.transform(queries))