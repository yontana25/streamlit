import streamlit as st
import numpy as np
import pandas as pd
import pymongo

from streamlit_google_oauth import google_oauth2_required

@google_oauth2_required
def main():
    user_id = st.session_state.user_id
    user_email = st.session_state.user_email 
    # st.write(f"You're logged in {user_id}, {user_email}")
    createList()

def getFielderData(connection, totalGame, mode):

    db = connection
    kiteiDaseki = totalGame * 3.1
    n = 0

    if (mode == 0):
        st.header('通算野手成績')
        #野手成績集計
        docs = db.t_fielder_data.aggregate([
            {"$match": {"game_id": {"$gt":n}}},
            { "$group": { "_id": "$player_name", "試合数": { "$sum": "$games" }, "打数": { "$sum": "$at_bat" }, "得点": { "$sum": "$run" }, "安打": { "$sum": "$single" }, "二塁打": { "$sum": "$double" }, "三塁打": { "$sum": "$triple" }, "本塁打": { "$sum": "$home_run" }, "打点": { "$sum": "$rbi" }, "三振": { "$sum": "$strikeout" }, "四死球": { "$sum": "$walk" }, "犠打": { "$sum": "$sacrifice" }, "盗塁": { "$sum": "$steal" }, "併殺": { "$sum": "$gdp" }, "失策": { "$sum": "$errors" } } }
            , { "$sort": { "_id": 1,  } }
        ])
        docs = list(docs)
    elif (mode == 1):
        st.header('最近の野手個人成績')
        n = st.number_input(label='試合数',
                            value=10,
                            )
        n = totalGame - n
        #野手成績集計
        docs = db.t_fielder_data.aggregate([
            {"$match": {"game_id": {"$gt":n}}},
            { "$group": { "_id": "$player_name", "試合数": { "$sum": "$games" }, "打数": { "$sum": "$at_bat" }, "得点": { "$sum": "$run" }, "安打": { "$sum": "$single" }, "二塁打": { "$sum": "$double" }, "三塁打": { "$sum": "$triple" }, "本塁打": { "$sum": "$home_run" }, "打点": { "$sum": "$rbi" }, "三振": { "$sum": "$strikeout" }, "四死球": { "$sum": "$walk" }, "犠打": { "$sum": "$sacrifice" }, "盗塁": { "$sum": "$steal" }, "併殺": { "$sum": "$gdp" }, "失策": { "$sum": "$errors" } } }
            , { "$sort": { "_id": 1,  } }
        ])
        docs = list(docs)
    else:
        st.header('チーム野手成績')
        #野手成績集計
        docs = db.t_fielder_data.aggregate([
            { "$group": { "_id": "$team_name", "試合数": { "$sum": "$games" }, "打数": { "$sum": "$at_bat" }, "得点": { "$sum": "$run" }, "安打": { "$sum": "$single" }, "二塁打": { "$sum": "$double" }, "三塁打": { "$sum": "$triple" }, "本塁打": { "$sum": "$home_run" }, "打点": { "$sum": "$rbi" }, "三振": { "$sum": "$strikeout" }, "四死球": { "$sum": "$walk" }, "犠打": { "$sum": "$sacrifice" }, "盗塁": { "$sum": "$steal" }, "併殺": { "$sum": "$gdp" }, "失策": { "$sum": "$errors" } } }
            , { "$sort": { "_id": 1,  } }
        ])
        docs = list(docs)

    for index in range(len(docs)):
        #打席 打数+四死球+犠打
        docs[index]['打席'] = docs[index]['打数'] + docs[index]['安打'] + docs[index]['犠打']
        #打率 安打/打数
        if docs[index]['打数'] == 0:
            docs[index]['打率'] = 0
        else:
            docs[index]['打率'] = docs[index]['安打'] / docs[index]['打数']
        #出塁率 (安打+四死球)/(打数+四死球+犠打)
        if (docs[index]['打数'] + docs[index]['四死球'] + docs[index]['犠打']) == 0:
            docs[index]['出塁率'] = 0
        else:
            docs[index]['出塁率'] = (docs[index]['安打'] + docs[index]['四死球']) / (docs[index]['打数'] + docs[index]['四死球'] + docs[index]['犠打'])
        #長打率 (塁打)/打数
        if docs[index]['打数'] == 0:
            docs[index]['長打率'] = 0
        else:
            docs[index]['長打率'] = (docs[index]['安打'] + docs[index]['二塁打'] + docs[index]['三塁打'] * 2 + docs[index]['本塁打'] * 3) / docs[index]['打数']
        #OPS 出塁率+長打率
        docs[index]['OPS'] = docs[index]['出塁率'] + docs[index]['長打率']
        if (mode == 2):
            docs[index]['試合数'] = totalGame

    #野手成績一覧表示
    df = pd.DataFrame(docs)
    df = df.round({'打率': 3, '出塁率': 3, '長打率': 3, 'OPS': 3})
    if (mode == 0):
        if st.checkbox('規定打席以上'):
            st.dataframe(df[df['打席']>=kiteiDaseki], None, 1000)
        else:
            st.dataframe(df, None, 1000)
    else:
        st.dataframe(df, None, 1000)

