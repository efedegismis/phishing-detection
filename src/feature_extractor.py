import pandas as pd
import ipaddress
from urllib.parse import urlsplit
from pathlib import Path


def extract_features_from_dataset() -> pd.DataFrame:
    BASE_DIR = Path(__file__).resolve().parent.parent
    data_path = BASE_DIR / "data" / "url_dataset.csv"

    df = pd.read_csv(data_path)

    features_list = []
    labels_list = []

    for _, row in df.iterrows():
        try:
            features_dict = extract_features_from_url(row['url'])
            features_list.append(features_dict)
            if row['type'] == 'phishing':
                labels_list.append(0)
            else:
                labels_list.append(1)
        except Exception:
            continue  # Skip rows that cause errors during feature extraction

    X_inference = pd.DataFrame(features_list)

    y_inference = pd.DataFrame(labels_list, columns=['label'])

    return X_inference, y_inference


def extract_features_from_url(url: str) -> dict:

    # Parse the URL
    parsed_url = urlsplit(url)

    # Extract features
    url_length = len(url) # Length of the entire URL

    domain_length = len(parsed_url.netloc) # Length of the domain (netloc)

    hostname = parsed_url.hostname
    try:
        ipaddress.ip_address(hostname) # Check if the domain is an IP address
        is_domain_ip = 1
    except ValueError:
        is_domain_ip = 0
    
    char_continuation_rate = _calculate_char_continuation_rate(url) # Calculate the character continuation rate

    if is_domain_ip:
        tld_length = 0 # If the domain is an IP address, set TLD length to 0
    else:
        tld_length = len(parsed_url.hostname.split('.')[-1]) if parsed_url.hostname else 0 # Length of the top-level domain

    if is_domain_ip or not parsed_url.hostname:
        no_of_subdomain = 0 # If the domain is an IP address or hostname is None, set number of subdomains to 0
    else:
        no_of_subdomain = max(0, len(parsed_url.hostname.split('.')) - 2) # Number of subdomains

    no_of_obfuscated_char = 0
    for i in range(url_length):
        if url[i] == '%' and i < url_length - 2 and url[i+1:i+3].isalnum():
            no_of_obfuscated_char += 1 # Count the number of obfuscated characters (percent-encoded)
        elif url[i] == '@':
            no_of_obfuscated_char += 1 # Count the number of obfuscated characters (presence of '@' symbol)
    
    has_obfuscation = 1 if no_of_obfuscated_char > 0 else 0 # Check if the URL has obfuscation

    obfuscation_ratio = no_of_obfuscated_char / url_length # Calculate the obfuscation ratio

    no_of_letters_in_url = sum(c.isalpha() for c in url) # Count the number of letters in the URL

    letter_ratio_in_url = no_of_letters_in_url / url_length # Calculate the letter ratio in the URL

    no_of_digits_in_url = sum(c.isdigit() for c in url) # Count the number of digits in the URL

    digit_ratio_in_url = no_of_digits_in_url / url_length # Calculate the digit ratio in the URL

    no_of_equals_in_url = url.count('=') # Count the number of '=' characters in the URL

    no_of_q_mark_in_url = url.count('?') # Count the number of '?' characters in the URL

    no_of_ampersand_in_url = url.count('&') # Count the number of '&' characters in the URL

    excluded_chars = {'=', '?', '&', ':', '/', '.', '-', '_'}

    no_of_other_special_chars_in_url = sum(1 for c in url if not c.isalnum() and not c.isspace() and c not in excluded_chars)
    
    # no_of_other_special_chars_in_url = sum(not c.isalnum() and not c.isspace() for c in url) - (no_of_equals_in_url + no_of_q_mark_in_url + no_of_ampersand_in_url) # Count the number of other special characters in the URL

    special_char_ratio_in_url = no_of_other_special_chars_in_url / url_length # Calculate the special character ratio in the URL

    is_https = 1 if parsed_url.scheme.lower() == 'https' else 0 # Check if the URL uses HTTPS

    # Create a DataFrame with the extracted features
    features = {
        'URLLength': url_length,
        'DomainLength': domain_length,
        'IsDomainIP': is_domain_ip,
        'CharContinuationRate': char_continuation_rate,
        'TLDLength': tld_length,
        'NoOfSubDomain': no_of_subdomain,
        'HasObfuscation': has_obfuscation,
        'NoOfObfuscatedChar': no_of_obfuscated_char,
        'ObfuscationRatio': obfuscation_ratio,
        'NoOfLettersInURL': no_of_letters_in_url,
        'LetterRatioInURL': letter_ratio_in_url,
        'NoOfDegitsInURL': no_of_digits_in_url,
        'DegitRatioInURL': digit_ratio_in_url,
        'NoOfEqualsInURL': no_of_equals_in_url,
        'NoOfQMarkInURL': no_of_q_mark_in_url,
        'NoOfAmpersandInURL': no_of_ampersand_in_url,
        'NoOfOtherSpecialCharsInURL': no_of_other_special_chars_in_url,
        'SpacialCharRatioInURL': special_char_ratio_in_url,
        'IsHTTPS': is_https
    }

    return features
    

def _calculate_char_continuation_rate(url: str) -> float:

    alnum_chars = [c for c in url if c.isalnum()]
    
    if not alnum_chars:
        return 0.0

    max_streak = 0
    current_streak = 0
    previous_type = None

    for char in alnum_chars:
        char_type = 1 if char.isalpha() else 2
        
        if char_type == previous_type:
            current_streak += 1
        else:
            previous_type = char_type
            current_streak = 1
            
        if current_streak > max_streak:
            max_streak = current_streak

    return max_streak / len(alnum_chars)