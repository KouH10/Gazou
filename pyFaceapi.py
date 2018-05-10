########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json

#### Request headers
#'Content-Type': APIに送るメディアのタイプ
#   'application/json' (URL指定の場合に選択する), 
#   'application/octet-stream' (Local ファイル転送の場合に選択する)
#'Ocp-Apim-Subscription-Key': APIキーを指定する
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '[key設定]',
}
 
#### Request parameters
# 取得したい情報について、パラメータを指定する
#   指定できるパラメータはコンマで分けて複数指定可能
#        returnFaceId : 検出された顔のIDを返す
#        returnFaceLandmarks : 写真の中のどこに顔があるか、目や口の位置はどこかといった「位置情報」を返す
#        returnFaceAttributes : 顔属性（年齢・性別・髪型・表情など）を分析するパラメーターで返す
# 'language' : 何語で出力を返すか. english, chineseのみ. 標準ではenglish
params = urllib.parse.urlencode({
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    'language': 'en',
})
 
#### Request body
# 入力したい画像の指定をする. 画像URLの指定, local ファイルの指定から選択
# 画像はJPEG, PNG, GIF, BMPに対応
# サイズの上限は4MB
 
## URL 指定の場合以下のコメントアウトを外すし、image_urlを指定する
#image_url = 'https://XXXXX'
#body = { 'url': image_url }
#body = json.dumps(body)
 
## Local file指定の場合
# 以下の image_file_path に読み込むファイルのパスを指定する
image_file_path = 'faceimage.jpg'
image_file = open(image_file_path,'rb')
body = image_file.read()
image_file.close()
 
#### API request
# 接続先リージョンによっては, 以下HTTPSConnection の "westus.api.cognitive.microsoft.com" 部分は変更する.
# この場合は「westus」なので北米西部リージョン
# なお "/vision/v1.0/analyze?%s"　の部分が接続先APIの機能を指定している
try:
    conn = http.client.HTTPSConnection('westus2.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
    response = conn.getresponse()
    data = json.loads(response.read().decode('utf-8'))
    print(json.dumps(data, indent=4))
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
