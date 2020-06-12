from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import psycopg2
import requests
import json
import threading
import pprint
import datetime
import time

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
MY_API_KEY = "43471229f9ff8ba1c9ec4faeb189b6f4"

def get_scopus_info(SCOPUS_ID):
    url = ("http://api.elsevier.com/content/abstract/scopus_id/" + str(SCOPUS_ID) + "?field=authors,citedby-count,prism:aggregationType")
    #print(url);
    resp = requests.get(
        url,
        headers={
            'Accept': 'application/json',
            'X-ELS-APIKey': MY_API_KEY
        })
    return json.loads(resp.text.encode('utf-8'))['abstracts-retrieval-response']

#bo_publ_get
#GET -> retrieves Backoffice Publication Get information
@app.route('/bo_publ_get', methods=['GET'])
@cross_origin()
def bo_publ_get_get():
    conn = psycopg2.connect("dbname=is_fe03 user=francisco password=password")
    cursor = conn.cursor()
    sql = "select * from bo_get"
    cursor.execute(sql)

    records_data = []

    for rec in cursor.fetchall():
        records_data.append({
            'id': rec[0],
            'fetched_records': rec[1],
            'fetch_time': rec[2],
        })

    cursor.close()
    conn.close()

    return jsonify({
        'records': records_data
    })

#POST -> retrieves Backoffice Publication Get information
@app.route('/bo_publ_get', methods=['POST'])
@cross_origin()
def bo_publ_get_post():
    conn = psycopg2.connect("dbname=is_fe03 user=francisco password=password")
    cursor = conn.cursor()

    data = request.get_json()
    print(data)

    cursor.execute('insert into bo_get (fetched_records, fetch_time, orcid) values (%s, %s, %s) returning id', (data['fetched_records'], data['fetch_time'], data['orcid']))

    ins_id = cursor.fetchone()[0]

    cursor.close()
    conn.commit()
    conn.close()

    return jsonify({
        'records': ins_id
    })

#bo_publ_insert
#GET -> retrieves Backoffice Publication Insert information
@app.route('/bo_publ_insert', methods=['GET'])
@cross_origin()
def bo_publ_ins_get():
    conn = psycopg2.connect("dbname=is_fe03 user=francisco password=password")
    cursor = conn.cursor()
    sql = "select * from bo_insert"
    cursor.execute(sql)

    records_data = []

    for rec in cursor.fetchall():
        records_data.append({
            'id': rec[0],
            'fetched_records': rec[1],
            'fetch_time': rec[2],
        })

    cursor.close()
    conn.close()

    return jsonify({
        'records': records_data
    })

# /bo
# GET -> retrieves orcids + status
@app.route('/bo', methods=['GET'])
@cross_origin()
def bo_get():
    conn = psycopg2.connect("dbname=is_fe03 user=francisco password=password")
    cursor = conn.cursor()
    sql = "select * from orcid"
    cursor.execute(sql)

    # print(cursor.fetchall())
    records_data = []

    for rec in cursor.fetchall():
        records_data.append({
            'orcid_id': rec[0],
            'name': rec[1],
            'status': rec[4],
            'last_update' : rec[5]
        })

    cursor.close()
    conn.close()

    return jsonify({
        'records': records_data
    })

