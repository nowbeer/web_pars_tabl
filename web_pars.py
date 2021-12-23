# запросы через python
import requests
import pandas as pd

def url_(url):
    response = requests.get(url)
    #print(response.status_code)
    #print(response.url)
    return(response.text)

#======================================== example ========================================
#url ='https://ya.ru/white'
#print(url_(url))
#=========================================================================================

def no_tab(seq):
	pass
	return seq


def parse_tab(responsed): # put in arg url_(url)
	columns = []
	data = []
	l = len(responsed)
	# how much tables in response html ?
	html_tab = responsed[responsed.find('<table'): responsed.find('</table')] # cut only first table
	l = len(html_tab) # len of table
	n_row = html_tab.count('<tr') # numbers of rows
	n_col = int(html_tab.count('<td')/n_row) # numbers of columns
	first_row = html_tab[html_tab.find('<tr'): html_tab.find('</tr'):] # cut first row with HEAD of table
	for i in range (0, n_col):
		n=first_row.find('<td') #find start of cell
		p=first_row.find('</td') #find start of cell
		seq = first_row[n+4: p] #make slice
		columns.append(seq) #append to columns
		first_row=first_row[p+1:] #cut cell, repeat until end of cell
	# -----------------------------------------------------------------------------
	html_tab = html_tab[html_tab.find('</tr')+5:] # cut only body of table
	for j in range (0, n_row-1): # -1 because without HEAD of table
		subdata = []
		k=html_tab.find('<tr')
		t=html_tab.find('</tr')
		seq_row = html_tab[k+3:t]
		html_tab = html_tab[t+1:]
		if 'hidden_row' in seq_row:
			pass
		else:
			for i in range (0, n_col):
				n=seq_row.find('<td')
				p=seq_row.find('</td')
				seq = seq_row[n+4: p]
				seq = no_tab(seq)
				if 'type_icon' in seq:
					seq = seq[seq.find('alt=')+5: seq.find('title=')-2]
				elif 'rating_list_position' in seq:
					seq = seq[seq.find('>')+1:]
				elif 'item_photo lazyload' in seq:
					seq = seq[seq.find('alt=')+5: seq.find('title=')-2]
				elif 'word_no_break' in seq:
					seq = seq[seq.find('word_no_break')+15:]
				elif (('title=' not in seq) and ('a href=' in seq)):
					seq = seq[seq.find('a href=')+18: seq.find('><div')-2]
				elif '&minus' in seq:
					seq = '-'
				else:
					pass
				subdata.append(seq)
				seq_row=seq_row[p+1:]
			data.append(subdata) 
	return columns, data


url_address = input('input url address -->') # url address to load html page -------------------
if url_address != '':
	url = url_address
	print(url)
else:
	url = 'http://technical.city/ru/video/rating' #https://technical.city/ru/cpu/rating'

#html_page = url_(url) # load html page
print('=====================================================================')
#s=parse_tab(html_page)
#print(s)

data_all=[]
p_count=1 #numbers of pages a table
while True:
	html_page = url_(url+'?pg='+str(p_count))
	p_count=p_count+1
	s = parse_tab(html_page)
	if s[1]==[]:
		data_all.append(s[0])
		print(p_count)
		break
	data_all.extend(s[1])

len_data=len(data_all)
df = pd.DataFrame(data = data_all[:len_data-1], columns = data_all[len_data-1])
df.info()

# сделать автораскрытие всей страницы url = 'https://technical.city/ru/video/rating?pg=4'"
# парсить Html и скидывать в таблицу новую

# pd.DataFrame(data = data, columns = columns)