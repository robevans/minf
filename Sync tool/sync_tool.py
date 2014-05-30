__author__ = 'robertevans'

import cv2
import matplotlib.pyplot as plt
import Tkinter as Tk
import tkFileDialog
import os
from numpy import loadtxt


class GUI(Tk.Frame):
    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Synchronisation tool")
        self.graph = None
        self.video_player = None

        menu_bar = Tk.Menu(self.parent)
        self.parent.config(menu=menu_bar)

        file_menu = Tk.Menu(menu_bar)
        file_menu.add_command(label="Load data/video", command=self.on_load_data_or_video)
        file_menu.add_command(label="Save events", command=self.quit)
        file_menu.add_command(label="Quit", command=self.quit)  # TODO: 'Are you sure?  Want to save?'
        menu_bar.add_cascade(label="File", menu=file_menu)

        # TODO: Add in buttons to advance the video :)

    def on_load_data_or_video(self):
        dlg = tkFileDialog.Open(self)
        fl = dlg.show()
        if fl != '':
            file_name, file_extension = os.path.splitext(fl)
            if file_extension == '.csv':
                # TODO: Add 'are you sure you want to close without saving?'
                if not self.graph:
                    self.graph = Graph(fl)
                else:
                    self.graph.load_file(fl)
            elif file_extension == '.events':
                pass # TODO: Load saved data annotations (e.g. gait phase events)
            else:
                if not self.video_player:
                    self.video_player = VideoPlayer(fl)
                else:
                    self.video_player.load_video(fl)

    def on_save_events(self):
        pass # TODO: save annotated events to .events file


class VideoPlayer:
    """ Manages frame by frame video playback through OpenCV and provides an API to control it. """

    def __init__(self, video_file):
        self._video_capture = None
        self._n_frames = None
        self._fps = None
        self._milliseconds_per_frame = None
        self._current_frame = None
        self._window_name = None

        self.load_video(video_file)

    def load_video(self, video_file):
        # TODO: Add optional size and position arguments
        # Load video from file
        self._video_capture = cv2.VideoCapture(video_file)
        if not self._video_capture.isOpened():
            raise ValueError("Invalid video file")
        self._n_frames = int(self._video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
        self._fps = self._video_capture.get(cv2.cv.CV_CAP_PROP_FPS)
        self._milliseconds_per_frame = int(1000/self._fps)

        # And display the first frame
        cv2.namedWindow(self._window_name)

        self._current_frame = -1
        self._show_current_frame()

    def show_next_frame(self):
        self._current_frame = (self._current_frame + 1) % self._n_frames
        self._show_current_frame()

    def show_prev_frame(self):
        self._current_frame = (self._current_frame - 1) % self._n_frames
        self._show_current_frame()

    def _show_current_frame(self):
        self._video_capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, self._current_frame)
        success, img = self._video_capture.read()
        cv2.imshow(self._window_name, img)
        cv2.waitKey(self._milliseconds_per_frame)

    def close_window(self):
        cv2.destroyWindow(self._window_name)

    def __del__(self):
        cv2.destroyWindow(self._window_name)


class Graph():
    """ Creates an interactive data plot with matplotlib and provides an API to control it. """

    def __init__(self, csv_file):
        self.current_x = None
        self.is_updated = None
        self._data = None
        self._fig = None
        self._ax = None
        self._toolbar = None
        self._line = None
        self._mouse_pressed = None

        self._load_data(csv_file)
        self._draw_graph()

    def _load_data(self, csv_file):
        # TODO: Add optional arguments for number of header lines and which columns to use.
        with open(csv_file, 'r') as fin:
            self._data = loadtxt(fin, delimiter=",")

    def _draw_graph(self):
        plt.ion()
        if not self._fig:
            self._fig = plt.figure()
            self._fig.canvas.mpl_connect('button_press_event', self.on_press)
            self._fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
            self._fig.canvas.mpl_connect('button_release_event', self.on_release)
            self._toolbar = plt.get_current_fig_manager().toolbar
        self._ax = self._fig.add_subplot(111)
        self._ax.plot(self._data)

    def load_file(self, csv_file):
        # TODO: Add optional arguments for number of header lines and which columns to use.
        plt.clf()
        self._ax = None
        self._line = None
        self.current_x = None
        self.is_updated = None
        self._mouse_pressed = None
        self._load_data(csv_file)
        self._draw_graph()

    def on_press(self, event):
        if self._toolbar.mode == '':
            if event.inaxes and event.xdata > 0:
                self.current_x = event.xdata
                self.is_updated = True
                self.set_line(event.xdata)
        self._mouse_pressed = True

    def on_motion(self, event):
        if self._toolbar.mode == '' and self._mouse_pressed:
            if event.inaxes and event.xdata > 0:
                self.current_x = event.xdata
                self.is_updated = True
                self.set_line(event.xdata)

    def on_release(self, event):
        if self._toolbar.mode == '':
            if event.inaxes and event.xdata > 0:
                self.current_x = event.xdata
                self.is_updated = True
                self.set_line(event.xdata)
        self._mouse_pressed = None

    def set_line(self, x):
        if self._line:
            del(self._ax.lines[-1])
            self._line = None
        if 0 <= x <= len(self._data):
            self._line = self._line = self._ax.axvline(x=x, color='red', linewidth=5)
            self._fig.canvas.draw()


if __name__ == '__main__':
    """ Launches and manages all of the application's components """
    import sys
    print sys.argv

    root = Tk.Tk()
    gui = GUI(root)
    root.geometry("300x250+300+300") # TODO: Make all the components launch in a nice configuration
    root.mainloop()
