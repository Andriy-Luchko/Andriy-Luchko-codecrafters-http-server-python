# Uncomment this to pass the first stage
import socket

successResponse = "HTTP/1.1 200 OK\r\n\r\n".encode()
failureResponse = "HTTP/1.1 404 NOT FOUND\r\n\r\n".encode()

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    connection, address = server_socket.accept() # wait for client
    data = connection.recv(1024)
    if b" / " in data:
        connection.send(successResponse)
    else:
        connection.send(failureResponse)
        


if __name__ == "__main__":
    main()
