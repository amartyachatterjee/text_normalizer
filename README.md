# text_normalizer
A comprehensive normalizing API for any English text cleaning and normalization

## **Installation:**
```
pip install git+https://github.com/amartyachatterjee/text_normalizer.git
```

## **Parameters**
```
- custom_stopwords: CustomStopWords | None = None -> Refer to example below
- nltk_data_path: str | Path | None = None -> Refer to example below
- is_remove_domain_specific_stops: bool = False -> Set to True if you want to remove domain-specific stop words you used to initialize the stop_words object. Must send a stop_words object initialized with domain-specific stop words in first argument
- is_remove_english_stops: bool = False -> Set to True if you want to remove English stop words assorted from several different sources
- is_remove_persons: bool = True -> Set to False if you do not want person names (identified using spacy's NER) removed from text
```
  
## **Usage:**
```
from pathlib import Path
from stop_words.stop_words.stop_words import CustomStopWords
from text_normalizer.text_normalizer.text_normalizer import TextNormalizer

nltk_data_path = Path("C:/path/to/nltk_data")

my_stop = CustomStopWords(domain_specific_stops=['stp1','custstop'],
                          nltk_data_path=nltk_data_path)
tn = TextNormalizer(custom_stopwords=my_stop,
                    nltk_data_path=nltk_data_path,
                    is_remove_domain_specific_stops=True)

text = f'''What'll be super fun to play around with Python code. Love it David! Test for domain stops like custstop :-) sdkhfgyudeewr874365843750tefxbchjgkjfdv'''
nt = tn.get_normalized_text(text, 
                            is_print_cleaned_text=True)
```
  
