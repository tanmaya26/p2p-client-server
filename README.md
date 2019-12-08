Name: Nikita Paranjape 	Student ID: 200259682	Unity ID: nparanj
Name: Tanmaya Nanda		Student ID: 200261608	Unity ID: tnanda

****************************************************************************************
Folder structure:
****************************************************************************************
Project1:
	- README
	- server.py
	- client.py
	- RFC1
	- RFC2
	
****************************************************************************************
Running instructions:
****************************************************************************************
Open Project1 separately in three terminals.

**First Terminal - Server**

Open the Project1 folder in the terminal.
Run the server as:
python server.py

**Second Terminal - Client 2**

Open the Project1 folder:
Run the client 1 as: 
python client.py <hostname> <RFC folder name>

For example: 
python client.py Tanmayas-MacBook-Pro.local RFC1

NOTE -> you can obtain the hostname of your server by using 'hostname' command on terminal

**Third Terminal - Client 2**

Open the Project1 folder:
Run the client 2 as: 
python client.py <hostname> <RFC folder name>

For example: 
python client.py Tanmayas-MacBook-Pro.local RFC2

*****************************************************************************************
Tasks
*****************************************************************************************

NOTE: The RFC title is of the format RFC<rfc_number>. 
Eg: RFC title for RFC number 1 is RFC1.

1. ADD 
    
    - Enter input ADD in the client 1 terminal. 
    - Enter RFC number
    - Enter RFC title. 
    
2. LOOKUP

    - Enter input LOOKUP in the client 1 terminal. 
    - Enter RFC number
    - Enter RFC title. 
    
2. GET 
    - Check the LOOKUP response to choose the RFC number to download
    - Enter input GET in the client 1 terminal. 
    - Enter RFC number
    - Enter RFC title 
    - Enter hostname from LOOKUP response
    - Enter port from LOOKUP response
    
3. LIST
    
    - Enter input LIST in the client 1 terminal. 
    
4. EXIT

    - Enter input EXIT in the client 1 terminal. 
You can repeat the above in client 2 terminal as well.

    
