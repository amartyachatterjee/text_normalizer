from setuptools import setup

setup(
    name='text_normalizer',
    version='0.1.0',
    description='An API to return normalized text after scrubbing it. Requires stop_words package.',
    # long_description=open('README.md').read(),
    author='Amartya Chatterjee',
    author_email='amartya.chatterjee@gmail.com',
    license='MIT',

    install_requires=[
        'spacy',
        'gensim',
        'nltk',
        'numpy==1.26.4',
        'pandas',
        'clean-text',
        'pyspellchecker',
        'nose',
        'contractions',
        'requests',
        'build',
        'unidecode',
        'setuptools',
        'nostril @ git+https://github.com/casics/nostril.git',
        'stop_words @ git+https://github.com/amartyachatterjee/stop_words.git',
        'en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl',
        'en_core_web_lg @ https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.8.0/en_core_web_lg-3.8.0-py3-none-any.whl',
        'abbreviations_py @ git+https://github.com/prajwalkhairnar/abbreviations_py.git'
    ],
    dependency_links=[
        '''https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl''',
        '''https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.8.0/en_core_web_lg-3.8.0-py3-none-any.whl'''
    ]
)
