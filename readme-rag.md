# **📚 Mini RAG Demo: Mistral AI for PDF** 

## **📝 Short Description**

**R**etrieval-**A**ugmented **G**eneration (RAG) system using the mistralai SDK. It demonstrates how to load context from a PDF file, manage dependencies in a virtual environment, and securely handle API keys using a .env file.

## **🏗️ Table of Contents**

* [Prerequisites](https://www.google.com/search?q=%23prerequisites)  
* [Setup and Installation](https://www.google.com/search?q=%23setup-and-installation)  
* [Configuration (API Key)](https://www.google.com/search?q=%23configuration-api-key)  
* [Data Source](https://www.google.com/search?q=%23data-source)  
* [Usage](https://www.google.com/search?q=%23usage)  
* [File Structure](https://www.google.com/search?q=%23file-structure)

## **⚙️ Prerequisites**

You must have **Python** (3.8+) installed on your system.

## **🚀 Setup and Installation**

Follow these steps to set up the project environment and install the required dependencies.

### **1\. Create Project Folder**

First, navigate to your desired root directory (e.g., C:\\Users\\Windows\\python\\lesson\\ai\\) and create the project folder:

mkdir mini\_rag\_demo  
cd mini\_rag\_demo

### **2\. Create and Activate Virtual Environment**

A virtual environment ensures project dependencies are isolated.

**Windows (PowerShell/CMD):**

python \-m venv venv  
venv\\Scripts\\activate

**Linux/macOS:**

python3 \-m venv venv  
source venv/bin/activate

### **3\. Install Dependencies**

Install all necessary libraries, including the Mistral AI SDK, PDF handling, and web scraping tools.

pip install mistralai PyPDF2 pandas python-dotenv requests beautifulsoup4

### **4\. Create Necessary Files and Folders**

Create the primary script, the configuration file, and the data directory.

\# Create data directory (where the PDF will go)  
mkdir data

\# Create main files  
New-Item \-Path mini\_rag.py \-ItemType File  
New-Item \-Path .env \-ItemType File

## **🔑 Configuration (API Key)**

For security, your Mistral API Key must be stored in the .env file, which is loaded by python-dotenv.

Open the .env file and add the following line, replacing the placeholder with your actual key:

MISTRAL\_API\_KEY=sk-your-api-key-here

## **📥 Data Source**

The project requires a PDF file named sample.pdf inside the data/ directory. This command will download a sample paper from arXiv using the specified URL:

**Windows (PowerShell):**

$URL \= "\[https://arxiv.org/pdf/2510.08941.pdf\](https://arxiv.org/pdf/2510.08941.pdf)"  
$OutFile \= "data\\sample.pdf"  
Invoke-WebRequest \-Uri $URL \-OutFile $OutFile

## **🎬 Usage**

Once the file structure is created, dependencies are installed, and the PDF is downloaded, you can run the main script (mini\_rag.py) with a path to the PDF and a question to query its content.

python mini\_rag.py \--pdf data/sample.pdf \--ask "What is this paper about?"

## **📂 File Structure**

The final project structure should look like this:

mini\_rag\_demo/  
├── venv/                 (Virtual Environment)  
├── mini\_rag.py           (Main RAG script)  
├── .env                  (API Key configuration)  
└── data/  
    └── sample.pdf        (The PDF used for context)  
