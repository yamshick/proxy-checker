# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import urllib
import json
import requests

hostName = "0.0.0.0"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
	def test_proxy(self, ip):
		proxy_servers = {
		   'https': f"https://{ip}",
		}

		test_url = 'https://ipinfo.io/json'
		# test_url = 'https://google.com'
		try:
			data = requests.get(test_url, proxies=proxy_servers, timeout=5)
			 
			return data.json()
		except Exception as e:
			print(e)
			return None


	def check_ip(self, query):
		ip = query.split('=')[1]
		data = self.test_proxy(ip)
		self.send_response(200)
		self.send_header("Content-type", "application/json")
		self.end_headers()
		self.wfile.write(bytes(json.dumps({'data': data}), "utf-8"))
	def do_GET(self):
		path = urllib.parse.urlparse(self.path)
		print(path.query)
		if path.path == '/check':
			self.check_ip(path.query)
			print('________ a am in')
			return
        
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
		self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
		self.wfile.write(bytes("<body>", "utf-8"))
		self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
		self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
