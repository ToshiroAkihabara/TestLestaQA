from wikipedia import WikiArticleTable
import pytest


class TestWiki:
    @pytest.mark.parametrize(
            "test_input, expected_result", 
            [(10**7, None),
            (1.5*(10**7), None),
            (5*(10**7), None),
            (10**8, None),
            (5*(10**8), None),
            (10**9, None),
            (1.5*(10**9), None)]
    )
    def test_table(self, test_input, expected_result):
        wiki = WikiArticleTable()
        content = wiki.get_websites_with_popularity()
        compared_numbers = wiki.compare_numbers(content, test_input)
        assert compared_numbers == expected_result
            
            