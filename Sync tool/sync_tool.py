__author__ = 'robertevans'

import cv2
import matplotlib.pyplot as plt
import Tkinter as Tk
import tkFileDialog
import tkMessageBox
import os
from numpy import loadtxt
import json


class GUI(Tk.Frame):
    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Synchronisation tool")
        self.graph = None
        self.video_player = None
        self._data_left_sync_point = None
        self._data_right_sync_point = None
        self._video_left_sync_point = None
        self._video_right_sync_point = None
        self._data_file_name = None
        self._video_file_name = None
        self._events_file_name = None

        menu_bar = Tk.Menu(self.parent)
        self.parent.config(menu=menu_bar)

        file_menu = Tk.Menu(menu_bar)
        file_menu.add_command(label="Open...", command=self.on_load_data_or_video)
        file_menu.add_command(label="Save events", command=self.on_save_events)
        file_menu.add_command(label="Quit", command=self.quit)  # TODO: 'Are you sure?  Want to save?'
        menu_bar.add_cascade(label="File", menu=file_menu)

        self._label_current_frames = Tk.Label(parent, text="Load a video and some data from the file menu!")
        self._label_current_frames.grid(row=0, column=0, columnspan=4)

        self._next_frame_button = Tk.Button(parent, text="Next frame", command=self.on_next_frame)
        self._next_frame_button.grid(row=2, column=1)
        self._prev_frame_button = Tk.Button(parent, text="Prev frame", command=self.on_prev_frame)
        self._prev_frame_button.grid(row=2, column=2)

        self._video_slider = Tk.Scale(parent, command=self._on_slider_change, state=Tk.DISABLED, orient=Tk.HORIZONTAL,
                                      length=300)
        self._video_slider.grid(row=1, column=0, columnspan=4)

        Tk.Label(parent, text="Set synchronisation events:").grid(row=3, column=0, columnspan=4)

        self._left_data_sync_button = Tk.Button(parent, text="Data start",
                                                command=lambda: self.set_synchronisation_point('LD'))
        self._left_data_sync_button.grid(row=4, column=1, sticky=Tk.E)
        self._right_data_sync_button = Tk.Button(parent, text="Data end",
                                                 command=lambda: self.set_synchronisation_point('RD'))
        self._right_data_sync_button.grid(row=4, column=2, sticky=Tk.W)
        self._left_video_sync_button = Tk.Button(parent, text="Video start",
                                                 command=lambda: self.set_synchronisation_point('LV'))
        self._left_video_sync_button.grid(row=5, column=1, sticky=Tk.E)
        self._right_video_sync_button = Tk.Button(parent, text="Video end",
                                                  command=lambda: self.set_synchronisation_point('RV'))
        self._right_video_sync_button.grid(row=5, column=2, sticky=Tk.W)

        self.label_data_sync_events = Tk.Label(parent, text="Load some data!")
        self.label_data_sync_events.grid(row=6, column=0, columnspan=4)
        self.label_video_sync_events = Tk.Label(parent, text="Load a video!")
        self.label_video_sync_events.grid(row=7, column=0, columnspan=4)

        self._update_ui()

    def set_synchronisation_point(self, point):
        if point == 'LD' and self.graph and self.graph.current_x is not None:
            self._data_left_sync_point = round(self.graph.current_x)
        elif point == 'RD' and self.graph and self.graph.current_x is not None:
            self._data_right_sync_point = round(self.graph.current_x)
        elif point == 'LV' and self.video_player:
            self._video_left_sync_point = self.video_player.get_current_frame()
        elif point == 'RV' and self.video_player:
            self._video_right_sync_point = self.video_player.get_current_frame()
        else:
            if point == 'LD' or point == 'RD':
                tkMessageBox.showwarning("Could not set synchronisation point", "Please load a data file.")
            if point == 'LV' or point == 'RV':
                tkMessageBox.showwarning("Could not set synchronisation point", "Please load a video file.")
        self._update_ui()

    def _update_ui(self):
        self._check_if_graph_has_been_closed()
        self._update_synchronisation_event_labels()
        self._update_frame_label()

        if self.graph:
            self._left_data_sync_button.config(state=Tk.NORMAL)
            self._right_data_sync_button.config(state=Tk.NORMAL)
        else:
            self._left_data_sync_button.config(state=Tk.DISABLED)
            self._right_data_sync_button.config(state=Tk.DISABLED)

        if self.video_player:
            self._left_video_sync_button.config(state=Tk.NORMAL)
            self._right_video_sync_button.config(state=Tk.NORMAL)
            self._next_frame_button.config(state=Tk.NORMAL)
            self._prev_frame_button.config(state=Tk.NORMAL)
            self._video_slider.config(state=Tk.NORMAL, from_=0, to=self.video_player.n_frames)
            self._video_slider.set(self.video_player.get_current_frame())
        else:
            self._left_video_sync_button.config(state=Tk.DISABLED)
            self._right_video_sync_button.config(state=Tk.DISABLED)
            self._next_frame_button.config(state=Tk.DISABLED)
            self._prev_frame_button.config(state=Tk.DISABLED)
            self._video_slider.config(state=Tk.DISABLED)

    def _update_synchronisation_event_labels(self):
        if self.graph:
            self.label_data_sync_events.config(
                text="Data sync start: {0}\tend: {1}"
                .format(int(self._data_left_sync_point), int(self._data_right_sync_point)))
        else:
            self.label_data_sync_events.config(text="Load some data!")
        if self.video_player:
            self.label_video_sync_events.config(text="Video sync start: {0}\tend: {1}"
                                                .format(self._video_left_sync_point, self._video_right_sync_point))
        else:
            self.label_video_sync_events.config(text="Load a video!")

    def _update_frame_label(self):
        if self.video_player and self.graph and self.graph.current_x:
            self._label_current_frames.config(text="Video frame: {0}\tData frame: {1}"
                                              .format(self.video_player.get_current_frame(), int(self.graph.current_x)))
        elif self.video_player:
            self._label_current_frames.config(text="Video frame: {0}".format(self.video_player.get_current_frame()))
        elif self.graph and self.graph.current_x:
            self._label_current_frames.config(text="Data frame: {0}".format(int(self.graph.current_x)))
        else:
            self._label_current_frames.config(text="Load a video and some data from the file menu.")

    def on_next_frame(self):
        if self.video_player:
            self.video_player.show_next_frame()
            if self.graph:
                self.graph.set_line(self._get_data_frame_from_video_frame(), call_callback=False)
        else:
            tkMessageBox.showwarning("Hello!", "Please load a video file.")
        self._update_ui()

    def on_prev_frame(self):
        if self.video_player:
            self.video_player.show_prev_frame()
            if self.graph:
                self.graph.set_line(self._get_data_frame_from_video_frame(), call_callback=False)
        else:
            tkMessageBox.showwarning("Hello!", "Please load a video file.")
        self._update_ui()

    def _on_slider_change(self, slider_value):
        if self.video_player:
            self.video_player.set_current_frame(int(slider_value))
        self._update_ui()

    def _on_graph_line_update(self):
        if self.video_player:
            self.video_player.set_current_frame(self._get_video_frame_from_data_frame())
        self._update_ui()

    def _get_data_frame_from_video_frame(self):
        if self.video_player and self.graph:
            scale_factor = 1.0 / self._data_to_video_scale_factor()
            offset = self.video_player.get_current_frame() - self._video_left_sync_point
            return self._data_left_sync_point + offset*scale_factor

    def _get_video_frame_from_data_frame(self):
        if self.video_player and self.graph and self.graph.current_x:
            scale_factor = self._data_to_video_scale_factor()
            offset = self.graph.current_x - self._data_left_sync_point
            return self._video_left_sync_point + offset*scale_factor

    def _data_to_video_scale_factor(self):
        if self._data_left_sync_point is not None and self._data_right_sync_point is not None \
                and self._video_left_sync_point is not None and self._video_right_sync_point is not None:
            data_duration = self._data_right_sync_point - self._data_left_sync_point
            video_duration = self._video_right_sync_point - self._video_left_sync_point
            scale_factor = float(video_duration) / data_duration
            return scale_factor

    def _check_if_graph_has_been_closed(self):
        if self.graph:
            if self.graph.figure_is_closed():
                del self.graph
                self.graph = None

    def on_load_data_or_video(self):
        dlg = tkFileDialog.Open(self)
        fl = dlg.show()
        if fl != '':
            file_name, file_extension = os.path.splitext(os.path.basename(fl))
            if file_extension == '.csv' or file_extension == '.txt':
                try:
                    # TODO: Add 'are you sure you want to close without saving?'
                    # TODO: Load data through dialog box exposing options of numpy.loadtxt
                    self._check_if_graph_has_been_closed()
                    if not self.graph:
                        self.graph = Graph(fl, self._on_graph_line_update)
                    else:
                        self.graph.load_file(fl)
                    self._data_left_sync_point = 0
                    self._data_right_sync_point = self.graph.data_length - 1
                    self._data_file_name = file_name
                except ValueError, e:
                    tkMessageBox.showerror("Error loading data file", e, icon=tkMessageBox.ERROR)
                    self.graph.close_figure()
                    del self.graph
                    self.graph = None
            elif file_extension == '.json':
                if self.video_player and self.graph:
                    try:
                        with open(fl, 'r') as events_file:
                            data = json.load(events_file)
                            points = data['synchronisation_points']
                            self._data_left_sync_point = int(points['data_start'])
                            self._data_right_sync_point = int(points['data_end'])
                            self._video_left_sync_point = int(points['video_start'])
                            self._video_right_sync_point = int(points['video_end'])
                            self._events_file_name = file_name
                            self.graph.set_line(self._get_data_frame_from_video_frame(), call_callback=False)
                            self._update_ui()
                    except Exception, e:
                        tkMessageBox.showerror("Error loading events", e, icon=tkMessageBox.ERROR)
                else:
                    tkMessageBox.showinfo("Could not load events", "Please load data and video files first.")
            else:
                try:
                    if not self.video_player:
                        self.video_player = VideoPlayer(fl)
                    else:
                        self.video_player.load_video(fl)
                    self._video_left_sync_point = 0
                    self._video_right_sync_point = self.video_player.n_frames - 1
                    self._video_file_name = file_name
                except ValueError, e:
                    tkMessageBox.showerror("Error loading video file", e, icon=tkMessageBox.ERROR)
                    del self.video_player
                    self.video_player = None
        self._update_ui()

    def on_save_events(self):
        if self.video_player and self.graph:
            if self._events_file_name is None:
                self._events_file_name = "{0}-{1}.json".format(self._data_file_name, self._video_file_name)
            filename = tkFileDialog.asksaveasfilename(parent=self, initialfile=self._events_file_name)
            if filename:
                with open(filename, 'w') as outfile:
                    data = {'synchronisation_points':
                                {'data_start': self._data_left_sync_point, 'data_end': self._data_right_sync_point,
                                 'video_start': self._video_left_sync_point, 'video_end': self._video_right_sync_point},
                            'segmentation_points': None}
                    json.dump(data, outfile)
        else:
            tkMessageBox.showinfo("Save events", "No events to save!")
        # TODO: save other annotated events (segmentation points)


