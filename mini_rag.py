from dotenv import load_dotenv
from mistralai import Mistral
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#come from scikit-learn (sklearn), and they’re used to compute text similarity using traditional (non-LLM) methods.
#They are part of a simple retrieval mechanism — the “R” in “RAG” (Retrieval-Augmented Generation).
import os, re
#Imports the operating system library and the regular expression library.

load_dotenv()
#Executes the function for the environment variables.

def read_pdf(path): #Defines a function to read text from a PDF file
    pages = [p.extract_text() or "" for p in PdfReader(path).pages] 
    # Opens the PDF, goes through every page, and extracts all the text
    # Gathers all the text into a list, preparing it for processing
    return " ".join(pages)
# Joins all the text from the list into a single string, separating pages with spaces

def chunk_text(t, size=900, overlap=180):   #Defines a function to split long text into chunks of smaller pieces 
    out=[]; i=0 # Initializes an empty list (out) for the chunks and a starting index (i). | 
    #Sets up the loop to begin the splitting process. |
    while i<len(t):
        # | Starts a loop that continues until the whole text has been processed. | 
        # Controls the chunking process until all text is covered. |
        out.append(t[i:i+size]); i+=max(1,size-overlap) 
    #Takes a piece of text (a chunk) of the specified size, adds it to the list, and then moves the starting point forward, but reusing some
    #text (overlap) to make sure context isn't lost at the chunk boundaries. | This creates the list of overlapping text chunk
    return out # Appends the current chunk to the list and updates the index for the next chunk, considering overlap.

def ask_with_context(question, chunks, k=5): #Defines a function takes a question and the chunks of the document, and will return an answer. | 
    #This is where the RAG logic happens: finding context and asking the LLM.
    vec = TfidfVectorizer(max_features=30000, ngram_range=(1,2)) 
    # Creates the TF-IDF converter tool. | Sets up the tool to turn text into math vectors.
    X = vec.fit_transform(chunks) 
    #  | Learns from the text chunks and then converts all the chunks into their numerical vector form (X). |
    # This creates the searchable "database" of text vectors. |
    qv = vec.transform([question]) 
    # | Converts the user's question into its numerical vector form (qv) using the same rules learned from the chunks. | 
    # The question needs to be in the same numerical format to be compared with the chunks. |
    sims = cosine_similarity(qv, X)[0]  
    # | Compares the question's vector (qv) with every chunk's vector (X) and calculates a similarity score for each. | 
    # This is the Retrieval step: finding out which chunks are most relevant to the question. |
    idxs = sims.argsort()[::-1][:k] 
    # | Sorts the similarity scores to find the indices (locations) of the top k (here, 5) most relevant chunks. | 
    # Identifies the top 5 pieces of information needed to answer the question. |
    ctx = "\n\n".join([f"[S{i+1}] {chunks[idx][:800]}" for i, idx in enumerate(idxs)])
    # | Creates one clean, combined block of text (ctx) by joining the top 5 relevant chunks. It also adds a source tag (e.g., [S1]) to each chunk. | 
    # This creates the context that will be passed to the LLM. |


#Formats the final, detailed instruction (prompt) for the LLM. It tells the LLM to use ONLY the provided Context and to return a specific format. | 
#A clear, detailed prompt is essential for getting a high-quality, focused answer from the LLM. |
    prompt = f"""You are a helpful assistant. Use ONLY the context below.
Question: {question}

Context:
{ctx}

Return exactly:
Final Answer: <one concise paragraph with [S#] citations>
"""
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
    # | Creates the connection object to the Mistral LLM, using the API key loaded at the beginning. | 
    # Prepares to send the request to the LLM. |
    r = client.chat.complete(model="mistral-medium-latest", messages=[{"role":"user","content":prompt}], temperature=0.2)
    # | Sends the prompt (with the question and the retrieved context) to the Mistral LLM and gets the response (r). | 
    # This is the Generation step: the LLM creates the answer based on the context. |
    content = r.choices[0].message.content 
    if isinstance(content, list):
        content = "".join([c.get("text","") for c in content])
    m = re.search(r"Final Answer:\s*(.*)", content, flags=re.I|re.S)
    return m.group(0).strip() if m else content.strip()

pdf_path = "data/sample.pdf"    # Path to the PDF file
text = read_pdf(pdf_path)   # Reads the entire text from the PDF
chunks = chunk_text(text) # Splits the text into manageable chunks
print(ask_with_context("What is the main contribution?", chunks, k=5))  # Asks a question using the chunks and prints the answer