def getPitcherData(connection, totalGame, mode):

    db = connection
    kiteiTokyu = totalGame
    n = 0

    if (mode == 0):
        st.header('通算投手成績')
        #投手成績集計
        docs = db.t_pitcher_data.aggregate([
            { "$group": { "_id": "$player_name", "登板数": { "$sum": "$games" }, "先発登板": { "$sum": "$games_started" }, "勝": { "$sum": "$wins" }, "負": { "$sum": "$losses" }, "救援勝利": { "$sum": "$relief_wins" }, "ホールド": { "$sum": "$hold" }, "セーブ": { "$sum": "$save" }, "投球回": { "$sum": "$number_of_piches" }, "被安打": { "$sum": "$hits" }, "奪三振": { "$sum": "$strikeouts" }, "四死球": { "$sum": "$walk" }, "失点": { "$sum": "$runs" }, "自責点": { "$sum": "$earned_runs" }, "暴投": { "$sum": "$wild_pitches" }, "被本塁": { "$sum": "$home_run" }, "完投": { "$sum": "$shutouts" }, "完封": { "$sum": "$complete_games" }, "QS": { "$sum": "$qs" }, "HQS": { "$sum": "$hqs" } } }
            , { "$sort": { "_id": 1,  } }
        ])
        docs = list(docs)
    elif (mode ==1):
        st.header('最近の投手個人成績')
        n = st.number_input(label='試合数',
                            value=10,
                            )
        n = kiteiTokyu - n
        #投手成績集計
        docs = db.t_pitcher_data.aggregate([
            {"$match": {"game_id": {"$gt":n}}},
            { "$group": { "_id": "$player_name", "登板数": { "$sum": "$games" }, "先発登板": { "$sum": "$games_started" }, "勝": { "$sum": "$wins" }, "負": { "$sum": "$losses" }, "救援勝利": { "$sum": "$relief_wins" }, "ホールド": { "$sum": "$hold" }, "セーブ": { "$sum": "$save" }, "投球回": { "$sum": "$number_of_piches" }, "被安打": { "$sum": "$hits" }, "奪三振": { "$sum": "$strikeouts" }, "四死球": { "$sum": "$walk" }, "失点": { "$sum": "$runs" }, "自責点": { "$sum": "$earned_runs" }, "暴投": { "$sum": "$wild_pitches" }, "被本塁": { "$sum": "$home_run" }, "完投": { "$sum": "$shutouts" }, "完封": { "$sum": "$complete_games" }, "QS": { "$sum": "$qs" }, "HQS": { "$sum": "$hqs" } } }
            , { "$sort": { "_id": 1,  } }
        ])
        docs = list(docs)
    else:
        st.header('チーム投手成績')
        #投手成績集計
        docs = db.t_pitcher_data.aggregate([
            { "$group": { "_id": "$team_name", "登板数": { "$sum": "$games" }, "先発登板": { "$sum": "$games_started" }, "勝": { "$sum": "$wins" }, "負": { "$sum": "$losses" }, "救援勝利": { "$sum": "$relief_wins" }, "ホールド": { "$sum": "$hold" }, "セーブ": { "$sum": "$save" }, "投球回": { "$sum": "$number_of_piches" }, "被安打": { "$sum": "$hits" }, "奪三振": { "$sum": "$strikeouts" }, "四死球": { "$sum": "$walk" }, "失点": { "$sum": "$runs" }, "自責点": { "$sum": "$earned_runs" }, "暴投": { "$sum": "$wild_pitches" }, "被本塁": { "$sum": "$home_run" }, "完投": { "$sum": "$shutouts" }, "完封": { "$sum": "$complete_games" }, "QS": { "$sum": "$qs" }, "HQS": { "$sum": "$hqs" } } }
            , { "$sort": { "_id": 1,  } }
        ])
        docs = list(docs)

    for index in range(len(docs)):
        #防御率 自責点/投球回*9
        if (docs[index]['投球回'] == 0) :
            docs[index]['防御率'] = 99.9
        else:
            docs[index]['防御率'] = docs[index]['自責点'] / docs[index]['投球回'] * 9
        #勝率 勝/(勝+負)
        if (docs[index]['勝'] + docs[index]['負']) == 0:
            docs[index]['勝率'] = 0.00
        else:
            docs[index]['勝率'] = docs[index]['勝'] / (docs[index]['勝'] + docs[index]['負'])
        #HP 救援勝利+ホールド
        docs[index]['HP'] = docs[index]['救援勝利'] + docs[index]['ホールド']
        #QS率 QS/先発登板
        if docs[index]['先発登板'] == 0:
            docs[index]['QS率'] = 0.00
        else:
            docs[index]['QS率'] = docs[index]['QS'] / docs[index]['先発登板']
        #HQS率 HQS/先発登板
        if docs[index]['先発登板'] == 0:
            docs[index]['HQS率'] = 0.00
        else:
            docs[index]['HQS率'] = docs[index]['HQS'] / docs[index]['先発登板']
        #WHIP (被安打+四死球)/投球回(実際は四死球ではなく与四球)
        if docs[index]['投球回'] == 0:
            docs[index]['WHIP'] = 0
        else:
            docs[index]['WHIP'] = (docs[index]['被安打'] + docs[index]['四死球']) / docs[index]['投球回']
        if (mode == 2):
            docs[index]['試合数'] = totalGame

    #投手成績一覧表示
    df = pd.DataFrame(docs)
    df = df.round({'投球回': 1})
    if (mode == 0):
        if st.checkbox('規定投球回以上'):
            st.dataframe(df[df['投球回']>=kiteiTokyu], None, 1000)
        else:
            st.dataframe(df, None, 1000)
    else:
        st.dataframe(df, None, 1000)

