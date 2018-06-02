import base64
import json
import urllib.request
import hashlib
import os

id_and_key = b"a8c77eca312b:002b9d12de6a5584c8fc661d59d88e160a32afe60c" # id and key comes from account id and application key.
basic_auth_string = 'Basic ' + base64.b64encode(id_and_key).decode("utf-8")
headers = { 'Authorization': basic_auth_string }

request = urllib.request.Request(
    'https://api.backblazeb2.com/b2api/v1/b2_authorize_account',
    headers = headers
    )
response = urllib.request.urlopen(request)
response_data = json.loads(response.read().decode("utf-8"))
response.close()

print ('auth token:', response_data['authorizationToken'])
print ('api url:', response_data['apiUrl'])
print ('download url:', response_data['downloadUrl'])
print ('minimum part size:', response_data['minimumPartSize'])

DOWNLOAD_URL = response_data['downloadUrl'] # Comes from b2_authorize_account
ACCOUNT_AUTHORIZATION_TOKEN = response_data['authorizationToken'] # Comes from the b2_authorize_account call

api_url = response_data['apiUrl'] # Provided by b2_authorize_account
account_authorization_token = response_data['authorizationToken'] # Provided by b2_authorize_account
bucket_id = "4a683c47e72e9cfa6331021b" # The ID of the bucket you want to upload your file to
headers = { 'Authorization': account_authorization_token }
url = api_url + "/b2api/v1/b2_get_upload_url"
content = json.dumps({'bucketId': bucket_id})
request = urllib.request.Request(
	url,
	data = content.encode("utf-8"),
	headers = headers
	)
response = urllib.request.urlopen(request)
response_data = json.loads(response.read().decode("utf-8"))
response.close()

print ('bucketId:', response_data['bucketId'])
print ('uploadUrl:', response_data['uploadUrl'])
print ('authorizationToken:', response_data['authorizationToken'])

upload_url = response_data['uploadUrl'] # Provided by b2_get_upload_url
upload_authorization_token = response_data['authorizationToken'] # Provided by b2_get_upload_url

for filename in os.listdir("./sample"): # directory path which contains all the images to upload
    fname = filename
    filename = "./sample/" + filename
    with open(filename, 'rb') as content_file:
        file_data = content_file.read()
    file_name = fname
    content_type = "image/jpeg"
    MIME_type = "image/jpeg"
    sha1_of_file_data = hashlib.sha1(file_data).hexdigest()
    
    headers = {
        'Authorization' : upload_authorization_token,
        'X-Bz-File-Name' :  file_name,
        'Content-Type' : content_type,
        'MIME-Type' : MIME_type,
        'X-Bz-Content-Sha1' : sha1_of_file_data
        }
    request = urllib.request.Request(upload_url, file_data, headers)
    
    response = urllib.request.urlopen(request)
    response_data = json.loads(response.read().decode("utf-8"))
    response.close()

# Download file by name
BUCKET_NAME = "naveenbucket" # bucket name 50 char max: letters, digits, “-“ and “_” 
FILE_NAME = "s2.jpg" # The name of the file in the bucket

url = DOWNLOAD_URL + '/file/' + BUCKET_NAME + '/' + FILE_NAME

headers = {
    'Authorization': ACCOUNT_AUTHORIZATION_TOKEN
    }

request = urllib.request.Request(url, None, headers)
response = urllib.request.urlopen(request)

urllib.request.urlretrieve(url, "download.jpg")