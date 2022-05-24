# removeController

server.py : Socket Server  

app.py : Hacker's Controller  

serverFile.py : Target Serverfile (섭파)  



socket server start command  
`gunicorn --bind 0:8000 --threads 50 server:app`