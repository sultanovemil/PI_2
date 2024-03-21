from streamlit.testing.v1 import AppTest


# Just a simple test
def test_url_input():
    at = AppTest.from_file('main.py', default_timeout=30)
    at.run()
    at.text_input[0].input('https://www.youtube.com/watch?v=wDmPgXhlDIg').run()    
    assert at.success[0].value == 'URL is OK'