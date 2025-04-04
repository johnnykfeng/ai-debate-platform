# AI Debate Platform

A web application that facilitates AI-powered debates between different language models. Users can input a debate topic and select two different AI models to argue opposing sides of the topic.

## Features

- Select from multiple AI models (OpenAI, Claude, Deepseek)
- Customize debate rounds
- Real-time debate display
- Clean and intuitive interface

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- API keys for:
  - OpenAI
  - Anthropic (Claude)
  - Deepseek

## Setup

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```
   Then edit the `.env` file to add your API keys.

6. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Enter a debate topic
3. Select two AI models to debate
4. Choose the position for the first model
5. Set the number of debate rounds
6. Click "Start Debate" to begin

## API Endpoints

- `POST /api/debate`: Start a new debate
  - Request body:
    ```json
    {
      "topic": "string",
      "model1": "string",
      "model2": "string",
      "position1": "support" | "oppose",
      "rounds": number
    }
    ```

## Contributing

Feel free to submit issues and enhancement requests! 