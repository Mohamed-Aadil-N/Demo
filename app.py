from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)

# AWS Config
S3_BUCKET = 'video-streaming-platform'
AWS_ACCESS_KEY = 'your-access-key'
AWS_SECRET_KEY = 'your-secret-key'

# Connect to S3
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Route to upload video
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    # Upload file to S3
    s3.upload_fileobj(file, S3_BUCKET, file.filename)
    
    return jsonify({"message": f"{file.filename} uploaded successfully"}), 200

# Route to stream video using presigned URL
@app.route('/stream/<filename>', methods=['GET'])
def stream_file(filename):
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': filename},
            ExpiresIn=3600  # URL expires in 1 hour
        )
        return jsonify({"url": url})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template

@app.route('/')
def home():
    return app.send_static_file('index.html')