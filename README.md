# Planogram Analysis API

This repository contains a FastAPI-based application that analyzes product placement errors on retail shelves by comparing an uploaded image against a provided planogram. The application leverages the OpenAI GPT-4 model to detect two types of errors: **empty spots** (missing products) and **product misplacements** (incorrect product locations). The planogram can be provided in JSON format, and the API processes images to return a structured JSON response with identified errors.

## Project Structure

```
example/
    test0.py                # Script to test the API
files/
    HackOxxo.csv           # Sample planogram in CSV format
    HackOxxo.json          # Sample planogram in JSON format
    img0.jpg               # Sample testing image
helper_scripts/
    csv2json.py            # Utility script to convert CSV planogram to JSON
main.py                    # Core FastAPI application
requirements.txt           # Python dependencies
.env                       # Environment variables (e.g., OpenAI API key)
.venv/                     # Virtual environment
.gitignore                 # Git ignore file
```

## Prerequisites

- **Python 3.10+**: Ensure Python is installed on your system.
- **Git**: For cloning the repository.
- **OpenAI API Key**: Required for GPT-4 vision capabilities. Obtain it from [OpenAI](https://platform.openai.com/account/api-keys).
- **Virtualenv**: For creating isolated Python environments (optional but recommended).

## Setup Instructions

Follow these steps to set up and run the FastAPI server locally.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create and Activate a Virtual Environment

Create a virtual environment to isolate dependencies:

```bash
python -m venv .venv
```

Activate the virtual environment:

- **Windows**:
  ```bash
  .venv\Scripts\activate
  ```

- **macOS/Linux**:
  ```bash
  source .venv/bin/activate
  ```

### 3. Install Dependencies

Install the required Python packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and add your OpenAI API key:

```bash
echo "OPENAI_API_KEY=your-openai-api-key" > .env
```

Replace `your-openai-api-key` with your actual OpenAI API key.

### 5. Run the FastAPI Server

Start the FastAPI server on port 8000 with auto-reload enabled for development:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

- `--host 0.0.0.0`: Makes the server accessible externally.
- `--port 8000`: Specifies the port (you can change it if needed).
- `--reload`: Enables auto-reload for development (remove for production).

The server will be available at `http://localhost:8000`.

### 6. Test the API

Use the provided `example/test0.py` script to test the API. Ensure the server is running, then execute:

```bash
python example/test0.py
```

This script sends a sample request to the `/analyze-shelf/` endpoint using the sample planogram (`files/HackOxxo.json`) and image (`files/img0.jpg`).

Alternatively, you can test the API using tools like `curl` or Postman:

```bash
curl -X POST "http://localhost:8000/analyze-shelf/" \
  -F "store_id=test_store" \
  -F "planograma=$(cat files/HackOxxo.json)" \
  -F "image=@files/img0.jpg"
```

### 7. Convert Planogram (Optional)

If you have a planogram in CSV format (`files/HackOxxo.csv`), convert it to JSON using the provided utility script:

```bash
python helper_scripts/csv2json.py
```

This generates a JSON file (`files/HackOxxo.json`) compatible with the API.

## API Endpoint

### `POST /analyze-shelf/`

Analyzes a shelf image against a planogram to identify product placement errors.

#### Request

- **Form Data**:
  - `store_id`: (string) Unique identifier for the store.
  - `planograma`: (string) JSON string containing the planogram data (list of products with shelf coordinates and product codes).
  - `image`: (file) Image of the shelf (JPEG format recommended).

#### Response

- **Success (200)**:
  ```json
  {
    "store_id": "string",
    "analysis_result": [
      {
        "error_type": "empty_spot",
        "coordinates": "(x, y)"
      },
      {
        "error_type": "product_misplaced",
        "coordinates": "(x, y)",
        "CB": "product_code"
      }
    ]
  }
  ```

- **Error (500)**:
  ```json
  {
    "error": "Internal Server Error"
  }
  ```

#### Example Request (using `curl`)

```bash
curl -X POST "http://localhost:8000/analyze-shelf/" \
  -F "store_id=test_store" \
  -F "planograma={\"products\": [{\"Charola\": 1, \"Posicion en Charola\": 1, \"Cantidad de Frentes\": 2, \"CB\": \"7501045403014\"}]}" \
  -F "image=@files/img0.jpg"
```

## Dependencies

The `requirements.txt` file includes:

```
fastapi==0.115.12
uvicorn==0.34.2
python-dotenv==1.1.0
openai==1.79.0
```

Ensure these versions are compatible with your Python environment. Run `pip install -r requirements.txt` to install them.

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key for accessing GPT-4 vision capabilities.

## Notes

- **Planogram Format**: The planogram should be a JSON object with a list of products, each containing:
  - `Charola`: Vertical shelf level (starting from 1 at the bottom).
  - `Posicion en Charola`: Horizontal position (left to right).
  - `Cantidad de Frentes`: Number of product units in sequence.
  - `CB`: Product barcode or identifier.
- **Image Requirements**: Use clear, well-lit images of the shelf for accurate analysis.
- **Error Handling**: The API handles invalid JSON, missing files, or OpenAI API errors gracefully, returning appropriate error messages.
- **Development Mode**: The `--reload` flag is for development only. For production, deploy with a WSGI server like Gunicorn and disable `--reload`.

## Troubleshooting

- **Port Conflict**: If port 8000 is in use, change the port in the `uvicorn` command (e.g., `--port 8001`).
- **Missing `.env`**: Ensure the `.env` file exists and contains a valid `OPENAI_API_KEY`.
- **Dependency Issues**: Verify Python version (3.10+) and re-run `pip install -r requirements.txt`.
- **API Errors**: Check server logs for detailed error messages.