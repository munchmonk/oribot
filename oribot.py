#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3

import requests
import bs4

with open('manga_list.txt') as f:
	manga_links = [line.rstrip() for line in f]

new_records = []

for manga_link in manga_links:
	url = manga_link
	page = requests.get(url)
	soup = bs4.BeautifulSoup(page.content, 'html.parser')

	manga_title = soup.find('title')
	manga_title = manga_title.text[:-76]

	last_chapter = soup.find('a', class_='ml-1 visited ch')
	last_chapter_number = last_chapter.text
	while not last_chapter_number.isdigit():
		last_chapter_number = last_chapter_number[1:]
	last_chapter_link = 'mangapark.net' + last_chapter.attrs['href']

	new_record = (manga_title, last_chapter_number, last_chapter_link, manga_link)
	new_records.append(new_record)

with open('latest_chapters_list.txt') as f:
	all_lines = [line.rstrip() for line in f]

	old_records = []
	for line in all_lines:

		# Empty lines check
		if line:
			line = line.split()
			old_record = (line[0], line[1])
			old_records.append(old_record)

for new_record in new_records:
	for old_record in old_records:
		if new_record[3] == old_record[0]:
			if int(new_record[1]) > int(old_record[1]):
				print('****************************************************')
				print('New chapter!')
				print('\tManga: ' + new_record[0])
				print('\tPrevious chapter: ' + old_record[1])
				print('\tLatest chapter: ' + new_record[1])
				print('\tLink to latest chapter: ' + new_record[2] + '\n')

# Overwrite old file
with open('latest_chapters_list.txt', 'w') as f:
	for new_record in new_records:
		f.write(new_record[3] + ' ' + new_record[1] + '\n')



