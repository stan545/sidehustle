from flask import Flask, render_template, request, jsonify
import re
import string

app = Flask(__name__)

# Advanced AI phrase replacements - contextual alternatives instead of removal
AI_PHRASE_REPLACEMENTS = {
    # AI identity phrases - these should often be completely removed or replaced with natural flow
    r'\b(?:as an ai|i\'m an ai|as a language model|i\'m a language model)\b': ['', '', ''],  # Mostly remove
    
    # Limitation phrases - replace with more natural alternatives
    r'\b(?:i don\'t have personal|i don\'t have the ability|i cannot provide personal)\b': ['research shows', 'studies indicate', 'evidence suggests'],
    
    # Formal transition words - replace with more natural connectors
    r'\bhowever\b': ['but', 'yet', 'though', 'still'],
    r'\bfurthermore\b': ['also', 'plus', 'what\'s more', 'additionally'],
    r'\bmoreover\b': ['also', 'besides', 'on top of that'],
    r'\badditionally\b': ['also', 'plus', 'and'],
    
    # Emphasis phrases - replace with more natural alternatives
    r'\b(?:it\'s important to note|it\'s worth noting|it should be noted)\b': ['importantly', 'note that', 'keep in mind', 'remember'],
    
    # Conclusion phrases - replace with natural endings
    r'\b(?:in conclusion|to summarize|in summary)\b': ['overall', 'in the end', 'to wrap up', 'finally'],
    
    # Invitation phrases - replace with warmer alternatives
    r'\b(?:feel free to|please don\'t hesitate to)\b': ['you can', 'go ahead and', 'simply', 'just'],
    
    # Help phrases - replace with more casual alternatives
    r'\b(?:i hope this helps|i hope this information is helpful)\b': ['hope this works', 'this should help', 'that covers it'],
    
    # Certainty phrases - replace with more natural confidence
    r'\b(?:certainly|absolutely|definitely)\b': ['yes', 'sure', 'of course', 'clearly'],
    
    # Formal note phrases - replace with casual alternatives
    r'\b(?:please note that|it\'s essential to understand)\b': ['remember that', 'keep in mind', 'just know that'],
    
    # Reference phrases - replace with natural references
    r'\b(?:as mentioned earlier|as previously discussed)\b': ['as we saw', 'like before', 'as noted', 'earlier']
}

def remove_ai_phrases(text):
    """Advanced AI phrase replacement - replace robotic phrases with natural alternatives while preserving meaning."""
    import random
    
    processed_text = text
    
    # Advanced replacement of AI phrases with contextual alternatives
    for pattern, replacements in AI_PHRASE_REPLACEMENTS.items():
        if re.search(pattern, processed_text, flags=re.IGNORECASE):
            # Choose a random replacement from the alternatives (empty string means remove)
            replacement = random.choice(replacements)
            processed_text = re.sub(pattern, replacement, processed_text, flags=re.IGNORECASE)
    
    # Handle sentence structure improvements after replacements
    processed_text = _fix_sentence_structure(processed_text)
    
    # Clean up extra spaces and punctuation issues
    processed_text = re.sub(r'\s+', ' ', processed_text)
    processed_text = re.sub(r'\s*,\s*,', ',', processed_text)
    processed_text = re.sub(r'\s*\.\s*\.', '.', processed_text)
    processed_text = re.sub(r'^\s*,\s*', '', processed_text)  # Remove leading comma
    processed_text = re.sub(r'\s*,\s*$', '', processed_text)  # Remove trailing comma
    processed_text = re.sub(r'\s*,\s*\.', '.', processed_text)  # Fix ", ." -> "."
    
    # Fix duplicate words that can occur after phrase replacement
    processed_text = re.sub(r'\b(\w+)\s+\1\b', r'\1', processed_text)  # "that that" -> "that"
    
    processed_text = processed_text.strip()
    
    # Ensure sentences start with capital letters
    sentences = re.split(r'(?<=[.!?])\s+', processed_text)
    capitalized_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            # Capitalize first letter of each sentence
            sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
            capitalized_sentences.append(sentence)
    
    processed_text = ' '.join(capitalized_sentences)
    
    return processed_text

