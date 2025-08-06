from flask import Flask, request, jsonify
from fitparse import FitFile

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    fitfile = FitFile(file)
    data = analyze_fit_file(fitfile)

    return jsonify(data)

def analyze_fit_file(fitfile):
    results = {
        'gps': None,
        'power': None,
        'heart_rate': None,
        'cadence': None,
        'elevation': None,
        'pace': None,
        'running_dynamics': {}
    }

    for record in fitfile.get_messages('record'):
        if 'position_lat' in record and 'position_long' in record:
            results['gps'] = {
                'latitude': record.get_value('position_lat'),
                'longitude': record.get_value('position_long')
            }
        if 'power' in record:
            results['power'] = record.get_value('power')
        if 'heart_rate' in record:
            results['heart_rate'] = record.get_value('heart_rate')
        if 'cadence' in record:
            results['cadence'] = record.get_value('cadence')
        if 'elevation' in record:
            results['elevation'] = record.get_value('elevation')
        if 'speed' in record:
            results['pace'] = record.get_value('speed')
        if 'ground_contact_time' in record:
            results['running_dynamics']['ground_contact_time'] = record.get_value('ground_contact_time')
        if 'vertical_oscillation' in record:
            results['running_dynamics']['vertical_oscillation'] = record.get_value('vertical_oscillation')

    return results

if __name__ == '__main__':
    app.run(debug=True)