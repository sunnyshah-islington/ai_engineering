### Step 1: Install uv | for Linux and Mac
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Install Python and create vitrual environment and activate it
```bash
uv python install 3.12
uv venv --python 3.12
source .venv/bin/activate
```

### Step 3: Install `fastapi[standard]` and `transformers[torch]`
```bash
uv pip compile requirements.in -o requirements.txt && uv pip install -r requirements.txt
```

### Step 4: Start FastAPI server 
`main.py` file is inside the folder `apis`
```bash
cd apis
fastapi dev
```
The server should be running after this command

### Step 5: Hit the API started by FastAPI
Once the server is running open another `terminal` and send the request below

For text generator
```bash
curl -X POST http://127.0.0.1:8000/generate_text \
  -H "Content-Type: application/json" \
  -d '{"prompt": "<YOUR PROMPT HERE>"}'
```
For sentiment analysis
```bash
curl -X POST http://127.0.0.1:8000/analyze_sentiment \
  -H "Content-Type: application/json"\
  -d '{"prompt": "<YOUR PROMPT HERE>"}'
```
OR

If you wish to use `Postman` send a `POST` request

<img src="image.png" alt="Postman POST request example" width="70%">