def _fix_sentence_structure(text):
    """Fix common sentence structure issues after AI phrase replacement."""
    # Fix sentences that start with commas after phrase removal
    text = re.sub(r'^\s*,\s*([a-z])', r'\1', text, flags=re.IGNORECASE)
    
    # Fix double commas and spacing issues
    text = re.sub(r',\s*,', ',', text)
    
    # Fix cases where commas appear before periods
    text = re.sub(r',\s*\.', '.', text)
    
    # Fix awkward sentence fragments - remove isolated AI identity phrases
    patterns_to_clean = [
        r',\s*language model,',  # ", language model,"
        r'language model,\s*([A-Z])',  # "language model, I" -> "I"
        r'\b(?:based on research|from what we know|studies indicate|evidence suggests),?\s*([a-z])',  # Fix standalone research phrases
    ]
    
    for pattern in patterns_to_clean:
        if 'language model' in pattern:
            text = re.sub(pattern, '', text)
        else:
            text = re.sub(pattern, r'\1', text, flags=re.IGNORECASE)
    
    # Fix sentences that begin with lonely conjunctions
    text = re.sub(r'^\s*(?:but|yet|though|also|plus|and),?\s*([a-z])', r'\1', text, flags=re.IGNORECASE)
    
    # Fix double spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Split into sentences and fix each one
    sentences = re.split(r'(?<=[.!?])\s+', text)
    fixed_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            # Remove leading commas
            sentence = re.sub(r'^\s*,\s*', '', sentence)
            
            # Capitalize first letter if it's lowercase
            if sentence and sentence[0].islower():
                sentence = sentence[0].upper() + sentence[1:]
            
            # Skip very short meaningless fragments
            if len(sentence.strip()) > 2:
                fixed_sentences.append(sentence)
    
    return ' '.join(fixed_sentences)

def humanize_text(text):
    """Make text more conversational and human-like."""
    # Replace formal phrases with more casual ones
    replacements = {
        r'\butilize\b': 'use',
        r'\bfacilitate\b': 'help',
        r'\bdemonstrate\b': 'show',
        r'\bimplement\b': 'do',
        r'\binitiate\b': 'start',
        r'\bterminate\b': 'end',
        r'\bsubsequently\b': 'then',
        r'\bconsequently\b': 'so',
        r'\btherefore\b': 'so',
        r'\bin order to\b': 'to',
        r'\bdue to the fact that\b': 'because',
        r'\bfor the purpose of\b': 'to',
        r'\bat this point in time\b': 'now',
        r'\bin the event that\b': 'if',
        r'\bmethodology\b': 'method',
        r'\boptimal\b': 'best',
        r'\benhance\b': 'improve',
        r'\bobtain\b': 'get',
        r'\bprovide\b': 'give',
        r'\bassist\b': 'help',
        r'\bcomprehensive\b': 'complete',
        r'\bsignificant\b': 'important',
        r'\bnumerous\b': 'many',
        r'\badditional\b': 'more',
        r'\beffective\b': 'good',
        r'\bappropriate\b': 'right'
    }
    
    processed_text = text
    for formal, casual in replacements.items():
        processed_text = re.sub(formal, casual, processed_text, flags=re.IGNORECASE)
    
    # Add more contractions for natural flow
    contractions = {
        r'\bit is\b': "it's",
        r'\byou are\b': "you're",
        r'\bwe are\b': "we're",
        r'\bthey are\b': "they're",
        r'\bthat is\b': "that's",
        r'\bwho is\b': "who's",
        r'\bwhat is\b': "what's",
        r'\bcannot\b': "can't",
        r'\bdo not\b': "don't",
        r'\bwill not\b': "won't",
        r'\bshould not\b': "shouldn't",
        r'\bwould not\b': "wouldn't",
        r'\bhave not\b': "haven't",
        r'\bhas not\b': "hasn't",
        r'\bhad not\b': "hadn't",
        r'\bwere not\b': "weren't",
        r'\bwas not\b': "wasn't"
    }
    
    for full_form, contraction in contractions.items():
        processed_text = re.sub(full_form, contraction, processed_text, flags=re.IGNORECASE)
    
    return processed_text