#POST -> receiver orcid and retrieves data related to it
@app.route('/bo', methods=['POST'])
@cross_origin()
def bo_post():
    conn = psycopg2.connect("dbname=is_fe03 user=francisco password=password")
    cursor = conn.cursor()

    data = request.get_json()
    orcid_id = data['orcid_id']

    author_info = {}
    print(orcid_id)
    cursor.execute("select * from orcid where id = %s", (orcid_id,))
    print(cursor.rowcount)
    if (cursor.rowcount > 0):
        #author info
        author = cursor.fetchone()
        author_info['orcid_id'] = author[0]
        author_info['name'] = author[1]
        author_info['citation-count'] = author[2]
        author_info['cited-by-count'] = author[3]
        author_info['subject-areas'] = []
        cursor.execute('select t.theme from orcidtheme ot join theme t on t.id = ot.theme_id where orcid_id = %s', (author_info['orcid_id'],))
        for sub in cursor.fetchall():
            author_info['subject-areas'].append(sub[0])

        # publication info
        publications = []
        cursor.execute('select p.id, p.title, p.type, p.date, p.citations, p.wosuid, p.eid, p.pref_source, p.journal_id from publication p where p.orcid_id = %s', (author_info['orcid_id'],))
        for publ in cursor.fetchall():
            #pprint.pprint(publ)
            pub = {}
            pub['id'] = publ[0]
            pub['title'] = publ[1]
            pub['citation-count'] = publ[4]
            pub['date'] = publ[3]
            pub['type'] = publ[2]
            pub['eid'] = publ[6]
            pub['wosuid'] = publ[5]
            pub['source'] = publ[7]
            pub['authors'] = []
            pub['journal'] = {}
            pub['journal']['id'] = publ[8]
            publications.append(pub)

        for it in range(0, len(publications)):

            # publication authors
            cursor.execute('select * from author where publication_id = %s', (publications[it]['id'],))
            for author in cursor.fetchall():
                publications[it]['authors'].append(
                    {
                        'name' : author[0],
                        'indexed-name' : author[1]
                    }
                )

            # publication journal
            if (publications[it]['journal']['id'] != -1): 
                # general publication info
                cursor.execute('select * from journal j join publisher p on j.publisher_id = p.id where j.id = %s', (publications[it]['journal']['id'],))
                for j in cursor.fetchall():
                    publications[it]['journal']['name'] = j[1]
                    publications[it]['journal']['publisher'] = j[11]
                    publications[it]['journal']['issn'] = j[2]
                    publications[it]['journal']['eissn'] = j[3]
                    publications[it]['journal']['start_year'] = j[4]
                    publications[it]['journal']['end_year'] = j[5]
                    publications[it]['journal']['scopus_source'] = j[7]
                    publications[it]['journal']['homepage'] = j[8]
                    publications[it]['journal']['citescore'] = []
                    publications[it]['journal']['sjr'] = []
                    publications[it]['journal']['snip'] = []
                    publications[it]['journal']['subject_areas'] = []
                
                #citescore
                cursor.execute('select year, value from citescore where journal_id = %s', (publications[it]['journal']['id'],))
                for cs in cursor.fetchall():
                    publications[it]['journal']['citescore'].append(
                        {
                            'year' : cs[0],
                            'value' : cs[1]
                        }
                    )

                #sjr
                cursor.execute('select year, value from sjr where journal_id = %s', (publications[it]['journal']['id'],))
                for sj in cursor.fetchall():
                    publications[it]['journal']['sjr'].append(
                        {
                            'year' : sj[0],
                            'value' : sj[1]
                        }
                    )

                #snip
                cursor.execute('select year, value from snip where journal_id = %s', (publications[it]['journal']['id'],))
                for sn in cursor.fetchall():
                    publications[it]['journal']['snip'].append(
                        {
                            'year' : sn[0],
                            'value' : sn[1]
                        }
                    )

                #themes
                cursor.execute('select t.theme from theme t join journaltheme jt on t.id = jt.theme_id where jt.journal_id = %s', (publications[it]['journal']['id'],))
                for t in cursor.fetchall():
                    publications[it]['journal']['subject_areas'].append(t[0])


        cursor.close()
        conn.close()
        return jsonify({
            'status' : 200,
            'author_info': author_info,
            'publications' : publications
        })

    else:
        cursor.close()
        conn.close()
        return json.dumps(
            {
                'status' : 300
            }
        )


