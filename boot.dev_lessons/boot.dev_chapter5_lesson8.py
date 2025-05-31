from main import *

run_cases = [
    (1, 2, 3, "You have 1 strength, 2 wisdom, and 3 dexterity for a total of 6 stats."),
    (2, 4, 2, "You have 2 strength, 4 wisdom, and 2 dexterity for a total of 8 stats."),
]

submit_cases = run_cases + [
    (
        10,
        50,
        100,
        "You have 10 strength, 50 wisdom, and 100 dexterity for a total of 160 stats.",
    ),
    (0, 0, 0, "You have 0 strength, 0 wisdom, and 0 dexterity for a total of 0 stats."),
    (1, 1, 1, "You have 1 strength, 1 wisdom, and 1 dexterity for a total of 3 stats."),
]


def test(input1, input2, input3, expected_output):
    print("---------------------------------")
    print(f"Inputs: {input1}, {input2}, {input3}")
    print(f"Expecting: {expected_output}")
    result = create_stats_message(input1, input2, input3)
    print(f"Actual: {result}")
    if result == expected_output:
        print("Pass")
        return True
    print("Fail")
    return False


def main():
    passed = 0
    failed = 0
    skipped = len(submit_cases) - len(test_cases)
    for test_case in test_cases:
        correct = test(*test_case)
        if correct:
            passed += 1
        else:
            failed += 1
    if failed == 0:
        print("============= PASS ==============")
    else:
        print("============= FAIL ==============")
    if skipped > 0:
        print(f"{passed} passed, {failed} failed, {skipped} skipped")
    else:
        print(f"{passed} passed, {failed} failed")


test_cases = submit_cases
if "__RUN__" in globals():
    test_cases = run_cases

main()