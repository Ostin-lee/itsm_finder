from flask import Flask, request, jsonify, render_template
import re
import pymysql
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

def getConnection():
    return pymysql.connect(host='195.224.157.110', user='remote', password='Lee2391e@s', db='hmmpi', charset='utf8')

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def cleanText(text):
    #text=re.sub("<^>]*>", " ", str(text))
    text=re.sub(r"^\s", " ", str(text))
    return text

def getSimilarText(inquiry):
    conn = getConnection()
    curs = conn.cursor()
    sql = "select distinct itsm_ref, itsm_summary, itsm_description from itsm_master where match(itsm_summary, itsm_description) against ('" + inquiry + "') AND itsm_ref like 'HSD%' limit 50"
    curs.execute(sql)
    rows = curs.fetchall()
    result_rows = len(rows)

    data_sets = []
    data_sets_final = []
    descriptions = [inquiry]
    rank = []
    
    if result_rows > 0 :
        
        for row in rows:
            data_set = {"itsm_ref": row[0], "itsm_summary": row[1], "itsm_description": row[2]}
            data_sets.append(data_set)
            descriptions.append(cleanText(row[2]))

        #print(descriptions)
        sin_result = calcuate_Similarity(descriptions)

        for i in range(len(sin_result[0])):
            #print(sin_result[0][i])
            if i>0:
                data_sets[i-1]['similarity'] = sin_result[0][i]
            temp_data_set = {"seq": i, "weight": sin_result[0][i]}
            rank.append(temp_data_set)

        #print(rank)
        alist = np.where(sin_result[0] > 0)

        for index in alist[0]:
            data_sets_final.append(data_sets[index-1])

        data_sets_final = sorted(data_sets_final, key=lambda k: k['similarity'], reverse=True) 
        #print(data_sets_final)
        
    else :
        data_sets_final.append('Nodata')     
        #data_sets_final = [ {"itsm_ref": row[0], "itsm_summary": row[1], "itsm_description": row[2]} ]
        
    conn.close()
    #return json.dumps(data_set, default=date_handler);
    #return json.dumps(rows, default=date_handler);
    return data_sets_final

def calcuate_Similarity(descriptions):
    #tfidfv = TfidfVectorizer().fit(descriptions)
    #print(tfidfv.transform(descriptions).toarray())
    #print(tfidfv.vocabulary_)
    #print(descriptions)
    #tfidf_vectorizer = TfidfVectorizer()
    tfidf_vectorizer = TfidfVectorizer(use_idf=True, smooth_idf=False, ngram_range=(1,1), stop_words='english') # to use only  bigrams ngram_range=(2,2)
    tfidf_matrix = tfidf_vectorizer.fit_transform(descriptions)
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    #print(type(cosine_sim))
    return cosine_sim

@app.route('/similarity', methods=['POST'])
def index():
    if request.method == 'POST':
        request_data = request.get_json()
        search = request_data["search"]
        #search = request.args.get("search")
        #search = request.form['search']
        return json.dumps(getSimilarText(search), default=date_handler);

if __name__ == '__main__':
    #app.run(host='localhost')
    app.run(host='localhost', port='5000', debug=True)
