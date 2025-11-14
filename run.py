import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import PyPDF2
import docx
import os

# ---------------------- Text Reading ----------------------
def read_file(filepath):
    text = ""
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
    elif ext == ".docx":
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

# ---------------------- Summarization ----------------------
def summarize_text(text):
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)

    freqTable = dict()
    for word in words:
        word = word.lower()
        if word not in stopWords:
            freqTable[word] = freqTable.get(word, 0) + 1

    sentences = sent_tokenize(text)
    sentenceValue = dict()
    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                sentenceValue[sentence] = sentenceValue.get(sentence, 0) + freq

    average = sum(sentenceValue.values()) / len(sentenceValue)
    summary = ' '.join([sentence for sentence in sentences if sentenceValue.get(sentence, 0) > 1.2 * average])
    return summary

# ---------------------- Sentiment Analysis ----------------------
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    sentiment = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
    return sentiment, polarity, subjectivity

# ---------------------- Dark Theme Styling ----------------------

def apply_dark_theme(win):
    win.configure(bg="#1e1e1e")
    style = {
        "bg": "#2e2e2e",
        "fg": "#ffffff",
        "font": ("Segoe UI", 12),
        "insertbackground": "white"
    }
    return style
# ---------------------- Text Summarizer Window ----------------------
def open_summarizer():
    def load_file():
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")])
        if path:
            text = read_file(path)
            input_text.delete(1.0, tk.END)
            input_text.insert(tk.END, text)

    def summarize():
        text = input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter or upload text first.")
            return
        summary = summarize_text(text)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, summary)
        stats_label.config(text=f"Original Length: {len(text)} | Summary Length: {len(summary)}")

    win = tk.Tk()
    win.title("Text Summarizer")
    win.geometry("1000x750")
    win.configure(bg="#1e1e1e")
    win.columnconfigure(0, weight=1)
    win.rowconfigure(1, weight=1)
    styles = apply_dark_theme(win)

    # Title
    tk.Label(win, text="Content Summarizer", font=("Segoe UI", 18, "bold"),
             bg="#1e1e1e", fg="#00bfff").grid(row=0, column=0, pady=10, sticky="n")

    # Upload Button
    upload_btn = tk.Button(win, text="Upload PDF/DOCX", command=load_file,
                           font=("Segoe UI", 10), bg="#444", fg="white")
    upload_btn.grid(row=1, column=0, pady=5)

    # Input Label & Text
    tk.Label(win, text="Input Text:", font=("Segoe UI", 14, "bold"),
             bg="#1e1e1e", fg="#aaaaaa").grid(row=2, column=0, sticky="w", padx=20)
    input_text = ScrolledText(win, height=10, wrap=tk.WORD, **styles)
    input_text.grid(row=3, column=0, padx=20, sticky="nsew")

    # Summarize Button (Centered)
    summarize_btn = tk.Button(win, text="Summarize", command=summarize,
                              font=("Segoe UI", 10, "bold"), bg="#00bfff", fg="black")
    summarize_btn.grid(row=4, column=0, pady=10)

    # Output Label & Text
    tk.Label(win, text="Summary Output:", font=("Segoe UI", 14, "bold"),
             bg="#1e1e1e", fg="#aaaaaa").grid(row=5, column=0, sticky="w", padx=20)
    output_text = ScrolledText(win, height=10, wrap=tk.WORD, **styles)
    output_text.grid(row=6, column=0, padx=20, sticky="nsew")

    # Stats Label
    stats_label = tk.Label(win, text="", font=("Segoe UI", 12), bg="#1e1e1e", fg="white")
    stats_label.grid(row=7, column=0, pady=5)

    # Back Button
    tk.Button(win, text="Back to Home", command=lambda: [win.destroy(), home_screen()],
              font=("Segoe UI", 10), bg="gray", fg="white").grid(row=8, column=0, pady=15)

    # Make text boxes expand properly
    win.grid_rowconfigure(3, weight=1)
    win.grid_rowconfigure(6, weight=1)
    win.grid_columnconfigure(0, weight=1)

    win.mainloop()



# ---------------------- Sentiment Analyzer Window ----------------------
def open_sentiment_analyzer():
    def analyze():
        text = input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter or upload text first.")
            return
        sentiment, polarity, subjectivity = analyze_sentiment(text)
        result_label.config(text=f"Sentiment: {sentiment}\nPolarity: {polarity:.2f}\nSubjectivity: {subjectivity:.2f}")

    def load_file():
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")])
        if path:
            text = read_file(path)
            input_text.delete(1.0, tk.END)
            input_text.insert(tk.END, text)

    def clear():
        input_text.delete(1.0, tk.END)
        result_label.config(text="")

    win = tk.Tk()
    win.title("Sentiment Analyzer")
    win.geometry("1000x700")
    win.configure(bg="#1e1e1e")
    win.columnconfigure(0, weight=1)
    win.rowconfigure(3, weight=1)
    styles = apply_dark_theme(win)

    # Title
    tk.Label(win, text="Sentiment Analyzer", font=("Segoe UI", 28, "bold"),
             bg="#1e1e1e", fg="#00ff88").grid(row=0, column=0, pady=10, sticky="n")

    # Upload Button
    tk.Button(win, text="Upload PDF/DOCX", command=load_file,
              font=("Segoe UI", 12), bg="#444", fg="white").grid(row=1, column=0, pady=5)

    # Input Label
    tk.Label(win, text="Input Text:", font=("Segoe UI", 14, "bold"),
             bg="#1e1e1e", fg="#aaaaaa").grid(row=2, column=0, sticky="w", padx=20)

    # Input Text Box
    input_text = ScrolledText(win, height=10, wrap=tk.WORD, **styles)
    input_text.grid(row=3, column=0, padx=20, sticky="nsew")

    # Analyze and Clear Buttons (Side by Side)
    button_frame = tk.Frame(win, bg="#1e1e1e")
    button_frame.grid(row=4, column=0, pady=10)

    tk.Button(button_frame, text="Analyze", command=analyze,
              font=("Segoe UI", 14, "bold"), bg="#00ff88", fg="black", width=12).pack(side=tk.LEFT, padx=10)

    tk.Button(button_frame, text="Clear", command=clear,
              font=("Segoe UI", 14, "bold"), bg="#555", fg="white", width=12).pack(side=tk.LEFT, padx=10)

    # Result Label
    result_label = tk.Label(win, text="", font=("Segoe UI", 14),
                            bg="#1e1e1e", fg="white")
    result_label.grid(row=5, column=0, pady=20)

    # Back Button
    tk.Button(win, text="Back to Home", command=lambda: [win.destroy(), home_screen()],
              font=("Segoe UI", 12), bg="gray", fg="white").grid(row=6, column=0, pady=15)

    win.mainloop()


