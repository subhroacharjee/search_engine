from src.parser.parser import Parser

def test_parser():
    parser = Parser()
    data = parser.parse("http://example.com")
    assert len(data.keys()) == 4