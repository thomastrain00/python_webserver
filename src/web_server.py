"""This module creates and runs a HTTP/1.1 web server"""
import socket
import os

# Bind to all interfaces at port 8080
SERVER_IP = '0.0.0.0'
SERVER_PORT = 8080
PATH_TO_SRC_DIR = os.path.dirname(os.path.realpath(__file__))
PATH_TO_SRC_DIR_IMG = os.path.join(PATH_TO_SRC_DIR, "images")
IMAGE_SUBSTRINGS = [".ico",".png",".jpg",".svg"]
UNAUTHORIZED_SUBSTRINGS = ["..", "~",] # Check if URL points to unauth files


def respond_get(connection, filename):
    """Respond to HTTP GET requests
    """

    try:
        if filename in ["/", "/index.html"]:
            with open(os.path.join(PATH_TO_SRC_DIR,"index.html"), "r", encoding="utf-8") as file:
                html_content = file.read()
                response = "HTTP/1.1 200 OK\r\n\n" + html_content
                image_content = None
        elif any(map(filename[1:].__contains__, IMAGE_SUBSTRINGS)):
            # Read images as binary data
            with open(os.path.join(PATH_TO_SRC_DIR_IMG,filename[1:]), "rb") as img:
                image_content = img.read()
                response = f"HTTP/1.1 200 OK\r\n \
                            Content-Type: image/png\r\n \
                            Content-Length: {len(image_content)}\r\n\n"
        else:
            if any(map(filename[1:].__contains__, UNAUTHORIZED_SUBSTRINGS)):
                print("Client tried to access unauthorized files.")
                raise FileNotFoundError
            requested_file_path = os.path.join(PATH_TO_SRC_DIR,filename[1:])
            with open(requested_file_path, "r",encoding="utf-8") as file:
                html_content = file.read()
                response = "HTTP/1.1 200 OK\r\n\n" + html_content
                image_content = None
    except FileNotFoundError:
        response = "HTTP/1.1 404 Not Found\r\n\nNot found"
        image_content = None
    except Exception as e:
        print(e)
        connection.close()
        return (None,None)

    return (response, image_content)


def init_socket():
    """Initialize socket
    """

    # Initialize TCP port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Re-bind server port after keyboard interrupt
    # Source: https://stackoverflow.com/a/6380198
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind TCP socket
    server_socket.bind((SERVER_IP, SERVER_PORT))

    # Listen on TCP socket ie allow client connections
    print(f"Web server listening at: {SERVER_IP}:{str(SERVER_PORT)}")
    server_socket.listen()

    return server_socket


def get_request(connection, address):
    """Get client request
    """
    try:
        request = connection.recv(1024).decode()
        if request:
            print(f"Received HTTP request from {address}:\n")
            print("/----------START HTTP REQUEST PACKET----------/")
            print(request)
            print("/-----------END HTTP REQUEST PACKET-----------/")
        else:
            print("Empty request. Closing connection...")
            connection.close()
            return None
    except UnicodeDecodeError as e:
        print(e)
        connection.close()
        return None

    return request


def parse_request(connection, request):
    """ Parse HTTP request header for the following:
        - Request Method
        - Filename
    """
    try:
        headers = request.split('\n')
        request_method = headers[0].split()[0]
        filename = headers[0].split()[1]
        # For images, get the filename without the "/images" directory 
        if "/images" in filename:
            filename = "/" + filename.split("/")[2]
    except TypeError as e:
        print(e)
        connection.close()
        return None,None
    except IndexError as e:
        print(e)
        connection.close()
        return None,None

    return request_method, filename


def main():
    """Main function
    """
    server_socket = init_socket()

    while True:
        # Wait for new client connection to socket (accept() is blocking)
        connection, address = server_socket.accept()
        print(f"Accepted connection from {address}")

        request = get_request(connection, address)
        if request is None:
            continue

        # Example HTTP request:
            # GET / HTTP/1.1
            # Host: localhost:8000
            # User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
            # Accept: text/html
            # Accept-Language: en-US,en;q=0.5
            # Accept-Encoding: gzip, deflate, br
            # Connection: keep-alive
            # Upgrade-Insecure-Requests: 1
            # Sec-Fetch-Dest: document
            # Sec-Fetch-Mode: navigate
            # Sec-Fetch-Site: none
            # Sec-Fetch-User: ?1

        # Parse the HTTP request
        request_method, filename = parse_request(connection, request)
        if (request_method, filename) == (None,None):
            continue

        # Generate HTTP response
        if request_method == "GET":
            response, image_content = respond_get(connection, filename)
            if (response,image_content) == (None,None):
                continue
        else:
            print("Request method not currently supported.")
            connection.close()
            continue

        # Send HTTP response
        try:
            if any(map(filename[1:].__contains__, IMAGE_SUBSTRINGS)):
                connection.sendall(response.encode() + image_content)
            else:
                connection.sendall(response.encode())
        except TypeError as e:
            print(e)
            connection.close()
            continue

        connection.close()
        print(f"Closed connection to {address}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nWeb server stopped")
