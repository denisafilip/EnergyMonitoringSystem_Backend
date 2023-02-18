# Energy Monitoring System - Backend

### Online Energy Utility Platform - an integrated energy monitoring system that stores energy consumption data for clients and their smart metering devices.

Written in *Django*, the web framework of Python, using *RabbitMQ* for asynchronous communication, *Web Sockets* for notification system implementation and *gRPC (Google Remote Procedure Call)* for a chat system between the administrator of the system and the existing clients.

### Requirements
An online platform should be designed and implemented to manage users, their associated smart energy metering devices, and the monitored data from each device. The system can be accessed by two types of users after a login process: *administrator (manager)*, and *clients*. The administrator can perform CRUD (Create-Read-Update-Delete) operations on user accounts (defined by ID, name, role: admin/client), registered smart energy metering devices (defined by ID, description, address, maximum hourly energy consumption), and on the mapping of users to devices (each user can own one or more smart devices in different locations). After the mapping is done, for each device the energy consumption is stored on hourly basis as tuples of the form <timestamp, energy consumption> in the database.

### Functional Requirements
- Users log in. Users are redirected to the page corresponding to their role.
- Administrator/Manager Role:
  - CRUD operations on users and devices.
  - Create user-device mappings.
- User/Client Role
  - Can view on his/her page all the associated devices.
  - Can view the daily energy consumption for each of his/her associated devices as line charts or bar charts per day (OX- hours; OY- energy value [kWh] for that hour). The day should be selected from a calendar.
- The users corresponding to one role will not be able to enter the pages corresponding to
the other role (e.g., by log-in and then copy-paste the admin URL to the browser).

## Asynchronous Communication

### Requirements
A *Smart Metering Device Simulator* module will be the *Message Producer*. It will simulate a sensor by reading energy data from a .csv file (one value at every 10 minutes) and sends data in the form _<timestamp, device_id, measurement_value>_ to the *Message Broker* (i.e., the queue). The timestamp is taken from the local clock, the measurement_value is read from the file and represents the energy measured in kWh, and the device_id is unique to each instance of the Smart Metering Device Simulator and corresponds to the device_id of a user from the database. The sensor simulator is a standalone application, a Python script. 
The measurements are sent to the queue using the following JSON format:
    ```{
    “timestamp": 1570654800000,
    “device_id”: “5c2494a3-1140-4c7a-991a-a1a2561c6bc2”
    “measurement_value”: 0.1,
    }```
A *Message Consumer* application will pre-process the data to compute the total hourly energy consumption and stores it in the database. If the computed total hourly energy consumption exceeds the smart device maximum value (as it appears in the database) it notifies asynchronously the user on their web interface, using WebSockets.

### Functional requirements:
- The message broker allows Smart Metering Device Simulator to act as messages producer and send data tuples in a JSON format.
-  The message consumer component of the system processes each message and notifies asynchronously using WebSockets the client application. 

## Remote Procedure Call (RPC)

### Requirements
Develop a chat system to offer support for the clients of the energy platform if they have questions related with their energy consumption. The chat system should allow communication between the clients and the administrator of the system.

### Functional requirements:
- The client application displays a chat box where clients can type messages.
- The message is sent asynchronously to the administrator, that receives the message together
with the client identifier, being able to start a chat with the client.
- Messages can be sent back and forth between the client and the administrator during chat
session.
- The administrator can chat with multiple clients at once.
- A notification is displayed for the user when the other user reads the message.
- A notification is displayed for the user (e.g., typing) while the user from the other end of
communication types its message