def simple_sentence_tokenize(text):
    """Simple sentence tokenization without NLTK."""
    # Split on sentence endings, but be careful with abbreviations
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def paraphrase_text(text):
    """Simple rule-based paraphrasing as the main method."""
    # Basic word replacements for paraphrasing
    synonyms = {
        r'\bbig\b': 'large',
        r'\bsmall\b': 'little',
        r'\bgood\b': 'excellent',
        r'\bbad\b': 'poor',
        r'\bfast\b': 'quick',
        r'\bslow\b': 'gradual',
        r'\bhelp\b': 'assist',
        r'\bmake\b': 'create',
        r'\bget\b': 'obtain',
        r'\bgive\b': 'provide',
        r'\bshow\b': 'display',
        r'\btell\b': 'inform',
        r'\bthink\b': 'believe',
        r'\bknow\b': 'understand',
        r'\bsee\b': 'observe',
        r'\bfind\b': 'discover',
        r'\bwork\b': 'function',
        r'\blearn\b': 'study',
        r'\btry\b': 'attempt',
        r'\bstart\b': 'begin',
        r'\bstop\b': 'cease',
        r'\bimportant\b': 'crucial',
        r'\binteresting\b': 'fascinating',
        r'\bdifficult\b': 'challenging',
        r'\beasy\b': 'simple',
        r'\bchange\b': 'modify',
        r'\bimprove\b': 'enhance',
        r'\breduce\b': 'decrease',
        r'\bincrease\b': 'boost'
    }
    
    processed_text = text
    
    # Apply synonyms
    for original, replacement in synonyms.items():
        processed_text = re.sub(original, replacement, processed_text, flags=re.IGNORECASE)
    
    # Simple sentence restructuring patterns
    restructuring_patterns = [
        # "It is X that Y" -> "Y because of X"
        (r'\bit is (\w+) that ([^.!?]+)', r'\2 because of \1'),
        # "There are many X" -> "Many X exist"
        (r'\bthere are many (\w+)', r'Many \1 exist'),
        # "This allows" -> "This enables"
        (r'\bthis allows\b', 'this enables'),
        # "It should be" -> "It needs to be"
        (r'\bit should be\b', 'it needs to be'),
        # "You can" -> "You may"
        (r'\byou can\b', 'you may'),
        # "In order to" -> "To"
        (r'\bin order to\b', 'to'),
    ]
    
    for pattern, replacement in restructuring_patterns:
        processed_text = re.sub(pattern, replacement, processed_text, flags=re.IGNORECASE)
    
    return processed_text

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_text():
    """Process text based on selected options."""
    data = request.get_json()
    
    input_text = data.get('text', '').strip()
    options = data.get('options', {})
    
    if not input_text:
        return jsonify({'error': 'No text provided'}), 400
    
    processed_text = input_text
    
    # Apply selected processing options
    if options.get('paraphrase', False):
        processed_text = paraphrase_text(processed_text)
    
    if options.get('remove_ai_phrases', False):
        processed_text = remove_ai_phrases(processed_text)
    
    if options.get('humanize', False):
        processed_text = humanize_text(processed_text)
    
    return jsonify({
        'original_text': input_text,
        'processed_text': processed_text,
        'options_applied': options
    })

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'version': '1.0.0'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.environ.get('FLASK_ENV') == 'development', host='0.0.0.0', port=port)