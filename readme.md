# Find-Books-In-Ankara-City
A Python program which searches and finds the desired book in second-hand book sellers of Ankara.<br>
All you need to do is to write the name of the book as parameter.
## Prerequisites
Install Postgres if it is not already the case.
Install the following libraries:
## Linux
```bash
sudo apt update
pip3 install requests 
pip3 install beautifulsoup4
```
## Usage
Once run scrape_url.py file to add the seller urls to your local database.<br>
Sample for the book Ince Memed by Yasar Kemal is following.
```bash
python3 scrape_url.py # this is for just once
python3 find.py "ince memed"
```
After the execution is over, the program create a .txt file in your current directory.
The list of the seller and the books with their prices are inside this file.
## Contributing
Pull requests are welcome.

## Project Roadmap
 * [x] Find by book name.
 * [ ] List the books by the author.
 * [x] Send the result list mail to the user.
 * [ ] Add a front end for the project.
