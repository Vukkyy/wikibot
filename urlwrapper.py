import time, os, random, pywikibot
import pywikibot.xmlreader as xmlreader
import pywikibot.pagegenerators as pagegenerators
site = pywikibot.Site()
site.login()
headers = {
    'User-Agent': 'VukkyBotURLWrapper/1.0 - User:Vukky',
}

dump_file = "/public/dumps/public/enwiki/latest/" + random.choice([x for x in os.listdir("/public/dumps/public/enwiki/latest") if "-pages-articles" in x and x.endswith(".bz2") and not "multistream" in x and os.path.isfile(os.path.join("/public/dumps/public/enwiki/latest", x))])
dump_parsed = xmlreader.XmlDump(dump_file).parse()

def report_problem(page):
    problem = False
    pageSplit = page.text.splitlines()
    for line in pageSplit:
        if not_edge_case(line) is True:
            problem = True
        if incompatible(line) is True:
            problem = False
            break
    if problem is True:
        return True
    else:
        return False

def treat_page(page, save):
    pageSplit = page.text.splitlines()
    changed = False
    for index, line in enumerate(pageSplit):
        if incompatible(line) is True:
            return
        if not_edge_case(line) is True:
            print(line.replace("http", "{{URL|http", 1) + "}}")
            pageSplit[index] = line.replace("http", "{{URL|http", 1) + "}}"
            changed = True

    if changed is True:
        page.text = "\n".join(pageSplit)
        if save is True:
            page.save("[[Wikipedia:Bots|Bot]]: Wrapping link in URL template")
            print("Saved to " + page.title())
        else:
            print("Would have saved to " + page.title())

def not_edge_case(line):
    if "website" in line and not "*" in line and not "{{" in line and not "[" in line and not "<!--" in line and not "<ref>" in line and not "</ref>" in line and "http" in line:
        return True
    else:
        return False

def incompatible(line):
    if "{{infobox television" in line.lower():
        return True
    else:
        return False

for p in dump_parsed:
    if report_problem(p) is True:
        p = pywikibot.Page(site, p.title)
        if p.namespace().id is 0 and report_problem(p) is True:
                treat_page(p, False)
        time.sleep(1)