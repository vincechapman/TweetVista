import os
import pytest


def check_files_for_debug_code():

    test_pass = True

    directories = list(os.walk('../app')) + list(os.walk('../TLInterface')) + list(os.walk('../models')) + list(os.walk('../helpers'))

    for directory in directories:
        for file in directory[2]:
            if file.endswith('.py'):
                file_location = directory[0] + '/' + file
                with open(file_location) as f:
                    lines = f.readlines()
                    for line in range(len(lines)):
                        if 'test10' in lines[line]:
                            print(f'\n\nError: Found debugging code that should have been removed:\n\n{lines[line]}\n')
                            print('File:', file_location)
                            print('Line:', line)
                            test_pass = False
    assert test_pass
    print('TEST PASSED: check_for_prefilled_user_details')

