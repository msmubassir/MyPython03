from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/ip')
def show_ip():
    # Common headers used by proxies to pass client IP address
    headers_to_check = [
        "X-Forwarded-For",
        "X-Real-IP",
        "CF-Connecting-IP",  # Cloudflare
        "True-Client-IP",    # Akamai and other CDNs
    ]

    # Loop through headers and get the first non-empty value
    ip_address = None
    for header in headers_to_check:
        ip_address = request.headers.get(header)
        if ip_address:
            # If multiple IPs are present, take the first one
            ip_address = ip_address.split(',')[0]
            break
    
    # Fallback to request.remote_addr if no headers are found
    if not ip_address:
        ip_address = request.remote_addr
    
    return render_template('ip.html', ip=ip_address, title='IP Address')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
