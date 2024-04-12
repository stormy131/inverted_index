# Inverted Index

## Structure
- main.py - main script for building the index, processing input queries and evaluation
- invert_index.py - contains implementation of the inverted-index data structure and
corresponding algorithms for processing boolean operators (intersection, union and
negation).
- query_parser.py - contains implementation of the Parser class

## Analysis
NO TEXT NORMALIZATION was applied to the input documents, so that may be a reason
for such low precision/recall scores. Also, as it was manually assured, there are many
documents which are annotated as relevant to some query but did not contain query tokens.
Such intuitive relevance (based on the semantic meaning of the document content)
decreased the effectiveness of the inverted index (as a data structure).

NOTE: In my solution I’ve used the external module `lxml` to parse the input .xml files and
corresponding files of the queries. At first, I was trying to work with Python built-in module
xml, but it was not able to work with several input files. The reason is that some of the input
files have invalid xml format (unclosed tags, etc.) or contain empty tags “< >”. Lxml parsers
support “recovery mode”, which can omit those places in files, and continue building the tag
tree.

## How to run:
To run my solution:
1) Create virtual environment in the project directory and activate it
``` shell
python -m venv venv
. ./venv/bin/activate
```
2) Install required dependency from the requirements.txt. In the project directory:
```
pip install -r requirements.txt
```
3) The data folder “data” (which contains query files, files with “ground truth” relevance
and corresponding directories for each language with documents to process) is
assumed to be located in the root of project directory
4) Run the script:
```
python main.py
```
5) Results for queries in each language and evaluation scores will be available in the
“output” folder.