class VideoPlayer:
    """ Manages frame by frame video playback through OpenCV and provides an API to control it. """

    def __init__(self, video_file):
        self.n_frames = None
        self._video_capture = None
        self._current_frame = None
        self._window_name = str(video_file)

        self.load_video(video_file)

    def load_video(self, video_file):
        # TODO: Add optional size and position arguments
        # Load video from file
        self._video_capture = cv2.VideoCapture(video_file)
        if not self._video_capture.isOpened():
            raise ValueError("Invalid video file")
        else:
            self.n_frames = int(self._video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

            # And display the first frame
            cv2.namedWindow(self._window_name)

            self._current_frame = 0
            self._show_current_frame()

    def show_next_frame(self):
        self._current_frame = (self._current_frame + 1) % self.n_frames
        self._show_current_frame()

    def show_prev_frame(self):
        self._current_frame = (self._current_frame - 1) % self.n_frames
        self._show_current_frame()

    def set_current_frame(self, frame_number):
        if 0 <= frame_number < self.n_frames:
            self._current_frame = int(round(frame_number))
            self._show_current_frame()

    def get_current_frame(self):
        return self._current_frame

    def _show_current_frame(self):
        self._video_capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, self._current_frame-1)
        success, img = self._video_capture.read()
        cv2.imshow(self._window_name, img)
        cv2.waitKey(1)


