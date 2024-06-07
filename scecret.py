import requests
import validators
from termcolor import colored
from colorama import Fore, Style, init
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

init()

def check_url_exists(url):
    if not validators.url(url):
        return False, "Invalid URL format"

    try:
        response = requests.head(url)
        if response.status_code == 200 or response.status_code == 301:
            return True, "URL Exists,Process Has Been Started"
        else:
            return False, f"URL returned a status code of {response.status_code}"
    except requests.RequestException as e:
        return False, f"URL is not reachable"

def fetch_and_save_urls(url, output_file):
    try:
        response = requests.get(url)
        response.raise_for_status()

        raw_urls = response.text

        with open(output_file, "w") as file:
            file.write(raw_urls)

        print(f"{Fore.MAGENTA}All URLs have been successfully saved to{Style.RESET_ALL} {Fore.BLUE}{output_file}{Style.RESET_ALL}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

prompt_text = colored("URL Format eg pythagorex.com, Do Not Add HTTPS or HTTP.", 'green')
enter_text = colored("Enter URL:", 'blue')

print(prompt_text)
link = input(enter_text)

full_url = f"http://{link}"
is_valid, message = check_url_exists(full_url)

if is_valid:
    print(colored(message, 'green'))
    url = f"https://web.archive.org/cdx/search/cdx?url=*.{link}/*&output=text&fl=original&collapse=urlkey"
    output_file = "urls.txt"
    fetch_and_save_urls(url, output_file)
    file=open("urls.txt","r")
    url=file.readlines()
    print(f"{Fore.CYAN}Total Fetched URL {Style.RESET_ALL}{Fore.RED}{len(url)}{Style.RESET_ALL}")

else:
    print(colored(message, 'red'))

###################################################################
with open('urls.txt', 'r') as file:
    urls = file.readlines()

js_urls = [url.strip() for url in urls if url.strip().endswith('.js')]

with open('js_urls.txt', 'w') as file:
    for url in js_urls:
        file.write(f"{url}\n")

file=open("js_urls.txt","r")
url=file.readlines()
js_count=len(url)
print(f"{Fore.YELLOW}Filtered {Style.RESET_ALL}{Fore.RED}{js_count}{Style.RESET_ALL} {Fore.YELLOW}JS URLs saved to js_urls.txt")

# #####################################################################


def check_url(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return url
    except requests.RequestException:
        return None

def check_urls(input_file_path, output_file_path):
    # Read URLs from the input text file
    with open(input_file_path, 'r') as file:
        urls = file.readlines()

    # Strip any whitespace characters like `\n` at the end of each line
    urls = [url.strip() for url in urls]

    working_urls = []

    # Use ThreadPoolExecutor for parallel requests and tqdm for progress bar
    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_url = {executor.submit(check_url, url): url for url in urls}
        for future in tqdm(as_completed(future_to_url), total=len(urls), desc="Checking URLs"):
            result = future.result()
            if result:
                working_urls.append(result)

    # Clear the output file before writing
    open(output_file_path, 'w').close()

    # Write the working URLs to the output text file
    with open(output_file_path, 'w') as file:
        for url in working_urls:
            file.write(url + '\n')

# Path to your input and output text files
input_file_path = 'js_urls.txt'
output_file_path = 'working_urls.txt'

check_urls(input_file_path, output_file_path)
working_js=open("working_urls.txt","r")
working_jss=working_js.readlines()
working=(len(working_jss))
print(f"{Style.RESET_ALL}{Fore.RED}{working}{Style.RESET_ALL} {Fore.GREEN}URL is Valid")

