import pywikibot
import mwparserfromhell
site = pywikibot.Site()
page = pywikibot.Page(site, "User:Vukky/sandbox")
pageContent = mwparserfromhell.parse(page.text)
for template in pageContent.filter_templates():
    if template.name.startsWith("Infobox "):
        print(template)