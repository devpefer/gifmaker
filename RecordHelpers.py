from datetime import datetime
import pyautogui
import os
from moviepy.editor import VideoFileClip

class RecordHelpers:
    isRecordingDisplay = False
        
    def grabar_pantalla_a_gif(output_path, area=None):
        screenshot_list = []
        fps = 30
        
        regionToCapture = None
        if (area != None ):
            regionToCapture = (int(area[0]), int(area[1]), int(area[2] - area[0]), int(area[3] - area[1]))

        startDateTime: datetime = datetime.now()
        
        while(RecordHelpers.isRecordingDisplay):
            screenshot = pyautogui.screenshot(region=regionToCapture)
            screenshot_list.append(screenshot)

        endDateTime: datetime = datetime.now()
        
        duration = (endDateTime - startDateTime).total_seconds()
        
        screenshot_list[0].save(output_path, save_all=True, append_images=screenshot_list[1:], duration=duration / fps, loop=0)
            
    def convertir_video_a_gif(self, video_path, gif_path, duracion_segundos, fps, inicio_segundos):
            if video_path.lower().endswith(('.mov', '.mov')):
                nuevo_video_path = video_path[:-4] + "_converted.mp4"
                video_clip = VideoFileClip(video_path)
                video_clip.write_videofile(nuevo_video_path, codec="libx264", audio_codec="aac")
                video_path = nuevo_video_path

            if video_path.lower().endswith('.mkv'):
                nuevo_video_path = video_path[:-4] + "_converted.mp4"
                os.system(f'ffmpeg -i "{video_path}" -codec:v libx264 -codec:a aac -strict experimental -b:a 192k -shortest "{nuevo_video_path}"')
                video_path = nuevo_video_path

            video_clip = VideoFileClip(video_path)

            if duracion_segundos:
                video_clip = video_clip.subclip(inicio_segundos, inicio_segundos + duracion_segundos)

            video_clip.write_gif(gif_path, fps=fps)