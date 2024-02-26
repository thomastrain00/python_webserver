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


def main():
    """Main function
    """
    # Initialize TCP port 80
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Re-bind server port after keyboard interrupt
    # Source: https://stackoverflow.com/a/6380198
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind TCP socket
    server_socket.bind((SERVER_IP, SERVER_PORT))

    # Listen on TCP socket ie allow client connections
    print(f"Web server listening at: {SERVER_IP}:{str(SERVER_PORT)}")
    server_socket.listen()

    try:
        while True:
            # Wait for client connection to socket (accept() is blocking)
            connection, address = server_socket.accept()
            print(f"Accepted connection from {address}")

            # Get client request
            try:
                request = connection.recv(1024).decode()
                print(f"Received HTTP request from {address}:\n")
                print("/----------START HTTP REQUEST PACKET----------/")
                print(request)
                print("/-----------END HTTP REQUEST PACKET-----------/")
            except UnicodeDecodeError as e:
                print(e)
                connection.close()
                continue

            # Example HTTP request:
                # GET / HTTP/1.1
                # Host: localhost:8000
                # User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
                # Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
                # Accept-Language: en-US,en;q=0.5
                # Accept-Encoding: gzip, deflate, br
                # Connection: keep-alive
                # Upgrade-Insecure-Requests: 1
                # Sec-Fetch-Dest: document
                # Sec-Fetch-Mode: navigate
                # Sec-Fetch-Site: none
                # Sec-Fetch-User: ?1

            # Handle the HTTP request
            try:
                if request:
                    headers = request.split('\n')
                    request_method = headers[0].split()[0]
                    filename = headers[0].split()[1]
                    if "/images" in filename:
                        filename = "/" + filename.split("/")[2]
                else:
                    print("Empty request. Closing connection...")
                    connection.close()
                    continue

            except TypeError as e:
                print(e)
                connection.close()
                continue
            except IndexError as e:
                print(e)
                connection.close()
                continue

            # Generate HTTP response
            response = None
            image_content = None

            if request_method == "GET":
                response, image_content = respond_get(connection, filename)
                if (response,image_content) == (None,None):
                    continue
            else:
                print("Request method not currently supported")
                connection.close()
                continue

            # Send HTTP response
            try:
                if any(map(filename[1:].__contains__, IMAGE_SUBSTRINGS)):
                    connection.sendall(response.encode() + image_content)
                elif response is None:
                    continue
                else:
                    connection.sendall(response.encode())
            except TypeError as e:
                print(e)
                connection.close()
                continue
            
            connection.close()
            print(f"Closed connection to {address}\n")

    except KeyboardInterrupt:
        # Close socket
        print("\nWeb server stopped")
        server_socket.close()


if __name__ == "__main__":
    main()
