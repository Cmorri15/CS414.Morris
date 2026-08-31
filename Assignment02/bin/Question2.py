import re

cpp_id_pattern = r"^[A-Za-z_][A-Za-z0-9_]*$"
cpp_id_tests = ["myVar", "_temp", "3bad", "valid_name123"]

phone_pattern = r"^(\(\d{3}\) \d{3}-\d{4}|\d{3}-\d{3}-\d{4})$"
phone_tests = ["(555) 123-4567", "555-123-4567", "5551234567"]

float_pattern = r"^[+-]?\d+(\.\d+)?$"
float_tests = ["3.14", "-2.5", "+7", "abc"]

palindrome_pattern = r"^([01])([01])\1$|^([01])([01])\4\3$"
palindrome_tests = ["101", "0110", "100", "1001"]

def run_tests(pattern, tests, label):
    print(f"--- {label} ---")
    for t in tests:
        print(t, "->", bool(re.match(pattern, t)))

run_tests(cpp_id_pattern, cpp_id_tests, "C++ Identifiers")
run_tests(phone_pattern, phone_tests, "Phone Numbers")
run_tests(float_pattern, float_tests, "Floats")
run_tests(palindrome_pattern, palindrome_tests, "Binary Palindromes")