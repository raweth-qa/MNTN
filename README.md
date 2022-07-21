# MNTN
# The public api being tested == https://httpbin.org and it does have a swagger page and a full variation of method calls Get,Post,Put,Delete
  ### I will be using the https protocol (no one should use http)  this is done without a key (auth token or jwt)  
  ### but I am very familiar with these and other security protocols
  
## The code will be standalone requiring python3 and the following modules:
   - requests
   - json
   - unittest (standard package)
   - sys
   - urllib
   - inspect
   - code
   
 
## For the assessment, please choose a public API to automate and provide the following:
 	- Executable automation you have written to verify the public API 
  - please run the following in shell (or windows.cmd) python3 /Users/rweth/keystone_qa/Scripts/httpbin_basic.py
 	- Explanation of your approach
 	    This is prototype code
      To cut corners this is one big encapsulated file with everything it needs.
      In a test framework you should never write code like this you should have a strong
        Frameowrk such as pytest or somthing else (unitest is a bit old)
        Libraries with class and function modules
        test scripts that employ the modules and the test framework
        ideally the test can and should be modified to handle
           a parameter based environment ie  dev qa or staging to run the approiate api calls in that framework
           unittest output or some other agreed format to record reults of the test in jenkins   
 	
  
 	- Pros and cons of approach
   
   
 
