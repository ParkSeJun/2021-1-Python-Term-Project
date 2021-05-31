from sys import exec_prefix
from tkinter import *
from tkinter import font
import tkinter.ttk
from dhlotto import *

class MainGUI:

    def __init__(self):
        self.window = Tk()
        self.window.title('대박인생')
        self.window.geometry('600x600')
        self.fonts = dict()

        self.MakeGui()

        self.window.mainloop()

    def MakeGui(self):
        tkinter.ttk.Style().configure('TNotebook.Tab', font=('','11','bold'), padding=[14, 12] )

        notebook = tkinter.ttk.Notebook(self.window, width=600, height=600)
        notebook.pack(anchor='nw')

        # 1페이지: 추첨 결과 조회
        frame1 = Frame(self.window)
        frame1.pack()
        notebook.add(frame1, text='추첨 결과 조회', )

        ## 상단: 콤보박스와 조회 버튼
        frame1_top = Frame(frame1)
        frame1_top.pack(expand=True, fill='both')

        ### 상단 좌측: 콤보박스
        frame1_top_left = Frame(frame1_top)
        frame1_top_left.pack(side='left', expand=True, fill='both')

        recent_round = dhlotto.get_recent_round()
        rounds = [x for x in range(recent_round, 0, -1)]
        self.frame1_round = tkinter.ttk.Combobox(frame1_top_left, width=8, justify='center', font=self.get_font(20), values=rounds)
        self.frame1_round.pack(expand=True)
        self.frame1_round.current(0)

        ### 상단 우측: 조회 버튼
        frame1_top_right = Frame(frame1_top)
        frame1_top_right.pack(side='right', expand=True, fill='both')
        Button(frame1_top_right, text='조회', font=self.get_font(20), width=10, command=self.onpress_frame1_query).pack(expand=True)

        
        ## 중단: 당첨번호 출력 Canvas
        frame1_middle = Frame(frame1)
        frame1_middle.pack(expand=True, fill='both')

        self.frame1_canvas = Canvas(frame1_middle, background='#f0f0f0', width=596, height=160)
        self.frame1_canvas.pack(expand=True, fill='both')


        ## 하단: 당첨결과 출력 Table
        frame1_bottom = Frame(frame1)
        frame1_bottom.pack(expand=False, fill='both')

        self.frame1_table_stringvars = []
        widths = [6, 30, 15, 30]
        height = 2
        Label(frame1_bottom, text='순위', borderwidth=2, relief='ridge', width=widths[0], height=height).grid(row=0, column=0, padx=[2, 0])
        Label(frame1_bottom, text='총 당첨금액', borderwidth=2, relief='ridge', width=widths[1], height=height).grid(row=0, column=1)
        Label(frame1_bottom, text='당첨게임 수', borderwidth=2, relief='ridge', width=widths[2], height=height).grid(row=0, column=2)
        Label(frame1_bottom, text='1게임당 당첨금액', borderwidth=2, relief='ridge', width=widths[3], height=height).grid(row=0, column=3)
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


        # 2페이지: 내 번호 확인
        frame2 = Frame(self.window)
        notebook.add(frame2, text='내 번호 확인')

        ## 상단: 번호 기입란
        frame2_top = Frame(frame2)
        frame2_top.pack(expand=True, fill='both')

        self.frame2_numbers = []
        for i in range(5):
            t_frame = Frame(frame2_top)
            t_frame.pack(expand=True, fill='both')
            Label(t_frame, text='{0}.'.format(i+1), font=self.get_font(15)).pack(side='left', expand=True, fill='both')
            self.frame2_numbers.append([Entry(t_frame, width=3, font=self.get_font(15)) for _ in range(6)])
            for x in self.frame2_numbers[i]:
                x.pack(side='left', expand=True, fill='both', padx=[0,15], pady=[10,10])

        frame2_middle = Frame(frame2)
        frame2_middle.pack(expand=True, fill='both')



        frame2_bottom = Frame(frame2)
        frame2_bottom.pack(expand=True, fill='both')


        # 3페이지: 판매점 찾기
        frame3 = Frame(self.window)
        notebook.add(frame3, text='판매점 찾기')

        # 4페이지: 시뮬레이션
        frame4 = Frame(self.window)
        notebook.add(frame4, text='시뮬레이션')

        # 5페이지: 번호 별 통계
        frame5 = Frame(self.window)
        notebook.add(frame5, text='번호 별 통계')



    # 폰트 얻어오기
    def get_font(self, font_size, is_bold = False):
        font_size = int(font_size)
        if (font_size, is_bold) not in self.fonts:
            self.fonts[(font_size, is_bold)] = font.Font(size=font_size, weight=('bold' if is_bold else 'normal'))
        return self.fonts[(font_size, is_bold)]
        


    def onpress_frame1_query(self):
        cur_round = eval(self.frame1_round.get())
        lotto_data = dhlotto.get_lotto_result(cur_round)

        # canvas에 그리기
        pad_x = 58
        pad_y = 30
        ball_size = 60
        ball_gap = 25
        bg_colors = ['#fbc400', '#69c8f2', '#ff7272', '#aaaaaa', '#b0d840']
        bg_default = '#f0f0f0'

        self.frame1_canvas.delete('*')
        self.frame1_canvas.create_text(300, 10, text='{0}회차 ({1})'.format(lotto_data['round'], lotto_data['date']), tags='*', font=self.get_font(13, is_bold=True))

        ## 공 6개
        for i in range(6):
            start_x = pad_x + i * (ball_size + ball_gap)
            start_y = pad_y
            end_x = start_x + ball_size
            end_y = start_y + ball_size
            self.frame1_canvas.create_oval(start_x, start_y, end_x, end_y, fill=bg_colors[(lotto_data['numbers'][i]-1)//10], outline=bg_default, tags='*')
            self.frame1_canvas.create_text(start_x + ball_size // 2, start_y + ball_size // 2, fill='white', text=lotto_data['numbers'][i], font=self.get_font(27), tags='*')

        ## 보너스
        bonus_ball_size = int(ball_size * 1.25)
        start_x = 600//2 - bonus_ball_size//2
        start_y = pad_y+ball_size+10
        end_x = 600//2 + bonus_ball_size//2
        end_y = start_y + bonus_ball_size
        self.frame1_canvas.create_oval(start_x, start_y, end_x, end_y, fill=bg_colors[(lotto_data['numbers'][6]-1)//10], outline=bg_default, tags='*')
        self.frame1_canvas.create_text(start_x + bonus_ball_size // 2, start_y + bonus_ball_size // 2, fill='white', text=lotto_data['numbers'][6], font=self.get_font(27 * 1.25), tags='*')
        self.frame1_canvas.create_text(start_x + bonus_ball_size // 2, start_y + bonus_ball_size + 15, text='보너스', font=font.Font(size=15, weight='bold'), tags='*')

        # Table 수정
        lotto_prizes = dhlotto.get_lotto_prize(cur_round)
        for i in range(5):
            for j in range(4):
                self.frame1_table_stringvars[i][j].set(lotto_prizes[i][j])

        
MainGUI()