class Graph():
    """ Creates an interactive data plot with matplotlib and provides an API to control it. """

    def __init__(self, csv_file, line_update_callback):
        self.current_x = None
        self.data_length = None
        self._data = None
        self._fig = None
        self._ax = None
        self._toolbar = None
        self._line = None
        self._mouse_pressed = None
        self._line_update_callback = line_update_callback

        self._load_data(csv_file)
        self._draw_graph(str(csv_file))

    def _load_data(self, csv_file):
        # TODO: Add optional arguments for number of header lines and which columns to use.
        with open(csv_file, 'r') as fin:
            # TODO: try different loadtxt args for different headers - eg if header == blah...
            self._data = loadtxt(fin, delimiter=",", skiprows=1, usecols=[8, 9, 10])
            self.data_length = len(self._data)

    def _draw_graph(self, title_):
        plt.ion()
        if not self._fig:
            self._fig = plt.figure()
            self._fig.canvas.mpl_connect('button_press_event', self.on_press)
            self._fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
            self._fig.canvas.mpl_connect('button_release_event', self.on_release)
            self._toolbar = plt.get_current_fig_manager().toolbar
        self._ax = self._fig.add_subplot(111)
        self._ax.plot(self._data)
        plt.title(title_)

    def load_file(self, csv_file):
        # TODO: Add optional arguments for number of header lines and which columns to use.
        plt.clf()
        self._ax = None
        self._line = None
        self.current_x = None
        self._mouse_pressed = None
        self._load_data(csv_file)
        self._draw_graph()

    def on_press(self, event):
        if self._toolbar.mode == '':
            if event.inaxes and event.xdata > 0:
                self.set_line(event.xdata)
        self._mouse_pressed = True

    def on_motion(self, event):
        if self._toolbar.mode == '' and self._mouse_pressed:
            if event.inaxes and event.xdata > 0:
                self.set_line(event.xdata)

    def on_release(self, event):
        if self._toolbar.mode == '':
            if event.inaxes and event.xdata > 0:
                self.set_line(event.xdata)
        self._mouse_pressed = None

    def set_line(self, x, call_callback=True):
        if self._line:
            del(self._ax.lines[-1])
            self._line = None
            self.current_x = None
        if 0 <= x <= len(self._data):
            self.current_x = x
            self._line = self._line = self._ax.axvline(x=x, color='red', linewidth=3)
            self._fig.canvas.draw()
            if call_callback:
                self._line_update_callback()

    def close_figure(self):
        plt.close(self._fig)

    def figure_is_closed(self):
        return self._fig.canvas.manager not in plt._pylab_helpers.Gcf.figs.values()


if __name__ == '__main__':
    """ Launches and manages all of the application's components """
    root = Tk.Tk()
    gui = GUI(root)
    root.geometry("310x220+50+50")  # TODO: Make all the components launch with a nice layout configuration
    root.mainloop()
