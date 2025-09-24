from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
from hashstuff import save_hash, generate_hash
from ipfsstuffs import ipfs_upload
from qrstuff import gen_qr
from pdfsstuff import embedpdf

app = Flask(__name__)

@app.route('/static/<filename>')
def static_file(filename):
    return send_from_directory('static', filename)

UPLOAD_FOLDER = 'uploads'
VERIFY_FOLDER = 'verify_uploads'
QR_FOLDER = 'qrs'

for folder in [UPLOAD_FOLDER, VERIFY_FOLDER, QR_FOLDER]:
    os.makedirs(folder, exist_ok=True)

stamped_certificates = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'certificate' not in request.files:
            return render_template('upload.html', error="Please select a file")
        
        file = request.files['certificate']
        
        if file.filename == '':
            return render_template('upload.html', error="No file selected")
        
        if file and file.filename.lower().endswith('.pdf'):
            try:
                filename = file.filename
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                
                # og wala hash
                original_hash = generate_hash(filepath)
                hash_filepath = save_hash(file.filename, original_hash)
                
                ipfs_link = ipfs_upload(filepath)
                
                qr_filename = f"{filename}_qr.png"
                qr_path = os.path.join(QR_FOLDER, qr_filename)
                gen_qr(ipfs_link, qr_path)
                
                final_filename = f"stamped_{filename}"
                final_path = os.path.join(UPLOAD_FOLDER, final_filename)
                embedpdf(filepath, qr_path, final_path)
                
                # stamp wala hash
                stamped_hash = generate_hash(final_path)
                
                # og aur stamp dono ka hash to verify
                stamped_certificates[original_hash] = {
                    'filename': final_filename,
                    'original_hash': original_hash,
                    'stamped_hash': stamped_hash,
                    'original_filename': filename,
                    'cid': ipfs_link
                }
                
                stamped_certificates[stamped_hash] = {
                    'filename': final_filename,
                    'original_hash': original_hash,
                    'stamped_hash': stamped_hash,
                    'original_filename': filename,
                    'cid': ipfs_link
                }
                
                print(f"Stored certificate:")
                print(f"Original hash: {original_hash}")
                print(f"Stamped hash: {stamped_hash}")
                print(f"CID: {ipfs_link}")
                
                return render_template('upload.html',
                                     success=True,
                                     filename=final_filename,
                                     original_filename=filename)
                
            except Exception as e:
                return render_template('upload.html', error=f"Error processing file: {str(e)}")
        else:
            return render_template('upload.html', error="Only PDF files are accepted")
    
    return render_template('upload.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        if 'certificate' not in request.files:
            return render_template('verify.html', error="Please select a file")
        
        file = request.files['certificate']
        
        if file.filename == '':
            return render_template('verify.html', error="No file selected")
        
        if file and file.filename.lower().endswith('.pdf'):
            try:
                filename = file.filename
                filepath = os.path.join(VERIFY_FOLDER, filename)
                file.save(filepath)
                
                # upload wale ka hash
                uploaded_hash = generate_hash(filepath)
                
                print(f"Verifying file: {filename}")
                print(f"Uploaded hash: {uploaded_hash}")
                print(f"Stored certificates: {list(stamped_certificates.keys())}")
                
                # verify
                is_verified = False
                matching_cert = None
                
                if uploaded_hash in stamped_certificates:
                    is_verified = True
                    matching_cert = stamped_certificates[uploaded_hash]
                    print(f"matched")
                else:
                    print(f"not matched")
                
                return render_template('verify.html',
                                     result=True,
                                     filename=filename,
                                     hash=uploaded_hash,
                                     verified=is_verified,
                                     cid=matching_cert['cid'] if matching_cert else None)
                
            except Exception as e:
                return render_template('verify.html', error=f"Error processing file: {str(e)}")
        else:
            return render_template('verify.html', error="Only PDF files are accepted")
    
    return render_template('verify.html')

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/debug')
def debug():
    return f"<pre>Stored certificates:\n{stamped_certificates}</pre>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
