import paramiko
import time

class SSH_Client():

    def __init__(self, router):
        ch = router['address']
        # check if we need to ssh from a jump server
        if router['jumpserver']:
            # initialize jump server Transport object
            jump_transport = paramiko.Transport(router['jumpserver']['address'])
            # negotiate ssh session with the jump server
            jump_transport.start_client()
            # authenticate to jump server with usern/passw
            jump_transport.auth_password(router['jumpserver']['usern'], router['jumpserver']['passw'])
            # wait for client to authenticate to jump server
            while not jump_transport.is_authenticated():
                time.sleep(0.1)
            # open a new channel using the jump server transport
            # the first parameter is the type of channel, the other two are dst and src for the port forwarding
            # the dst is the target router and src is a random localhost port
            ch = jump_transport.open_channel('direct-tcpip', router['address'], ('localhost', 0))

        # build transport object of the desired router
        self.transport = paramiko.Transport(ch)
        # negotiate ssh session with the router
        self.transport.start_client()
        # authenticate to the router
        self.transport.auth_password(router['usern'], router['passw'])
        # wait for client to authenticate to router
        while not self.transport.is_authenticated():
            time.sleep(0.1)
        # request a channel stream on the router
        self.channel = self.transport.open_session()

    def run(self, cmd):
        channel = self.channel
        # execut cmd on the router, channel will be closed after command finishes execution
        channel.exec_command(cmd)
        # non-blocking way to find out if the process on the router has finished and exited
        while not channel.exit_status_ready():
            # call .recv method to fetch the stream of data coming from the router
            yield channel.recv(5565)

    def close(self):
        # making sure we close session and not just the channel
        self.transport.close()

