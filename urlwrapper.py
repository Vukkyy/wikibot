import time, os, random, pywikibot
import pywikibot.xmlreader as xmlreader
import pywikibot.pagegenerators as pagegenerators
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

dump_file = "/public/dumps/public/enwiki/latest/" + random.choice([x for x in os.listdir("/public/dumps/public/enwiki/latest") if "-pages-articles" in x and x.endswith(".bz2") and not "multistream" in x and os.path.isfile(os.path.join("/public/dumps/public/enwiki/latest", x))])
dump_parsed = xmlreader.XmlDump(dump_file).parse()

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

for p in dump_parsed:
    print("Checking if " + p.title + " should be treated...")
    if report_problem(p) is True:
        print("Checking " + p.title + " online...")
        p = pywikibot.Page(site, p.title)
        if report_problem(p) is True:
            print("Treating " + p.title())
            treat_page(p, False)
            time.sleep(5)
        else:
            print("No problem found on " + p.title())