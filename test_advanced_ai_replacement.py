#!/usr/bin/env python3
"""
Test cases for the enhanced AI phrase replacement functionality.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import remove_ai_phrases


def test_ai_phrase_replacement():
    """Test that AI phrases are replaced with natural alternatives instead of being removed."""
    
    test_cases = [
        # Test AI identity phrases
        {
            'input': "As an AI language model, I think this is important.",
            'expected_contains': "think this is important"  # Should preserve core meaning
        },
        
        # Test transition words
        {
            'input': "However, this is good. Furthermore, it works well.",
            'expected_words': ['but', 'yet', 'though', 'still', 'also', 'plus', 'additionally']  # Should contain natural transitions
        },
        
        # Test formal phrases
        {
            'input': "It's important to note that this works.",
            'expected_words': ['importantly', 'note that', 'keep in mind', 'remember']  # Should use casual alternatives
        },
        
        # Test complex example
        {
            'input': "However, as an AI language model, I must note that it's important to understand that artificial intelligence has significantly transformed the way we process information. Furthermore, it should be noted that these technologies facilitate enhanced communication.",
            'must_not_contain': ['as an ai language model', 'however,', 'furthermore,', 'it should be noted'],
            'must_contain': ['transformed', 'information', 'communication']  # Core meaning preserved
        }
    ]
    
    print("Testing Advanced AI Phrase Replacement...")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Input: {test_case['input']}")
        
        result = remove_ai_phrases(test_case['input'])
        print(f"Output: {result}")
        
        # Check that result is not empty
        assert result.strip(), "Result should not be empty"
        
        # Check that result is different from input (processing occurred)
        assert result != test_case['input'], "Result should be different from input"
        
        # Check specific expectations
        if 'expected_contains' in test_case:
            result_lower = result.lower()
            expected_lower = test_case['expected_contains'].lower()
            assert expected_lower in result_lower, f"Expected '{test_case['expected_contains']}' in result"
        
        if 'expected_improvement' in test_case:
            assert test_case['expected_improvement'] in result, f"Expected '{test_case['expected_improvement']}' in result"
        
        if 'expected_words' in test_case:
            result_lower = result.lower()
            found_expected = any(word.lower() in result_lower for word in test_case['expected_words'])
            assert found_expected, f"Expected one of {test_case['expected_words']} in result"
        
        if 'must_not_contain' in test_case:
            result_lower = result.lower()
            for phrase in test_case['must_not_contain']:
                assert phrase.lower() not in result_lower, f"Result should not contain '{phrase}'"
        
        if 'must_contain' in test_case:
            result_lower = result.lower()
            for phrase in test_case['must_contain']:
                assert phrase.lower() in result_lower, f"Result should contain '{phrase}'"
        
        print("✓ Test passed")
    
    print("\n🎉 All tests passed! Advanced AI Phrase Replacement is working correctly.")


def test_sentence_structure():
    """Test that sentence structure is properly maintained after replacement."""
    
    test_cases = [
        "However, as an AI, I think this is good.",
        "Furthermore, it's important to note that this works.",
        "As mentioned earlier, this is the way."
    ]
    
    print("\nTesting sentence structure preservation...")
    
    for test_input in test_cases:
        result = remove_ai_phrases(test_input)
        
        # Check that sentences start with capital letters
        sentences = result.split('. ')
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                assert sentence[0].isupper(), f"Sentence should start with capital letter: '{sentence}'"
        
        # Check no double spaces
        assert '  ' not in result, "Should not have double spaces"
        
        # Check no weird punctuation
        assert ', .' not in result, "Should not have ', .'"
        assert ',,' not in result, "Should not have double commas"
        
        print(f"✓ Structure test passed for: {test_input[:30]}...")
    
    print("✓ All sentence structure tests passed!")


if __name__ == "__main__":
    test_ai_phrase_replacement()
    test_sentence_structure()
    print("\n🚀 All tests completed successfully!")