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

        self.MakeGui()

        self.window.mainloop()

    def MakeGui(self):
        tkinter.ttk.Style().configure('TNotebook.Tab', font=('','11','bold'), padding=[14, 12] )
        big_font = font.Font(size=20)
        default_font = font.Font()

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
        self.gui_1_round = tkinter.ttk.Combobox(frame1_top_left, width=8, justify='center', font=big_font, values=rounds)
        self.gui_1_round.pack(expand=True)
        self.gui_1_round.current(0)

        ### 상단 우측: 조회 버튼
        frame1_top_right = Frame(frame1_top)
        frame1_top_right.pack(side='right', expand=True, fill='both')
        Button(frame1_top_right, text='조회', font=big_font, width=10).pack(expand=True)

        
        ## 중단: 당첨번호 출력 Canvas
        frame1_middle = Frame(frame1)
        frame1_middle.pack(expand=True, fill='both')

        self.frame1_canvas = Canvas(frame1_middle, background='white', width=596, height=1)
        self.frame1_canvas.pack(expand=True, fill='both')


        ## 하단: 당첨결과 출력 Table
        frame1_bottom = Frame(frame1)
        frame1_bottom.pack(expand=True, fill='both')


        # 2페이지: 내 번호 확인
        frame2 = Frame(self.window)
        notebook.add(frame2, text='내 번호 확인')

        # 3페이지: 판매점 찾기
        frame3 = Frame(self.window)
        notebook.add(frame3, text='판매점 찾기')

        # 4페이지: 시뮬레이션
        frame4 = Frame(self.window)
        notebook.add(frame4, text='시뮬레이션')

        # 5페이지: 번호 별 통계
        frame5 = Frame(self.window)
        notebook.add(frame5, text='번호 별 통계')

MainGUI()
