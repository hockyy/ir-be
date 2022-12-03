from bsbi import BSBIIndex
from compression import VBEPostings

# sebelumnya sudah dilakukan indexing
# BSBIIndex hanya sebagai abstraksi untuk index tersebut
BSBI_instance = BSBIIndex(data_dir='collection',
                          postings_encoding=VBEPostings,
                          output_dir='index')

queries = ["alkylated with radioactive iodoacetate",
           "psychodrama for disturbed children",
           "lipid metabolism in toxemia and normal pregnancy"]

for query in queries:
    print("Query  : ", query)
    K = 10
    # result = BSBI_instance.retrieve_tfidf(query, k=K, optimize=False)
    # result2 = BSBI_instance.retrieve_tfidf(query, k=K, optimize=True)
    result = BSBI_instance.retrieve_bm25(query, k=K, optimize=False)
    result2 = BSBI_instance.retrieve_bm25(query, k=K, optimize=True)
    print("Results:")
    print(f"{'Document Name':30} Score")
    assert len(result) == len(result2), "Optimization caused different result"
    for i in range(len(result)):
        assert (abs(result[i][0] - result2[i][0]) < 1e-8), \
            f"Optimization caused different result {result[i][0]} and {result2[i][0]}"
        print(f"{result[i][1]:30} {result2[i][0]:>.3f}")
    print()
