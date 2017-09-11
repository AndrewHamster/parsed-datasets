from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup
from sys import argv
from csv import writer
url_base = 'http://www.nbuviap.gov.ua/bpnu/index.php?familie=&ustanova=0&gorod=%C2%F1%B3&vidomstvo=%C2%F1%B3&napryam=%EF%F0%E0%E2%EE&napryam_google=&hirsh_lt=&page='

errors = []


def scrape_page(i, f=None):
    if not f == None:
        f.write("Number,Full Name,Google Scholar,Scopus,Subject\n")
    url = url_base + str(i);    
    response = ureq(url)
    response_data = response.read()
    response.close()

    page_soup = soup(response_data, "html.parser")

    rows = page_soup.findAll("tr")[-20:]

    for r in rows:
        row = r.findAll("td")

        try:
            number = row[0].text
            name = row[1].text
            scholar = row[2].text
            scopus = row[3].text
            subject = row[4].text
            print((number, name, scholar, scopus, subject))
            if not f == None:
                f.write(number + "," + name.replace(",", "|") + "," + scholar + "," + scopus + "," + subject.replace(",", "|") + "\n")
        except:
            print("<!=======WARNING=======!>")
            print("Error in row\n", row)
            errors.append(number)
            if not f == None:
                pass
                # f.write(number + "err\n")
        


print("Scraping started...")
start = int(argv[1])
end = int(argv[2])
f = open("data.csv", "a")
for i in range(start, end):
    print("page ", i)
    scrape_page(i, f)
        
f.close()

print("Number of errors", len(errors))
