Root folder to make project 
cd C:\Users\Windows\python\lesson\ai\

Project Folder 
mkdir mini_rag_demo
cd mini_rag_demo

Virtual Environment
# Create venv
python -m venv venv

venv\Scripts\activate

Dependencies 
pip install mistralai(Sends your query and gets a text response)
PyPDF2(Reads and extracts text from PDFs)
pandas(CSV)
python-dotenv(Reads .env files so you can store your API keys securely instead of hardcoding them) 
requests(code download files or web page) 
beautifulsoup4 (web scraping and HTML parsing)

File Structure
mini_rag_demo/
│
├── mini_rag.py          ← (main )
├── .env                 ← (API key)
└── data/
    └── sample.pdf       ← (PDF)

Create file structure
New-Item -Path .env -ItemType File

New-Item -Path mini_rag.py -ItemType File

Environmental Variables to hide key
In .env    MISTRAL_API_KEY=sk-your-api-key-here

Pdf file from arxiv 
$URL = "https://arxiv.org/pdf/2510.08941.pdf" 
$OutFile = "data\sample.pdf" 
Invoke-WebRequest -Uri $URL -OutFile $OutFile

Check to see if it works
python mini_rag.py --pdf data/sample.pdf --ask "What is this paper about?"
