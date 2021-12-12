import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tokenize import TweetTokenizer
tknzr = TweetTokenizer()

translater=Translator()
    
st.write("""
# LIVE SPEECH TRANSLATOR, SENTIMENT ANALYSER AND SUMMARISER
This web-app detects speech, translates it summarises it, and detects **Emotion**!
""")
option = st.selectbox('PICK YOUR LANGUAGE!',('af - afrikaans',
    'sq - albanian',   'am - amharic',    'ar - arabic',    'hy - armenian',    'az - azerbaijani',    'eu - basque',    'be - belarusian',
    'bn - bengali',    'bs - bosnian',    'bg - bulgarian',    'ca - catalan',    'ceb - cebuano',    'ny - chichewa',    'zh-cn - chinese (simplified)',
    'zh-tw - chinese (traditional)',    'co - corsican',    'hr - croatian',    'cs - czech',    'da - danish',    'nl - dutch',    'en - english',
    'eo - esperanto',    'et - estonian',    'tl - filipino',    'fi - finnish',    'fr - french',    'fy - frisian',    'gl - galician',    'ka - georgian',
    'de - german',    'el - greek',    'gu - gujarati',    'ht - haitian creole',    'ha - hausa',    'haw - hawaiian',    'iw - hebrew',    'he - hebrew',
    'hi - hindi',    'hmn - hmong',    'hu - hungarian',    'is - icelandic',    'ig - igbo',    'id - indonesian',    'ga - irish',    'it - italian',
    'ja - japanese',    'jw - javanese',    'kn - kannada',    'kk - kazakh',    'km - khmer',    'ko - korean',    'ku - kurdish (kurmanji)',    'ky - kyrgyz',
    'lo - lao',    'la - latin',    'lv - latvian',    'lt - lithuanian',    'lb - luxembourgish',    'mk - macedonian',    'mg - malagasy',    'ms - malay',
    'ml - malayalam',    'mt - maltese',    'mi - maori',    'mr - marathi',    'mn - mongolian',    'my - myanmar (burmese)',    'ne - nepali',    'no - norwegian',
    'or - odia',    'ps - pashto',    'fa - persian',    'pl - polish',    'pt - portuguese',    'pa - punjabi',    'ro - romanian',    'ru - russian',
    'sm - samoan',    'gd - scots gaelic',    'sr - serbian',    'st - sesotho',    'sn - shona',    'sd - sindhi',    'si - sinhala',    'sk - slovak',
    'sl - slovenian',    'so - somali',    'es - spanish',    'su - sundanese',    'sw - swahili',    'sv - swedish',    'tg - tajik',    'ta - tamil',
    'te - telugu',    'th - thai',    'tr - turkish',    'uk - ukrainian',    'ur - urdu',    'ug - uyghur',    'uz - uzbek',    'vi - vietnamese',
    'cy - welsh',    'xh - xhosa',    'yi - yiddish',    'yo - yoruba',    'zu - zulu',))
lang = option[0:2]
if st.button("Click me"):
    r=sr.Recognizer()
    with sr.Microphone() as source:
        st.write("YOU MAY SPEAK...")
        audio=r.listen(source)
        try:
            text=r.recognize_google(audio)
            st.write("You  said :",text)
            out = translater.translate(text,dest=lang)
            st.write(out.text)
            blob = TextBlob(text)
            st.write('TONE:',blob.sentiment.polarity)
            if int(blob.sentiment.polarity) > 0:
                st.write('YOU SOUND POSITIVE TO THE READERS')
            
            from lib.punctuator import Punctuator
            P = Punctuator(
                tokenize_func=tknzr.tokenize)
            P.load()
            st.write(P.punctuate(text))
            stopWords = set(stopwords.words("english"))
            words = word_tokenize(text)
            freqTable = dict()
            for word in words:
                word = word.lower()
                if word in stopWords:
                    continue
                if word in freqTable:
                    freqTable[word] += 1
                else:
                    freqTable[word] = 1
            sentences = sent_tokenize(text)
            sentenceValue = dict()
            for sentence in sentences:
                for word, freq in freqTable.items():
                    if word in sentence.lower():
                        if sentence in sentenceValue:
                            sentenceValue[sentence] += freq
                        else:
                            sentenceValue[sentence] = freq
            sumValues = 0
            for sentence in sentenceValue:
                sumValues += sentenceValue[sentence]
            # Average value of a sentence from the original text
            average = int(sumValues / len(sentenceValue))

            # Storing sentences into our summary.
            summary = ''
            for sentence in sentences:
                if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
                    summary += " " + sentence
            st.write(summary)
        except:
            st.write("Please say again ..")
        
