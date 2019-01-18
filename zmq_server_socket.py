"""
A zmq_server_socket that hosts a publish socket in order to broadcast 
information across a server.

Created by James Park and Mohit Verma.
"""
import zmq
import time

class zmq_server_socket:
    """ 
    Uses zmq to publish a python dictionary on a port with a 
    given topic.
    
    A port is a logical connection method that connects the server
    with the client.
    
    A topic is the connecting device that is used to measure some 
    values.
    """

    def __init__(self, port, topic):
        """ This is an abstract ZMQ_socket class that creates a 
        publishing zmq socket for client zmq sockets to connect to.
        
        Hosts a zmq publishing socket on a port(random 4 digits)
        and connects to a topic(a topic is a device that can be 
        connected to).
        
        Note: zmq.Context() must be run to initialize the connections
        between the sockets. It will be used to manage any sockets 
        that are connected.
        
        @type self: zmq_server_socket
        @type port: int
        @type topic: string
        @rtype: None
        """
        zmq_context = zmq.Context() #intializes zmq
        self.topic = topic
        self.current_data = ""
        self.pub_socket = zmq_context.socket(zmq.PUB)  #initialized to be a publishing socket.
        self.pub_socket.bind("tcp://*:%s" % port) #binds this zmq to the open port.
        print('Broadcasting on port {0} with topic {1}'.format(port, topic))
        
    def send(self, data_dict):
        """This method is used to send information to the publishing socket.
        
        A publishing socket is just a socket that broadcasts some 
        information. The zmq object will grab information from that 
        publisher.
        
        @type self: zmq_server_socket
        @type data_dict: Dictionary
        @rtype: None
        """
        timestamp = time.time()
        send_string = "%s %f %s" % (self.topic, timestamp, repr(data_dict))
        self.current_data = send_string
        
        # Uploads the data to the publishing socket. This lets any 
        # connecting client socket grab the available data from the pub.
        self.pub_socket.send(send_string) 
        

    def close(self):
        """This method is used to close and destroy the publishing
        socket. This will result in the destruction of any client socket
        and cease connection to the topic.
        
        @type self: zmq_server_socket
        @rtype: None
        """
        self.pub_socket.close()
        
    def print_current_data(self):
        """ This method can be used to print the current data that is 
        uploaded on the publishing socket.
        
        @type self: zmq_server_client
        @rtype: None
        """
        print(self.current_data)
        
    def get_current_data(self):
        """ This method can be used to get the current data that is 
        uploaded on the publishing socket.
        
        @type self: zmq_server_client
        @rtype: String
        """
        return self.current_data