__author__ = 'robertevans'

import cv2
import Tkinter as Tk
import matplotlib.pyplot as plt
import ttk
import tkFileDialog
import tkMessageBox
import os
import json
from collections import OrderedDict
from numpy import loadtxt
import threading


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
        self._events_file = None
        self._annotated_events = {}
        self._lock = threading.Lock()

        # Menu controls
        menu_bar = Tk.Menu(self.parent)
        self.parent.config(menu=menu_bar)

        file_menu = Tk.Menu(menu_bar)
        file_menu.add_command(label="Load...", command=self.on_load_data_or_video)
        file_menu.add_command(label="Save events", command=self.on_save_events)
        file_menu.add_command(label="Quit", command=self.quit)  # TODO: 'Are you sure?  Want to save?'
        menu_bar.add_cascade(label="File", menu=file_menu)

        self._label_current_frames = Tk.Label(parent, text="Load a video and data from the file menu!")
        self._label_current_frames.grid(row=10, column=0, columnspan=4)

        # Video controls
        ttk.Separator(parent, orient=Tk.HORIZONTAL).grid(row=15, column=0, columnspan=4, sticky="ew")
        Tk.Label(parent, text="Video controls:").grid(row=16, column=0, columnspan=4)

        self._video_slider = Tk.Scale(parent, command=self._on_video_slider_change, orient=Tk.HORIZONTAL, length=300)
        self._video_slider.grid(row=20, column=0, columnspan=4)

        self._prev_video_frame_button = Tk.Button(parent, text="Prev video frame", command=self.on_prev_video_frame)
        self._prev_video_frame_button.grid(row=30, column=1)
        self._next_video_frame_button = Tk.Button(parent, text="Next video frame", command=self.on_next_video_frame)
        self._next_video_frame_button.grid(row=30, column=2)

        # Data controls
        ttk.Separator(parent, orient=Tk.HORIZONTAL).grid(row=32, column=0, columnspan=4, sticky="ew")
        Tk.Label(parent, text="Data controls:").grid(row=33, column=0, columnspan=4)

        self._data_slider = Tk.Scale(parent, command=self._on_data_slider_change, orient=Tk.HORIZONTAL, length=300)
        self._data_slider.grid(row=34, column=0, columnspan=4)

        self._prev_data_frame_button = Tk.Button(parent, text="Prev data frame", command=self.on_prev_data_frame)
        self._prev_data_frame_button.grid(row=35, column=1)
        self._next_data_frame_button = Tk.Button(parent, text="Next data frame", command=self.on_next_data_frame)
        self._next_data_frame_button.grid(row=35, column=2)

        # Synchronisation controls
        ttk.Separator(parent, orient=Tk.HORIZONTAL).grid(row=40, column=0, columnspan=4, sticky="ew")
        Tk.Label(parent, text="Set synchronisation events:").grid(row=50, column=0, columnspan=4)

        self._left_data_sync_button = Tk.Button(parent, text="Data start",
                                                command=lambda: self.set_synchronisation_point('LD'))
        self._left_data_sync_button.grid(row=60, column=1, sticky=Tk.E)
        self._right_data_sync_button = Tk.Button(parent, text="Data end",
                                                 command=lambda: self.set_synchronisation_point('RD'))
        self._right_data_sync_button.grid(row=60, column=2, sticky=Tk.W)
        self._left_video_sync_button = Tk.Button(parent, text="Video start",
                                                 command=lambda: self.set_synchronisation_point('LV'))
        self._left_video_sync_button.grid(row=70, column=1, sticky=Tk.E)
        self._right_video_sync_button = Tk.Button(parent, text="Video end",
                                                  command=lambda: self.set_synchronisation_point('RV'))
        self._right_video_sync_button.grid(row=70, column=2, sticky=Tk.W)

        self.label_data_sync_events = Tk.Label(parent, text="Load some data!")
        self.label_data_sync_events.grid(row=80, column=0, columnspan=4)
        self.label_video_sync_events = Tk.Label(parent, text="Load a video!")
        self.label_video_sync_events.grid(row=90, column=0, columnspan=4)

        # Annotation controls
        ttk.Separator(parent, orient=Tk.HORIZONTAL).grid(row=100, column=0, columnspan=4, sticky="ew")
        Tk.Label(parent, text="Annotate data events:").grid(row=110, column=0, columnspan=4)

        Tk.Label(parent, text="Press a key (0-9) to mark an event.").grid(row=120, column=0, columnspan=4)

        scrollbar = Tk.Scrollbar(parent)
        scrollbar.grid(row=130, column=3, sticky='wns')
        self.events_listbox = \
            Tk.Listbox(parent, width=30, height=10, relief=Tk.RIDGE, borderwidth=2, yscrollcommand=scrollbar.set)
        self.events_listbox.grid(row=130, column=1, columnspan=2, sticky='we')
        scrollbar.config(command=self.events_listbox.yview)

        self.events_listbox.bind('<<ListboxSelect>>', self._on_listbox_selection)

        def remove_listbox_focus(event):
            if self.events_listbox is not self.winfo_containing(event.x_root, event.y_root):
                self.events_listbox.selection_clear(0, Tk.END)
                parent.focus()
        parent.bind("<Button>", remove_listbox_focus)

        Tk.Label(parent, text="Data index : Event type").grid(row=140, column=0, columnspan=4, sticky='we')

        # TODO: add keypress event bindings for graph and video player windows as well (here be dragons)
        parent.bind("<Key>", self.on_key_press_event)

        self._update_ui(caller='init')

    def _on_listbox_selection(self, event):
        try:
            widget = event.widget
            selection = widget.curselection()
            value = widget.get(selection[0])
            event_index, event_type = map(int, value.split(':'))
            if self.graph:
                self.graph.set_line(event_index)
        except IndexError:
            pass

    def on_key_press_event(self, event):
        def process_char(key):
            if key.isdigit() and self.graph and self.graph.current_x is not None:
                self._annotated_events[int(round(self.graph.current_x))] = int(key)
                self._display_annotated_events()
                self._auto_save()
            elif ord(key) == 127:  # Backspace key deletes any selected listbox item
                selected_value = self.events_listbox.get(self.events_listbox.curselection()[0])
                event_index, event_type = map(int, selected_value.split(':'))
                del self._annotated_events[event_index]
                self._display_annotated_events()
                self._auto_save()
        try:
            process_char(event.char)  # If the event came from Tkinter
        except AttributeError:
            pass  # process_char(event.key)  # If the event came from Pyplot.  (Crashes on insertion into listbox).
            # http://stackoverflow.com/questions/24035881/fatal-python-error-pyeval-restorethread-null-tstate-when-inserting-into-tkin
        except TypeError, e:
            print "Type Error processing key press:", e

    def _display_annotated_events(self):
        self.events_listbox.delete(0, Tk.END)
        if self._annotated_events:
            sorted_events = sorted(self._annotated_events.items())
            listbox_items = map(lambda t: "{0} : {1}".format(t[0], t[1]), sorted_events)
            self.events_listbox.insert(Tk.END, *listbox_items)

    def set_synchronisation_point(self, point):
        if point == 'LD' and self.graph and self.graph.current_x is not None:
            self._data_left_sync_point = int(round(self.graph.current_x))
        elif point == 'RD' and self.graph and self.graph.current_x is not None:
            self._data_right_sync_point = int(round(self.graph.current_x))
        elif point == 'LV' and self.video_player:
            self._video_left_sync_point = self.video_player.get_current_frame()
        elif point == 'RV' and self.video_player:
            self._video_right_sync_point = self.video_player.get_current_frame()
        else:
            if point == 'LD' or point == 'RD':
                tkMessageBox.showwarning("Could not set synchronisation point", "Please load a data file.")
            if point == 'LV' or point == 'RV':
                tkMessageBox.showwarning("Could not set synchronisation point", "Please load a video file.")
        self._auto_save()
        self._update_ui(caller='set_sync_point')

    def _update_ui(self, caller=None):
        self._check_if_graph_has_been_closed()
        self._update_synchronisation_event_labels()
        self._update_frame_label()
        self._display_annotated_events()

        if self.graph:
            self._left_data_sync_button.config(state=Tk.NORMAL)
            self._right_data_sync_button.config(state=Tk.NORMAL)
            self._next_data_frame_button.config(state=Tk.NORMAL)
            self._prev_data_frame_button.config(state=Tk.NORMAL)
            self._data_slider.config(state=Tk.NORMAL, from_=0, to=self.graph.data_length)
            if self.graph.current_x is not None and caller is not 'data_slider':
                self._data_slider.set(self.graph.current_x)
        else:
            self._left_data_sync_button.config(state=Tk.DISABLED)
            self._right_data_sync_button.config(state=Tk.DISABLED)
            self._next_data_frame_button.config(state=Tk.DISABLED)
            self._next_data_frame_button.config(state=Tk.DISABLED)
            self._prev_data_frame_button.config(state=Tk.DISABLED)
            self._data_slider.config(state=Tk.DISABLED)

        if self.video_player:
            self._left_video_sync_button.config(state=Tk.NORMAL)
            self._right_video_sync_button.config(state=Tk.NORMAL)
            self._next_video_frame_button.config(state=Tk.NORMAL)
            self._prev_video_frame_button.config(state=Tk.NORMAL)
            self._video_slider.config(state=Tk.NORMAL, from_=0, to=self.video_player.n_frames)
            if caller is not "video_slider":
                self._video_slider.set(self.video_player.get_current_frame())
        else:
            self._left_video_sync_button.config(state=Tk.DISABLED)
            self._right_video_sync_button.config(state=Tk.DISABLED)
            self._next_video_frame_button.config(state=Tk.DISABLED)
            self._prev_video_frame_button.config(state=Tk.DISABLED)
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
        if self.video_player and self.graph and self.graph.current_x is not None:
            self._label_current_frames.config(text="Video frame: {0}\tData frame: {1}"
                                              .format(self.video_player.get_current_frame(), int(self.graph.current_x)))
        elif self.video_player:
            self._label_current_frames.config(text="Video frame: {0}".format(self.video_player.get_current_frame()))
        elif self.graph and self.graph.current_x is not None:
            self._label_current_frames.config(text="Data frame: {0}".format(int(self.graph.current_x)))
        else:
            self._label_current_frames.config(text="Load a video and data from the file menu.")

    def on_next_video_frame(self):
        if self.video_player:
            self._video_slider.set((self._video_slider.get() + 1) % self.video_player.n_frames)

    def on_prev_video_frame(self):
        if self.video_player:
            self._video_slider.set((self._video_slider.get() - 1) % self.video_player.n_frames)

    def _on_video_slider_change(self, slider_value):
        if self.video_player:
            self.video_player.set_current_frame(int(slider_value))
            if self.graph:
                self.graph.set_line(self._get_data_frame_from_video_frame(), call_callback=False)
            self._update_ui(caller="video_slider")

    def on_next_data_frame(self):
        if self.graph and self.graph.data_length:
            if self.graph.current_x is None:
                data_value = 0
            else:
                data_value = (self.graph.current_x + 1) % self.graph.data_length
            self._data_slider.set(data_value)

    def on_prev_data_frame(self):
        if self.graph and self.graph.data_length:
            if self.graph.current_x is None:
                data_value = self.graph.data_length - 1
            else:
                data_value = (self.graph.current_x - 1) % self.graph.data_length
            self._data_slider.set(data_value)

    def _on_data_slider_change(self, slider_value):
        if self.graph:
            self.graph.set_line(int(slider_value))
            self._update_ui(caller="data_slider")

    def _on_graph_line_update(self):
        if self.video_player:
            self.video_player.set_current_frame(self._get_video_frame_from_data_frame())
        self._update_ui(caller="graph_line_update")

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
        try:
            if self._data_left_sync_point is not None and self._data_right_sync_point is not None \
                    and self._video_left_sync_point is not None and self._video_right_sync_point is not None:
                data_duration = self._data_right_sync_point - self._data_left_sync_point
                video_duration = self._video_right_sync_point - self._video_left_sync_point
                scale_factor = float(video_duration) / data_duration
                return scale_factor
        except ZeroDivisionError, e:
            import sys
            sys.stderr.write("warning: {0}".format(e))
            return 1

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
                        self.graph = Graph(fl, self._on_graph_line_update, self.on_key_press_event)
                    else:
                        self.graph.load_file(fl)
                    if self._data_left_sync_point is None or self._data_left_sync_point < 0:
                        self._data_left_sync_point = 0
                    if self._data_right_sync_point is None or self._data_right_sync_point >= self.graph.data_length:
                        self._data_right_sync_point = self.graph.data_length - 1
                    self._data_file_name = file_name
                except ValueError, e:
                    tkMessageBox.showerror("Error loading data file", e, icon=tkMessageBox.ERROR)
                    self.graph.close_figure()
                    del self.graph
                    self.graph = None
            elif file_extension == '.json':
                try:
                    with open(fl, 'r') as events_file:
                        data = json.load(events_file)
                        points = data['synchronisation_points']
                        events = data['event_annotations']
                        if type(events) is dict:
                            self._annotated_events = \
                                {int(data_index): int(event_type) for data_index, event_type in events.items()}
                        else:
                            self._annotated_events = {}
                        if not self.graph or 0 <= points['data_start'] < self.graph.data_length:
                            self._data_left_sync_point = points['data_start']
                        if not self.graph or 0 <= points['data_end'] < self.graph.data_length:
                            self._data_right_sync_point = points['data_end']
                        if not self.video_player or 0 <= points['video_start'] < self.video_player.n_frames:
                            self._video_left_sync_point = points['video_start']
                        if not self.video_player or 0 <= points['video_end'] < self.video_player.n_frames:
                            self._video_right_sync_point = points['video_end']
                        self._events_file = "{0}{1}".format(file_name, file_extension)
                        if self.graph and self.video_player:
                            self.graph.set_line(self._get_data_frame_from_video_frame(), call_callback=False)
                except Exception, e:
                    tkMessageBox.showerror("Error loading events", e, icon=tkMessageBox.ERROR)
            else:
                try:
                    if not self.video_player:
                        self.video_player = VideoPlayer(fl)
                    else:
                        self.video_player.load_video(fl)
                    if self._video_left_sync_point is None or self._video_left_sync_point < 0:
                        self._video_left_sync_point = 0
                    if self._video_right_sync_point is None \
                            or self._video_right_sync_point >= self.video_player.n_frames:
                        self._video_right_sync_point = self.video_player.n_frames - 1
                    self._video_file_name = file_name
                except ValueError, e:
                    tkMessageBox.showerror("Error loading video file", e, icon=tkMessageBox.ERROR)
                    del self.video_player
                    self.video_player = None
            self._update_ui(caller='load')

    def on_save_events(self):
        if self._events_file is None:
            self._events_file = "{0}.json".format(self._data_file_name)
        filename = tkFileDialog.asksaveasfilename(parent=self, initialfile=self._events_file)
        if filename:
            with open(filename, 'w') as outfile:
                data = {'synchronisation_points':
                            {'data_start': self._data_left_sync_point, 'data_end': self._data_right_sync_point,
                             'video_start': self._video_left_sync_point, 'video_end': self._video_right_sync_point},
                        'event_annotations': OrderedDict(sorted(self._annotated_events.items()))}
                json.dump(data, outfile)

    def _auto_save(self):
        with open('events_auto_save.json', 'w') as outfile:
            data = {'synchronisation_points':
                        {'data_start': self._data_left_sync_point, 'data_end': self._data_right_sync_point,
                         'video_start': self._video_left_sync_point, 'video_end': self._video_right_sync_point},
                    'event_annotations': OrderedDict(sorted(self._annotated_events.items()))}
            json.dump(data, outfile)


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
        if frame_number is not None:
            if self._current_frame != int(round(frame_number)) and 0 <= frame_number < self.n_frames:
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

    def __init__(self, csv_file, line_update_callback, key_press_callback):
        self.current_x = None
        self.data_length = None
        self._data = None
        self._fig = None
        self._ax = None
        self._toolbar = None
        self._line = None
        self._mouse_pressed = None
        self._line_update_callback = line_update_callback
        self._key_press_callback = key_press_callback

        self._load_data(csv_file)
        self._draw_graph(str(csv_file))

    def _load_data(self, csv_file):
        # TODO: Add optional arguments for number of header lines and which columns to use.
        with open(csv_file, 'r') as fin:
            # TODO: try different loadtxt args for different headers - eg if header == blah, use these args...
            self._data = loadtxt(fin, delimiter=",", skiprows=1, usecols=[8, 9, 10])
            self.data_length = len(self._data)

    def _draw_graph(self, title_):
        plt.ion()
        if not self._fig:
            self._fig = plt.figure()
            self._fig.canvas.mpl_connect('button_press_event', self.on_press)
            self._fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
            self._fig.canvas.mpl_connect('button_release_event', self.on_release)
            self._fig.canvas.mpl_connect('key_press_event', self._key_press_callback)
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
        self._draw_graph(str(csv_file))

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
        if self.current_x is None or abs(self.current_x - x) > 0.0001:
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
    synchronisation_window = GUI(root)
    root.title("Video-Data Tool")
    root.geometry("302x600+50+50")

    # TODO: Make all the components launch with a nice layout configuration
    root.mainloop()
