import requests
import json
import textwrap
#import cx_Oracle
import pprint

MY_API_KEY = "43471229f9ff8ba1c9ec4faeb189b6f4"
USERNAME = "oracle"
PASSWORD = "oracle"

def s(texto_):
	return "'" + texto_.replace("'"," ") + "'"

def get_scopus_info(SCOPUS_ID):
	#url = ("http://api.elsevier.com/content/abstract/scopus_id/" + str(SCOPUS_ID))
	#url = ("http://api.elsevier.com/content/abstract/scopus_id/" + str(SCOPUS_ID) + "?field=source-id,authors,title,publicationName,volume,issueIdentifier,prism:pageRange,coverDate,article-number,doi,issn,citedby-count,prism:aggregationType")
	#url = "https://api.elsevier.com/content/author/orcid/0000-0001-6457-0756?field=citation-count,cited-by-count,surname,author-profile"
	#url = "https://api.elsevier.com/content/author/orcid/0000-0001-6457-0756?field=citation-count,cited-by-count,surname"
	url = "https://api.elsevier.com/content/author/orcid/0000-0001-6457-0756"
	print(url);
	resp = requests.get(url,
	headers= {
		'Accept':'application/json',
		'X-ELS-APIKey': MY_API_KEY
	})
	res = json.loads(resp.text.encode('utf-8'))
	return res

def get_orcid_ids(ORCID_ID_):
	resp = requests.get("https://pub.orcid.org/v3.0/"+ORCID_ID_+"/works", headers= { 'Accept':'application/json'})
	results = resp.json()
	my_list = []
	for r in results['group']:
		for r2 in r['work-summary']:
			try:
				my_list.append(r2['url']['value'])
			except:
				my_list.append('None')
	my_list2 = []
	for r in my_list:
		if r.find('eid=') > 0:
			k1 = r.find('eid=')
			k2 = r.find('&',k1)
			if r[k1+11:k2] not in my_list2:
				my_list2.append(r[k1+11:k2])
	return my_list2

results = get_scopus_info(38349047757);
pprint.pprint(results)

'''
for result in results:
	print(result)


dsn = cx_Oracle.makedsn("oracledocker", 1521, service_name="orclpdb1")

con = cx_Oracle.connect(USERNAME, PASSWORD, dsn, encoding="UTF-8")

print "ligacao a Base de dados efectuada com sucesso"

i = 0

cursor = con.cursor()
sql = "select grupo,lab,nome,integrado,orcid from orcid_author where orcid is not null order by integrado desc"
cursor.execute(sql)

for resultado in cursor:
	ORCID_ID = resultado[4]
	for sid in get_orcid_ids(ORCID_ID):
		i += 1
		print i,sid,ORCID_ID
		# o sid e' o eid gravar sid e orcid na bd
		# verificar se ja estagravar = 1
		sql = "select * from orcid_scopus where eid = " + s(sid)
		cur2 = con.cursor()
		cur2.execute(sql)
		resultSet = cur2.fetchone()
		if (resultSet == None):
			results=get_scopus_info(sid)
			title = ""
			journal = ""
			volume = ""
			issn = ""
			date = ""
			doi = ""
			cites = 0
			gravar = 0
			#"AUTHORS","TITLE","YEAR" N,"SOURCE","CITED"N,"ISSN","EID","SJR","Q",DOI

			try:
				authors=', '.join([au['ce:indexed-name'] for au in results['abstracts-retrieval-response']['authors']['author']])
			except:
				authors = ""
			try:
				title=results['abstracts-retrieval-response']['coredata']['dc:title']
				gravar = 1
			except:
				title = ""
			try:
				journal=results['abstracts-retrieval-response']['coredata'].get('prism:publicationName', '')
			except:
				journal = ""
			try:
				volume=results['abstracts-retrieval-response']['coredata'].get('prism:volume', '')
			except:
				volume = ""
			try:
				issn=results['abstracts-retrieval-response']['coredata'].get('prism:issn','')
			except:
				issn=""
			try:
				date=results['abstracts-retrieval-response']['coredata']['prism:coverDate']
				date = date[0:4]
			except:
				date=""
			try:
				doi= results['abstracts-retrieval-response']['coredata'].get('prism:doi','')
			except:
				doi=""
			try:
				cites= int(results['abstracts-retrieval-response']['coredata']['citedby-count'])
			except:
				cites = 0
			
			if (gravar == 1):
				try:
					sql = "insert into orcid_scopus(authors,title,year,source,cited,issn,eid,doi) values ("
					sql = sql + s(authors) + "," +s(title) + "," + date + "," + s(journal) + "," + str(cites) + ","
					sql = sql + s(issn) + "," + s(sid) + "," +s(doi) + ")"
					cur = con.cursor()
					cur.execute(sql)
					cur.execute("commit")
				except:
					print authors
					print title
					print date
					print journal
					print str(cites)
					print issn
					print doi
					gravar = 0
				else:
					print results
				
			if (gravar == 1):
				sql = "select * from orcid_author_scopus where eid = " + s(sid) + "and " + "orcid = " + s(ORCID_ID)
				cur3 = con.cursor()
				cur3.execute(sql)
				resultSet = cur3.fetchone()
				if (resultSet == None):
					sql = "insert into orcid_author_scopus(orcid,eid) values (" + s(ORCID_ID) + "," + s(sid) + ")"
					cur = con.cursor()
					cur.execute(sql)
					cur.execute("commit")
				cur3.close
			cur2.close
		cursor.close
		con.close()
		print "ligacao a Base de dados encerrada com sucesso"
'''