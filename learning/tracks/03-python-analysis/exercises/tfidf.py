""" Use tf-idf to identify the most important words in a document
relative to other documents in a corpus. """


from argparse import ArgumentParser
from collections import Counter
from math import log
from pathlib import Path
import re
import sys


class TfidfCalculator:
    """ Determine the top n important words in the file according to the tf-idf metric
    
    Attributes:
        tf (dict[str, Counter]): Maps each filename (str) to a Counter object
            containing the word frequencies (term counts) for that document.
        df (Counter): A Counter tracking document frequencies, mapping each
            unique word (str) to the total number of documents in which it appears.
    """
    def __init__(self):
        self.tf = {}
        self.df = Counter()
        
    def read_file(self, filename):
        """ Read files from a directory and update term and document frequency counts.
        
        Args: 
            filename (str): The path to the file to be read.
        
        Returns: 
            None.
        
        Side effects: 
            Adds a new entry to self.tf mapping filename to a Counter of its words.
            Increments the count in self.df by 1 for each unique word found in the file.
        """
        with open (filename, 'r', encoding="utf-8") as file:
           script = file.read()
           word = get_words(script)
           
           self.tf[filename] = Counter(word)
           self.df.update(set(word))
               
    def important_words(self, filename, num_words = 10):
        """ Calculate and return the top words in a file ranked by TF-IDF score.
        
        Args: 
            filename (str): The path or identifier of a previously read file in the corpus.
            num_words (int or None, optional): The maximum number of words to return. 
                If None, returns all words in the document. Defaults to 10.
        
        Returns: 
            dict: A mapping of words to their TF-IDF scores, ordered from highest to lowest score.
       
        Side effects:
            None.
        """
        if num_words is not None and not isinstance(num_words, int):
            raise TypeError("num_words must be an int or None")
        
        total_words = sum(self.tf[filename].values())
        total_documents = len(self.tf)
        
        tfidf_scores = {
            word: (count / total_words) * log(total_documents / self.df[word])
            for word, count in self.tf[filename].items()
        }
    
        word_score = sorted(tfidf_scores, key = tfidf_scores.get, reverse = True)[:num_words]

        return {word: tfidf_scores[word] for word in word_score}
    
def get_words(s):
    """ Extract a list of words from string s.

    Args:
        s (str): a string containing one or more words.

    Returns:
        list of str: a list of words from s converted to lower-case.
    """
    words = list()
    s = re.sub(r"--+", " ", s)
    for word in re.findall(r"[\w'-]+", s):
        word = word.strip("'-_")
        if len(word) > 0:
            words.append(word.lower())
    return words


def main(directory, files, pattern="*", num_words=10):
    """ Read files from a directory, and identify the most important
    words in one or more specified files.
    
    Args:
        directory (str or Path): path to a directory containing a corpus
            of texts to read in.
        files (list of (str or Path)): paths to files for which the user
            wants to identify the most important words.
        pattern (str): glob pattern for files to include from directory.
            (Default: "*")
        num_words (int): the number of important words to report for
            each specified file.
    
    Side effects:
        Writes to stdout.
    """
    calc = TfidfCalculator()
    for document in Path(directory).glob(pattern):
        calc.read_file(str(document))
    if not files:
        files = sorted(calc.tf)
    for n, filename in enumerate(files):
        if n != 0:
            print()
        print(f"Most important words in f{str(filename)}:")
        important = calc.important_words(str(filename), num_words=num_words)
        for word, score in important.items():
            print(f"  {word}: {score}")


def parse_args(arglist):
    """ Parse command-line arguments.
    
    Required command-line argument:
    
        directory: a path to a directory of files to read in.
        
    Optional command-line arguments:
    
        files: zero or more files for which to identify the most
            important words. If no files are specified, important words
            will be output for all files.
        -p / --pattern: a glob pattern indicating which files in the
            directory to read in (default: "*", meaning read all files
            in the directory)
        -n / --num_words: the number of words to display for each file
            (default: 10)
            
    Args:
        arglist (list of str): command-line arguments to parse.
        
    Returns:
        A namespace with the following variables (see above for
        descriptions):
            directory (pathlib.Path)
            files (list of pathlib.Path)
            pattern (str)
            num_words (int)
    """
    parser = ArgumentParser()
    parser.add_argument("directory", type=Path,
                        help="directory containing documents to read in")
    parser.add_argument("files", type=Path, nargs="*",
                        help="file(s) you want to identify important words in")
    parser.add_argument("-p", "--pattern", default="*",
                        help="glob pattern specifying which files to read in")
    parser.add_argument("-n", "--num_words", type=int, default=10,
                        help="number of words to display (default is 10)")
    args = parser.parse_args(arglist)
    for path in args.files:
        if not path.exists():
            sys.exit(f"file {str(path)} not found")
        pattern = args.directory / args.pattern
        if not path.match(str(pattern)):
            sys.exit(f"file {str(path)} is not in the specified corpus"
                     f" ({str(pattern)})")
    return args


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.directory, args.files, pattern=args.pattern,
         num_words=args.num_words)
