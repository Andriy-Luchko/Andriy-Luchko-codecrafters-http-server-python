# Uncomment this to pass the first stage
import socket

successResponse = "HTTP/1.1 200 OK\r\n\r\n".encode()
failureResponse = "HTTP/1.1 404 NOT FOUND\r\n\r\n".encode()

def parse_path(data):
    lines = data.split(b"\r\n")
    if len(lines) > 0:
        path = lines[0].split(b" ")[1]
        return path
    return b""

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    connection, address = server_socket.accept() # wait for client
    data = connection.recv(1024)
    path = parse_path(data)

    if b"/" == path:
        connection.send(successResponse)
    else:
        pathArray = path.split(b"/")

        if b"echo" == pathArray[1]:
            content = b"/".join(pathArray[2:])
            contentLength = str(len(content)).encode()
            res = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + contentLength + b"\r\n\n" + content + b"\n\r\n"
            connection.send(res)
        else:
            connection.send(failureResponse)


        


if __name__ == "__main__":
    main()
