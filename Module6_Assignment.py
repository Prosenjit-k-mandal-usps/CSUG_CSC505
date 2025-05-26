# Check Writer Program
# Converts a numeric amount to a textual representation for use on checks.
# Includes logging and follows stepwise refinement principles.
import math
import logging

# Configure logging
logging.basicConfig(filename='check_writer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Mappings for number words
ONES = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
TEENS = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]


def convert_hundreds(n):
    """
    Converts a number less than 1000 to words.
    Example: 245 -> "Two Hundred Forty Five"
    """
    words = ""
    if n >= 100:
        words += ONES[n // 100] + " Hundred "
        n %= 100
    if n >= 20:
        words += TENS[n // 10] + " "
        n %= 10
    elif n >= 10:
        words += TEENS[n - 10] + " "
        n = 0
    if n > 0:
        words += ONES[n] + " "
    return words.strip()


def convert_dollars_to_words(amount):
    """
    Converts the dollar portion of the amount to words.
    Handles grouping in thousands, millions, etc.
    """
    if amount == 0:
        return "Zero Dollars"

    original_amount = amount  # Preserve original amount for plural check
    parts = []
    units = ["", "Thousand", "Million", "Billion"]
    i = 0

    while amount > 0:
        chunk = amount % 1000
        if chunk > 0:
            words = convert_hundreds(chunk)
            if units[i]:
                words += " " + units[i]
            parts.insert(0, words)
        amount //= 1000
        i += 1

    return ' '.join(parts) + (" Dollar" if original_amount == 1 else " Dollars")


def convert_cents_to_words(cents):
    """
    Converts the cents portion of the amount to words.
    """
    if cents == 0:
        return "Zero Cents"
    return convert_hundreds(cents) + " Cent" + ("s" if cents != 1 else "")


def check_writer(amount):
    """
    Main function that receives a float input amount and
    prints out the formatted check text (e.g., "One Hundred Twenty Dollars and Fifty Cents Only.")
    """
    logging.info(f"Received amount: {amount}")
    try:
        if amount < 0:
            logging.error("Negative amount detected.")
            raise ValueError("Negative amounts not allowed.")
        dollars = int(math.floor(amount))
        cents = int(round((amount - dollars) * 100))
        dollar_words = convert_dollars_to_words(dollars)
        cent_words = convert_cents_to_words(cents)
        full_output = f"{dollar_words} and {cent_words} Only."
        logging.info(f"Converted to words: {full_output}")
        print(full_output)
    except Exception as e:
        logging.exception("An error occurred during check writing.")
        print("Error:", e)


# Example usage
if __name__ == '__main__':
    # Prompt user for input and validate it
    try:
        user_input = input("Enter amount (e.g., 1234.56 or 'One Thousand'): ")

        # Try parsing as a float first
        try:
            input_amount = float(user_input)
        except ValueError:
            # Attempt to convert word input to a numeric value using external package (e.g., word2number)
            from word2number import w2n
            try:
                input_amount = float(w2n.word_to_num(user_input))
                logging.info(f"Converted word input to number: {input_amount}")
            except Exception:
                logging.error("Invalid input. Could not parse number from text.")
                print("Invalid input. Please enter a valid number or numeric phrase.")
                exit(1)

        check_writer(input_amount)

    except Exception as e:
        logging.error("Unexpected error.")
        print("An unexpected error occurred:", e)