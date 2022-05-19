
class AdapterUserGui:

    def __init__(self, stop: bool, video_canvas):
        self._stop = stop
        self._video_canvas = video_canvas
        self._cap = None

    def set_capture(self, cap):
        self._cap = cap

    def set_stop(self, stop):
        self._stop = stop

    @property
    def stop(self):
        return self._stop

    @property
    def video_canvas(self):
        return self._video_canvas

    @property
    def a_capture(self):
        return self._cap