# ---------------------- Home Page ----------------------
import tkinter as tk

def home_screen():
    home = tk.Tk()
    home.title("Content Analysis and Summarization Tool")
    home.geometry("1000x700")
    home.configure(bg="#1e1e1e")

    # Title
    tk.Label(home, text="Content Analysis and Summarization Tool", font=("Segoe UI", 28, "bold"),
             fg="#00ffff", bg="#1e1e1e").pack(pady=20)

    # Frame for content layout
    content_frame = tk.Frame(home, bg="#1e1e1e")
    content_frame.pack(expand=True, fill="both", padx=40, pady=10)

    # Summarizer Section
    summarizer_frame = tk.Frame(content_frame, bg="#2e2e2e", bd=2, relief="groove")
    summarizer_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    tk.Label(summarizer_frame, text="Content Summarizer", font=("Segoe UI", 18, "bold"), bg="#2e2e2e", fg="#00bfff").pack(pady=10)
    tk.Label(summarizer_frame, text=(
        "• Extracts key points from long documents.\n"
        "• Uses frequency-based scoring of sentences.\n"
        "• Supports PDF and Word file uploads.\n"
        "• Helps save time and boost reading efficiency.\n"
        "• Easy-to-use dark mode interface."
    ), justify="left", font=("Segoe UI", 12), bg="#2e2e2e", fg="white").pack(padx=10)
    tk.Button(summarizer_frame, text="Open Summarizer", font=("Segoe UI", 12, "bold"),
              bg="#007acc", fg="white", command=lambda: [home.destroy(), open_summarizer()]).pack(pady=15)

    # Sentiment Analyzer Section
    analyzer_frame = tk.Frame(content_frame, bg="#2e2e2e", bd=2, relief="groove")
    analyzer_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
    tk.Label(analyzer_frame, text="Sentiment Analyzer", font=("Segoe UI", 18, "bold"), bg="#2e2e2e", fg="#00ff88").pack(pady=10)
    tk.Label(analyzer_frame, text=(
        "• Analyzes emotions in text (Positive, Neutral, Negative).\n"
        "• Powered by TextBlob sentiment engine.\n"
        "• Displays polarity and subjectivity values.\n"
        "• Useful for social media, reviews, and more.\n"
        "• Supports file upload or direct typing."
    ), justify="left", font=("Segoe UI", 12), bg="#2e2e2e", fg="white").pack(padx=10)
    tk.Button(analyzer_frame, text="Open Analyzer", font=("Segoe UI", 12, "bold"),
              bg="#00cc99", fg="black", command=lambda: [home.destroy(), open_sentiment_analyzer()]).pack(pady=15)

    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)

    # Exit Button
    tk.Button(home, text="Exit", font=("Segoe UI", 12), command=home.destroy,
              bg="red", fg="white").pack(pady=10)

    # Author credit
    tk.Label(home, text="Created by:", font=("Segoe UI", 14), fg="#aaaaaa", bg="#1e1e1e").pack(pady=10)

    # Authors Section (Names + USNs only)
    authors_frame = tk.Frame(home, bg="#1e1e1e")
    authors_frame.pack(pady=10)

    def add_author(frame, name, usn):
        tk.Label(frame, text=name, font=("Segoe UI", 12, "bold"), bg="#1e1e1e", fg="white").pack()
        tk.Label(frame, text=usn, font=("Segoe UI", 10), bg="#1e1e1e", fg="#aaaaaa").pack()

    # Individual author profiles (No images)
    author1 = tk.Frame(authors_frame, bg="#1e1e1e")
    author1.pack(side="left", padx=40)
    add_author(author1, "Chethana R", "1SJ21CS029")

    author2 = tk.Frame(authors_frame, bg="#1e1e1e")
    author2.pack(side="left", padx=40)
    add_author(author2, "Chandana L U", "1SJ21CS026")

    author3 = tk.Frame(authors_frame, bg="#1e1e1e")
    author3.pack(side="left", padx=40)
    add_author(author3, "Bhavana G S", "1SJ21CS023")

    home.mainloop()




# ---------------------- Start App ----------------------
home_screen()
