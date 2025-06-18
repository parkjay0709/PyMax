import pygame.image
import pygame.transform
import pygame, math, time, os
from VideoPlayer import *
from PIL import Image, ImageFilter, ImageEnhance
from decimal import Decimal

pygame.init()
pygame.mixer.init()
w = 1200
h = w * (9/16)

# class VideoPlayer :
#     def __init__(self, path, size, screen):
#         self.cap = cv2.VideoCapture(path)
#         self.size = (int(size[0]), int(size[1]))
#         self.screen = screen
#         self.clock = pygame.time.Clock()

#         self.fps = int( self.cap.get( cv2.CAP_PROP_FPS ) )
#         if self.fps == 0:
#             self.fps = 120

#     def play(self):

#         ret, frame = self.cap.read()
#         if not ret:
#             self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             ret, frame = self.cap.read()

#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         frame = cv2.flip(frame, 1)
#         frame = cv2.resize(frame, self.size)
#         frame_surface = pygame.surfarray.make_surface(np.rot90(frame))
#         self.screen.blit(frame_surface, (0, 0))

#         self.clock.tick(self.fps)

#     def restart(self):
#         self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

#     def release(self):
#         self.cap.release()

flag = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.HWACCEL | pygame.NOFRAME
#pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.HWACCEL | 
screen = pygame.display.set_mode((w, h), flag)  # | pygame.FULLSCREEN 
alpha_display = pygame.Surface((w, h), flag)
alpha_display2 = pygame.Surface((w, h), flag | pygame.SRCALPHA)
alpha_display3 = pygame.Surface((w, h), flag)
pygame.display.init()

clock = pygame.time.Clock()

main = True
ingame = True
result_mode = False
PlayVideo = False

keys = [0, 0, 0, 0]
keyset = [0, 0, 0, 0]

maxframe = 60
fps = 0

gst = time.time()
Time = time.time() - gst

ty = 0
tst = Time

t1 = []
t2 = []
t3 = []
t4 = []

gear_num = 1

Cpath = os.path.dirname(__file__)
Fpath = os.path.join(Cpath, "font")
Spath = os.path.join(Cpath, "song")
Dpath = os.path.join(Cpath, "note")
#imgs================================
Ipath = os.path.join(Cpath, "img")
BGpath = os.path.join(Ipath, "bg")
BGVpath = "D:\\Python\\WorkSpace\\Project\\img\\bg\\"
GEARpath = os.path.join(Ipath, "gear" + str(gear_num))

rate = "READY"

ingame_font_rate = pygame.font.Font(os.path.join(Fpath, "2.ttf"), int(w / 23))
rate_text = ingame_font_rate.render(str(rate), False, (255, 255, 255))
speed = 2.8

combo = 0
combo_effect = 0
combo_effect2 = 0
miss_anim = 0
last_combo = 0

combo_time = Time + 2

rate_data = [0, 0, 0, 0]

effect_key = [0,0,0,0]
effect_key_size = [13,13,13,13]

score = 0

score_font = pygame.font.Font(os.path.join(Fpath, "3.ttf"), int(w / 130))

fever = 1

fever_gauge = 0

fever_gauge_smooth = 0

fever_anim = 0
fever_anim2 = 0

fever_anim_cool = 0

def rating(n):
  global combo, miss_anim, last_combo, combo_effect, combo_effect2, combo_time, rate, score, fever_gauge

  if note_count == 0:
        return
  
  if abs(Time - rate_data[n - 1]) < 240 / bpm / 5 and abs(Time - rate_data[n - 1]) >= 240 / bpm / 8:
    last_combo = combo
    miss_anim = 1
    combo = 0 
    combo_effect = 0.2
    combo_time = Time + 1
    combo_effect2 = 1.3
    rate = "WORST"
    score += (100000 / note_count) * 0.2
  if abs(Time - rate_data[n - 1]) < 240 / bpm / 8 and abs(Time - rate_data[n - 1]) >= 240 / bpm / 12:
    last_combo = combo
    miss_anim = 1
    combo = 0 
    combo_effect = 0.2
    combo_time = Time + 1
    combo_effect2 = 1.3
    rate = "BAD"
    score += (100000 / note_count) * 0.4
  if abs(Time - rate_data[n - 1]) < 240 / bpm / 12 and abs(Time - rate_data[n - 1]) >= 240 / bpm / 24:
    combo_effect = 0.2
    combo_time = Time + 1
    combo_effect2 = 1.3
    rate = "GOOD"
    combo += 1 * fever
    effect_key[n - 1] = 0
    effect_key_size[n - 1] = 33
    score += (100000 / note_count) * 0.7
    fever_gauge += 1
  if abs(Time - rate_data[n - 1]) < 240 / bpm / 24 and abs(Time - rate_data[n - 1]) >= 240 / bpm / 32:
    combo_effect = 0.2
    combo_time = Time + 1
    combo_effect2 = 1.3
    rate = "GREAT"
    combo += 1 * fever
    effect_key[n - 1] = 0
    effect_key_size[n - 1] = 24
    score += (100000 / note_count) * 0.9
    fever_gauge += 1
  if abs(Time - rate_data[n - 1]) < 240 / bpm / 32 and abs(Time - rate_data[n - 1]) >= 0:
    combo_effect = 0.2
    combo_time = Time + 1
    combo_effect2 = 1.3
    rate = "PERFECT"
    combo += 1 * fever
    effect_key[n - 1] = 0
    effect_key_size[n - 1] = 13
    score += (100000 / note_count) * 1
    fever_gauge += 1

