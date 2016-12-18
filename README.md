# Seminarthesis

scripts/automate.py
loads list of correspondences with related html pages and compares content. Used to determine the label of the correspondences

scripts/count.py
counts pages in warc archive

scripts/count_pages.py
collects statistics of content of warc files, e.g. numbers of products, errors, or other pages (like disclaimers)

scripts/extract_records.py
extract some records from warc file. can be used for testing

scripts/extracthtml.py
extracts records from warc and saves them as html

scripts/extracturls.py
extracts urls contained in header of warc

scripts/sample_creator.py
creates random sample of warc files

scripts/warc_id.py
assigns new id to each warc record

scripts/dedup/SparsLSHMaster/
LSH library for sparse matrices

scripts/dedup/dedup.py
performs LSH and outputs correspondences with distance threshold

scripts/dedup/deduplicator.py
uses LSH to deduplicate dataset

scripts/dedup/gold.py
creates gold standard taking distance threshold into account

scripts/dedup/preprocessing
performs preprocessing, i.e. remove html and script and convert everything into sparse matrices of tfidf vectors
