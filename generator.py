import os

from engine.bsbi import BSBIIndex
from engine.compression import VBEPostings

def generate_bsbi():
  output_dir = os.path.join(os.getcwd(), "engine", "index")
  data_dir = os.path.join(os.getcwd(), "engine", "collection")
  BSBI_instance = BSBIIndex(data_dir=data_dir,
                            postings_encoding=VBEPostings,
                            output_dir=output_dir)
  # BSBI_instance.index()  # memulai indexing!
  return BSBI_instance

if __name__ == '__main__':
    generate_bsbi()