song_play = 0

check = True

load = False

song_num = 0

#songloading===========================================================================================

loading_font = pygame.font.Font( os.path.join( Fpath, "3.ttf" ), int( w / 30 ))

load_message = loading_font.render( "loading image", False, ( 255, 255, 255 ))

screen.blit( load_message, ( w / 2 - load_message.get_width() / 2, h / 2 - load_message.get_height() / 2 ))

pygame.display.flip()

def pilImageToSurface( pilImage ):
  return pygame.image.frombuffer(
    pilImage.tobytes(), pilImage.size, pilImage.mode ).convert()

song_data = [
  [ "PUPA", 911, 202,pygame.image.load( os.path.join( BGpath, "PUPA.jpg" ))],
  #["light it up", 911, 202,pygame.image.load(os.path.join(BGpath, "light it up.jpg"))],
  #["nacreous snowmelt", 911, 202,pygame.image.load(os.path.join(BGpath, "nacreous snowmelt.jpg"))],
  [ "MANITO", 911, 180, pygame.image.load( os.path.join( BGpath, "MANITO.jpg" ))],
  [ "Odysseus", 911, 180, pygame.image.load( os.path.join( BGpath, "Odysseus.jpg" ))],
  [ "Hell'o", 911, 180, pygame.image.load( os.path.join( BGpath, "Hell'o.jpg" ))],
  [ "Dear", 911, 180, pygame.image.load( os.path.join( BGpath, "Dear.jpg" ))],
  [ "IDOL", 911, 180, pygame.image.load( os.path.join( BGpath, "IDOL.jpg" ))],
] # name, line, bpm
song_name = song_data[ song_num ][ 0 ]

def load_img():
  global data, song, note, bg, gear_line, gear_under, gear_deco, rate_line, p_key, key_imgs, effect_imgs, fever_deco_r, fever_deco_l, fever_bg, PlayVideo
  song_name = song_data[ song_num ][ 0 ]

  data = open( os.path.join( Dpath, str( song_name ) + ".txt" ), "r" )

  note = pygame.image.load( os.path.join( GEARpath, "NOTE1.png" ))
  note = pygame.transform.smoothscale( note, ( w / 20, w / 65 )).convert()

  bg = pygame.image.load( os.path.join( BGpath, str( song_name ) + ".jpg" ))
  bg = pygame.transform.smoothscale( bg, ( w, h ))

  fever_bg = pygame.image.load( os.path.join( GEARpath, "BG.png" ))
  fever_bg = pygame.transform.smoothscale( fever_bg, ( w / 4, h ))
  #fever_bg.set_colorkey((255, 255, 255))

  gear_line = pygame.image.load(os.path.join(GEARpath, "GEAR1.png")).convert()
  gear_line = pygame.transform.smoothscale(gear_line, (w / 4, h))
  gear_line.set_colorkey((0, 0, 0))

  gear_under = pygame.image.load(os.path.join(GEARpath, "GEAR2.png")).convert()
  gear_under = pygame.transform.smoothscale(gear_under, (w / 4, h))
  gear_under.set_colorkey((0, 0, 0))

  gear_deco = pygame.image.load(os.path.join(GEARpath, "GEAR3.png"))
  gear_deco = pygame.transform.smoothscale(gear_deco, (w / 9, w / 18))

  rate_line = pygame.image.load(os.path.join(GEARpath, "RATE_LINE.png"))
  rate_line = pygame.transform.smoothscale(rate_line, (w / 5, w / 40)).convert_alpha()


  p_key = pygame.image.load(os.path.join(GEARpath, "KEY.png"))
  p_key = pygame.transform.smoothscale(p_key, (w / 18, w / 18.2))

  fever_deco_r = pygame.image.load(os.path.join(GEARpath, "fever_R_1.png"))
  fever_deco_r = pygame.transform.smoothscale(fever_deco_r, (w / 35, w / 1.5))

  fever_deco_l = pygame.image.load(os.path.join(GEARpath, "fever_L_1.png"))
  fever_deco_l = pygame.transform.smoothscale(fever_deco_l, (w / 35, w / 1.5))

  key_imgs = [
    pygame.image.load(os.path.join(GEARpath, "KEY.png")),
    pygame.image.load(os.path.join(GEARpath, "key_anim1.png")),
    pygame.image.load(os.path.join(GEARpath, "key_anim2.png")),
    pygame.image.load(os.path.join(GEARpath, "key_anim3.png")),
    pygame.image.load(os.path.join(GEARpath, "key_anim4.png")),
    pygame.image.load(os.path.join(GEARpath, "key_anim5.png")),
    pygame.image.load(os.path.join(GEARpath, "key_anim6.png")),
    pygame.image.load(os.path.join(GEARpath, "key_anim7.png")),
    pygame.image.load(os.path.join(GEARpath, "key_anim8.png")),
    pygame.image.load(os.path.join(GEARpath, "key_anim9.png")),
    pygame.image.load(os.path.join(GEARpath, "key_anim10.png")),
    pygame.image.load(os.path.join(GEARpath, "key_anim11.png")),
  ]

  effect_imgs = [
    pygame.transform.scale(pygame.image.load(os.path.join(GEARpath, "effect1.png")), (w / 15, w / 15)),
    pygame.transform.scale(pygame.image.load(os.path.join(GEARpath, "effect2.png")), (w / 15, w / 15)),
    pygame.transform.scale(pygame.image.load(os.path.join(GEARpath, "effect3.png")), (w / 15, w / 15)),
    pygame.transform.scale(pygame.image.load(os.path.join(GEARpath, "effect4.png")), (w / 15, w / 15)),
    pygame.transform.scale(pygame.image.load(os.path.join(GEARpath, "effect5.png")), (w / 15, w / 15))
  ]

