def test_text_box(**test_data) -> str:
    if test_data['name'] == '':
        return 'Name is empty'
    elif test_data['email'] == '':
        return 'Email is empty'
    else:
        return f'Something is empty: {test_data}'