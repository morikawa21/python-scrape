from flask import Flask, request
import api_scrape

# flask
app = Flask(__name__)

# 日本語文字化け対策
app.config['JSON_AS_ASCII'] = False

# rest api
@app.route('/post', methods=['POST'])
def post_data():
  
  # For posted form input, use request.form.
  if request.headers.get("Content-Type") == 'application/x-www-form-urlencoded':
    url = request.form['url']
    id = request.form['id']
  
  # For JSON posted with content type application/json.
  if request.headers.get("Content-Type") == 'application/json':
    data = request.get_json()
    url = data['url']
    id = data['id']
  
  if not url and id:
    return {}
    
  return api_scrape.scrape({
    'url': url,
    'id': id,
  }, request.headers.get("Origin"))

# rest api
@app.route('/get', methods=['GET'])
def get_url():
  
  # For URL query parameters, use request.args.
  url = request.args.get('url')
  id = request.args.get('id')
  
  if not url and id:
    return {}
    
  return api_scrape.scrape({
    'url': url,
    'id': id,
  }, request.headers.get("Origin"))

# main
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5050)