# PUT -> receives orcid and inserts data related to it into db
@app.route('/bo', methods=['PUT'])
@cross_origin()
def bo_put():
    conn = psycopg2.connect("dbname=is_fe03 user=francisco password=password")
    cursor = conn.cursor()
    start = time.time()
    data = request.get_json()
    orcid_id = str(data['orcid_id'])
    
    #orcid + orcidtheme + theme
    orcid_url = "https://api.elsevier.com/content/author/orcid/" + orcid_id
    orcid_resp = requests.get(orcid_url,
    headers= {
        'Accept':'application/json',
        'X-ELS-APIKey': MY_API_KEY
    })

    orcid_res = json.loads(orcid_resp.text.encode('utf-8'))
    orcid = {}
    if (orcid_resp):
        print('ORCID: 200!')
        orcid_res = json.loads(orcid_resp.text.encode('utf-8'))['author-retrieval-response'][0]
        orcid['orcid_id'] = str(orcid_id)
        orcid['citation-count'] = orcid_res['coredata']['citation-count']
        orcid['cited-by-count'] = orcid_res['coredata']['cited-by-count']
        orcid['name'] = orcid_res['author-profile']['preferred-name']['given-name'] + ' ' + orcid_res['author-profile']['preferred-name']['surname']
        cursor.execute('select * from orcid where id = %s', (orcid['orcid_id'],))
        if (cursor.rowcount == 0):
            cursor.execute('insert into orcid values (%s, %s, %s, %s, %s, %s) returning id', (orcid['orcid_id'], orcid['name'], orcid['citation-count'], orcid['cited-by-count'], 'Pendente', datetime.date.today()))

        for subj in orcid_res['subject-areas']['subject-area']:
            cursor.execute('select * from theme where theme = %s', (subj['$'],))
            if (cursor.rowcount == 0):
                # theme is not in db so we insert it
                cursor.execute('insert into theme (theme) values (%s) returning id', (subj['$'],))
                
            theme_id = cursor.fetchone()[0]    
            # at this point the theme is in the db
            cursor.execute('select * from orcidtheme where orcid_id = %s and theme_id = %s', (orcid['orcid_id'], theme_id, ))
            if (cursor.rowcount == 0):
                #orcid does not have theme associated so we associate it
                cursor.execute('insert into orcidtheme (orcid_id, theme_id) values (%s, %s)', (orcid['orcid_id'], theme_id, ))
            
            # at this point the orcid has the theme associated to itself


    else:
        print('ORCID: Not 200!')
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({
            'status' : 400
        })
        

    # publications (BUT NO INSERTION)
    pub_url = "https://pub.orcid.org/v2.0/" + orcid_id + "/works"
    pub_resp = requests.get(pub_url,
    headers= {
        'Accept':'application/json',
        'X-ELS-APIKey': MY_API_KEY
    })
    publishings = []
    if (pub_resp):
        print('200!')
        data = json.loads(pub_resp.text.encode('utf-8'))
        for work_sum in data['group']:
            # iterate different publishings
            publishing = {}
            publishing['sources'] = {}
            for summ in work_sum['work-summary']:
                # iterate different sources for the publishing
                if ( summ['source']['source-name']['value'] == 'Scopus - Elsevier' or summ['source']['source-name']['value'] == 'ResearcherID'):
                    src = {}
                    src['name'] = summ['source']['source-name']['value']
                    src['title'] = summ['title']['title']['value']
                    src['publish_date'] = summ['created-date']['value']
                    src['authors'] = []
                    src['type'] = summ['type']
                    src['source_map'] = {}
                    if (summ['external-ids']):
                        for source in summ['external-ids']['external-id']:
                            #src['source_map'][source['external-id-type']] = source['external-id-value']
                            if (source['external-id-type'] == 'eid'):
                                src['source_map'][source['external-id-type']] = source['external-id-value']
                                src['eid'] = source['external-id-value']
                                publishing['sources'][src['name']] = src
                            if (source['external-id-type'] == 'wosuid'):
                                src['source_map'][source['external-id-type']] = source['external-id-value']
                                src['wosuid'] = source['external-id-value']
                                publishing['sources'][src['name']] = src

            if (len(publishing['sources']) > 0):
                publishings.append(publishing)

    else:
        print('Not 200!')
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({
            'status' : 400
        })

    scopus_ctr = 0
    wosu_ctr = 0;
    #author + journal + publisher + journaltheme + orcidtheme + sjr + snip + citescore
    for it in range(0, len(publishings)):
        print(f'it -> {it}')
        if ('Scopus - Elsevier' in publishings[it]['sources']):
            print('Scopus in sources')
            scopus_ctr = scopus_ctr + 1
            #pprint.pprint(publishings[it])
            mixed_url = ("http://api.elsevier.com/content/abstract/scopus_id/" + publishings[it]['sources']['Scopus - Elsevier']['source_map']['eid'][7:] + "?field=authors,issn,citedby-count,prism:aggregationType,source-id")
            mixed_resp = requests.get(
                mixed_url,
                headers={
                    'Accept': 'application/json',
                    'X-ELS-APIKey': MY_API_KEY
                }
            )
            if (mixed_resp):
                mix_res = json.loads(mixed_resp.text.encode('utf-8'))['abstracts-retrieval-response']
                publishings[it]['sources']['Scopus - Elsevier']['citedby-count'] = mix_res['coredata']['citedby-count']
                journal_id = -1
                if ('prism:issn' in mix_res['coredata']):
                    # publishing has issn associated
                    issns = mix_res['coredata']['prism:issn'].split()
                    
                    journal_url = "http://api.elsevier.com/content/serial/title/issn/" + issns[0]
                    journal_resp = requests.get(
                        journal_url,
                        headers={
                            'Accept': 'application/json',
                            'X-ELS-APIKey': MY_API_KEY
                        }
                    )
                    if (journal_resp):
                        j_res = json.loads(journal_resp.text.encode('utf-8'))['serial-metadata-response']['entry'][0]
                        issn = None
                        if ('prism:issn' in j_res):
                            issn = j_res['prism:issn']
                        eissn = None
                        if ('prism:eIssn' in j_res):
                            eissn = j_res['prism:eIssn']

                        # verify if journal already exists in db
                        cursor.execute("select id from journal where issn = %s or eissn = %s", (issn, eissn))
                        if (cursor.rowcount == 0):
                            # journal is not in db so we insert it
                            # first we need to verify if the publisher exists
                            cursor.execute("select * from publisher where name = %s", (j_res['dc:publisher'],))
                            if (cursor.rowcount == 0):
                                # publisher is not in db so we insert it
                                cursor.execute("insert into publisher (name) values (%s) returning id", (j_res['dc:publisher'],))
                            
                            publisher_id = cursor.fetchone()[0]

                            links = {}
                            for link in j_res['link']:
                                links[link['@ref']] = link['@href']
                            
                            scopus_source = links['scopus-source']
                            homepage = None
                            if ('homepage' in links):
                                homepage = links['homepage']
                            cursor.execute("insert into journal values (%s, %s, %s ,%s, %s, %s ,%s, %s, %s ,%s) returning id", (mix_res['coredata']['source-id'], j_res['dc:title'], issn, eissn, j_res['coverageStartYear'], j_res['coverageEndYear'], mix_res['coredata']['source-id'], scopus_source, homepage, publisher_id,))
                        journal_id = cursor.fetchone()[0]

                        #theme + journaltheme
                        for subj in j_res['subject-area']:
                            cursor.execute('select * from theme where theme = %s', (subj['$'],))
                            if (cursor.rowcount == 0):
                                # theme is not in db so we insert it
                                cursor.execute('insert into theme (theme) values (%s) returning id', (subj['$'],))
                                
                            theme_id = cursor.fetchone()[0]    
                            # at this point the theme is in the db
                            cursor.execute('select * from journaltheme where journal_id = %s and theme_id = %s', (journal_id, theme_id, ))
                            if (cursor.rowcount == 0):
                                #journal does not have theme associated so we associate it
                                cursor.execute('insert into journaltheme (journal_id, theme_id) values (%s, %s)', (journal_id, theme_id, ))
                            # at this point the journal has the theme associated to itself

                        # as of now the journal + publisher are inserted so we can insert the sjr, snip and citescore values
                        #sjr
                        if ('SJRList' in j_res):
                            cursor.execute('select * from sjr where year = %s and journal_id = %s', (j_res['SJRList']['SJR'][0]['@year'], journal_id,))
                            if (cursor.rowcount == 0):
                                cursor.execute('insert into sjr (year, value, journal_id) values (%s, %s, %s)', (j_res['SJRList']['SJR'][0]['@year'], float(j_res['SJRList']['SJR'][0]['$']), journal_id,))
                            else:
                                cursor.execute('update sjr set value = %s where journal_id = %s and year = %s', (float(j_res['SJRList']['SJR'][0]['$']), journal_id, j_res['SJRList']['SJR'][0]['@year'],))

                        #snip
                        if ('SNIPList' in j_res):
                            cursor.execute('select * from snip where year = %s and journal_id = %s', (j_res['SNIPList']['SNIP'][0]['@year'], journal_id,))
                            if (cursor.rowcount == 0):
                                cursor.execute('insert into snip (year, value, journal_id) values (%s, %s, %s)', (j_res['SNIPList']['SNIP'][0]['@year'], float(j_res['SNIPList']['SNIP'][0]['$']), journal_id,))
                            else:
                                cursor.execute('update snip set value = %s where journal_id = %s and year = %s', (float(j_res['SNIPList']['SNIP'][0]['$']), journal_id, j_res['SNIPList']['SNIP'][0]['@year'],))

                        #citescore
                        if ('citeScoreYearInfoList' in j_res):
                            #past year
                            if ('citeScoreCurrentMetricYear' in j_res['citeScoreYearInfoList'] and 'citeScoreCurrentMetric' in j_res['citeScoreYearInfoList']):
                                cursor.execute('select * from citescore where year = %s and journal_id = %s', (j_res['citeScoreYearInfoList']['citeScoreCurrentMetricYear'], journal_id,))
                                if (cursor.rowcount == 0):
                                    cursor.execute('insert into citescore (year, value, journal_id) values (%s, %s, %s)', (j_res['citeScoreYearInfoList']['citeScoreCurrentMetricYear'], float(j_res['citeScoreYearInfoList']['citeScoreCurrentMetric']), journal_id,))
                                else:
                                    cursor.execute('update citescore set value = %s where journal_id = %s and year = %s', (j_res['citeScoreYearInfoList']['citeScoreCurrentMetric'], journal_id, j_res['citeScoreYearInfoList']['citeScoreCurrentMetricYear'],))

                            #present year
                            if ('citeScoreTracerkYear' in j_res['citeScoreYearInfoList'] and 'citeScoreTracker' in j_res['citeScoreYearInfoList']):
                                cursor.execute('select * from citescore where year = %s and journal_id = %s', (j_res['citeScoreYearInfoList']['citeScoreTrackerYear'], journal_id,))
                                if (cursor.rowcount == 0):
                                    cursor.execute('insert into citescore (year, value, journal_id) values (%s, %s, %s)', (j_res['citeScoreYearInfoList']['citeScoreTrackerYear'], float(j_res['citeScoreYearInfoList']['citeScoreTracker']), journal_id,))
                                else:
                                    cursor.execute('update citescore set value = %s where journal_id = %s and year = %s', (j_res['citeScoreYearInfoList']['citeScoreTracker'], journal_id, j_res['citeScoreYearInfoList']['citeScoreTrackerYear'],))    

                #publication
                scopus_id = None
                if ('Scopus - Elsevier' in publishings[it]['sources'] and 'eid' in publishings[it]['sources']['Scopus - Elsevier']['source_map']):
                    scopus_id = publishings[it]['sources']['Scopus - Elsevier']['source_map']['eid'][7:]
                
                researcherid = None
                if ('ResearcherID' in publishings[it]['sources'] and 'wosuid' in publishings[it]['sources']['ResearcherID']['source_map']):
                    researcherid = publishings[it]['sources']['ResearcherID']['source_map']['wosuid']
                
                cursor.execute('select * from publication where (eid = %s or wosuid = %s) and orcid_id = %s', (scopus_id, researcherid, orcid['orcid_id']))
                if (cursor.rowcount == 0):
                    #publication is not in db so we need to insert it
                    if ('Scopus - Elsevier' in publishings[it]['sources']):
                        publ = publishings[it]['sources']['Scopus - Elsevier']
                        #if (publishings[it]['sources']['Scopus - Elsevier']['source_map']['eid'][7:])
                    else:
                        publ = publishings[it]['sources']['ResearcherID']
                        publishings[it]['sources']['ResearcherID']['citedby-count'] = -1

                    s = 1236472051807 / 1000.0
                    publ['publish_date'] = datetime.datetime.fromtimestamp(publ['publish_date'] / 1000).strftime('%Y-%m-%d %H:%M')
                    #'2009-03-08 09:27:31.807000'
                    print(f"Scopus: Publcation #{it+1} of {len(publishings)}.\nTitle: {publ['title']}.\nCitations: {publ['title']}.\nSource: {publ['name']}.\n\n")
                    cursor.execute('insert into publication (title, type, date, citations, wosuid, eid, pref_source, journal_id, orcid_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s) returning id', (publ['title'], publ['type'], publ['publish_date'], mix_res['coredata']['citedby-count'], researcherid, scopus_id, publ['name'], journal_id, orcid['orcid_id'],))
                
                #authors
                publication_id = cursor.fetchone()[0]
                for auth in mix_res['authors']['author']:
                    given_name = auth['preferred-name']['ce:given-name']
                    if given_name == None:
                        given_name = ""

                    surname = auth['preferred-name']['ce:surname']
                    if surname == None:
                        surname = ""

                    indexed_name = auth['preferred-name']['ce:indexed-name']
                    if indexed_name == None:
                        indexed_name = ""

                    cursor.execute('select * from author where publication_id = %s and name = %s and indexed_name = %s', (publication_id, (given_name + ' ' + surname), indexed_name,))
                    if (cursor.rowcount == 0):
                        cursor.execute('insert into author values (%s, %s, %s)', ((given_name + ' ' + surname), indexed_name, publication_id, ))

            else:       
                print('Mixed: Not 200!')

        else: 
            print('Researcher in sources')
            print(publishings[it])
            scopus_id = None
            if ('Scopus - Elsevier' in publishings[it]['sources'] and 'eid' in publishings[it]['sources']['Scopus - Elsevier']['source_map']):
                    scopus_id = publishings[it]['sources']['Scopus - Elsevier']['source_map']['eid'][7:]
            researcherid = None
            if ('ResearcherID' in publishings[it]['sources'] and 'wosuid' in publishings[it]['sources']['ResearcherID']['source_map']):
                researcherid = publishings[it]['sources']['ResearcherID']['source_map']['wosuid']
            print(scopus_id, researcherid)
            cursor.execute('select * from publication where (eid = %s or wosuid = %s) and orcid_id = %s', (scopus_id, researcherid, orcid['orcid_id']))
            if (cursor.rowcount == 0):
                #publication is not in db so we need to insert it
                publ = publishings[it]['sources']['ResearcherID']
                publishings[it]['sources']['ResearcherID']['citedby-count'] = -1

                s = 1236472051807 / 1000.0
                publ['publish_date'] = datetime.datetime.fromtimestamp(publ['publish_date'] / 1000).strftime('%Y-%m-%d %H:%M')
                #'2009-03-08 09:27:31.807000'
                print(f"ResearcherID: Publcation #{it+1} of {len(publishings)}.\nTitle: {publ['title']}.\nCitations: {publ['title']}.\nSource: {publ['name']}.\n\n")
                cursor.execute('insert into publication (title, type, date, citations, wosuid, eid, pref_source, journal_id, orcid_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s) returning id', (publ['title'], publ['type'], publ['publish_date'], mix_res['coredata']['citedby-count'], researcherid, scopus_id, publ['name'], journal_id, orcid['orcid_id'],))

    end = time.time() - start
    cursor.execute('select * from orcid where id = %s', (orcid['orcid_id'],))
    cursor.execute('update orcid set status = %s, last_upd_date = %s where id = %s', ('Atualizado', datetime.date.today(), orcid['orcid_id']))
    cursor.execute('insert into bo_insert (fetched_records, fetch_time, orcid) values (%s, %s, %s)', (len(publishings), end, orcid['orcid_id'],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({
        'status' : 400
    })
       

# author_info -> POST -> retrieves information about orcid
# WILL NOT WORK IF NOT IN UM'S VPN!!!
@app.route('/author_info', methods=['POST'])
@cross_origin()
def autor_info_post():
    data = request.get_json()
    url = "https://api.elsevier.com/content/author/orcid/" + str(data['orcid'])
    resp = requests.get(url,
    headers= {
        'Accept':'application/json',
        'X-ELS-APIKey': MY_API_KEY
    })

    res = json.loads(resp.text.encode('utf-8'))
    #print(res)
    jsono = {}
    jsono['coredata'] = res['author-retrieval-response'][0]['coredata']
    jsono['subject-areas'] = res['author-retrieval-response'][0]['subject-areas']
    jsono['preferred-name'] = res['author-retrieval-response'][0]['author-profile']['preferred-name']
    return jsono

# /publishings
# retrieves information about a certain publishing
@app.route('/publishings', methods=['POST'])
@cross_origin()
def get_publishing_info():
    data = request.get_json()
    scopus_id = str(data['scopus_id'])
    url = ("http://api.elsevier.com/content/abstract/scopus_id/" + scopus_id + "?field=authors,issn,citedby-count,prism:aggregationType,source-id")
    resp = requests.get(
        url,
        headers={
            'Accept': 'application/json',
            'X-ELS-APIKey': MY_API_KEY
        })
    return json.loads(resp.text.encode('utf-8'))


# /records
# retrieves information regarding the record information
@app.route('/records', methods=['GET'])
@cross_origin()
def get_records():
    conn = psycopg2.connect("dbname=is_fe03 user=francisco password=password")
    cursor = conn.cursor()

    sql = "select * from records"
    cursor.execute(sql)

    # print(cursor.fetchall())
    records_data = []

    for rec in cursor.fetchall():
        records_data.append({
            'id': rec[0],
            'fetched_records': rec[1],
            'fetch_time': rec[2]
        })
    cursor.close()
    conn.close()

    return jsonify({
        'records': records_data
    })


@app.route('/records', methods=['POST'])
@cross_origin()
def insert_record():
    conn = psycopg2.connect("dbname=is_fe03 user=francisco password=password")
    cursor = conn.cursor()

    data = request.get_json()
    if (data is not None):
        f_r = data['fetched_records']
        f_t = data['fetch_time']
        sql = 'insert into records (fetched_records, fetch_time) values (%s, %s)'
        cursor.execute(sql, (f_r, f_t))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({
        'fetched_records' : f_r,
        'fetch_time' : f_t
    })

if __name__ == '__main__':
    app.run()
