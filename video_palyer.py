import cv2
import time


class VideoPlayer:
    """Allows play video (without a sound)"""
    def __init__(self,video_path):
        self.cap = cv2.VideoCapture(video_path)
        self.waitkey = cv2.waitKey(0)
        self.isStop = False

    def get_cap(self):
        """Gets capture of video"""
        return self.cap.read()

    def get_cap_frame(self):
        """Get every frame"""
        return self.cap.get(cv2.CAP_PROP_POS_FRAMES)

    def restart(self):
        """Sets video in starting position"""
        # if self.isStop == True:
        #     self.isStop = False
        self.cap.set(cv2.CAP_PROP_POS_FRAMES,0)


def main(file_name: str):
    """Main function"""
    player = VideoPlayer(file_name)

    i=0
    while(1):
        if player.isStop == False:
            ret, frame = player.get_cap()

        # PRINTS i AND WHICH FRAME IS RIGHT NOW
        print(i, player.get_cap_frame())

        cv2.imshow('frame', frame)
        # ENDS THE VIDEO
        if cv2.waitKey(7) & 0xFF == ord('q'):
            break

        # PAUSE
        if cv2.waitKey(15) & 0xFF == ord('s') and player.isStop == False:
            player.isStop = True

        # RESUME
        if cv2.waitKey(15) & 0xFF == ord('f') and player.isStop == True:
            player.isStop = False

        # RESTART
        if cv2.waitKey(15) & 0xFF == ord('r'):
            player.restart()

        i += 1

    player.cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main('example.mp4')
