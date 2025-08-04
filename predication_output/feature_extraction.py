import re
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
import joblib
from datetime import datetime
import numpy as np
import whois

# Load the preprocessor and model once at the beginning of your script
# This is a one-time operation, not for every prediction
try:
    preprocessor = joblib.load('final_model/preprocessor.pkl')
    #model = joblib.load('final_model/your_trained_model.pkl') # Assuming you have saved your model
except FileNotFoundError as e:
    print(f"Error: Missing model or preprocessor file. Please check the path. {e}")
    preprocessor, model = None, None

def extract_features(url):
    """
    Extracts a set of 30 features from a given URL.
    Returns a dictionary of feature values, with np.nan for missing data.
    """
    features = {
        'having_IP_Address': np.nan, 'URL_Length': np.nan, 'Shortining_Service': np.nan,
        'having_At_Symbol': np.nan, 'double_slash_redirecting': np.nan, 'Prefix_Suffix': np.nan,
        'having_Sub_Domain': np.nan, 'SSLfinal_State': np.nan, 'Domain_registeration_length': np.nan,
        'Favicon': np.nan, 'port': np.nan, 'HTTPS_token': np.nan, 'Request_URL': np.nan,
        'URL_of_Anchor': np.nan, 'Links_in_tags': np.nan, 'SFH': np.nan, 'Submitting_to_email': np.nan,
        'Abnormal_URL': np.nan, 'Redirect': np.nan, 'on_mouseover': np.nan, 'RightClick': np.nan,
        'popUpWidnow': np.nan, 'Iframe': np.nan, 'age_of_domain': np.nan, 'DNSRecord': np.nan,
        'web_traffic': np.nan, 'Page_Rank': np.nan, 'Google_Index': np.nan,
        'Links_pointing_to_page': np.nan, 'Statistical_report': np.nan
    }

    try:
        parsed_url = urlparse(url)

        # --- Feature Extraction Logic (as before) ---
        features['having_IP_Address'] = 1 if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", parsed_url.hostname) else -1
        features['URL_Length'] = 1 if len(url) >= 54 else -1
        shortening_services = ['bit.ly', 'tinyurl.com', 'is.gd', 't.co', 'goo.gl']
        features['Shortining_Service'] = 1 if any(service in parsed_url.hostname for service in shortening_services) else -1
        features['having_At_Symbol'] = 1 if '@' in url else -1
        features['double_slash_redirecting'] = 1 if '//' in parsed_url.path else -1
        features['Prefix_Suffix'] = 1 if '-' in parsed_url.hostname else -1
        num_dots = parsed_url.hostname.count('.')
        if num_dots >= 3: features['having_Sub_Domain'] = 1
        elif num_dots == 2: features['having_Sub_Domain'] = 0
        else: features['having_Sub_Domain'] = -1
        features['port'] = 1 if parsed_url.port not in (80, 443, None) else -1
        features['HTTPS_token'] = 1 if 'https' in parsed_url.hostname else -1
        
        # WHOIS and DNS Features
        whois_info = whois.whois(parsed_url.hostname)
        if whois_info.expiration_date and whois_info.creation_date:
            try:
                exp_date = whois_info.expiration_date if isinstance(whois_info.expiration_date, datetime) else whois_info.expiration_date[0]
                cre_date = whois_info.creation_date if isinstance(whois_info.creation_date, datetime) else whois_info.creation_date[0]
                registration_days = (exp_date - cre_date).days
                features['Domain_registeration_length'] = 1 if registration_days <= 365 else -1
            except: pass
        if whois_info.creation_date:
            try:
                creation_date = whois_info.creation_date if isinstance(whois_info.creation_date, datetime) else whois_info.creation_date[0]
                age_in_days = (datetime.now() - creation_date).days
                features['age_of_domain'] = 1 if age_in_days <= 180 else -1
            except: pass
        features['DNSRecord'] = 1 if not whois_info.creation_date else -1
        
        # HTTP Request-Based Features
        response = requests.get(url, timeout=10, allow_redirects=False)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        if parsed_url.scheme == 'https': features['SSLfinal_State'] = 1
        else: features['SSLfinal_State'] = -1
        
        favicon_link = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
        if favicon_link:
            favicon_url = urljoin(url, favicon_link.get('href', ''))
            features['Favicon'] = 1 if parsed_url.hostname not in urlparse(favicon_url).hostname else -1
        
        img_tags = soup.find_all('img')
        features['Request_URL'] = 1 if any(parsed_url.hostname not in urlparse(img.get('src', '')).hostname for img in img_tags) else -1
        
        anchor_tags = soup.find_all('a')
        features['URL_of_Anchor'] = 1 if any(parsed_url.hostname not in urlparse(anchor.get('href', '')).hostname for anchor in anchor_tags) else -1
        total_links = len(anchor_tags)
        external_links = sum(1 for anchor in anchor_tags if parsed_url.hostname not in urlparse(anchor.get('href', '')).hostname)
        if total_links == 0: features['Links_in_tags'] = 1
        elif (external_links / total_links) >= 0.6: features['Links_in_tags'] = 1
        elif (external_links / total_links) >= 0.2: features['Links_in_tags'] = 0
        else: features['Links_in_tags'] = -1
        
        form_tags = soup.find_all('form')
        if not form_tags: features['SFH'] = 1
        else:
            form_action = form_tags[0].get('action', None)
            if form_action is None or form_action == '' or urlparse(form_action).hostname != parsed_url.hostname: features['SFH'] = 1
            else: features['SFH'] = -1
        
        features['Submitting_to_email'] = 1 if soup.find('form', action=re.compile(r'mailto:')) else -1
        
        script_tags = soup.find_all('script')
        if script_tags: features['Abnormal_URL'] = 1 if not any(parsed_url.hostname in script.get('src', '') for script in script_tags) else -1
        else: features['Abnormal_URL'] = -1

        if len(response.history) > 1: features['Redirect'] = 1
        elif len(response.history) == 1: features['Redirect'] = 0
        else: features['Redirect'] = -1
            
        features['on_mouseover'] = 1 if re.search(r'onMouseOver=.*', html_content, re.IGNORECASE) else -1
        features['RightClick'] = 1 if re.search(r'oncontextmenu=.*return false.*', html_content, re.IGNORECASE) else -1
        features['popUpWidnow'] = 1 if re.search(r'window.open', html_content, re.IGNORECASE) else -1
        features['Iframe'] = 1 if soup.find('iframe') else -1
        
        # --- End of extraction logic ---
        
    except Exception as e:
        print(f"Warning: Error extracting features for {url}. Some values will be imputed. {e}")
        # The `features` dict will contain `np.nan` for any feature that failed to be extracted
        
    return features
