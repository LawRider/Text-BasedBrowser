import os
import requests
from bs4 import BeautifulSoup
from sys import argv
from colorama import Fore


class Browser:
    def __init__(self):
        self.history = []
        self.folder = self.init_folder()
        self.main()

    @staticmethod
    def init_folder():
        folder = argv[1] if len(argv) == 2 else exit()
        os.makedirs(folder, exist_ok=True)
        return folder

    def main(self):
        user_input = input()
        website_short = user_input.rsplit('.', 1)[0]
        path = os.path.join(self.folder, website_short)
        if user_input == 'exit':
            exit()
        elif user_input == 'back' and self.history:
            self.history.pop()
            self.open_website(self.history.pop())
        elif website_short in self.history:
            self.open_website(website_short)
        elif '.' not in user_input:
            print("Error: Incorrect URL")
        else:
            r = requests.get('https://' + user_input)
            soup = BeautifulSoup(r.content, 'html.parser')
            n_scripts = len(soup.find_all('script'))
            for n in range(n_scripts):
                soup.script.decompose()
            tags = soup.find_all(['p', 'a', 'ul', 'ol', 'li', 'span'], text=True)
            for i in tags:
                if i.name == 'a':
                    text = f'{Fore.BLUE}{i.text}'
                else:
                    text = f'{Fore.WHITE}{i.text}'
                print(text)
                self.save_website(path, text + '\n')
            self.history.append(website_short)

    @staticmethod
    def save_website(path, content):
        with open(path, 'a+') as f:
            f.write(content + '\n')

    @staticmethod
    def open_website(path):
        with open(path) as f:
            print(f.read())


if __name__ == "__main__":
    browser = Browser()
    while True:
        browser.main()
