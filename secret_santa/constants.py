WEBSITE_URL = "http://secret-santa.schoentgen.com"

INIT_EVENT_NAME = "🌠 Top départ ! {}"
INIT_EVENT_DESC = f"""Salutations {{{{ santa.nature.title() }}}} Noël {{{{ santa.name }}}} !

C’est le début des hostilités, et je t’invite à aller sur cette page pour remplir ta liste des souhaits : {WEBSITE_URL}/{{{{ event.hash }}}}/{{{{ santa.hash }}}}

La suite début décembre,
La bise 💋
"""  # noqa: E501
