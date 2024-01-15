import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime
from AreaSelection import AreaSelection
from RecordHelpers import RecordHelpers

class GIFMaker:
    def __init__(self, master):
        self.master = master
        master.title("GIF Maker")

        self.notebook = ttk.Notebook(master)

        self.tab1 = tk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Area")

        self.label_input = tk.Label(self.tab1, text="Seleccionar Video o Grabar Pantalla:")
        self.label_input.pack()

        self.button_screen_record = tk.Button(self.tab1, text="Iniciar Grabación", command=self.iniciar_grabacion)
        self.button_screen_record.pack()

        self.button_stop_record = tk.Button(self.tab1, text="Detener Grabación", command=self.detener_grabacion, state=tk.DISABLED)
        self.button_stop_record.pack()

        self.button_select_area = tk.Button(self.tab1, text="Seleccionar Área", command=self.seleccionar_area)
        self.button_select_area.pack()
        
        self.button_deselect_area = tk.Button(self.tab1, text="Deseleccionar Área", command=self.deseleccionar_area)
        self.button_deselect_area.pack()

        self.tab2 = tk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Video")
        
        self.label_input = tk.Label(self.tab2, text="Seleccionar Video:")
        self.label_input.pack()

        self.button_input = tk.Button(self.tab2, text="Seleccionar", command=self.seleccionar_video)
        self.button_input.pack()

        self.label_output = tk.Label(self.master, text="Guardar GIF en:")
        self.label_output.pack()

        self.button_output = tk.Button(self.master, text="Seleccionar", command=self.seleccionar_salida)
        self.button_output.pack()
        
        self.label_inicio = tk.Label(self.tab2, text="Inicio del GIF (segundos):")
        self.label_inicio.pack()

        self.entry_inicio = tk.Entry(self.tab2)
        self.entry_inicio.pack()

        self.label_duracion = tk.Label(self.tab2, text="Duración del GIF (segundos):")
        self.label_duracion.pack()

        self.entry_duracion = tk.Entry(self.tab2)
        self.entry_duracion.pack()

        self.label_fps = tk.Label(self.tab2, text="FPS del GIF:")
        self.label_fps.pack()

        self.entry_fps = tk.Entry(self.tab2)
        self.entry_fps.pack()

        self.label_info = tk.Label(self.tab2, text="")
        self.label_info.pack()

        self.button_convertir = tk.Button(self.tab2, text="Convertir a GIF", command=self.convertir_a_gif)
        self.button_convertir.pack()

        self.video_path = None
        self.gif_path = None
        self.area_selected = None

        self.notebook.pack(expand=1, fill="both")

        self.area_selected_event = threading.Event()

    def seleccionar_video(self):
        video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.mov;*.mkv")])
        self.label_input.config(text=f"Seleccionar Video: {video_path}")
        self.video_path = video_path
        
    def seleccionar_salida(self):
        gif_path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF Files", "*.gif")])
        self.label_output.config(text=f"Guardar GIF en: {gif_path}")
        self.gif_path = gif_path
        
    def convertir_a_gif(self):
        try:
            duracion_segundos = float(self.entry_duracion.get())
            fps = float(self.entry_fps.get())
            inicio_segundos = float(self.entry_inicio.get())

            RecordHelpers.convertir_video_a_gif(RecordHelpers, self.video_path, self.gif_path, duracion_segundos, fps, inicio_segundos)

            self.label_info.config(text="El GIF se ha creado con éxito.")

        except Exception as e:
            self.label_info.config(text=f"Error: {str(e)}")

    def iniciar_grabacion(self):
        if not RecordHelpers.isRecordingDisplay:
            RecordHelpers.isRecordingDisplay = True
            self.button_screen_record.config(text="Grabación en curso", state=tk.DISABLED)
            self.button_stop_record.config(state=tk.NORMAL)
            self.button_select_area.config(state=tk.DISABLED)
            self.button_deselect_area.config(state=tk.DISABLED)

            RecordHelpers.isRecordingDisplay = True
            threading.Thread(target=RecordHelpers.grabar_pantalla_a_gif, args=(self.gif_path, self.area_selected),).start()
        else:
            self.label_info.config(text="Ya se está grabando. Detén la grabación actual antes de iniciar una nueva.")

    def detener_grabacion(self):
        if RecordHelpers.isRecordingDisplay:
            RecordHelpers.isRecordingDisplay = False
            self.button_screen_record.config(text="Iniciar Grabación", state=tk.NORMAL)
            self.button_stop_record.config(state=tk.DISABLED)
            self.button_select_area.config(state=tk.NORMAL)
            self.button_deselect_area.config(state=tk.NORMAL)

            RecordHelpers.isRecordingDisplay = False
            self.label_info.config(text="La grabación de pantalla se ha creado con éxito.")
        else:
            self.label_info.config(text="No hay grabación en curso para detener.")
        
    def seleccionar_area(self):
        self.label_info.config(text="Selecciona un área en la pantalla.")
        area_seleccionada = AreaSelection(self.master, self.guardar_area_seleccionada, self.area_selected_event)
        area_seleccionada.wait_window()
        
    def deseleccionar_area(self):
        self.area_selected = None

    def guardar_area_seleccionada(self, x1, y1, x2, y2):
        self.area_selected = (x1, y1, x2, y2)
        self.label_info.config(text=f"Área seleccionada: {self.area_selected}")
        self.area_selected_event.set()

if __name__ == "__main__":
    root = tk.Tk()
    app = GIFMaker(root)
    root.mainloop()
