import time
import os
import random
import pywikibot
site = pywikibot.Site()
headers = {
    'User-Agent': 'VukkyBotURLWrapper/1.0 - User:Vukky',
}

def report_problem(page):
    pageSplit = page.text.splitlines()
    for line in pageSplit:
        if "website" in line and not "{{" in line and not "[" in line and "http" in line:
            return True
        else:
            return False

dump_file = random.choice([x for x in os.listdir("/public/dumps/public/enwiki/latest") if x.contains("-pages-articles")])
dump_parsed = pywikibot.xmlreader.XmlDump(dump_file).parse()
gen = (pywikibot.Page(site, p.title) for p in dump_parsed if report_problem(p))
gen = pywikibot.pagegenerators.PreloadingGenerator(gen)

def treat_page(page, save):
    pageSplit = page.text.splitlines()
    changed = False
    for index, line in enumerate(pageSplit):
        if "website" in line and not "{{" in line and not "[" in line and "http" in line:
            print(line.replace("http", "{{URL|http", 1) + "}}")
            pageSplit[index] = line.replace("http", "{{URL|http", 1) + "}}"
            changed = True

    if changed is True:
        page.text = "\n".join(pageSplit)
        if save is True:
            page.save("[[Wikipedia:Bots|Bot]]: Wrapping link in URL template")
        else:
            print("Would have saved to " + page.title())

for page in gen:
    if report_problem(page) is True:
        treat_page(page, False)
        time.sleep(5)
    else:
        print("No problem found on " + page.title())