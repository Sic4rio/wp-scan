import requests
import os
import re
import sys
import colorama
from colorama import Fore, Back, Style
from bs4 import BeautifulSoup
import readline

def banners():
    print(f"""{Style.BRIGHT + Fore.RED}

                        ██╗    ██╗██████╗       ███████╗ ██████╗ █████╗ ███╗   ██╗
                        ██║    ██║██╔══██╗      ██╔════╝██╔════╝██╔══██╗████╗  ██║
                        ██║ █╗ ██║██████╔╝█████╗███████╗██║     ███████║██╔██╗ ██║
                        ██║███╗██║██╔═══╝ ╚════╝╚════██║██║     ██╔══██║██║╚██╗██║
                        ╚███╔███╔╝██║           ███████║╚██████╗██║  ██║██║ ╚████║
                         ╚══╝╚══╝ ╚═╝           ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
		                                                                          
    {Fore.WHITE}═════════════════════════════════════════════════════════════════════════════════════════════════════════════
    {Style.BRIGHT + Fore.YELLOW}  
                                                Code By SICARI0\n
                            [+] Wordpress Version, Plugins & Themes Enumeration [+]
   
    {Fore.WHITE}════════════════════════════════════════════════════════════════════════════════════════════════════════════
    """)
banners()

def URLdomain(site):
    if site.startswith("http://"):
        site = site.replace("http://","")
    elif site.startswith("https://"):
        site = site.replace("https://","")
    else:
        pass
    pattern = re.compile('(.*)/')
    while re.findall(pattern,site):
        sitez = re.findall(pattern,site)
        site = sitez[0]
    return site

def Version(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        version = soup.find("meta", {"name": "generator"})
        if version:
            version = version["content"].split()[1]
        else:
            version = "Not Found"

        plugins = []
        for link in soup.find_all("link", {"rel": "stylesheet"}):
            href = link.get("href")
            if "plugins" in href:
                plugins.append(href.split("plugins/")[1].split("/")[0])

        theme_link = soup.find("link", {"rel": "stylesheet"})
        theme = None
        if theme_link:
            href = theme_link.get("href")
            theme_parts = href.split("themes/")
            if len(theme_parts) > 1:
                theme = theme_parts[1].split("/")[0]

        return version, plugins, theme
    except Exception as e:
        return None, [], None

def scan_single_url():
    url = input("Enter the URL to scan: ")
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    version, plugins, theme = Version(url)
    if version:
        print(Fore.GREEN + "URL: {}\nWordPress Version: {}\nInstalled Plugins: {}\nActive Theme: {}\n".format(url, version, ", ".join(plugins), theme))
        save_output(url, version, plugins, theme)
    else:
        print(Fore.RED + "Unable to retrieve WordPress information for the provided URL.")

def scan_multiple_urls():
    file_path = input("Enter the path to the file containing URLs: ")
    try:
        with open(file_path, "r") as file:
            urls = file.readlines()
            urls = [url.strip() for url in urls]
        for url in urls:
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url
            version, plugins, theme = Version(url)
            if version:
                print(Fore.GREEN + "URL: {}\nWordPress Version: {}\nInstalled Plugins: {}\nActive Theme: {}\n".format(url, version, ", ".join(plugins), theme))
                save_output(url, version, plugins, theme)
            else:
                print(Fore.RED + "Unable to retrieve WordPress information for the URL: {}".format(url))
            print("--------------------")
    except FileNotFoundError:
        print(Fore.RED + "File not found.")
    except Exception as e:
        print(Fore.RED + "An error occurred while processing the URLs.")

def save_output(url, version, plugins, theme):
    choice = input("Do you want to save the output to a file? (y/n): ")
    if choice.lower() == "y":
        file_name = input("Enter the file name (without extension): ")
        file_name += ".txt"
        output = "URL: {}\nWordPress Version: {}\nInstalled Plugins: {}\nActive Theme: {}\n".format(url, version, ", ".join(plugins), theme)
        with open(file_name, "w") as file:
            file.write(output)
        print(Fore.GREEN + "Output saved to {}".format(file_name))

def main():
    while True:
        try:
            print(Style.RESET_ALL)
            choice = input("Select an option:\n1. Scan a single URL\n2. Scan multiple URLs from a file\n3. Exit\n")
            if choice == "1":
                scan_single_url()
            elif choice == "2":
                scan_multiple_urls()
            elif choice == "3":
                print("Exiting the program.")
                break
            else:
                print(Fore.RED + "Invalid choice. Please try again.")
            print("--------------------")
        except KeyboardInterrupt:
            print(Fore.RED + "Keyboard interrupt detected. Exiting the program.")
            break

if __name__ == "__main__":
    # Enable tab auto-completion
    readline.parse_and_bind("tab: complete")
    main()
