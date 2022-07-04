from flask import Flask, jsonify
import stonks

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def helloworld():
  return jsonify({ 'msg': 'hellow world' })

@app.route('/stonks/<symbol>', methods=['GET'])
def get_stonk(symbol):
  return jsonify({ 'stonk': stonks.current_market_price(symbol) })

@app.route('/stonks/<symbol>/details', methods=['GET'])
def get_details(symbol):
  return jsonify(stonks.company_details(symbol))

if __name__ == "__main__":
  app.run(debug=True)

# to run type pythong app.py in terminal