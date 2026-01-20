# Vision-Based Language Translation Chatbot

A Streamlit-based translation application powered by **Qubrid AI** and **Agno agents**. Upload an image with text, and the app will automatically detect the language and translate it to your target language.

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.53+-red.svg)
![Agno](https://img.shields.io/badge/agno-2.4+-green.svg)

---

## Features

- 🖼️ **Image OCR** - Extract text from images using Qubrid Hunyuan OCR
- 🌍 **Language Detection** - Automatically detect source language via Agno agent
- 🔄 **Translation** - Translate to 50+ languages using Agno + Qubrid GPT-OSS-20B
- 💬 **Chat History** - Persistent conversation storage with SQLite
- 🎨 **Modern UI** - Clean Streamlit interface with real-time results
- 🤖 **Agno Agents** - Production-ready agent orchestration framework
- 🔒 **No OpenAI Dependency** - Fully powered by Qubrid AI platform

---

## Architecture

```
User Upload Image
    ↓
OCR Extraction (Qubrid Hunyuan OCR)
    ↓
Agno Agent Pipeline
    ├─ Language Detection Agent → Qubrid GPT-OSS-20B
    └─ Translation Agent → Qubrid GPT-OSS-20B
    ↓
Results Display + History Storage
```

### Tech Stack

- **Frontend**: Streamlit
- **Agent Framework**: Agno (v2.4+)
- **AI Models**: Qubrid AI Platform
  - Hunyuan OCR 1B (text extraction)
  - GPT-OSS-20B (language detection & translation)
- **Database**: SQLite
- **HTTP Client**: Requests

---

## Project Structure

```
Translate-AI/
├── backend/
│   ├── agents/
│   │   ├── language_detector.py    # Agno agent for language detection
│   │   └── translator.py           # Agno agent for translation
│   ├── llm/
│   │   ├── qubrid_client.py        # Pure function Qubrid API client
│   │   └── agno_qubrid_model.py    # Custom Agno model wrapper
│   ├── ocr/
│   │   └── ocr.py                  # OCR text extraction
│   ├── db/
│   │   └── sqlite.py               # Conversation persistence
│   └── pipeline.py                 # Translation orchestration
├── frontend/
│   ├── ui_components.py            # Reusable UI components
│   └── base_config.py              # Streamlit configuration
├── app.py                          # Main Streamlit application
├── .env                            # Environment variables
└── pyproject.toml                  # Dependencies
```

---

## Installation

### Prerequisites

- Python 3.13+
- Qubrid API Key ([Get one here](https://platform.qubrid.com))

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/kannan-qubrid/Translate-AI.git
   cd Translate-AI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # or with uv
   uv pip install -e .
   ```

3. **Configure environment variables**
   
   Create a `.env` file:
   ```env
   QUBRID_API_KEY=your_api_key_here
   QUBRID_OCR_URL=https://platform.qubrid.com/api/v1/qubridai/ocr/chat
   QUBRID_CHAT_URL=https://platform.qubrid.com/api/v1/qubridai
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   # or with uv
   uv run streamlit run app.py
   ```

5. **Open in browser**
   
   Navigate to `http://localhost:8501`

---

## Usage

1. **Upload an Image**
   - Click "📤 Upload Image" and select an image containing text
   - Supported formats: PNG, JPG, JPEG

2. **Select Target Language**
   - Choose from 50+ supported languages in the dropdown

3. **Translate**
   - Click "🚀 Translate" to start the pipeline
   - View extracted text, detected language, and translation

4. **Chat History**
   - Access previous translations from the sidebar
   - Delete unwanted conversations

---

## Key Components

### Agno Agents

**Language Detection Agent** ([language_detector.py](backend/agents/language_detector.py))
```python
Agent(
    name="Language Detection Specialist",
    model=QubridModel(id="openai/gpt-oss-20b"),
    instructions=["Identify language", "Return only language name"],
    stream=True,
    debug_mode=True
)
```

**Translation Agent** ([translator.py](backend/agents/translator.py))
```python
Agent(
    name="Translation Specialist",
    model=QubridModel(id="openai/gpt-oss-20b"),
    instructions=["Translate text", "Preserve meaning and tone"],
    stream=True,
    debug_mode=True
)
```

### Custom Qubrid Model

The `QubridModel` wrapper ([agno_qubrid_model.py](backend/llm/agno_qubrid_model.py)) extends Agno's `OpenAIChat` to:
- Auto-configure Qubrid API credentials
- Handle base URL formatting
- Ensure OpenAI-compatible streaming responses

### Translation Pipeline

The `TranslationPipeline` ([pipeline.py](backend/pipeline.py)) orchestrates:
1. Agent instantiation
2. Streaming response collection
3. Error handling
4. Result formatting

---

## Configuration

### Supported Languages

English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese (Simplified), Chinese (Traditional), Arabic, Hindi, Bengali, Turkish, Vietnamese, Thai, Indonesian, Malay, Filipino, Dutch, Polish, Swedish, Norwegian, Danish, Finnish, Greek, Hebrew, Czech, Romanian, Hungarian, Ukrainian, Bulgarian, Serbian, Croatian, Slovak, Slovenian, Lithuanian, Latvian, Estonian, Icelandic, Irish, Welsh, Catalan, Basque, Galician, Swahili, Zulu

### Debug Mode

Enable detailed Agno execution logs by setting `debug_mode=True` in agent configurations (already enabled by default).

---

## API Reference

### Qubrid Endpoints

- **OCR**: `POST /api/v1/qubridai/ocr/chat`
- **Chat**: `POST /api/v1/qubridai/chat/completions`

### Models Used

- **Hunyuan OCR 1B**: Text extraction from images
- **GPT-OSS-20B**: Language detection and translation

---

## Troubleshooting

### Common Issues

**404 Not Found Error**
- Ensure `QUBRID_CHAT_URL` does NOT end with `/chat/completions`
- Correct: `https://platform.qubrid.com/api/v1/qubridai`
- Wrong: `https://platform.qubrid.com/api/v1/qubridai/chat/completions`

**'str' object has no attribute 'choices'**
- Ensure `stream=True` in agent configuration
- Verify `_collect_streaming_response()` is handling chunks correctly

**No OpenAI Key Error**
- This app does NOT use OpenAI - ignore any OpenAI-related warnings
- Ensure `QUBRID_API_KEY` is set in `.env`

---

## Development

### Running Tests

```bash
# Test pipeline instantiation
python -c "from backend.pipeline import TranslationPipeline; p = TranslationPipeline(); print('✓ Success')"

# Test without OpenAI key
python -c "import os; os.environ.pop('OPENAI_API_KEY', None); from backend.pipeline import TranslationPipeline; p = TranslationPipeline(); print('✓ No OpenAI required')"
```

### Debug Logs

Watch terminal output when running the app to see:
- Agent initialization
- Model configuration
- Input/output for each agent
- Streaming chunk collection

---

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

- **Qubrid AI** - For providing the AI infrastructure
- **Agno** - For the agent orchestration framework
- **Streamlit** - For the web application framework

---

## Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using Qubrid AI and Agno**
