# api.py
from flask import Flask, request, render_template, send_file, jsonify
import os
import traceback
from io import BytesIO
from werkzeug.utils import secure_filename
import pandas as pd
from email_verifier import EmailVerifier
import tempfile
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize the EmailVerifier
verifier = EmailVerifier()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/upload', methods=['POST'])
def upload_file():
    input_filepath = None
    output_filepath = None
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        if file and file.filename.endswith('.xlsx'):
            filename = secure_filename(file.filename)
            input_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_filepath)
            
            # Process the file
            df = pd.read_excel(input_filepath)
            
            def progress_callback(data):
                progress = data.get('progress', 0)
                status = data.get('status', '')
                print(f"Progress: {progress}%, Status: {status}")
            
            processed_df = verifier.process_dataframe(df, callback=progress_callback)
            
            # Save the processed file
            output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'Verified_Lemon_Batch.xlsx')
            processed_df.to_excel(output_filepath, index=False)
            
            # Read the file into memory before sending
            with open(output_filepath, 'rb') as f:
                file_data = f.read()
            
            # Clean up files
            if input_filepath and os.path.exists(input_filepath):
                os.remove(input_filepath)
            if output_filepath and os.path.exists(output_filepath):
                os.remove(output_filepath)
            
            return send_file(
                BytesIO(file_data),
                as_attachment=True,
                download_name='Verified_Lemon_Batch.xlsx',
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
        return jsonify({'error': 'Invalid file format'}), 400
        
    except Exception as e:
        # Clean up files in case of error
        if input_filepath and os.path.exists(input_filepath):
            os.remove(input_filepath)
        if output_filepath and os.path.exists(output_filepath):
            os.remove(output_filepath)
        return jsonify({'error': str(e)}), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    try:
        if os.path.exists(verifier.errors_log_file):
            with open(verifier.errors_log_file, 'r') as log_file:
                logs = log_file.read()
            return jsonify({'logs': logs}), 200
        return jsonify({'logs': 'No logs found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)