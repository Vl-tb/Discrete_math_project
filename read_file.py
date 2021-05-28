# import cv2
#
# cap = cv2.VideoCapture("v2.mp4")
# ret, frame = cap.read()
# while 1:
#     ret, frame = cap.read()
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q') or ret == False:
#         cap.release()
#         cv2.destroyAllWindows()
#         break
#     cv2.imshow('frame', frame)
import base64

with open("example_files/example.mp4", "rb") as videoFile:
    text = base64.b64encode(videoFile.read())

    # file = open("textTest.txt", "wb")
    # file.write(text)
    # file.close()

    # fh = open("video.mp4", "wb")
    # fh.write(base64.b64decode(text))
    # fh.close()
