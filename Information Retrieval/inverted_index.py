class InvertedIndex:
    def __init__(self):
        self.index={} #inverted index is defined by dictionary

    def add_document(self,document_id,document):
        terms=document.split() #split strings e.g. apple banana apple -> ['apple','banana','apple']
        for position,term in enumerate(terms): #loop over docuemnt id and document e.g position -> 0,apple ->1, banana and so on
            if term not in self.index:
                self.index[term]={}
            if document_id not in self.index[term]:
                self.index[term][document_id]=[] #THIS LIST WILL contain position of the word in the document
            
            self.index [term][document_id].append(position) #append the position defined above to the index term docuemnt id and the position is going to be an empty list that was just created above

    def search (self,query): #searching an inverted index that will input query for search
        terms= query.split()
        results=None
        for term in terms: #loop over query terms
            if term in self.index:
                if results is None:
                    results= set(self.index[term].keys())
                else:
                    results.intersection_update(self.index[term].keys()) #intersect all the result with the keys
        if results is None:
            return []
        else:
            search_results=[]
            for document_id in results: #loop over all results found in list
                 positions=[self.index[term][document_id] for term in terms] #list comprehension
                 search_results.append((document_id,positions))

            return search_results     
            
        



index = InvertedIndex() #insitantiating this class

index.add_document(1, "apple banana apple") #first doocuemnt is index 1 and docuemnt is apple banana apple
index.add_document(2, "banana cherry") #second document is index 2 and   
index.add_document(3,"apple cherry") #third document is index 3 and docuemnt iss apple cherry

print()
print("Docuemnts added to inverted index: ")
print(index.index)

'''
Output is 
Docuemnts added to inverted index: 
{'apple': {1: [0, 2], 3: [0]}, 'banana': {1: [1], 2: [0]}, 'cherry': {2: [1], 3: [1]}}
this means:

1. apple is in 1st document at position 0 and 2 & 3rd document position 0. 
2. banana is in 1st document postion 1 and 2nd document at position 0 
3. Cherry is in 2nd document 1st position and 3rd docuemnt 1st position
'''
print()
query="apple"
search_results=index.search(query)
print(f"Search results for '{query}': ")

if search_results==[]: #if the search result list is empty
    print("Not found")

for document_id, positions in search_results: #print the actual results
    print(f"Document Id: {document_id}")
    print(f"Position: {positions}")
    print()




