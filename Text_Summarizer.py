# ----------------------------------TEXT SUMMARIZER----------------------------#

# Importing Libraries
import streamlit as st
import spacy
import heapq

# Loading spacy model
nlp = spacy.load("en_core_web_sm")


# FUNCTION for SUMMARIZATION
def summarize_text(text, max_sentences=None, percentage=None):
    doc = nlp(text)
    word_frequencies = {}

    # Building word frequency table
    for word in doc:
        if not word.is_stop and not word.is_punct:
            word_lower = word.text.lower()
            word_frequencies[word_lower] = word_frequencies.get(word_lower, 0) + 1

    # Normalizing frequencies
    max_freq = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] /= max_freq

    # Score sentences
    sentence_scores = {}
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in word_frequencies:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word.text.lower()]

    # Decide how many sentences to pick
    sentence_tokens = list(doc.sents)
    if percentage:
        select_length = max(1, int(len(sentence_tokens) * (percentage / 100)))
    else:
        select_length = max_sentences

    # Get top sentences
    summary_sentences = heapq.nlargest(select_length, sentence_scores, key=sentence_scores.get)
    summary = " ".join([sent.text for sent in summary_sentences])
    return summary


# ------------------- Streamlit UI -------------------
st.title("Text Summarizer")
st.write("Paste your text below and get a summary.")

text_input = st.text_area("Enter text:", height=400)

mode = st.radio("Choose summarization mode:", ["Fixed Sentences", "Percentage"])

if mode == "Fixed Sentences":
    num_sentences = st.slider("Number of sentences in summary", 1, 20, 5)
else:
    percentage = st.slider("Summary length (% of original text)", 20, 90, 40)

if st.button("Summarize"):
    if text_input.strip():
        if mode == "Fixed Sentences":
            summary = summarize_text(text_input, max_sentences=num_sentences)
        else:
            summary = summarize_text(text_input, percentage=percentage)

        st.subheader("Summary")
        st.write(summary)
    else:
        st.warning("Please enter some text first.")