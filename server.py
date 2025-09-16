import socket, cv2, numpy as np, time

# -------- Configuration --------
VIDEO_FILE = "sample.mp4"      # put your video file here
SERVER_IP  = "0.0.0.0"         # listen on all interfaces
PORT       = 5000
CHUNK_SIZE = 1024              # bytes
FPS        = 30                # target frames per second
# --------------------------------

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_addr = None

cap = cv2.VideoCapture(VIDEO_FILE)
if not cap.isOpened():
    raise RuntimeError("Could not open video file")

print(f"Server ready. Waiting for client on port {PORT}...")

# Wait until first packet from client to learn its address
sock.bind((SERVER_IP, PORT))
data, client_addr = sock.recvfrom(1024)
print("Client connected:", client_addr)

frame_interval = 1.0 / FPS

while True:
    ret, frame = cap.read()
    if not ret:
        break  # video ended

    # Encode frame as JPEG
    _, encoded = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    frame_bytes = encoded.tobytes()

    # Send in chunks; last chunk header byte = 1 else 0
    for i in range(0, len(frame_bytes), CHUNK_SIZE):
        chunk = frame_bytes[i:i+CHUNK_SIZE]
        marker = b'\x01' if i + CHUNK_SIZE >= len(frame_bytes) else b'\x00'
        sock.sendto(marker + chunk, client_addr)

    time.sleep(frame_interval)

cap.release()
sock.close()
print("Streaming finished.")
