# Wikipedia-Scraper

This repository contains a Python script that will take a Wikipedia page URL as input and print out the page's sections, the frequent words within each section (excluding stop words), and the links contained each section. To access this code, you can find it in main.py (scroll all the way to the bottom of main.py and you can designate a URL to see  and test out how the script functions).


### What I Did

---

To give some idea as to how this script works, I had first compiled a list of stopwords from various libraries and combined them into a singular list of 411 stop words. The libraries that I ended up using to get these stop words include NLTK, Spacy, and Stop_Words.

I wrote a helper function (called count_words) to take the text within a section and return the word count of all words within the section. The word count is returned as a dictionary that is sorted in descending order so that the most frequent words can be seen first.

Lastly, I wrote the main function that uses methods from Beautiful Soup to read the contents of the Wiki page, print out the section names of the Wiki page (section names were typically under an h2 tag and a class called mw-headline), uses the helper function to print out the word frequency dictionary, and print out an array containing the links in each section.


### What Does The Output Look Like

---
