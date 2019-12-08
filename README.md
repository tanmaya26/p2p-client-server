Name: Nikita Paranjape 	Student ID: 200259682	Unity ID: nparanj
Name: Tanmaya Nanda		Student ID: 200261608	Unity ID: tnanda

****************************************************************************************
Folder structure:
****************************************************************************************
p2p-rfc:
	- README
	- server.py
	- client.py
	- RFC1
	- RFC2
	
****************************************************************************************
Running instructions:
****************************************************************************************
Open p2p-rfc separately in three terminals.

**First Terminal - Client 1**

Open the p2p-rfc folder in the terminal.
Run the server as:
python server.py

**Second Terminal - Client 2**

Open the p2p-rfc folder:
Run the client 1 as: 
python client.py <hostname> <RFC folder name>

For example: 
python client.py Tanmayas-MacBook-Pro.local RFC1

NOTE -> you can obtain the hostname of your server by using ``hostname`` command on terminal

**Third Terminal**

Open the p2p-rfc folder:
Run the client 1 as: 
python client.py <hostname> <RFC folder name>

For example: 
python client.py Tanmayas-MacBook-Pro.local RFC2

*****************************************************************************************
Tasks
*****************************************************************************************

1. LOOKUP

    - Enter input ``LOOKUP`` in the client 1 terminal. 
    - Enter RFC number
    - Enter RFC title. The RFC title is of the format RFC<rfc_number>. 
    Eg: RFC title for RFC number 1 is RFC1.
    
