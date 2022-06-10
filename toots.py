import json
from os import path
with open("outbox.json", 'r') as outbox_file:
    outbox = json.loads(outbox_file.read())
with open("actor.json", 'r') as actor_file:
    actor = json.loads(actor_file.read())

statuses = [status['object'] for status in outbox["orderedItems"]]

statuses = list(reversed(statuses))

toots = []

pathOffset = 1

for status in statuses:
    if type(status) == type({}):
        date = status['published'][:10]
        content = status['content']
        summary = status['summary']
        attachments = [attachment['url']
                       for attachment in status['attachment']]
        images = ""
        for imageURL in attachments:
            # only runs the loop for the first media url in the archive
            if pathOffset == 1:
                while not path.exists(imageURL[pathOffset:]) and pathOffset < len(imageURL):
                    pathOffset += 1

            if imageURL[-4:] == ".mp4" or imageURL[-5:] == ".webm":
                images += "<video controls muted src='{0}' class='toots_image'>There should be a video here.</video>".format(
                    imageURL[pathOffset:])
            else:
                images += "<img class='toots_image' src='{0}'>".format(
                    imageURL[pathOffset:])
        if summary:
            toot = "<article class='toot'>\
			<div class='date'><span>{0}</span></div>\
			<details><summary class='summary'>{1}</summary>\
			<div class='content'>{2}</div>\
			<div class='media'>{3}</div>\
			</details>\
			</article>".format(date, summary, content, images)
        else:
            toot = "<article class='status'>\
			<div class='date'><span >{0}</span></div>\
			<div class='content'>{1}</div>\
			<div class='media'>{2}</div>\
			</article>".format(date, content, images)
        toots.append(toot)

outfile = open("my_toots.html", "w")

outfile.write("<!DOCTYPE html><html>\
	<head>\
	<title>Mastodon Archive</title>\
	<meta charset='UTF-8'>\
	<meta name='viewport' content='width=device-width, initial-scale=1.0'>")

outfile.write(
    "<link href=\"style.css\" rel=\"stylesheet\" type=\"text/css\"/>")

outfile.write("</head><body><main>\
	<section id='header'>\
		<img src='avatar.jpeg'>\
		<div id=preferred-name>{0}</div>\
		<a id=user-name>{1}</a>\
	</section>".format(actor["preferredUsername"], actor["name"]))

for toot in toots:
    outfile.write(toot)

outfile.write("</main></body></html>")

outfile.close()
