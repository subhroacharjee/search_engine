from src.utils.tokenizer import tokenizer

SAMPLE_TEXTS = [
    'I was finishing A horror story, so I wrote \'The End.\' Then, my keyboard typed \'Is coming\' completely by itself.'
]

# need better test for this one but will do that latter.
def test_tokenize():
    for text in SAMPLE_TEXTS:
        tags = tokenizer(text)
        assert 'is' not in tags
        assert 'Is' not in tags
        assert 'by' not in tags
        assert 'I' not in tags
        assert 'was' not in tags