def createList():

    USERNAME = st.secrets["db_username"]
    PASSWORD = st.secrets["db_password"]
    CLUSTER  = st.secrets["db_cluster"]

    conection = 'mongodb+srv://{0}:{1}@{2}.xbnjp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'.format(USERNAME, PASSWORD, CLUSTER)

    client = pymongo.MongoClient(conection)
    db  = client['test_data']

    # 規定打席、規定投球回取得
    docs = db.t_fielder_data.find().sort("game_id",-1).limit(1)
    totalGame = docs[0]['game_id']

    ##セレクトボックス作成##
    tempList = ['通算野手成績', '最近の野手成績', '通算投手成績', '最近の投手成績', 'チーム成績']
    selectedList = st.selectbox(
        '選択：',
        tempList
    )

    if (selectedList == '通算野手成績'):
        getFielderData(db, totalGame, 0)
    elif (selectedList == '最近の野手成績'):
        getFielderData(db, totalGame, 1)
    elif (selectedList == '通算投手成績'):
        getPitcherData(db, totalGame, 0)
    elif (selectedList == '最近の投手成績'):
        getPitcherData(db, totalGame, 1)
    else:
        getFielderData(db, totalGame, 2)
        getPitcherData(db, totalGame, 2)
        
    client.close()

st.set_page_config(
    page_title="kleague",
    page_icon="baseball",
    layout="wide"
    )
st.title('Kリーグ')
main()
