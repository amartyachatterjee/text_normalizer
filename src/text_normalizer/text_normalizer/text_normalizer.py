import html
import re
import string
from pathlib import Path

import spacy
from cleantext import clean
import contractions
from nostril import nonsense_detector as nd
from abbreviations_py.textes.abbreviator import fix
from stop_words.stop_words.stop_words import CustomStopWords

import nltk

class TextNormalizer:
    def __init__(self,
                 custom_stopwords: CustomStopWords|None=None,
                 nltk_data_path: str|Path|None=None,
                 is_remove_domain_specific_stops: bool=False,
                 is_remove_english_stops: bool=False,
                 is_remove_persons: bool=True):
        self.is_remove_domain_specific_stops = is_remove_domain_specific_stops
        self.is_remove_english_stops = is_remove_english_stops
        self.is_remove_persons = is_remove_persons
        self.nltk_data_path = nltk_data_path

        if self.nltk_data_path is not None:
            if isinstance(self.nltk_data_path, str):
                self.nltk_data_path = Path(self.nltk_data_path)
            nltk.data.path.append(self.nltk_data_path)
        from nltk.corpus import RegexpTokenizer

        self.regexp = RegexpTokenizer(r"[\w']+")

        self.my_stops = custom_stopwords if custom_stopwords is not None else CustomStopWords(self.nltk_data_path)

        self.nlp = spacy.load('en_core_web_lg')

    def convert_to_lower_case(self,text):
        return text.lower()

    def remove_whitespace(self,text):
        return text.strip()

    def remove_punctuation(self,text):
        punct_str = string.punctuation
        punct_str = punct_str.replace("'","")
        punct_str = punct_str.replace('-',"")
        return text.translate(str.maketrans('','',punct_str))

    def remove_html(self,text):
        return re.sub(r'<.*?>','',text)

    def remove_emoji(self,text):
        emoji_pattern = re.compile('['
                                   u'\U0001F600-\U0001F64F'
                                   u'\U0001F300-\U0001F5FF'
                                   u'\U0001F680-\U0001F6FF'
                                   u'\U0001F1E0-\U0001F1FF'
                                   u'\U00002702-\U000027B0'
                                   u'\U000024C2-\U0001F251'
                                   ']+', flags=re.UNICODE
                                   )
        return emoji_pattern.sub(r'', text)

    def remove_http(self,text):
        http = r"http(s)?://\S+|www\.\S+"
        return re.sub(http,"",text)

    def convert_acronyms(self,text):
        result = fix(text)
        return result

    def convert_contractions(self,text):
        result = contractions.fix(text)
        return result

    def remove_domain_specific_stopwords(self, text):
        if self.is_remove_domain_specific_stops:
            result = ' '.join([word for word in self.regexp.tokenize(text)
                               if word not in self.my_stops.domain_specific_stops])
        else:
            result = text
        return result

    def remove_english_stopwords(self, text):
        if self.is_remove_english_stops:
            result = ' '.join([word for word in self.regexp.tokenize(text)
                               if word not in self.my_stops.english_stops])
        else:
            result = text
        return result

    def remove_sentiment_custom_stopwords(self,text):
        result = ' '.join([word for word in self.regexp.tokenize(text)
                           if word not in self.my_stops.sentiment_custom_stops])
        return result

    def stem_text(self,text):
        from nltk.stem.porter import PorterStemmer
        result = ' '.join([PorterStemmer().stem(word) for word in self.regexp.tokenize(text)])
        return result

    def lemmatize_text(self,text):
        max_length = self.nlp.max_length
        full_iterations, last_iteration = divmod(len(text), max_length)
        full_iterations = 1 if full_iterations == 0 else full_iterations

        lemma_list = []
        for i in range(full_iterations):
            if len(text) <= max_length:
                tmp_text = text
            else:
                tmp_text = text[i*max_length:(i+1)*max_length]
            lemma_list.append(' '.join([token.lemma_ for token in self.nlp(tmp_text)]))

            if (len(text) > max_length) and i == full_iterations - 1:
                if last_iteration > 0:
                    tmp_text = text[max_length*(i+1):]
                    lemma_list.append(' '.join([token.lemma_ for token in self.nlp(tmp_text)]))
                    
        result = ' '.join(lemma_list)
        return result

    def discard_non_alpha(self,text):
        result = ' '.join([word for word in self.regexp.tokenize(text) if word.isalpha()])
        return result

    def keep_pos(self, text):
        tokens = self.regexp.tokenize(text)
        tokens_tagged = nltk.pos_tag(tokens)
        keep_tags = ['NN','NNS','NNP','NNPS','FW','PRP','PRPS','RB','RBR','RBS','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WPS','WRB']
        result = ' '.join([x[0] for x in tokens_tagged if x[1] in keep_tags])
        return result

    def is_crap(self,text,length):
        if length < 6:
            return False
        if nd.nonsense(text):
            return True
        else:
            return False

    def get_clean_words(self,text):
        result = ' '.join([token for token in self.regexp.tokenize(text)
                           if not self.is_crap(token,len(token))])
        return result

    def get_persons(self,text):
        max_length = self.nlp.max_length
        full_iterations, last_iteration = divmod(len(text), max_length)
        full_iterations = 1 if full_iterations == 0 else full_iterations

        person_list = []
        for i in range(full_iterations):
            if len(text) <= max_length:
                tmp_text = text
            else:
                tmp_text = text[i*max_length:(i+1)*max_length]
            person_list += self.fetch_person_list(tmp_text)

            if (len(text) > max_length) and i == full_iterations - 1:
                if last_iteration > 0:
                    tmp_text = text[max_length*(i+1):]
                    person_list += self.fetch_person_list(tmp_text)

        return list(set(person_list))

    def fetch_person_list(self,text):
        doc = self.nlp(text)

        person_list = []
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                person_list.append(ent.text)

        return list(set(person_list))

    def remove_persons(self,text):
        if not self.is_remove_persons:
            return text

        person_regex = re.compile(r'\b%s\b' % r'\b|\b'.join(map(re.escape,self.get_persons(text))), re.IGNORECASE)
        result = person_regex.sub('',text)
        return result

    def get_normalized_text(self,
                            raw_text: str,
                            is_print_cleaned_text: bool=False) -> str:
        text = str(raw_text)

        text = html.unescape(text)
        text = self.remove_whitespace(text)
        text = re.sub(r'\[.*?\]','',text)

        text = self.remove_http(text)
        text = self.remove_emoji(text)
        text = self.remove_html(text)
        text = self.convert_contractions(text)
        text = self.convert_acronyms(text)
        text = self.lemmatize_text(text)

        text = clean(text,
                     fix_unicode=True,
                     to_ascii=True,
                     lower=True,
                     no_line_breaks=True,
                     no_urls=True,
                     no_emails=True,
                     no_phone_numbers=True,
                     no_numbers=True,
                     no_digits=True,
                     no_currency_symbols=True,
                     no_punct=True,
                     replace_with_punct="",
                     replace_with_url="",
                     replace_with_email="",
                     replace_with_phone_number="",
                     replace_with_number="",
                     replace_with_digit="",
                     replace_with_currency_symbol="",
                     lang="en")

        text = self.remove_domain_specific_stopwords(text)
        text = self.remove_english_stopwords(text)
        text = self.remove_sentiment_custom_stopwords(text)
        text = self.remove_persons(text)
        text = self.discard_non_alpha(text)
        text = self.get_clean_words(text)

        if is_print_cleaned_text:
            print(f'''Cleaned text: \n\t{text}''')

        return text


