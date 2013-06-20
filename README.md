NetGhost
========

An online version of the word game Ghost. In Ghost, players take turn selecting a letter. The player whose letter results in the completion of a valid word loses. 

**Usage**

There are two programs, one for the player acting as the server, and one for the client. Before launch, the current local IP of the server should replace the "ip" variable in the source code. When the server program is launched, the server's IP is displayed for convenience (the client will need to know this). After pressing enter at the prompt, the server will wait for clients attempting to connect to it. 

The client program prompts for an IP address to connect to. Once given, a connection is established, names are exchanged by the players, and the gameplay begins.
