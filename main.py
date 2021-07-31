import requests
from bs4 import BeautifulSoup
import spacy as sp
from nltk.corpus import stopwords
from stop_words import get_stop_words
import string

"""
Compiled a list of stop words

Combined stop words list from libraries including:

- nltk
- spacy
- stop_words

"""

stop_words_list = get_stop_words('english')
nltk_list = stopwords.words('english')
sp = sp.load('en_core_web_sm')
spacy_stopwords = sp.Defaults.stop_words
combined_stop_words = nltk_list + list(spacy_stopwords) + stop_words_list
stop_words = set(combined_stop_words)


"""
Word count helper function used in main function

param: text (str)
return: dictionary with count of each word in text in descending order

"""

def count_words(text):
    word_counts = {}

    # Removes random punctuation - added em dash, dash, and curved apostrophe into list of punctuation
    punct = string.punctuation
    punct += "—–‘"
    text = text.translate(str.maketrans(punct, ' ' * len(punct))).replace(' '*4, ' ').replace(' '*3, ' ').replace(' '*2, ' ').strip()
    words = text.lower().split()

    # Gets word count for all words that aren't stop words or numbers/dates or single letters
    for word in words:
        if (word in word_counts) and (word not in stop_words) and (word.isdigit() == False) and (len(word) != 1):
            word_counts[word] += 1
        elif (word not in word_counts) and (word not in stop_words) and (word.isdigit() == False) and (len(word) != 1):
            word_counts[word] = 1

    # Sort dictionary so most frequent words are at the top
    sorted_count = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # Reset to return as dictionary instead of list of tuples
    word_counts = {}
    for i in range(len(sorted_count)):
        word_counts[sorted_count[i][0]] = sorted_count[i][1]

    return word_counts


"""
Function to print out the section name, frequent words, and links
of a Wikipedia page

params: Wikipedia URL (str)
return: print statements for section name, frequent words, and links in order of page

"""

def WikipediaScraper(URL):

    # GET request to Wikipedia page
    page = requests.get(URL)

    # Get the Wiki page content
    soup = BeautifulSoup(page.content, "html.parser")

    # Dictionary that will hold section text
    wiki_holder = {}

    # Dictionary that will hold section links
    links_holder = {}

    # Get all sections (*Note: sections have h2 tag and subsections have h3 tag)
    sections = soup.find_all("h2")
    for section in sections:

        # Condition to only catch section and not other h2 tags
        if section.find(class_='mw-headline'):

            # Get section name
            section_name = section.find(class_='mw-headline')
            section_name = section_name.text

            # Print out the section name
            print('Section Name: ', section_name)

            # Initialize section name within respective dictionaries
            wiki_holder[section_name] = []
            links_holder[section_name] = []

            # Loop through html tags
            for para in section.find_next_siblings():

                # Stop once it gets to next section headline
                if para.find(class_='mw-headline') and para.name == 'h2':
                    headline = para.find(class_='mw-headline')
                    if headline['class'][0]:
                        break

                # Will hold all content in section including citation warning box
                wiki_holder[section_name].append(para)

                # Extract links in section including links for images
                if para.find('a'):
                    links = para.find_all('a')
                    for link in links:
                        if link.has_attr('href'):

                            # Replace en-dash so that link isn't broken
                            if '–' in link['href']:
                                link['href'] = link['href'].replace("–", '%E2%80%93')

                            # Replace em-dash so that link isn't broken
                            if '—' in link['href']:
                                link['href'] = link['href'].replace("–", '%E2%80%94')

                            # Replace single apostrophe in link so that link isn't broken
                            if "'" in link['href']:
                                link['href'] = link['href'].replace("'", '%27')

                            # Replace double apostrophe in link so that link isn't broken
                            if '"' in link['href']:
                                link['href'] = link['href'].replace('"', '%22')

                            # Replace parenthesis in link so that link isn't broken
                            if ('(' in link['href']) and (')' in link['href']):
                                link['href'] = link['href'].replace('(', '%28')
                                link['href'] = link['href'].replace(')', '%29')

                            # Add to partial links so link is accessible
                            if (link['href'][:6] == '/wiki/') or (link['href'][:3] == '/w/'):
                                links_holder[section_name].append('https://en.wikipedia.org' + link['href'])
                            elif link['href'][:10] == '#cite_ref-' or link['href'][:11] == '#cite_note-':
                                links_holder[section_name].append(URL + link['href'])
                            else:
                                if 'https://' not in link['href']:
                                    links_holder[section_name].append('https://' + link['href'])
                                else:
                                    links_holder[section_name].append(link['href'])

            # Combines all the text in section and does frequent word count
            combined = ''.join([content.text for content in wiki_holder[section_name]])
            section_word_count = count_words(combined)

            # Print out top 15 word count in section
            count = 0
            top_25_word_count = {}
            for key, value in section_word_count.items():
                top_25_word_count[key] = value
                count += 1
                if count == 25:
                    break

            print('Top 25 word count for ' + section_name + ': ', top_25_word_count)

            # Print out links in section
            print('Links in ' + section_name + ': ', links_holder[section_name])

            # Separator so that outputs are easier to read
            print('─' * 25)


"""
Call the main function to test it out!
"""

# Initialize the Wiki page URL as a string, change out the URL to test out other Wiki pages

# Example URLs:
# URL = "https://en.wikipedia.org/wiki/United_States_Department_of_State"
# URL = 'https://en.wikipedia.org/wiki/Julianne_Moore'
# URL = 'https://en.wikipedia.org/wiki/Federal_government_of_the_United_States'
# URL = 'https://en.wikipedia.org/wiki/Roblox'
URL = 'https://en.wikipedia.org/wiki/Minecraft'
# URL = 'https://en.wikipedia.org/wiki/Poptropica'


# Call the function
WikipediaScraper(URL)

