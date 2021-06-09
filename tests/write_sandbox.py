import pywikibot
site = pywikibot.Site()
page = pywikibot.Page(site, "User:VukkyBot/sandbox")
page.text = input("New sandbox text: ")
page.save("Sandbox test")
