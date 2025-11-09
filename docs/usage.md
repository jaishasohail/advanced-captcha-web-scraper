wn# Usage Guide

## 1. Installation

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt

2. Quick Start
Run the scraper with default settings:
bashpython src/main.py

Common options:
bashpython src/main.py --output-format json
python src/main.py --output-format csv
python src/main.py --max-pages 5 --use-proxies

3. Proxies
Edit src/config/proxies.txt and add one proxy per line in host:port or user:pass@host:port format, then enable proxy usage:
bashpython src/main.py --use-proxies

4. Captcha Provider
Set the following environment variables to enable real captcha solving:

CAPTCHA_PROVIDER_URL – Base URL of your captcha solver API.

CAPTCHA_API_KEY – API key or token.

Without these values, the solver returns deterministic dummy tokens and the scraper behaves in a safe debug mode.
5. Running Tests
Install dev dependencies (pytest is in requirements.txt) and run:
bashpytest

6. Docker
Build the image:
bashdocker build -t advanced-captcha-web-scraper .

Run the container:
bashdocker run --rm advanced-captcha-web-scraper

shell
### advanced-captcha-web-scraper/requirements.txt
```text
requests>=2.32.0
beautifulsoup4>=4.12.0
lxml>=5.0.0
pytest>=8.2.0

advanced-captcha-web-scraper/Dockerfile
dockerfileFROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]

advanced-captcha-web-scraper/LICENSE
textMIT License

Copyright (c) 2025 Bitbash

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.