def load_note_data():
  data_list.clear()
  speed_list.clear()
  with open(data, "r") as f:
      for line in f:
          try:
            if line.strip() == "" or not line[0].isdigit():
              continue
            data_list.append([line[0:4], float(line[5:8]), float(line[9:12])])
            speed_list.append([float(line[5:8]), float(line[13:16])])
          except ValueError as e:
            print(f"Parsing error: {e}")

load_img()

anim = 0

anim2 = 0
anim2p = 0

anim3 = 0

data_list = []

linec = 0


ms = 5

def sum_note(n, t):
  if n == 1:
    ty = 0
    #tst = Time + 2 + t
    tst = t + 2 + (ms / 1000)
    t1.append([ty, tst])
  if n == 2:
    ty = 0
    #tst = Time + 2 + t
    tst = t + 2 + (ms / 1000)
    t2.append([ty, tst])
  if n == 3:
    ty = 0
    #tst = Time + 2 + t
    tst = t + 2 + (ms / 1000)
    t3.append([ty, tst])
  if n == 4:
    ty = 0
    #tst = Time + 2 + t
    tst = t + 2 + (ms / 1000)
    t4.append([ty, tst])

speed_list = []


song_start_time = 0
note_start_time = 0
bpm = 0

notes = 0 
notess = 0 

speeds = 0
speedss = 0

sst = 0 


angle = 0
angz = 1
angt = 1

key_press_anim = [0, 0, 0, 0]


pygame.event.set_blocked([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.MOUSEWHEEL])
pygame.event.set_allowed([pygame.QUIT, pygame.KEYUP, pygame.KEYDOWN])
speed_set = 2

lobby = True

lobby_select_anim = 0

lobby_font_chart = pygame.font.Font(os.path.join(Fpath, "3.ttf"), int(w / 70))

song_num_anim = 0

bg_blurs = []
bgv_blurs = []

for i in range(0, len(song_data)):
  bg_blur = Image.open(os.path.join(BGpath, str(song_data[i][0]) + ".jpg"))
  bgv_blur = VideoPlayer(BGVpath + str(song_data[i][0]) + ".mp4", (w, h), screen )
  bg_blur = bg_blur.filter(ImageFilter.GaussianBlur(4))
  bg_br = ImageEnhance.Brightness(bg_blur)
  bg_blur = bg_br.enhance(0.3)
  bg_blur = pilImageToSurface(bg_blur)
  bg_blur = pygame.transform.scale(bg_blur, (w, h))
  bg_blurs.append(bg_blur)
  bgv_blurs.append(bgv_blur)

songs = []

load_message = loading_font.render("loading songs", False, (255, 255, 255))

screen.fill((0, 0, 0))
screen.set_colorkey((0, 0, 0))
screen.blit(load_message, (w / 2 - load_message.get_width() / 2, h / 2 - load_message.get_height() / 2))

pygame.display.flip()

song_long = []
#'''
for i in range(0, len(song_data)):
  s = pygame.mixer.Sound(os.path.join(Spath, str(song_data[i][0]) + ".mp3"))

  songs.append(s)
  #song_long.append(s_l)
#'''
note_lenght = 0

note_count = 0

perfect_bpms = [60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 720, 780, 840, 900, 960, 1020, 1080]

dfdf = 0

end_time = 0

end_check = 0

