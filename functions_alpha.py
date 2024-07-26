import fitz
import spacy
import re
from googletrans import Translator
from requests.exceptions import RequestException
from tkinter import messagebox

# region By Words


def extract_w(pdfpathfoo):
    foolist = []
    seen_words = set()
    try:
        doc = fitz.open(pdfpathfoo)
        translation_table = str.maketrans("", "", ".,!?;:-")
        for _ in range(len(doc)):
            page = doc.load_page(_)
            text = page.get_text()
            words = text.split()
            cleaned_words = [___.translate(translation_table) for ___ in words]
            for __ in cleaned_words:
                if __ not in seen_words:
                    foolist.append(__)
                    seen_words.add(__)
        doc.close()
    except (FileNotFoundError, PermissionError, IOError) as e:
        messagebox.showinfo("Permiso de archivo", f"Error abriendo archivo PDF: {e}")
        raise
    return foolist


def cleansing_w(foolist, model_foo):
    try:
        nlp = spacy.load(model_foo)
    except (OSError, IOError) as e:
        messagebox.showinfo("Error de modelo", f"Error cargando el modelo: {e}")
        raise
    proper_nouns = []
    cleaned = list(foolist)
    for _ in foolist:
        try:
            do1 = nlp(_)
            for __ in do1:
                if __.pos_ == 'PROPN' or __.ent_type_ in ['PER', 'ORG', 'X', 'LOC']:
                    proper_nouns.append(__.text)
        except Exception as e:
            print(f"Error processing word '{_}' with spaCy: {e}")
            continue
    cleaned = [_ for _ in cleaned if _ not in proper_nouns]
    cleaned_lower = [_.lower() for _ in cleaned]
    return cleaned_lower


def lemmatization_w(fooset3, model_foo):
    try:
        nlp = spacy.load(model_foo)
    except (OSError, IOError) as e:
        messagebox.showinfo("Error de modelo", f"Error cargando el modelo: {e}")
        raise
    lemmatized_words = []
    cleaned_unique = []
    for _ in range(len(fooset3)):
        try:
            do2 = nlp(fooset3[_])
            for __ in do2:
                lemmatized_words.append(__.lemma_)
        except Exception as e:
            print(f"Error lemmatizing word '{_}' with spaCy: {e}")
            continue
    [cleaned_unique.append(_) for _ in lemmatized_words if _ not in cleaned_unique]
    return cleaned_unique


def translation_w(fooset4, source, destin):
    translator = Translator()
    translated_words = []
    for _ in range(len(fooset4)):
        try:
            translated = translator.translate(fooset4[_], src=source, dest=destin)
            translated_words.append(translated.text)
        except TypeError:
            translated_words.append("Translation Error")
            continue
        except (RequestException, Exception) as e:
            messagebox.showinfo("Falla de conexión",
                                f"Error conectando al servicio de traducción o traduciendo palabra: {e}")
            raise
    return translated_words


# endregion

# region By Sentences


def extract_s(pdfpathfoo):
    foolist = []
    seen_words = set()
    try:
        doc = fitz.open(pdfpathfoo)
        sentence_splitter = re.compile(r'[.!?]')
        for _ in range(len(doc)):
            page = doc.load_page(_)
            text = page.get_text()
            sentences = sentence_splitter.split(text)
            for __ in sentences:
                cleaned_sentence = __.replace('\n', '').strip()
                if __ not in seen_words:
                    foolist.append(cleaned_sentence)
                    seen_words.add(cleaned_sentence)
        doc.close()
    except (FileNotFoundError, PermissionError, IOError) as e:
        messagebox.showinfo("Permiso de archivo", f"Error abriendo archivo PDF: {e}")
        raise
    return foolist


def translation_s(fooset4, source, destin):
    translator = Translator()
    translated_sentences = []
    for _ in range(len(fooset4)):
        try:
            translated = translator.translate(fooset4[_], src=source, dest=destin)
            translated_sentences.append(translated.text)
        except TypeError:
            continue
        except (RequestException, Exception) as e:
            messagebox.showinfo("Falla de conexión",
                                f"Error conectando al servicio de traducción o traduciendo palabra: {e}")
            raise
    return translated_sentences


# endregion

# region By Parragraphs


def extract_p(pdfpathfoo):
    foolist = []
    seen_words = set()
    try:
        doc = fitz.open(pdfpathfoo)
        for _ in range(len(doc)):
            page = doc.load_page(_)
            text = page.get_text()
            sentences = text.split(". \n")
            for __ in sentences:
                if __ not in seen_words:
                    cleaned_sentence = __.replace('\n', '').strip()
                    foolist.append(cleaned_sentence)
                    seen_words.add(cleaned_sentence)
        doc.close()
    except (FileNotFoundError, PermissionError, IOError) as e:
        messagebox.showinfo("Permiso de archivo", f"Error abriendo archivo PDF: {e}")
        raise
    return foolist


def translation_p(fooset4, source, destin):
    translator = Translator()
    translated_sentences = []
    for _ in range(len(fooset4)):
        try:
            translated = translator.translate(fooset4[_], src=source, dest=destin)
            translated_sentences.append(translated.text)
        except TypeError:
            continue
        except (RequestException, Exception) as e:
            messagebox.showinfo("Falla de conexión",
                                f"Error conectando al servicio de traducción o traduciendo palabra: {e}")
            raise
    return translated_sentences


# endregion
