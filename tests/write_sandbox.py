print("oh ok give me a sec")
import pywikibot
site = pywikibot.Site()
page = pywikibot.Page(site, "User:VukkyBot/sandbox")
page.text = input("what do ya wanna write: ")
print("okay sure saving that, whatever you say")
page.save("Sandbox test")