while main:
  while lobby:
    for event in pygame.event.get():
      if event.type == pygame.quit:
        load = False
        ingame = False
        main = False
        lobby = False
        pygame.quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_DOWN:
          songs[song_num].stop()
          song_num += 1
          if song_num > len(song_data) - 1:
            song_num = len(song_data) - 1
          song_name = song_data[song_num][0]
          bg = song_data[song_num][3]
          bgv_blurs[song_num].restart()
          songs[song_num].play()
          lobby_select_anim = -25
        
        if event.key == pygame.K_UP:
          songs[song_num].stop()
          song_num -= 1
          if song_num < 0:
            song_num = 0
            song_name = song_data[song_num][0]
          bg = song_data[song_num][3]
          bgv_blurs[song_num].restart()
          songs[song_num].play()
          lobby_select_anim = -25
        if event.key == pygame.K_SPACE:
          bgv_blurs[song_num].restart()
          songs[song_num].stop()
          song_name = song_data[song_num][0]
          lobby = False
          load = True
          ingame = True
          song_name = song_data[song_num][0]
          data = open(os.path.join(Dpath, str(song_name) + ".txt"), "r")
          song = songs[song_num]
          song.set_volume(0.3)

    #bg_blur = bg_blurs[song_num]
    #screen.blit(bg_blur, (0, 0))

    bgv_blurs[song_num].play()
    #pygame.display.update()

    #alpha_display.set_alpha(170)
    #alpha_display.fill((0, 0, 0))
    #pygame.draw.rect(alpha_display, (0, 0, 0), (0, 0, w / 4, h / 4))
    #screen.blit(alpha_display, (0, 0))

    #bg_resize = pygame.transform.smoothscale(bg, (w / 2.3, h / 2.3))
    #screen.blit(bg_resize, (w / 4 - bg_resize.get_width() / 2 + (lobby_select_anim * (h / 900)), h / 4 - bg_resize.get_height() / 2))


    for songdata in song_data:
      a = song_data.index(songdata)

      #alpha_display2.set_alpha(230)

      if song_num == a:
        data_text = lobby_font_chart.render(str(song_data[a][0]), False, (255, 255, 255))
      else:
        data_text = lobby_font_chart.render(str(song_data[a][0]), False, (120, 120, 120))
      alpha_display2.fill((0, 0, 0, 0))
      pygame.draw.line(alpha_display2, (0, 0, 0, 125), (w / 2 + w / 17, h / 4 + (h / 12) * a - ((h / 12) * song_num_anim)), (w, h / 4 + (h / 12) * a - ((h / 12) * song_num_anim)), int(h / 20))
      screen.blit(alpha_display2, (0, 0))
      screen.blit(data_text, (w / 2 + w / 15, h / 4 + (h / 12) * a - data_text.get_height() / 2 - ((h / 12) * song_num_anim)))

    if fps == 0:
      fps = 30

    lobby_select_anim += (0 - lobby_select_anim) / (12 / (60 / fps))

    song_num_anim += (song_num - song_num_anim) / (7 / (60 / fps))

    pygame.display.update((0, 0, w, h))

    #'''
    fps = clock.get_fps()

    pygame.display.set_caption(str(fps))


    clock.tick(30)
    #'''
  while check:

    pygame.draw.rect(screen, (0, 0, 0), (0, (h / 900) * 600, w, h / 6))
    pygame.draw.rect(screen, (255, 255, 255), (0, (h / 900) * 675 - (h / 72), (w / song_data[song_num][1]) * linec, h / 36))
    pygame.display.flip()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        check = False
        ingame = False
        main = False
        pygame.quit()

    line = data.readline()

    if not line:
      gst = time.time()
      combo_time = Time + 1 + (note_start_time - 1)
      screen.fill((0, 0, 0))
      bg_resize = pygame.transform.smoothscale(bg_blurs[song_num], (w, h))
      #bgv_resize = pygame.transform.smoothscale(bgv_blurs[song_num], (w, h))
      screen.blit(bg_resize, (0, 0))
      check = False
      ingame = False
      load = True
      #error_lenght = notess - song_long[song_num]
      linec = 0
      data_list.clear()
      speed_list.clear()
      song_start_time = 0
      note_start_time = 0
      data.close()
      data = open(os.path.join(Dpath, str(song_name) + ".txt"), "r")
      #print(error_lenght)
      break

    linec += 1
    if linec == 2:
      song_start_time = line[11:17]
      song_start_time = float(Decimal(str(song_start_time)))
    if linec == 1:
      note_start_time = line[11:17]
      note_start_time = float(Decimal(str(note_start_time)))
      screen.fill((0, 0, 0))
      bg_resize = pygame.transform.smoothscale(bg, (w, h))
      screen.blit(bg_resize, (0, 0))
    if linec == 3:
      bpm = line[11:17]
      obpm = float(bpm)
      #bpm = float(Decimal(str(bpm))) + (obpm / (202 / 0.128))
      bpm = float(Decimal(str(bpm)))
      #bpm = obpm
      notess = note_start_time
      speedss = note_start_time + 2
    if linec > 3:
      data_list.append([line[0:4], float(line[5:8]), float(line[9:12])])
      speed_list.append([float(line[5:8]), float(line[13:16])])

      if not data_list[0][2] == 0:
        bpm = float(Decimal(str(data_list[0][2])))
        obpm = float(bpm)
        #bpm = float(Decimal(str(data_list[0][2]))) + (obpm / (202 / 0.128))
        #bpm = obpm
      if "1" in data_list[0][0]:
        note_count += 1
      if "2" in data_list[0][0]:
        note_count += 1
      if "3" in data_list[0][0]:
        note_count += 1
      if "4" in data_list[0][0]:
        note_count += 1
    
      notes = 240 / bpm / data_list[0][1]
      notess += notes
      del data_list[0]

    fps = clock.get_fps()

    clock.tick(maxframe * 8)

    
  while load:

    load

    pygame.draw.rect(screen, (0, 0, 0), (0, (h / 900) * 600, w, h / 6))
    pygame.draw.rect(screen, (255, 255, 255), (0, (h / 900) * 675 - (h / 72), (w / song_data[song_num][1]) * linec, h / 36))
    pygame.display.flip()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        load = False
        ingame = False
        main = False
        pygame.quit()

    line = data.readline()

    if not line:
      combo_time = Time + 1 + (note_start_time - 1)
      screen.fill((0, 0, 0))
      bg_resize = pygame.transform.smoothscale(bg_blurs[song_num], (w, h))
      screen.blit(bg_resize, (0, 0))
      load = False
      ingame = True
      gst = time.time()
      
      break

    linec += 1
    if linec == 2:
      song_start_time = line[11:17]
      song_start_time = float(Decimal(str(song_start_time)))
    if linec == 1:
      note_start_time = line[11:17]
      note_start_time = float(Decimal(str(note_start_time)))
      screen.fill((0, 0, 0))
      bg_resize = pygame.transform.smoothscale(bg, (w, h))
      screen.blit(bg_resize, (0, 0))
    if linec == 3:
      bpm = line[11:17]
      obpm = float(bpm)
      #bpm = float(Decimal(str(bpm))) + (obpm / (202 / 0.128))
      bpm = float(Decimal(str(bpm)))
      #bpm = obpm
      notess = note_start_time
      speedss = note_start_time + 2
    if linec > 3:
      try:
        data_list.append([line[0:4], float(line[5:8]), float(line[9:12])])
        speed_list.append([float(line[5:8]), float(line[13:16])])
      except ValueError as e:
        print(f"Parsing error: {e}")
      try :
        if not data_list[0][2] == 0:
          bpm = float(Decimal(str(data_list[0][2])))
          obpm = float(bpm)
          #bpm = float(Decimal(str(data_list[0][2]))) + (obpm / (202 / 0.128))
          #bpm = obpm
        if "1" in data_list[0][0]:
          sum_note(1, notess)
        if "2" in data_list[0][0]:
          sum_note(2, notess)
        if "3" in data_list[0][0]:
          sum_note(3, notess)
        if "4" in data_list[0][0]:
          sum_note(4, notess)
        if not bpm in perfect_bpms:
          notes = 240 / bpm / data_list[0][1]
        else:
          notes = 240 / bpm / data_list[0][1] - (240 / bpm / data_list[0][1]) / 98 * (12 / data_list[0][1])
        notess += notes
        del data_list[0]
      except IndexError as e :
        print( e )

    fps = clock.get_fps()

    clock.tick(maxframe * 8)

  while ingame == True:
    
    fps = clock.get_fps()
    Time = float(Decimal(str(time.time() - gst)))

    if song_play == 0 and song_start_time < Time:
      PlayVideo = True
      song.play()
      sst = Time - (song_start_time)
      song_play = 1

    if len(t1) > 0:
      rate_data[0] = t1[0][1]
    if len(t2) > 0:
      rate_data[1] = t2[0][1]
    if len(t3) > 0:
      rate_data[2] = t3[0][1]
    if len(t4) > 0:
      rate_data[3] = t4[0][1]

    if Time > speedss and len(speed_list) > 0:
      if not speed_list[0][1] == 0:
        speed_set = speed_list[0][1]
      speeds = float(Decimal(str((60 / bpm) / (speed_list[0][0] / 4))))
      speedss += speeds
      del speed_list[0]

    try:
      ingame_font_combo = pygame.font.Font(os.path.join(Fpath, "3.ttf"), int((w / 80) * combo_effect2))
      combo_text = ingame_font_combo.render(str(combo), False, (0, 255, 70))

      fever_font = pygame.font.Font(os.path.join(Fpath, "3.ttf"), int((w / 240) * combo_effect2))
      fever_text = fever_font.render("x" + str(fever), False, (0, 255, 70))

      rate_text = ingame_font_rate.render(str(rate), False, (255, 255, 255))
      rate_text = pygame.transform.scale(rate_text, (int(w / 110 * len(rate) * combo_effect2), int((w / 90 * combo_effect * combo_effect2))))

      ingame_font_miss = pygame.font.Font(os.path.join(Fpath, "3.ttf"), int((w / 80 * miss_anim)))
      miss_text = ingame_font_miss.render(str(last_combo), False, (255, 0, 0))
    except ValueError:
      pass

    if fps == 0:
      fps = maxframe

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        load = False
        ingame = False
        main = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          lobby = False
          main = False
          ingame = False
        if event.key == pygame.K_SPACE:
          data_list.clear()
          speed_list.clear()
          t1.clear()
          t2.clear()
          t3.clear()
          t4.clear()
          notess = 0
          note_count = 0
          fever = 1
          fever_gauge = 0
          fever_anim = 0
          fever_anim2 = 0
          PlayVideo = False
          song_play = 0
          song.stop()
          song.play()
          bgv_blurs[song_num].restart()
          gst = time.time()
          linec = 0
          data = open(os.path.join(Dpath, str(song_name) + ".txt"), "r")
          ingame = False
          lobby = True
          main = True
          load = True
        if event.key == pygame.K_q:
          keyset[0] = 1
          if len(t1) > 0:
            if abs(Time - rate_data[0]) < 240 / bpm / 5:
              rating(1)
              del t1[0]
        if event.key == pygame.K_w:
          keyset[1] = 1
          if len(t2) > 0:
            if abs(Time - rate_data[1]) < 240 / bpm / 5:
              rating(2)
              del t2[0]
        if event.key == pygame.K_o:
          keyset[2] = 1
          if len(t3) > 0:
            if abs(Time - rate_data[2]) < 240 / bpm / 5:
              rating(3)
              del t3[0]
        if event.key == pygame.K_p:
          keyset[3] = 1
          if len(t4) > 0:
            if abs(Time - rate_data[3]) < 240 / bpm / 5:
              rating(4)
              del t4[0]
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_q:
          keyset[0] = 0
          key_press_anim[0] = 0
        if event.key == pygame.K_w:
          keyset[1] = 0
          key_press_anim[1] = 0
        if event.key == pygame.K_o:
          keyset[2] = 0
          key_press_anim[2] = 0
        if event.key == pygame.K_p:
          keyset[3] = 0
          key_press_anim[3] = 0
    
  #gear===========================================================================================================

    #screen.fill((0, 0, 0))

    screen.blit(bg_resize, (0, 0))

    if PlayVideo == True :
      bgv_blurs[song_num].play()
      #pygame.display.update()

    alpha_display.set_alpha(170)
    alpha_display.fill((0, 0, 0))

    #screen.blit(alpha_display, (0, 0))

    keys[0] += (keyset[0] - keys[0]) / (3 / (60 / fps))
    keys[1] += (keyset[1] - keys[1]) / (3 / (60 / fps))
    keys[2] += (keyset[2] - keys[2]) / (3 / (60 / fps))
    keys[3] += (keyset[3] - keys[3]) / (3 / (60 / fps))

    #speed += (speed_set - speed) / (6 / (60 / fps))

    if keyset[0] == 1:
      key_press_anim[0] += (11.9 - key_press_anim[0]) / (3.5 / (60 / fps))
    if keyset[1] == 1:
      key_press_anim[1] += (11.9 - key_press_anim[1]) / (3.5 / (60 / fps))
    if keyset[2] == 1:
      key_press_anim[2] += (11.9 - key_press_anim[2]) / (3.5 / (60 / fps))
    if keyset[3] == 1:
      key_press_anim[3] += (11.9 - key_press_anim[3]) / (3.5 / (60 / fps))


    #text_anim===================================================================


    if not len(t1) + len(t2) + len(t3) + len(t4) == 0:
      anim += (1 - anim) / (17 / (60 / fps))
      if Time > combo_time:
        combo_effect += (0 - combo_effect) / (7 / (60 / fps))
      if Time < combo_time:
        combo_effect += (1 - combo_effect) / (7 / (60 / fps))
      end_time = Time

      combo_effect2 += (2 - combo_effect2) / (7 / (60 / fps))
    if Time - end_time > 1.5:
      anim += (0 - anim) / (17 / (60 / fps))
      combo_effect += (0 - combo_effect) / (7 / (60 / fps))
      combo_effect2 += (0 - combo_effect2) / (7 / (60 / fps))
    if anim > 0.97:
      anim3 += (1 - anim3) / (17 / (60 / fps))
    else:
      anim3 += (0 - anim3) / (17 / (60 / fps))
    miss_anim += (4 - miss_anim) / (14 / (60 / fps))

    fever_r = pygame.transform.smoothscale(fever_deco_r, ((w / 25), (w / 3) * fever_anim))
    fever_l = pygame.transform.smoothscale(fever_deco_l, ((w / 25), (w / 3) * fever_anim))

    screen.blit(fever_r, (w / 2 + (w / 7) * fever_anim - fever_r.get_width() / 2, h / 2 - fever_l.get_height() / 2))
    screen.blit(fever_l, (w / 2 - (w / 7) * fever_anim - fever_l.get_width() / 2, h / 2 - fever_l.get_height() / 2))

    pygame.draw.rect(screen, (30, 30, 30), (w / 2 - (w / 8.8) * anim, 0, (w / 4.4) * anim, h))
    pygame.draw.rect(screen, (0, 50, 0), (w / 2 - (w / 8.8) * fever_anim * anim, 0, (w / 4.4) * fever_anim * anim, h * fever_anim))
    f_bg = pygame.transform.smoothscale(fever_bg, (int((w / 4.4) * anim), h))
    # f_bg.set_colorkey((255, 255, 255))
    screen.blit(f_bg, (w / 2 - f_bg.get_width() / 2, 0))
    # rateline=====================================================================================
    
    rate_l = pygame.transform.smoothscale(rate_line, ((int((w / 4.4) * anim), w / 30)))
    screen.blit(rate_l, (w / 2 - rate_l.get_width() / 2, (h / 24) * 17 - (rate_l.get_height() / 2)))
    # key fx===========================================================================================================
    
    '''

    for i in range(7):
      i += 1
      pygame.draw.rect(screen, (0, 150 - (50 / 7) * i, 255 - ((200 / 7) * i)), (w / 2 - w / 8 + w / 32 - (w / 32) * keys[0], (h / 24) * 16 - (h / 30) * keys[0] * i, w / 16 * keys[0], (h / 35) / i))
    for i in range(7):
      i += 1
      pygame.draw.rect(screen, (0, 150 - (50 / 7) * i, 255 - ((200 / 7) * i)), (w / 2 - w / 16 + w / 32 - (w / 32) * keys[1], (h / 24) * 16 - (h / 30) * keys[1] * i, w / 16 * keys[1], (h / 35) / i))
    for i in range(7):
      i += 1
      pygame.draw.rect(screen, (0, 150 - (50 / 7) * i, 255 - ((200 / 7) * i)), (w / 2 + w / 32 - (w / 32) * keys[2], (h / 24) * 16 - (h / 30) * keys[2] * i, w / 16 * keys[2], (h / 35) / i))
    for i in range(7):
      i += 1
      pygame.draw.rect(screen, (0, 150 - (50 / 7) * i, 255 - ((200 / 7) * i)), (w / 2 + w / 16 + w / 32 - (w / 32) * keys[3], (h / 24) * 16 - (h / 30) * keys[3] * i, w / 16 * keys[3], (h / 35) / i))

    '''

    # note============================================================================================================================
    for tile_data in t1:
      tile_data[0] = ((h / 24) * 17) + (Time + sst - tile_data[1]) * 350 * speed * (h / 900)
      if tile_data[0] + note.get_height() > 0:
        screen.blit(note, (w / 2 - w / 10, tile_data[0] - note.get_height() / 2))
      if tile_data[0] > h - (h / 9):
        last_combo = combo
        miss_anim = 1
        combo = 0 
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "MISS"
        t1.remove(tile_data)

    for tile_data in t2:
      tile_data[0] = ((h / 24) * 17) + (Time + sst - tile_data[1]) * 350 * speed * (h / 900)
      if tile_data[0] + note.get_height() > 0:
        screen.blit(note, (w / 2 - w / 20, tile_data[0] - note.get_height() / 2))
      if tile_data[0] > h - (h / 9):
        last_combo = combo
        miss_anim = 1
        combo = 0 
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "MISS"
        t2.remove(tile_data)

    for tile_data in t3:
      tile_data[0] = ((h / 24) * 17) + (Time + sst - tile_data[1]) * 350 * speed * (h / 900)
      if tile_data[0] + note.get_height() > 0:
        screen.blit(note, (w / 2, tile_data[0] - note.get_height() / 2))
      if tile_data[0] > h - (h / 9):
        last_combo = combo
        miss_anim = 1
        combo = 0 
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "MISS"
        t3.remove(tile_data)

    for tile_data in t4:
      tile_data[0] = ((h / 24) * 17) + (Time + sst - tile_data[1]) * 350 * speed * (h / 900)
      if tile_data[0] + note.get_height() > 0:
        screen.blit(note, (w / 2 + w / 20, tile_data[0] - note.get_height() / 2))
      if tile_data[0] > h - (h / 9):
        last_combo = combo
        miss_anim = 1
        combo = 0 
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "MISS"
        t4.remove(tile_data)

    for i in range(0,4):
      effect_key[i] += 0.5
      if effect_key[i] >= 5:
        effect_key[i] = 5

    anim2p += 0.03
    if anim2p > 180:
      anim2p = 0
    anim2 = math.sin(anim2p) / 35
    anim3s = math.sin(anim2p / 2) / 15

    score = round(score)

    score_text_none = score_font.render(str(score), False, (0, 255, 70))

    gear_l = pygame.transform.smoothscale(gear_line, (int((w / 4.4) * anim), h))
    gear_u = pygame.transform.smoothscale(gear_under, (int((w / 1600) * 315 * anim), h))
    gear_d = pygame.transform.smoothscale(gear_deco, (int((w / 9) * anim3), (w / 18)))
    gear_dd = pygame.transform.rotate(gear_d, anim3s * 50)

    score_text = pygame.transform.rotate(score_text_none, anim3s * 50)

    fever_anim += (fever_anim2 - fever_anim) / (22 / (60 / fps))

    screen.blit(gear_l, (w / 2 - gear_l.get_width() / 2, 0))
    screen.blit(gear_u, (w / 2 - gear_u.get_width() / 2, 0))
    if anim3 > 0.3 and anim3 < 0.4 or anim3 > 0.5 and anim3 < 0.6 or anim3 > 0.6 and anim3 < 0.7 or anim3 > 0.8 and anim3 < 0.85 or anim3 > 0.9 and anim3 < 1.1:
      screen.blit(gear_dd, (w / 2 - gear_d.get_width() / 2, (h / 48) * 38 - gear_d.get_height() / 2 + (h / 400) * (anim2 * 100)))
      screen.blit(score_text, (w / 2 - score_text_none.get_width() / 2, (h / 96) * 75.5 - score_text_none.get_height() / 2 + (h / 200) * (anim2 * 100)))

    if not fever_anim2 == 0 and not int((w / 100) - (w / 100) * fever_anim) == 0:
      pygame.draw.circle(screen, (0, 255, 70), (w / 2, h / 2), ((w / 2) * fever_anim), int((w / 100) - (w / 100) * fever_anim))
      pygame.draw.circle(screen, (0, 255, 70), (w / 2, h / 2), ((w) * fever_anim), int((w / 100) - (w / 100) * fever_anim))

    # blinder=========================================================================================================================


    pygame.display.set_caption(str(fps))
    # 2
    try:
      screen.blit(pygame.transform.smoothscale(key_imgs[int(key_press_anim[1])], (w / 18, w / 18.2)), (w / 2 - (w / 29) - p_key.get_width() / 2, (h / 48) * (44 * (2 - anim)) + (h / 48) * (keys[1] / 2) - p_key.get_height() / 2))
    except IndexError:
      pass
    # 3
    try:
      screen.blit(pygame.transform.smoothscale(key_imgs[int(key_press_anim[2])], (w / 18, w / 18.2)), (w / 2 + (w / 29) - p_key.get_width() / 2, (h / 48) * (44 * (2 - anim)) + (h / 48) * (keys[2] / 2) - p_key.get_height() / 2))
    except IndexError:
      pass
    # 1
    try:
      screen.blit(pygame.transform.smoothscale(key_imgs[int(key_press_anim[0])], (w / 18, w / 18.2)), (w / 2 - (w / 15.5) - p_key.get_width() / 2, (h / 96) * (83 * (2 - anim)) + (h / 48) * (keys[0] / 2) - p_key.get_height() / 2))
    except IndexError:
      pass
    # 4
    try:
      screen.blit(pygame.transform.smoothscale(key_imgs[int(key_press_anim[3])], (w / 18, w / 18.2)), (w / 2 + (w / 15.5) - p_key.get_width() / 2, (h / 96) * (83 * (2 - anim)) + (h / 48) * (keys[3] / 2) - p_key.get_height() / 2))
    except IndexError:
      pass
    miss_text.set_alpha(255 - (255 / 4) * miss_anim)

    if not effect_key[1] == 5:
      screen.blit(effect_imgs[int(effect_key[1])], (w / 2 - (w / 33) - effect_imgs[int(effect_key[1])].get_width() / 2, (h / 24) * 17 - effect_imgs[int(effect_key[1])].get_height() / 2))
    if not effect_key[2] == 5:
      screen.blit(effect_imgs[int(effect_key[2])], (w / 2 + (w / 33) - effect_imgs[int(effect_key[2])].get_width() / 2, (h / 24) * 17 - effect_imgs[int(effect_key[2])].get_height() / 2))
    if not effect_key[0] == 5:
      screen.blit(effect_imgs[int(effect_key[0])], (w / 2 - (w / 33) * 2.5 - effect_imgs[int(effect_key[0])].get_width() / 2, (h / 24) * 17 - effect_imgs[int(effect_key[0])].get_height() / 2))
    if not effect_key[3] == 5:
      screen.blit(effect_imgs[int(effect_key[3])], (w / 2 + (w / 33) * 2.5 - effect_imgs[int(effect_key[3])].get_width() / 2, (h / 24) * 17 - effect_imgs[int(effect_key[3])].get_height() / 2))

    if fever_gauge >= 128:
      fever += 1
      fever_gauge = 0
      fever_anim_cool = Time
      fever_anim2 = 1

    if Time - fever_anim_cool > 2:
      fever_anim2 = 0

    fever_gauge_smooth += (fever_gauge - fever_gauge_smooth) / (17 / (60 / fps))

    if fever > 5:
      fever = 5

    pygame.draw.rect(screen, (0, 255, 70), (w / 2 - (w / 30), (h / 3.4), ((w / 15) * (fever_gauge_smooth / 128) * anim), (h / 300)))
    pygame.draw.rect(screen, (0, 255, 70), (w / 2 - (w / 29) * anim, (h / 3.4), (w / 800) * anim, (h / 300)))
    pygame.draw.rect(screen, (0, 255, 70), (w / 2 + (w / 29) - (w / 800) * anim, (h / 3.4), (w / 800) * anim, (h / 300)))

    screen.blit(combo_text, (w / 2 - combo_text.get_width() / 2, (h / 48) * 16 - combo_text.get_height() / 2))
    screen.blit(fever_text, (w / 2 - fever_text.get_width() / 2, (h / 48) * 18 - fever_text.get_height() / 2))
    screen.blit(rate_text, (w / 2 - rate_text.get_width() / 2, (h / 48) * 30 - rate_text.get_height() / 2))
    screen.blit(miss_text, (w / 2 - miss_text.get_width() / 2, (h / 48) * 16 - miss_text.get_height() / 2))

    pygame.display.update((0, 0, w, h))
    #pygame.display.flip()
    
    clock.tick(maxframe)

    if len(t1) == 0 and len(t2) == 0 and len(t3) == 0 and len(t4) == 0:
      delay_duration = 2.0
      
      print(time.time() - delay_start)
      if time.time() - delay_start >= delay_duration:        
        while True :
          for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    data_list.clear()
                    speed_list.clear()
                    note_count = 0
                    notess = 0
                    song.stop()
                    song.play()
                    bgv_blurs[song_num].restart()
                    lobby = True
                    break
  
          screen.fill((0, 0, 0))

          result_font = pygame.font.Font(os.path.join(Fpath, "3.ttf"), int(w / 20))
          score_text = result_font.render(f"Score: {score}", True, (0, 255, 70))
          combo_text = result_font.render(f"Max Combo: {last_combo}", True, (255, 255, 0))
          rate_text = result_font.render(f"Last Rate: {rate}", True, (255, 255, 255))
          info_text = result_font.render("Press SPACE to return", True, (180, 180, 180))

          screen.blit(score_text, (w/2 - score_text.get_width()/2, h/3))
          screen.blit(combo_text, (w/2 - combo_text.get_width()/2, h/3 + 80))
          screen.blit(rate_text, (w/2 - rate_text.get_width()/2, h/3 + 160))
          screen.blit(info_text, (w/2 - info_text.get_width()/2, h - 100))

          pygame.display.flip()
          clock.tick(30)
          ingame = False

pygame.quit()