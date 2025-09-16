import socket, cv2, numpy as np

# -------- Configuration --------
SERVER_IP = "127.0.0.1"   # change to server’s IP if on different machine
PORT      = 5000
CHUNK_SIZE = 1024
# --------------------------------

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b'hello', (SERVER_IP, PORT))  # handshake
sock.settimeout(5)

print("Receiving stream... Press 'q' to quit.")
frame_data = b""

while True:
    try:
        packet, _ = sock.recvfrom(CHUNK_SIZE + 1)
    except socket.timeout:
        break

    marker = packet[0]        # first byte is marker
    frame_data += packet[1:]

    if marker == 1:  # last packet of this frame
        # Decode and show
        npdata = np.frombuffer(frame_data, dtype=np.uint8)
        frame = cv2.imdecode(npdata, cv2.IMREAD_COLOR)
        if frame is not None:
            cv2.imshow('Video', frame)

        frame_data = b""

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
sock.close()
