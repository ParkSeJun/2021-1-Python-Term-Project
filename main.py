from sys import exec_prefix
from tkinter import *
from tkinter import font
import tkinter.ttk
from dhlotto import *
import random
import threading
from cefpython3 import cefpython as cef
import folium
import sys
import smtplib
from email.mime.text import MIMEText

class InputBox:
    answer = None
    answered = False

    def __init__(self):
        pass

    def on_close(self):
        InputBox.answer = 'cancel'
        InputBox.answered = True
        self.root.destroy()
        self.root.quit()

    def commit(self):
        InputBox.answer = self.entry1.get()
        InputBox.answered = True
        self.root.destroy()
        self.root.quit()

    def show(self, label):
        InputBox.answered = False
        InputBox.answer = None

        # creating root
        self.root = Tk()
        
        # specifying geometry
        self.root.geometry('200x100')
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        
        Label(self.root, text=label).pack()
        self.entry1 = Entry(self.root, justify = CENTER)
        
        # focus_force is used to take focus
        # as soon as application starts
        self.entry1.focus_force()
        self.entry1.pack(side = TOP, ipadx = 30, ipady = 6)
        
        save = Button(self.root, text = 'Submit', command = self.commit)
        save.pack(side = TOP, pady = 10)
        
        self.root.mainloop()

class MainGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title('λλ°μΈμ')
        self.window.geometry('600x600')
        self.window.protocol('WM_DELETE_WINDOW', lambda : self.window.destroy())
        self.window.resizable(0, 0)
        self.fonts = dict()
        self.frame3_store_data = None

        self.MakeGui()

        self.window.mainloop()

    def MakeGui(self):
        tkinter.ttk.Style().configure('TNotebook.Tab', font=('','11','bold'), padding=[14, 12] )

        notebook = tkinter.ttk.Notebook(self.window, width=600, height=600)
        notebook.pack(anchor='nw')


        #########################################################################################################################

        # 1νμ΄μ§: μΆμ²¨ κ²°κ³Ό μ‘°ν
        frame1 = Frame(self.window)
        frame1.pack()
        notebook.add(frame1, text='μΆμ²¨ κ²°κ³Ό μ‘°ν', )

        ## μλ¨: μ½€λ³΄λ°μ€μ μ‘°ν λ²νΌ
        frame1_top = Frame(frame1)
        frame1_top.pack(expand=True, fill='both')

        ### μλ¨ μ’μΈ‘: μ½€λ³΄λ°μ€
        frame1_top_left = Frame(frame1_top)
        frame1_top_left.pack(side='left', expand=True, fill='both')

        recent_round = dhlotto.get_recent_round()
        rounds = [x for x in range(recent_round, 0, -1)]
        self.frame1_round = tkinter.ttk.Combobox(frame1_top_left, width=8, justify='center', font=self.get_font(20), values=rounds)
        self.frame1_round.pack(expand=True)
        self.frame1_round.current(0)

        ### μλ¨ μ°μΈ‘: μ‘°ν λ²νΌ
        frame1_top_right = Frame(frame1_top)
        frame1_top_right.pack(side='right', expand=True, fill='both')
        Button(frame1_top_right, text='μ‘°ν', font=self.get_font(20), width=10, command=self.onpress_frame1_query).pack(expand=True)

        
        ## μ€λ¨: λΉμ²¨λ²νΈ μΆλ ₯ Canvas
        frame1_middle = Frame(frame1)
        frame1_middle.pack(expand=True, fill='both')

        self.frame1_canvas = Canvas(frame1_middle, background='#f0f0f0', width=596, height=160)
        self.frame1_canvas.pack(expand=True, fill='both')


        ## νλ¨: λΉμ²¨κ²°κ³Ό μΆλ ₯ Table
        frame1_bottom = Frame(frame1)
        frame1_bottom.pack(expand=False, fill='both')

        self.frame1_table_stringvars = []
        widths = [6, 30, 15, 30]
        height = 2
        Label(frame1_bottom, text='μμ', borderwidth=2, relief='ridge', width=widths[0], height=height).grid(row=0, column=0, padx=[2, 0])
        Label(frame1_bottom, text='μ΄ λΉμ²¨κΈμ‘', borderwidth=2, relief='ridge', width=widths[1], height=height).grid(row=0, column=1)
        Label(frame1_bottom, text='λΉμ²¨κ²μ μ', borderwidth=2, relief='ridge', width=widths[2], height=height).grid(row=0, column=2)
        Label(frame1_bottom, text='1κ²μλΉ λΉμ²¨κΈμ‘', borderwidth=2, relief='ridge', width=widths[3], height=height).grid(row=0, column=3)
        for i in range(5):
            t = [StringVar(), StringVar(), StringVar(), StringVar()]
            for e in t:
                e.set('-')
            _pad_y = [0, 0 if i < 5 - 1 else 5]
            Label(frame1_bottom, textvariable=t[0], borderwidth=2, relief='ridge', width=widths[0], height=height).grid(row=1 + i, column=0, pady=_pad_y, padx=[2, 0])
            Label(frame1_bottom, textvariable=t[1], anchor='e', borderwidth=2, relief='ridge', width=widths[1], height=height).grid(row=1 + i, column=1, pady=_pad_y)
            Label(frame1_bottom, textvariable=t[2], borderwidth=2, relief='ridge', width=widths[2], height=height).grid(row=1 + i, column=2, pady=_pad_y)
            Label(frame1_bottom, textvariable=t[3], anchor='e', borderwidth=2, relief='ridge', width=widths[3], height=height).grid(row=1 + i, column=3, pady=_pad_y)
            self.frame1_table_stringvars.append(t)

        #########################################################################################################################

        # 2νμ΄μ§: λ΄ λ²νΈ νμΈ
        frame2 = Frame(self.window)
        notebook.add(frame2, text='λ΄ λ²νΈ νμΈ')

        ## μλ¨: λ²νΈ κΈ°μλ
        frame2_top = Frame(frame2)
        frame2_top.pack(expand=True, fill='both', padx=[20,20], pady=[10, 0])

        self.frame2_numbers = []
        for i in range(5):
            t_frame = Frame(frame2_top)
            t_frame.pack(expand=True, fill='both')
            Label(t_frame, text='{0}.'.format(i+1), font=self.get_font(15)).pack(side='left', expand=True, fill='both')
            self.frame2_numbers.append([Entry(t_frame, width=7,  font=self.get_font(13), justify='center') for _ in range(6)])
            for x in self.frame2_numbers[i]:
                x.pack(side='left', expand=True, ipady=8, pady=[0,0])

        ## μ€λ¨ : μ‘°ν λ²νΌ
        frame2_middle = Frame(frame2)
        frame2_middle.pack(expand=True, fill='both')

        ### μ€λ¨ μ’μΈ‘: μ½€λ³΄λ°μ€
        frame2_middle_left = Frame(frame2_middle)
        frame2_middle_left.pack(side='left', expand=True, fill='both')

        # recent_round = dhlotto.get_recent_round()
        rounds = [x for x in range(recent_round, 0, -1)]
        self.frame2_round = tkinter.ttk.Combobox(frame2_middle_left, width=8, justify='center', font=self.get_font(20), values=rounds)
        self.frame2_round.pack(expand=True, pady=[30, 55])
        self.frame2_round.current(0)

        ### μ€λ¨ μ°μΈ‘: μ‘°ν λ²νΌ
        frame2_middle_right = Frame(frame2_middle)
        frame2_middle_right.pack(side='right', expand=True, fill='both')
        Button(frame2_middle_right, text='μ‘°ν', font=self.get_font(20), width=10, command=self.onpress_frame2_query).pack(expand=True, pady=[30, 55])

        ## νλ¨ : μ‘°ν κ²°κ³Ό ν
        frame2_bottom = Frame(frame2)
        frame2_bottom.pack(expand=True, fill='both')

        self.frame2_table_stringvars = []
        widths = [6, 30, 15, 30]
        height = 2
        Label(frame2_bottom, text='λ²νΈ', borderwidth=2, relief='ridge', width=widths[0], height=height).grid(row=0, column=0, padx=[2, 0])
        Label(frame2_bottom, text='μΌμΉ', borderwidth=2, relief='ridge', width=widths[1], height=height).grid(row=0, column=1)
        Label(frame2_bottom, text='λ±μ', borderwidth=2, relief='ridge', width=widths[2], height=height).grid(row=0, column=2)
        Label(frame2_bottom, text='λΉμ²¨ κΈμ‘', borderwidth=2, relief='ridge', width=widths[3], height=height).grid(row=0, column=3)
        for i in range(5):
            t = [StringVar(), StringVar(), StringVar(), StringVar()]
            for e in t:
                e.set('-')
            _pad_y = [0, 0 if i < 5 - 1 else 5]
            Label(frame2_bottom, textvariable=t[0], borderwidth=2, relief='ridge', width=widths[0], height=height).grid(row=1 + i, column=0, pady=_pad_y, padx=[2, 0])
            Label(frame2_bottom, textvariable=t[1], borderwidth=2, relief='ridge', width=widths[1], height=height).grid(row=1 + i, column=1, pady=_pad_y)
            Label(frame2_bottom, textvariable=t[2], borderwidth=2, relief='ridge', width=widths[2], height=height).grid(row=1 + i, column=2, pady=_pad_y)
            Label(frame2_bottom, textvariable=t[3], anchor='e', borderwidth=2, relief='ridge', width=widths[3], height=height).grid(row=1 + i, column=3, pady=_pad_y)
            self.frame2_table_stringvars.append(t)

        #########################################################################################################################

        # 3νμ΄μ§: νλ§€μ  μ°ΎκΈ°
        frame3 = Frame(self.window)
        notebook.add(frame3, text='νλ§€μ  μ°ΎκΈ°')

        frame3_top = Frame(frame3)
        frame3_top.pack(expand=True, fill='both')

        frame3_top_left = Frame(frame3_top)
        frame3_top_left.pack(expand=True, fill='both', side='left')

        

        frame3_top_left_top = Frame(frame3_top_left)
        frame3_top_left_top.pack(expand=True, fill='both', side='top')

        Label(frame3_top_left_top, text='μ/λ', font=self.get_font(16, is_bold=True)).pack(side='top', anchor='sw', expand=True, fill='y', padx=[20, 0])
        # city1 = ['μμΈ', 'κ²½κΈ°', 'λΆμ°', 'λκ΅¬', 'μΈμ²', 'λμ ', 'μΈμ°', 'κ°μ', 'μΆ©λΆ', 'μΆ©λ¨', 'κ΄μ£Ό', 'μ λΆ', 'μ λ¨', 'κ²½λΆ', 'κ²½λ¨', 'μ μ£Ό', 'μΈμ’']
        city1 = ['μμΈ']
        self.frame3_city1 = tkinter.ttk.Combobox(frame3_top_left_top, width=8, justify='center', font=self.get_font(15, is_bold=True), values=city1)
        self.frame3_city1.pack(expand=True, side='bottom', anchor='nw', padx=[20, 0])
        self.frame3_city1.current(0)
        self.frame3_city1.bind("<<ComboboxSelected>>", self.onvalidate_frame3_city1)

        frame3_top_left_bottom = Frame(frame3_top_left)
        frame3_top_left_bottom.pack(expand=True, fill='both', side='bottom')

        Label(frame3_top_left_bottom, text='κ΅¬/κ΅°', font=self.get_font(16, is_bold=True)).pack(side='top', anchor='sw', expand=True, fill='y', padx=[20, 0], pady=[0, 0])
        city2 = ['κ°λ¨κ΅¬', 'κ°λκ΅¬', 'κ°λΆκ΅¬', 'κ°μκ΅¬', 'κ΄μκ΅¬', 'κ΄μ§κ΅¬', 'κ΅¬λ‘κ΅¬', 'κΈμ²κ΅¬', 'λΈμκ΅¬', 'λλ΄κ΅¬', 'λλλ¬Έκ΅¬', 'λμκ΅¬', 'λ§ν¬κ΅¬', \
            'μλλ¬Έκ΅¬', 'μμ΄κ΅¬', 'μ±λκ΅¬', 'μ±λΆκ΅¬', 'μ‘νκ΅¬', 'μμ²κ΅¬', 'μλ±ν¬κ΅¬', 'μ©μ°κ΅¬', 'μνκ΅¬', 'μ’λ‘κ΅¬', 'μ€κ΅¬', 'μ€λκ΅¬']
        self.frame3_city2 = tkinter.ttk.Combobox(frame3_top_left_bottom, width=8, justify='center', font=self.get_font(15, is_bold=True), values=city2)
        self.frame3_city2.pack(expand=True, side='bottom', anchor='nw', padx=[20, 0])
        self.frame3_city2.current(0)

        frame3_top_right = Frame(frame3_top)
        frame3_top_right.pack(expand=True, fill='both', side='right')

        Button(frame3_top_right, text='μ‘°ν', command=self.onpress_frame3_query, font=self.get_font(21, is_bold=True)).pack(expand=True, fill='both', padx=20, pady=20)

        ## μ€μλ¨: μ§λ
        frame3_middle = Frame(frame3, bg='blue')
        frame3_middle.pack(expand=True, fill='both', ipady=170)

        thread = threading.Thread(target=self.cef_thread, args=(frame3_middle, [0, 0, 600, 350]))
        thread.setDaemon(True)
        thread.start()


        ## μ€νλ¨: μμΈμ λ³΄ λ° κ³΅μ λ²νΌ
        frame3_middle2 = Frame(frame3)
        frame3_middle2.pack(expand=True, fill='both')

        self.frame3_name = StringVar()
        Label(frame3_middle2, textvariable=self.frame3_name, font=self.get_font(14, is_bold=True)).pack(expand=True)
        self.frame3_name.set('-')
        # self.frame3_name.set('λλμ¨ κ΅¬νλ°λ‘λ (02-1231-4535)')

        self.frame3_share = Button(frame3_middle2, text='κ³΅μ ', command=self.onpress_frame3_share, font=self.get_font(12))
        self.frame3_share.place(x=520, y=2)
        self.frame3_share['state']= 'disable'

        ## νλ¨: νμ΄μ§
        frame3_bottom = Frame(frame3)
        frame3_bottom.pack(expand=True, fill='both')

        self.frame3_page = StringVar()
        self.frame3_current_page = 1
        Button(frame3_bottom, text='β', font=self.get_font(15), command=self.opress_frame3_prev).pack(expand=True, side='left', anchor='e')
        Label(frame3_bottom, textvariable=self.frame3_page, font=self.get_font(16)).pack(expand=True, side='left', anchor='center')
        Button(frame3_bottom, text='βΆ', font=self.get_font(15), command=self.opress_frame3_next).pack(expand=True, side='left', anchor='w')
        self.frame3_page.set('-/-')


        #########################################################################################################################

        # 4νμ΄μ§: λ²νΈ λ³ ν΅κ³
        frame4 = Frame(self.window)
        notebook.add(frame4, text='λ²νΈ λ³ ν΅κ³')

        self.frame4_canvas = Canvas(frame4, background='#f0f0f0', width=596, height=550)
        self.frame4_canvas.pack(expand=True, fill='both')

        y = 500
        sx = 10
        ex = 590
        self.frame4_canvas.create_line(sx, y, ex, y)
        bar_width = (ex - sx) / 45

        frequency = dhlotto.get_frequency()
        max_val = max(frequency)
        height_per_val = (y - 20) / max_val

        bg_colors = ['#fbc400', '#69c8f2', '#ff7272', '#aaaaaa', '#b0d840']

        for i in range(45):
            rect_sx = sx + i * bar_width
            rect_ex = sx + (i+1) * bar_width 
            rect_sy = y
            rect_ey = y - height_per_val * frequency[i]
            self.frame4_canvas.create_rectangle(rect_sx, rect_sy, rect_ex, rect_ey, fill=bg_colors[i//10])
            self.frame4_canvas.create_text(rect_sx+bar_width//2, rect_sy+10, text=i+1, font=self.get_font(8))

        #########################################################################################################################



    # ν°νΈ μ»μ΄μ€κΈ°
    def get_font(self, font_size, is_bold = False):
        font_size = int(font_size)
        if (font_size, is_bold) not in self.fonts:
            self.fonts[(font_size, is_bold)] = font.Font(size=font_size, weight=('bold' if is_bold else 'normal'))
        return self.fonts[(font_size, is_bold)]
    

    def onpress_frame1_query(self):
        cur_round = eval(self.frame1_round.get())
        lotto_data = dhlotto.get_lotto_result(cur_round)

        # canvasμ κ·Έλ¦¬κΈ°
        pad_x = 58
        pad_y = 30
        ball_size = 60
        ball_gap = 25
        bg_colors = ['#fbc400', '#69c8f2', '#ff7272', '#aaaaaa', '#b0d840']
        bg_default = '#f0f0f0'

        self.frame1_canvas.delete('*')
        self.frame1_canvas.create_text(300, 10, text='{0}νμ°¨ ({1})'.format(lotto_data['round'], lotto_data['date']), tags='*', font=self.get_font(13, is_bold=True))

        ## κ³΅ 6κ°
        for i in range(6):
            start_x = pad_x + i * (ball_size + ball_gap)
            start_y = pad_y
            end_x = start_x + ball_size
            end_y = start_y + ball_size
            self.frame1_canvas.create_oval(start_x, start_y, end_x, end_y, fill=bg_colors[(lotto_data['numbers'][i]-1)//10], outline=bg_default, tags='*')
            self.frame1_canvas.create_text(start_x + ball_size // 2, start_y + ball_size // 2, fill='white', text=lotto_data['numbers'][i], font=self.get_font(27), tags='*')

        ## λ³΄λμ€
        bonus_ball_size = int(ball_size * 1.25)
        start_x = 600//2 - bonus_ball_size//2
        start_y = pad_y+ball_size+10
        end_x = 600//2 + bonus_ball_size//2
        end_y = start_y + bonus_ball_size
        self.frame1_canvas.create_oval(start_x, start_y, end_x, end_y, fill=bg_colors[(lotto_data['numbers'][6]-1)//10], outline=bg_default, tags='*')
        self.frame1_canvas.create_text(start_x + bonus_ball_size // 2, start_y + bonus_ball_size // 2, fill='white', text=lotto_data['numbers'][6], font=self.get_font(27 * 1.25), tags='*')
        self.frame1_canvas.create_text(start_x + bonus_ball_size // 2, start_y + bonus_ball_size + 15, text='λ³΄λμ€', font=font.Font(size=15, weight='bold'), tags='*')

        # Table μμ 
        lotto_prizes = dhlotto.get_lotto_prize(cur_round)
        for i in range(5):
            for j in range(4):
                self.frame1_table_stringvars[i][j].set(lotto_prizes[i][j])

    def onpress_frame2_query(self):

        def is_validate(lst): # κ³΅λ°±μ΄ μλ λ©μ©‘ν λ¦¬μ€νΈμΈμ§ μ²΄ν¬ν΄μ£Όλ ν¨μ
            for x in lst:
                if not x:
                    return False
            return True

        cur_round = eval(self.frame1_round.get())
        lotto_data = dhlotto.get_lotto_result(cur_round)
        lotto_prize = dhlotto.get_lotto_prize(cur_round)

        numbers = lotto_data['numbers'][0:6] # λ³΄λμ€λ²νΈ μ μΈ λΉμ²¨λ²νΈλ€
        bonus_num = lotto_data['numbers'][6]

        for i in range(5):
            self.frame2_table_stringvars[i][0].set(i+1) # νμ 'λ²νΈ' μ€μ 
            try:
                picks = [eval(self.frame2_numbers[i][idx].get()) for idx in range(6)] # λ΄ λ²νΈλ€
            except Exception as e:
                self.frame2_table_stringvars[i][1].set('-') # μΌμΉ
                self.frame2_table_stringvars[i][2].set('-') # λ±μ
                self.frame2_table_stringvars[i][3].set('-') # λΉμ²¨ κΈμ‘
                continue

            # Validate μ²΄ν¬
            if not is_validate(picks):
                self.frame2_table_stringvars[i][1].set('-') # μΌμΉ
                self.frame2_table_stringvars[i][2].set('-') # λ±μ
                self.frame2_table_stringvars[i][3].set('-') # λΉμ²¨ κΈμ‘
                continue

            pick_str_list = list(map(lambda x : '[{0}]'.format(x) if x in numbers else ('λ³΄λμ€({0})'.format(x) if x == bonus_num else str(x)), picks))
            self.frame2_table_stringvars[i][1].set(' '.join(pick_str_list))

            hit_count = len(list(filter(lambda x : x in numbers, picks)))
            if hit_count < 3: # λ―ΈλΉμ²¨
                self.frame2_table_stringvars[i][2].set('X')
                self.frame2_table_stringvars[i][3].set('0 μ')
            elif hit_count == 3: # 5λ±
                self.frame2_table_stringvars[i][2].set('5λ±')
                self.frame2_table_stringvars[i][3].set(lotto_prize[4][3])
            elif hit_count == 4: # 4λ±
                self.frame2_table_stringvars[i][2].set('4λ±')
                self.frame2_table_stringvars[i][3].set(lotto_prize[3][3])
            elif hit_count == 5: # 3λ±/2λ±
                if bonus_num not in picks:
                    self.frame2_table_stringvars[i][2].set('3λ±')
                    self.frame2_table_stringvars[i][3].set(lotto_prize[2][3])
                self.frame2_table_stringvars[i][2].set('2λ±')
                self.frame2_table_stringvars[i][3].set(lotto_prize[1][3])
            elif hit_count == 6: # 1λ±
                self.frame2_table_stringvars[i][2].set('1λ±')
                self.frame2_table_stringvars[i][3].set(lotto_prize[0][3])

    def onpress_frame3_query(self):
        self.frame3_store_data = dhlotto.get_store(self.frame3_city1.get(), self.frame3_city2.get())
        self.frame3_current_page = 1

        self.frame3_name.set('{0} ({1})'.format(self.frame3_store_data[0]['name'], self.frame3_store_data[0]['tel']))
        self.frame3_page.set('{0}/{1}'.format(self.frame3_current_page, len(self.frame3_store_data)))

        self.frame3_share['state'] = 'normal'
        # m = folium.Map(location=[37.3402849, 126.7313189], zoom_start=15)
        m = folium.Map(location=[self.frame3_store_data[0]['lat'], self.frame3_store_data[0]['lon']], zoom_start=16)
        
        # λ§μ»€ μ§μ 
        folium.Marker([self.frame3_store_data[0]['lat'], self.frame3_store_data[0]['lon']], popup=self.frame3_store_data[0]['name']).add_to(m)
        # html νμΌλ‘ μ μ₯
        m.save('map.html')
        self.browser.Navigate('file:///map.html')

    def onpress_frame3_share(self):
        InputBox().show('E-mail μλ ₯:')
        # μΈμ μμ±
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # TLS λ³΄μ μμ
        s.starttls()

        id = 'test.project.lotto@gmail.com'
        password = ''

        # λ‘κ·ΈμΈ μΈμ¦
        s.login(id, password)


        # λ³΄λΌ λ©μμ§ μ€μ 
        msg = MIMEText('μ§μ λͺ : {0}\nμ νλ²νΈ : {1}\n'.format(self.frame3_store_data[self.frame3_current_page - 1]['name'], self.frame3_store_data[self.frame3_current_page - 1]['tel']) )
        msg['Subject'] = '{0} {1} {2}λ²μ§Έ λ³΅κΆ νλ§€μ  μ‘°ν'.format(self.frame3_city1.get(), self.frame3_city2.get(), self.frame3_current_page)

        # λ©μΌ λ³΄λ΄κΈ°
        s.sendmail(id, InputBox().answer, msg.as_string())

        # μΈμ μ’λ£
        s.quit()

    def opress_frame3_prev(self):
        if not self.frame3_store_data:
            return
        if self.frame3_current_page <= 1:
            return
        self.frame3_current_page -= 1

        self.frame3_name.set('{0} ({1})'.format(self.frame3_store_data[self.frame3_current_page - 1]['name'], self.frame3_store_data[self.frame3_current_page - 1]['tel']))
        self.frame3_page.set('{0}/{1}'.format(self.frame3_current_page, len(self.frame3_store_data)))
        m = folium.Map(location=[self.frame3_store_data[self.frame3_current_page - 1]['lat'], self.frame3_store_data[self.frame3_current_page - 1]['lon']], zoom_start=16)
        # λ§μ»€ μ§μ 
        folium.Marker([self.frame3_store_data[self.frame3_current_page - 1]['lat'], self.frame3_store_data[self.frame3_current_page - 1]['lon']], popup=self.frame3_store_data[self.frame3_current_page - 1]['name']).add_to(m)
        # html νμΌλ‘ μ μ₯
        m.save('map.html')
        self.browser.Navigate('file:///map.html')

    def opress_frame3_next(self):
        if not self.frame3_store_data:
            return
        if self.frame3_current_page >= len(self.frame3_store_data):
            return
        self.frame3_current_page += 1

        self.frame3_name.set('{0} ({1})'.format(self.frame3_store_data[self.frame3_current_page - 1]['name'], self.frame3_store_data[self.frame3_current_page - 1]['tel']))
        self.frame3_page.set('{0}/{1}'.format(self.frame3_current_page, len(self.frame3_store_data)))
        m = folium.Map(location=[self.frame3_store_data[self.frame3_current_page - 1]['lat'], self.frame3_store_data[self.frame3_current_page - 1]['lon']], zoom_start=16)
        # λ§μ»€ μ§μ 
        folium.Marker([self.frame3_store_data[self.frame3_current_page - 1]['lat'], self.frame3_store_data[self.frame3_current_page - 1]['lon']], popup=self.frame3_store_data[self.frame3_current_page - 1]['name']).add_to(m)
        # html νμΌλ‘ μ μ₯
        m.save('map.html')
        self.browser.Navigate('file:///map.html')
        
    def onvalidate_frame3_city1(self, _):
        city = self.frame3_city1.get()
        pass


    def cef_thread(self, *arg):
        sys.excepthook = cef.ExceptHook
        window_info = cef.WindowInfo(arg[0].winfo_id())
        window_info.SetAsChild(arg[0].winfo_id(), arg[1])
        cef.Initialize()
        self.browser = cef.CreateBrowserSync(window_info, url='about:blank')
        # browser.ExecuteJavascript('alert(1);');
        cef.MessageLoop()


        
MainGUI()
