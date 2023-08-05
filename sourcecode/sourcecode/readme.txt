This algorithm can be used to generate parallel corpus from comparable corpus (Combination of various machine translation system's output)
Requirement:
MEMT should be installed. Follow: 


First in SimilarityApi directory execute following command:
java -cp similarityapi.jar:py4j-0.10.5.jar:. Score

Then, start MEMT server through
MEMT/MEMT/scripts/server.sh --lm.file MEMT/corpora_train.lm.final.arpa.hi --port 2000

Also mention memt root directory inside script for valid execution of script.

Then finally execute general_parallel.py script to generate parallel corpus in following way.
Usage:
        python3 generate_parallel.py english_corpus hindi_corpus [-i]|[-n]
            -i: do searching using IR based system
            -n: do neighbourhood search
            
            
            
            
            
            
            
Cite:
Anasua Banerjee, Vinay Kumar, Achyut Shankar, Rutvij H. Jhaveri, Debajyoty Banik, Automatic Resource Augmentation for Machine Translation in Low Resource Language: EnIndic Corpus, ACM Transactions on Asian and Low-Resource Language Information Processing, 2023.
