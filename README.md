# VerbMiner

**Do you want to learn how good writers use verbs? This tool can help you summarize verbs from PDF.**
The input could be either a PDF or a txt file (e.g., academic papers, textbooks, magazines). The output is a csv file summarizing all the verbs found in the input. The next step would be to visualize the verbs and to identify the novel ones.

### Example input
![Example input](http://i.imgur.com/1zptycB.png)

### Example output
![Example output](http://i.imgur.com/2s0dKDq.png)

### Usage
`python src/verbminer.py [path_to_input]`

### Dependencies
* [nltk](http://www.nltk.org/)
* [pdfminer](https://pypi.python.org/pypi/pdfminer/)
