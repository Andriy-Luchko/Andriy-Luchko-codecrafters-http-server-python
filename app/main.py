import socket
import threading
import argparse 
import os 

successResponse = "HTTP/1.1 200 OK\r\n\r\n".encode()
failureResponse = "HTTP/1.1 404 NOT FOUND\r\n\r\n".encode()

def parse_path(data):
    lines = data.split(b"\r\n")
    if len(lines) > 0:
        path = lines[0].split(b" ")[1]
        return path
    return b""

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", help="serving files dir")
    args = parser.parse_args()

    while True:
        connection, address = server_socket.accept()
        responseThread = threading.Thread(target=handleReq, args=(connection, args.directory))
        responseThread.start()




def handleReq(connection, directory):
    data = connection.recv(1024)
    path = parse_path(data)
    if b"/" == path:
        connection.send(successResponse)
    else:
        pathArray = path.split(b"/")

        if b"echo" == pathArray[1]:
            # echo the rest of the path to the client
            content = b"/".join(pathArray[2:])
            contentLength = str(len(content)).encode()
            res = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + contentLength + b"\r\n\n" + content + b"\n\r\n"
            connection.send(res)
        elif b"user-agent" == pathArray[1]:
            # figure out user agent
            startIdx = data.find(b"User-Agent: ") + len(b"User-Agent: ")
            endIdx = startIdx + data[startIdx:].find(b"\r\n") 
            userAgent = data[startIdx:endIdx]

            # respond back to client
            content = userAgent
            contentLength = str(len(content)).encode()
            res = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + contentLength + b"\r\n\n" + content + b"\n\r\n"
            connection.send(res)
        elif b"files" == pathArray[1]:
            fileName = pathArray[2]
            path = os.path.join(directory, fileName.decode("ascii"))
            if os.path.isfile(path):
                with open(path, "rb") as file:
                    fileBody = file.read().decode("ascii")
                    print(fileBody)
                    content = fileBody
                    contentLength = str(len(content)).encode("ascii")
                    res = b"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: " + contentLength + b"\r\n\n" + content + b"\n\r\n"
                    connection.send(res)
        else:
            connection.send(failureResponse)


        


if __name__ == "__main__":
    main()
