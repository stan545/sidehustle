# Text Processor - Paraphrasing & Humanization Tool

A Python web application that transforms text through paraphrasing, AI phrase removal, and humanization to make content more natural and conversational.

## Features

- **Paraphrasing**: Rephrases text while preserving original meaning using synonym replacement and sentence restructuring
- **Advanced AI Phrase Replacement**: Intelligently replaces robotic AI phrases with natural alternatives while preserving meaning
- **Humanization**: Converts formal language to conversational tone with contractions and casual replacements
- **Context Preservation**: Maintains the original intent and meaning of the text
- **Interactive UI**: Clean, responsive interface with real-time character counting
- **Copy to Clipboard**: Easy sharing of processed results

## Screenshots

### Main Interface
![Text Processor Interface](https://github.com/user-attachments/assets/621291b1-e07c-4f68-af26-59a93dfcb044)

### Processing Example
![Text Processing Example](https://github.com/user-attachments/assets/b8c1ed78-1be4-41fd-94ff-4039faf7bb84)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd sidehustle
   ```

2. **Install Python dependencies**:
   ```bash
   # For Ubuntu/Debian systems
   sudo apt update && sudo apt install python3-flask

   # Or using pip
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python3 app.py
   ```

4. **Access the application**:
   Open your browser and go to `http://localhost:5000`

## Usage

1. **Select Processing Options**: Choose from Paraphrasing, AI Phrase Removal, and/or Humanization
2. **Input Text**: Type or paste your text in the input area
3. **Process**: Click "Process Text" to transform your content
4. **Copy Results**: Use the "Copy Result" button to copy the processed text
5. **Try Sample**: Use "Try Sample Text" to see a demonstration

## Deployment

### Heroku Deployment

1. **Create Procfile**:
   ```
   web: python app.py
   ```

2. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy text processor"
   git push heroku main
   ```

### AWS Deployment

The application can be deployed on AWS using:
- **AWS Elastic Beanstalk** for easy deployment
- **AWS EC2** with manual setup
- **AWS Lambda** with serverless framework

## API Endpoints

- `GET /` - Main application interface
- `POST /process` - Text processing API endpoint
- `GET /health` - Health check endpoint

### API Usage Example

```bash
curl -X POST http://localhost:5000/process \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your text here",
    "options": {
      "paraphrase": true,
      "remove_ai_phrases": true,
      "humanize": true
    }
  }'
```

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Text Processing**: Custom rule-based algorithms using regular expressions
- **Styling**: CSS Grid and Flexbox for responsive design
- **Deployment Ready**: Prepared for Heroku, AWS, and other platforms

## Text Processing Algorithms

### Advanced AI Phrase Replacement
- Intelligently replaces common AI-generated phrases like "as an AI language model" with natural alternatives
- Preserves sentence meaning and structure instead of just removing phrases
- Uses contextual replacements to maintain readability and flow
- Handles formal transition words and converts them to casual alternatives

### Humanization
- Replaces formal vocabulary with casual alternatives
- Adds contractions for natural flow
- Converts business jargon to everyday language

### Paraphrasing
- Synonym replacement for variety
- Simple sentence restructuring
- Maintains semantic meaning while changing expression

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.