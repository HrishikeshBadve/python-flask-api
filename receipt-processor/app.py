from flask import Flask, request, jsonify
import uuid
import math

app = Flask(__name__)
receipts = {}

def calculate_points(receipt):
    points = 0

    # 1 point for every alphanumeric character in the retailer name
    for c in receipt['retailer']:
        if (c.isalnum()):
            points += 1

    # 50 points if the total is a round dollar amount with no cents
    if (float(receipt['total']).is_integer()):
        points += 50
    
    # 25 points if the total is a multiple of 0.25
    if (float(receipt['total']) % 0.25 == 0):
        points += 25
    
    # 5 points for every two items on the receipt
    points += (len(receipt['items']) // 2) * 5

    # Points for item descriptions
    for item in receipt['items']:
        description_length = len(item['shortDescription'].strip())
        if (description_length % 3 == 0):
            item_points = math.ceil(float(item['price'])*0.2)
            points += item_points
    
    # 6 points if the day in the purchase date is odd
    day = int(receipt['purchaseDate'].split('-')[2])
    if (day % 2 == 1):
        points += 6

    # 10 points if the time of purchase is after 2:00pm and before 4:00pm
    hour = int(receipt['purchaseTime'].split(':')[0])
    if (14 <= hour and hour < 16):
        points += 10
    
    return points

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    receipt = request.json
    receipt_id = str(uuid.uuid4())
    receipts[receipt_id] = {'receipt': receipt, 'points': calculate_points(receipt)}
    return jsonify({'id': receipt_id})

@app.route('/receipts/<id>/points', methods=['GET'])
def get_points(id):
    if (id in receipts):
        return jsonify({'points': receipts[id]['points']})
    else:
        return jsonify({'error': 'Receipt not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
