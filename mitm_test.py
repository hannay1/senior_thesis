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

		'''print(type(headers)) #netlib.http.headers.Headers'''

