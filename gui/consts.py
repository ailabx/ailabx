from enum import Enum

class FRAMES(Enum):
    FRAME_DATA_TABLE = 1,

class FramesMgr(object):
    def __init__(self):
        self.frames = {}

    def add_frame(self, key, frame):
        if key in self.frames.keys():
            print('名字已存在，将覆盖原有组件')
        self.frames[key] = frame

    def get_frame(self, key):
        return self.frames[key]

mgr_frames = FramesMgr()