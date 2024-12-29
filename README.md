# stir
stir tech task

Instructions for Setting Up and Running the Task

1. Install Required Dependencies:-
   
   Use the following commands to install the necessary dependencies:
   
   pip install selenium
   pip install pymongo
   pip install flask
   pip install webdriver-manager

2. Ensure MongoDB is Running:-
    
   Make sure your MongoDB service is running. If you are using MongoDB Compass or a local MongoDB 
   server, verify that it is active before executing the script. 
   
3. Setup ProxyMesh:-  
    
   Configure ProxyMesh credentials using the following format:
   http://username:password@host
  
   Update the credentials.py file with your ProxyMesh username, password, and host.

4. Run the Script:-   

   To start the scraper, execute the following command in your terminal:
   
   python3 scraper.py

5. Access the HTML Interface:-
   You can view the results through the browser interface:
   
   1.Open your browser and navigate to:
     http://127.0.0.1:5000
     
   2.Alternatively, click on the link (http://127.0.0.1:5000) displayed in your terminal after running  
     the script.
 



