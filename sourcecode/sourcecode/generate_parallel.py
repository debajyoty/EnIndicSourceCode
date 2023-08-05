# Generate parallel corpora using inputs from multiple existing trnaslation system
from __future__ import print_function

import os
import subprocess
from xml.etree import ElementTree as ET
import LeBLEU.lebleu.lebleu as lb
import sys

from auth import AzureAuthClient
import requests

from googleapiclient.discovery import build
import requests.packages.urllib3.contrib.pyopenssl
import hi_index


def get_translation_using_google(service, source_sentences, source_lang_code, target_lang_code):
    """
    Get translation of given sentences using google translate service
    :param service: Google service object consisting developer key
    :param source_sentences: list of sentences to be translated
    :param source_lang_code: language code of source sentence's language
    :param target_lang_code: language code of target language
    """
    received_translations_json = service.translations().list(
        source=source_lang_code,
        target=target_lang_code,
        q=source_sentences
    ).execute()
    translations = received_translations_json['translations']
    return [translatedText['translatedText'] for translatedText in translations]


def get_translation_using_microsoft(bearer_token, source_sentences, source_lang_code, target_lang_code):
    """
    Get translation of given sentences using microsoft translate service
    :param bearer_token: bearer token got from authorisation client
    :param source_sentences: list of sentences to be translated
    :param source_lang_code: language code of source sentence's language
    :param target_lang_code: language code of target language
    """
    headers = {"Authorization ": bearer_token, 'Content-Type': 'application/xml'}
    translateUrl = "https://api.microsofttranslator.com/V2/Http.svc/TranslateArray"
    xml_string = '''<TranslateArrayRequest><AppId /><From></From><Texts></Texts><To></To></TranslateArrayRequest>'''
    xml_data = ET.fromstring(xml_string)
    for child in xml_data:
        if child.tag == 'From':
            child.text = source_lang_code
        elif child.tag == 'To':
            child.text = target_lang_code
        elif child.tag == 'Texts':
            for source_sentence in source_sentences:
                ET.SubElement(child, "string", xmlns="http://schemas.microsoft.com/2003/10/Serialization/Arrays"). \
                    text = source_sentence
    xml_stringto_send = ET.tostring(xml_data, encoding='utf-8')
    response = requests.post(translateUrl, data=xml_stringto_send, headers=headers).text
    try:
        translated_sentences = []
        root = ET.fromstring(response)
        for child in root:
            if child.tag == '{http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2' \
                            '}TranslateArrayResponse':
                for subchild in child:
                    if subchild.tag == '{http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2' \
                                       '}TranslatedText':
                        translated_sentences.append(subchild.text)
        return translated_sentences
    except Exception:
        print('error')


def align_using_ir(english_file, hindi_file, threshold):
    # get translations from google microsoft and moses
    # combine them using memt
    # then use it as query in hindi comparable corpus
    # then form sentence pairs
    inverted_index_obj = hi_index.InvertedIndex()
    index_dict = inverted_index_obj.make_index(sys.argv[2])
    N = inverted_index_obj.N
    final_en_corpus = open('final_en.corpus', 'w')
    final_hi_corpus = open('final_hi.corpus', 'w')
    english_comparable_corpus = open(english_file)
    english_sentences = english_comparable_corpus.readlines()
    english_comparable_corpus.close()
    hindi_comparable_corpus = open(hindi_file, 'r')
    hindi_sentences = hindi_comparable_corpus.readlines()
    hindi_comparable_corpus.close()
    with open('output.1best', 'r') as memt_output_file:
        translations_from_memt = memt_output_file.readlines()
        for i, translation in enumerate(translations_from_memt):
            translation = translation.rstrip()
            best_matches = hi_index.InvertedIndex().search(translation, indexDict=index_dict, N=N)[:5]
            max = 0
            max_i = None
            for (sentence_index, score) in best_matches:
                sentence_similiraity_score = hindiLeBLEU.eval_single(hindi_sentences[sentence_index].rstrip(),
                                                                     translation)
                print(sentence_similiraity_score)
                if sentence_similiraity_score > max:
                    max = sentence_similiraity_score
                    max_i = sentence_index
            if max > threshold:
                final_en_corpus.write(english_sentences[i])
                final_hi_corpus.write(hindi_sentences[max_i])
    final_hi_corpus.close()
    final_en_corpus.close()


def neighbourhood_alignment(english_file, hindi_file, threshold):
    # get translations from google microsoft and moses
    # combine them using memt
    # then use it as query in hindi comparable corpus
    # then form sentence pairs
    final_en_corpus = open('final_en_neighbour.corpus', 'w')
    final_hi_corpus = open('final_hi_neighbour.corpus', 'w')
    english_comparable_corpus = open(english_file)
    english_sentences = english_comparable_corpus.readlines()
    english_comparable_corpus.close()
    hindi_comparable_corpus = open(hindi_file, 'r')
    hindi_sentences = hindi_comparable_corpus.readlines()
    hindi_comparable_corpus.close()
    with open('output.1best', 'r') as memt_output_file:
        translations_from_memt = memt_output_file.readlines()
        last_match = 0
        for i, translation in enumerate(translations_from_memt):
            translation = translation.rstrip()
            max = 0
            max_i = None
            for j in range(last_match - 3, last_match + 3):
                if j < 0:
                    pass
                sentence_similiraity_score = hindiLeBLEU.eval_single(hindi_sentences[j].rstrip(),
                                                                     translation)
                print(sentence_similiraity_score)
                if sentence_similiraity_score > max:
                    max = sentence_similiraity_score
                    max_i = j
            last_match = max_i
            if max > threshold:
                final_en_corpus.write(english_sentences[i])
                final_hi_corpus.write(hindi_sentences[max_i])
    final_hi_corpus.close()
    final_en_corpus.close()


if __name__ == '__main__':
    if len(sys.argv) == 4:
        english_file_name = sys.argv[1]
        hindi_file_name = sys.argv[2]
        google_translated_file_name = english_file_name + ".higoogle"
        if not os.path.exists(google_translated_file_name):
            print("{} file not exists".format(google_translated_file_name))
            exit(1)
        microsoft_translated_file_name = english_file_name + ".himicro"
        if not os.path.exists(microsoft_translated_file_name):
            print("{} file not exists".format(microsoft_translated_file_name))
            exit(1)
        moses_translated_file_name = english_file_name + ".himoses"
        if not os.path.exists(moses_translated_file_name):
            print("{} file not exists".format(moses_translated_file_name))
            exit(1)
        memt_root_dir = "~/MEMT/MEMT/"
        subprocess.run(
            memt_root_dir + 'Alignment/match.sh' + ' ' + google_translated_file_name + ' ' + moses_translated_file_name +
            ' ' + microsoft_translated_file_name + ' > dev.matched',
            shell=True)
        subprocess.run(
            '~/MEMT/MEMT/scripts/simple_decode.rb 2000 decoder_config dev.matched output', shell=True)
        hindiLeBLEU = lb.HindiModifiedLeBLEU()
        if sys.argv[3] == '-n':
            neighbourhood_alignment(english_file_name, hindi_file_name, 0.5)
        elif sys.argv[3] == '-i':
            align_using_ir(english_file_name,hindi_file_name,0.5)
        else:
            print('Invalid argument use -n or -i')
    else:
        print("""Insufficient arguments passed.
        Usage:
        python3 generate_parallel.py english_corpus hindi_corpus [-i]|[-n]
            -i: do searching using IR based system
            -n: do neighbourhood search
        """)





