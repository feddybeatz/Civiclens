# CivicLens 🇰🇪

### Where Did Our Money Go?

**CivicLens** is an AI-powered civic transparency platform that helps Kenyans understand government and county budgets, explore public spending information, and make informed decisions through evidence-based insights.

Powered by **Google Gemma 4**, CivicLens aims to make complex government financial documents easier to understand through natural-language questions, document analysis and visual insights.

## 🎯 Problem Statement

Government budget documents are often lengthy, technical and difficult for ordinary citizens to interpret. This limits public understanding of how public funds are allocated and spent, making meaningful public participation more difficult.

## 💡 Our Solution

CivicLens provides a platform where users can explore official government budget information, upload PDF documents, ask questions and receive clear explanations supported by relevant document evidence.

## ✨ Key Features

* **AI Budget Assistant:** Ask questions about government and county budgets using natural language.
* **Document Analysis:** Upload and analyse official government budget PDFs.
* **Evidence-Based Answers:** Display supporting excerpts, document names and page references.
* **Budget Insights:** Explore financial allocations and expenditure information through visualisations.
* **Public Participation:** Generate relevant questions citizens can raise during public participation forums.
* **Information Gap Detection:** Highlight unclear allocations and missing explanations that require clarification.
* **Cross-Source Analysis:** Designed to bring information from multiple official government platforms into one accessible interface.

## 🛠️ Technology Stack

| Technology     | Purpose             |
| -------------- | ------------------- |
| Python         | Backend development |
| Streamlit      | User interface      |
| Google Gemma 4 | AI-powered analysis |
| PyMuPDF        | PDF text extraction |
| Pandas         | Data processing     |
| Plotly         | Data visualisation  |
| Pydantic       | Data validation     |
| Git & GitHub   | Version control     |

## 🔄 How It Works

1. Users upload official government budget documents or access available indexed information.
2. CivicLens extracts and processes relevant document content.
3. The system retrieves information related to the user's question.
4. Gemma 4 analyses the retrieved evidence.
5. CivicLens presents a plain-language response with supporting sources and page references where available.

## 🏛️ Data Sources

CivicLens is designed to use publicly available information from official Kenyan government platforms, including:

* [Bajeti Yetu – National Treasury](https://bajetiyetu.treasury.go.ke/)
* [The National Treasury](https://www.treasury.go.ke/)
* [Office of the Controller of Budget](https://cob.go.ke/)
* [Commission on Revenue Allocation](https://cra.go.ke/)
* [Kenya Parliament](https://www.parliament.go.ke/)

Data availability depends on the documents and information accessible from each source.

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate into the project

```bash
cd CivicLens
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file in the project root and add the required Gemma 4 API configuration.

```env
GEMMA_API_KEY=your_api_key_here
```

Use the actual environment variable names expected by your implementation.

**Never upload API keys or secrets to GitHub.**

### 7. Run the application

```bash
streamlit run app.py
```

The application should open in your browser.

## 🔐 Transparency and Reliability

CivicLens is designed around responsible use of AI and public financial information.

* Answers should be grounded in available official documents.
* Financial figures should not be invented.
* Sources and page references should be provided where available.
* Documented facts should be distinguished from AI interpretations.
* Missing or unclear information should be identified honestly.
* Unclear allocations should not automatically be treated as evidence of corruption.

## 🌍 Expected Impact

CivicLens aims to:

* Improve public access to government budget information.
* Make financial documents easier for citizens to understand.
* Encourage evidence-based public participation.
* Support transparency and accountability in public spending.

## 🔮 Future Improvements

* Automated collection of documents from official government portals.
* Regular updates when new budget documents become available.
* Comparison of county and national budgets across financial years.
* Improved financial data extraction and validation.
* More advanced expenditure tracking and visual analytics.
* Expanded support for additional government data sources.



## 👥 Project

**CivicLens – Where Did Our Money Go?**

Making public financial information easier to understand, question and verify.
