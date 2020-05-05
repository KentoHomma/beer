import pickle
import requests
import numpy as np
from pandas import DataFrame as df
from django.shortcuts import render

# ググるための布石
url = 'https://www.google.co.jp/search'
# 機械学習モデルの読込
with open('./catboost_model.pkl', 'rb') as f:
    model = pickle.load(f)
# データフレームの読込
with open('./beer_df.pkl', 'rb') as f:
    df = pickle.load(f)

def index(request):
    if request.method == "POST":
        # 入力値の取得してパラメータ形に
        param_abv = float(request.POST['abv'])
        param_ibu = float(request.POST['ibu'])
        param = (param_abv, param_ibu)
        
        # 分類結果の取得し、データフレーム化
        pred_id = int(model.predict([param])[0])
        pred_df = df[df['style_id'] == pred_id].copy()

        # ユークリッド距離の列を追加して昇順ソートして取得
        distance = np.linalg.norm(pred_df[['abv', 'ibu']] - param, axis=1)
        pred_df['distance'] = distance
        result_df = pred_df.sort_values(by='distance', ascending=True).head()

        # 容量(ounces)によるビールの重複を除去&アルコール度数を小数点一桁までに
        result_df = result_df.drop_duplicates(['name'])
        result_df['abv'] = round(result_df['abv'],1)

        # ビールのスタイル名、一位のビール名、醸造所名、都市名を取得
        style = result_df['style'].values[0]
        first = result_df['name'].values[0]
        city = result_df['city'].values[0]
        brewery = result_df['brewery_name'].values[0]
        
        # 一位の検索URLをググるためのパラメータを渡す
        beer_url = requests.get(url, params={'q': result_df['name'].values[0]+" beer"})
        style_url = requests.get(url, params={'q': result_df['style'].values[0]+" ビール"})

        return render(request, 'ml_app1/result.html', {'param': param,
                                    'style': style, 'result': result_df,
                                    'first': first, 'city': city,
                                    'brewery': brewery,
                                    'beer_url':beer_url, 'style_url': style_url})
    else:
        return render(request, 'ml_app1/index.html')

def result(request):
    return render(request, 'ml_app1/result.html')
