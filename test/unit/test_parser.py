from src.parser.parser import Parser

def test_parser():

    print("Testing the parse method from Parser class".center(10))
    parser = Parser()
    data = parser.parse("http://example.com")
    assert len(data.keys()) == 4
    assert data.get('title') is not None
    assert data.get('description') is not None
    assert data.get('tags') is not None
    assert data.get('urls') is not None
    assert len(data.get('tags')) > 0
    assert len(data.get('urls')) > 0