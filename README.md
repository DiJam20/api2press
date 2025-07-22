# api2press
Python application that fetches the latest articles 
from online news sources, formats them into a printable newspaper-style PDF, 
and optionally sends the result to a printer. It's ideal for those who prefer 
reading news on paper.

## Features
- Fetches news via API or web-scraping, currently supports:
  - TheGuardian
  - NYT Mini Crossword
- Converts news into a clean, print-ready PDF
- Optional local printing

## Project Structure
```
api2press/
├── Dockerfile
├── .env
├── .gitignore
├── requirements.txt
├── README.md
├── src/
│   └── api2press/
│       ├── __init__.py
│       ├── main.py
│       ├── guardian_news.py
│       ├── nyt_crossword.py
│       ├── pdf_generator.py
│       └── printing.py
```

## Getting Started
### 1. Clone the repository
```bash
git clone https://github.com/DiJam20/api2press.git
cd api2press
```

### 2. Create and activate virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API key
Create a .env file:
```bash
GUARDIAN_API_KEY=your_guardian_api_key # request from https://open-platform.theguardian.com/access/
```

## Usage
Run the main script:
```bash
python src/api2press/main.py
```
The script will:
- Fetch news data
- Generate a PDF
- Optionally print the result (see printing.py)

## Docker (Optional)
Build and run the app with Docker:
```bash
docker build -t api2press .
docker run --env-file .env api2press
```

## TODO
Multi-column PDF layout