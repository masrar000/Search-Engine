import math

corpus={
    "doc 1": "the quick brown fox",
    "doc 2": "jumped over the lazy dog",
    "doc 3": "the quick brown fox jumed over the lazy dog",
    "doc 4":"the lazy dog slept"   
}

#creating a function to tokenize document
def tokenize(doc):
    return doc.split()

#calculating TF-IDF of weights in a document
def tfidf(term,doc): #tf-idf is a combination of tf and idf
    tf=doc.count(term)/len(tokenize(doc))
    idf=math.log(len(corpus)/sum(1 for d in corpus.values() if term in tokenize(d)))
    return tf*idf

#function to find vector of a tf-idf document
def tfidf_vector(doc):
    vector={}
    for term in set(tokenize(doc)):
        vector[term]=tfidf(term,doc)
    return vector

#calculating tf-idf of all documents in a vector corpus
vectors={}
for doc_id, doc in corpus.items():
    vectors[doc_id]=tfidf_vector(doc)

def cosine_similarity(vec1, vec2):
    dot_product=sum(vec1.get(term,0)*vec2.get(term,0) for term in set(vec1) & set(vec2))
    norm1=math.sqrt(sum(val**2 for val in vec1.values())) #magnitude of vector 1
    norm2=math.sqrt(sum(val**2 for val in vec2.values())) #magnitude of vector 2
    return dot_product/(norm1*norm2)

#function to perform vector space retrieval
def vector_space_retrieval(query):
    query_vec=tfidf_vector(query) #vectorize the query passed to tfidf function
    results=[]
    for doc_id,doc_vec in vectors.items():
        score=cosine_similarity(query_vec,doc_vec)
        results.append((doc_id,score))
    results.sort(key=lambda x:x[1],reverse=True)
    return results

query="quick brown dog"
results=vector_space_retrieval(query)
print(f"Results for query: {query}")
for doc_id,score in results:
    print(f"{doc_id}\t{score}")












  




