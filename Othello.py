import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import time, random

def main():
    othello = Game()
    othello.window.mainloop()

class Game:

    def __init__(self):

        # สร้าง Tk window
        self.window = tk.Tk()
        self.window.geometry("950x615")                                     
    
        # สร้างรูปภาพ
        self.img = self.image_othello()
        self.kao = self.image_kao()
        self.dum = self.image_dum()

        # สร้างเฟรมเพื่อแยกหน้า
        self.page_one()
        self.page_two()
        self.page_three()
        self.page_four()

        # ดึงหน้านั้น ๆ ให้ขึ้นมาเป็นหน้าแรกสุด ref : https://www.youtube.com/watch?v=qw_XHRJP-vc
        self.page1.tkraise()

        # สร้าง board
        self.board = [[0 for _ in range(8)] for _ in range(8)]

        self.time_running = 0
        self.time_display = tk.StringVar(value = "00:00:00")

        self.nub_time()
        self.krongsang()
        self.othello_board()
        self.board_row()
        self.board_column()

        self.deactivate_bot_basic()
        self.deactivate_bot_pla()
        self.deactivate_bot_im()

        self.start_button = False
        self.true_start = False

    def image_othello(self):    # รูปหน้าเกม Othello จาก https://www.linkedin.com/pulse/othello-japanese-board-game-erai-technologies
        img = ImageTk.PhotoImage(Image.open("1649738189150.png")) 
        return img
    
    def image_kao(self):        # รูปหมากดำ screenshot จาก https://www.eothello.com/
        kao = ImageTk.PhotoImage(Image.open("kao_74_64.png"))
        return kao

    def image_dum(self):        # รูปหมากขาว screenshot จาก https://www.eothello.com/
        dum = ImageTk.PhotoImage(Image.open("dum_74_64.png"))
        return dum
    
    def quit(self):
        self.window.quit()

    def page_one(self):                                    # เฟรม 1 Main Menu
        self.page1 = Frame(self.window)
        self.page1.config(bg = 'darkgreen')
        self.page1.place(relheight = 1, relwidth = 1)
    
    def page_two(self):                                    # เฟรม 2 Select Mode
        self.page2 = Frame(self.window)
        self.page2.config(bg = 'darkgreen')
        self.page2.place(relheight = 1, relwidth = 1)

    def page_three(self):                                  # เฟรม 3 Othello Board
        self.page3 = Frame(self.window)
        self.page3.config(bg = 'darkgray')
        self.page3.place(relheight = 1, relwidth = 1)

    def page_four(self):                                   # เฟรม 4 Difficulties Bot
        self.page4 = Frame(self.window)
        self.page4.config(bg = 'darkgreen')
        self.page4.place(relheight = 1, relwidth = 1)

    # ref สร้างตาราง : chatgpt
    def othello_board(self):
        for row in range(8):
            for col in range(8):
                self.board[row][col]= tk.Button(self.page3, bg = "#00bc8c"
                                        , command = lambda row = row, col = col : [self.click(row, col)],
                                        height = 4, width = 10, state = 'disabled')
                self.board[row][col].grid(row = row, column = col)
                
                if (row, col) == (3, 3) or (row, col) == (4, 4):
                    self.board[row][col].config(state = "disabled")
                    mhark = tk.Label(self.page3, image = self.kao, text = "White_piece", borderwidth = 0, highlightthickness = 0)
                    mhark.grid(row = row, column = col)
                elif (row, col) == (3, 4) or (row,col) == (4, 3):
                    self.board[row][col].config(state = "disabled")
                    mhark = tk.Label(self.page3, image = self.dum, text = "Black_piece", borderwidth = 0, highlightthickness = 0)
                    mhark.grid(row = row, column = col)

                self.player = 'B'
                show = "Player Turn : ⚫"
                self.Player_Turn.config(text = show)

        self.count_mhark()
        self.board_row()
        self.board_column()
        self.truaj_mhark()

    def board_row(self):
        # หมายเลขแต่ละ row
        col = 8
        for row in range(1, 9):
            row_num = tk.Label(self.page3, text =  row, bg = 'darkgray')
            row_num.grid(row = row - 1, column = col, padx = 10)
    
    def board_column(self):
        # หมายเลขแต่ละ column
        row = 8
        c = 0
        for col in range(8):
            show = ''
            show = chr(ord('A') + c)
            c += 1
            
            col_num = tk.Label(self.page3, text = show, bg = 'darkgray')
            col_num.grid(row = row, column = col, pady = 5)

    # ทำให้ปุ่มสามารถกดได้
    def click(self, row, col):
        # สลับเทิร์นคนเล่น
        if self.player == "B":
            p = "Black_piece"
            show = self.dum
            self.player = "W"
            text = "Player Turn : ⚪"
            self.Player_Turn.config(text = text)
        else:
            p = "White_piece"
            show = self.kao
            self.player = "B"
            text = "Player Turn : ⚫"
            self.Player_Turn.config(text = text)

        self.board[row][col] = self.page3.grid_slaves(row = row, column = col)[0] # รับข้อมูล Text จากปุ่มนั้นๆ
        self.board[row][col].config(state = "disabled", text = p) # กำหนดข้อความในปุ่ม # state = "disabled" กำหนดให้ปุ่มที่กดแล้วไม่สามารถกดซ้ำได้อีก
        
        mhark = tk.Label(self.page3, image = show, text = p, borderwidth = 0, highlightthickness = 0)
        mhark.grid(row = row, column = col)

        self.clear_truaj()
        self.place_piece(row, col)
        self.truaj_mhark()
        self.count_mhark()
        self.check_game_end()
        self.yod_bot()
        self.pla2_bot()
        self.impossible_bot()

    
    def truaj_mhark(self):
        # กำหนดตัวแปรฝ่ายตัวเอง และ ฝ่ายตรงข้าม
        if self.player == 'B':
            self.opposite = "White_piece"
            self.me = "Black_piece"
        elif self.player == 'W':
            self.opposite = "Black_piece"
            self.me = "White_piece"
        for row in range(8):
            for col in range(8):
                
                all_button = self.page3.grid_slaves(row = row, column = col)[0]
                info = all_button.cget("text")

                if info == self.me:

                    for drow in range(-1, 2):
                        for dcol in range(-1, 2):

                            if(drow == 0 and dcol == 0):
                                continue
                            
                            self.check_everything(row,col,drow,dcol)

    # Check ตำแหน่งที่ผู้เล่นสามารถวางได้ ref : ให้เพื่อนที่สนิทต่างมอ. กับเพื่อนในคณะสอน
    def check_everything(self, row, col, drow, dcol):
            
        diff = 1                            # กำหนดระยะห่างจากปุ่มที่เราอยู่
        vx = row + (drow * diff)            
        vy = col + (dcol * diff)

        if not (vx >= 0 and vy >= 0 and vx < 8 and vy < 8):     
            return 
        
        top_left = self.page3.grid_slaves(row = vx, column = vy)[0]
        info = top_left.cget("text")

        if info == self.opposite:

            while (vx >= 0 and vy >= 0 and vx < 8 and vy < 8) and (info == self.opposite):

                top_left = self.page3.grid_slaves(row = vx, column = vy)[0]
                info = top_left.cget("text")

                diff += 1
                vx = row + (drow * diff)
                vy = col + (dcol * diff)

            diff -= 1
            vx = row + (drow * diff)
            vy = col + (dcol * diff)
            
            top_left = self.page3.grid_slaves(row = vx, column = vy)[0]
            check_poop = top_left.cget("text")
            if check_poop == '':
                self.board[vx][vy].config(state = 'normal',text = '💩')

    # เปลี่ยนสีหมากที่ถูกกิน ref : ให้เพื่อนที่สนิทต่างมอ. ช่วย
    def place_piece(self,row,col):
        
        img = ''
        txt = ''
        if self.player == 'W':
            img = self.dum
            txt = 'Black_piece'
        else:
            img = self.kao
            txt = 'White_piece'

        for drow in range(-1, 2):
            for dcol in range(-1, 2):

                if drow == 0 and dcol == 0:       # ตำแหน่งที่เราอยู่
                    continue

                diff = 1
                vx = row + (drow * diff)
                vy = col + (dcol * diff)

                if not (vx >= 0 and vy >= 0 and vx < 8 and vy < 8):   
                    continue
                
                top_left = self.page3.grid_slaves(row = vx, column = vy)[0]      # รับข้อมูล text ณ ตำแหน่ง vx, vy
                info = top_left.cget("text")
                
                if info != self.opposite:          # หาขาว opposite = ขาว
                    continue

                while (True):
                    diff += 1
                    vx = row + (drow * diff)
                    vy = col + (dcol * diff)

                    if not (vx >= 0 and vy >= 0 and vx < 8 and vy < 8):
                        break

                    top_left = self.page3.grid_slaves(row = vx, column = vy)[0]
                    info = top_left.cget("text")

                    if info == self.me:            # me = ดำ

                        for diff_fill in range(0, diff):    # ตำแหน่งที่เราอยู่ ถึง ตำแหน่งที่เจอหมากเรา (self.me)

                            vx = row + (drow * diff_fill)
                            vy = col + (dcol * diff_fill)

                            self.board[vx][vy].config(state = 'disable')
                            mhark = tk.Label(self.page3, image = img, text = txt, borderwidth = 0, highlightthickness = 0)
                            mhark.grid(row = vx, column = vy)

                        break

    # Bot สุ่มตำแหน่งที่สามารถลงได้บนกระดานหมาก
    def yod_bot(self):
        stop = False
        kee_list = []

        if self.basic_mode == True:
            if self.player == 'W':
                for row in range(8):
                    for col in range(8):
                        button = self.page3.grid_slaves(row = row, column = col)[0]
                        text = button.cget("text")

                        if text == '💩':
                            list = []
                            list.append(row)
                            list.append(col)
                            kee_list.append(list)

        if kee_list:
            row, col = random.choice(kee_list)
            self.board[row][col].invoke()   # .invoke() เป็นฟังก์ชันที่ทำให้ปุ่มถูกกด

    # Bot พยายามที่จะวางขอบกระดานหมาก
    def pla2_bot(self):
        playable_cor = []
        row_list = []
        col_list = []
        combine_maxmin = []

        if self.advance_mode == True and self.player == 'W' and self.true_start == False:
            for row_bot in range(8):
                for col_bot in range(8):
                    button = self.page3.grid_slaves(row = row_bot, column = col_bot)[0]
                    text = button.cget("text") 
                    if text == '💩':
                        cor = []
                        cor.append(row_bot)
                        cor.append(col_bot)
                        playable_cor.append(cor)
            for position in playable_cor:
                row_list.append(position[0])
                col_list.append(position[0])

            print(playable_cor)
            if len(playable_cor) == 1:
                self.board[playable_cor[0][0]][playable_cor[0][1]].invoke()

            print(row_list)
            minrow = min(row_list)
            maxrow = max(row_list)
            print(minrow)

            mincol = min(col_list)
            maxcol = max(col_list)

            if abs(0 - minrow) < abs(7 - maxrow):
                bot_row_path = minrow
                print('1 work')
            elif abs(0 - minrow) > abs(7 - maxrow):
                print('2 work')
                bot_row_path = maxrow
            else:
                bot_row_path = minrow
                print('3 work')
        
            if abs(0 - mincol) < abs(7 - maxcol):
                bot_col_path = mincol
            elif abs(0 - mincol) > abs(7 - maxcol):
                bot_col_path = maxcol
            else:
                bot_col_path = mincol

            combine_maxmin.append(bot_row_path)
            combine_maxmin.append(bot_col_path)

            print(combine_maxmin)
            for coordinate in playable_cor:
                if combine_maxmin == coordinate:
                    print('match')
                    self.board[coordinate[0]][coordinate[1]].invoke()

            while True:
                stop = 0
                lucky_coin = random.choice(playable_cor)
                print(lucky_coin, 'lucky')
                if lucky_coin == combine_maxmin:
                    continue
                else:
                    while stop < 11:
                        self.board[lucky_coin[0]][lucky_coin[1]].invoke()
                        stop += 1
                        break
                    break
        elif self.advance_mode == True and self.player == 'B' and self.true_start == True:
            for row_bot in range(8):
                for col_bot in range(8):
                    button = self.page3.grid_slaves(row = row_bot, column = col_bot)[0]
                    text = button.cget("text") 
                    if text == '💩':
                        cor = []
                        cor.append(row_bot)
                        cor.append(col_bot)
                        playable_cor.append(cor)
            for position in playable_cor:
                row_list.append(position[0])
                col_list.append(position[0])

            print(playable_cor)
            if len(playable_cor) == 1:
                self.board[playable_cor[0][0]][playable_cor[0][1]].invoke()

            print(row_list)
            minrow = min(row_list)
            maxrow = max(row_list)
            print(minrow)

            mincol = min(col_list)
            maxcol = max(col_list)

            if abs(0 - minrow) < abs(7 - maxrow):
                bot_row_path = minrow
                print('1 work')
            elif abs(0 - minrow) > abs(7 - maxrow):
                print('2 work')
                bot_row_path = maxrow
            else:
                bot_row_path = minrow
                print('3 work')
        
            if abs(0 - mincol) < abs(7 - maxcol):
                bot_col_path = mincol
            elif abs(0 - mincol) > abs(7 - maxcol):
                bot_col_path = maxcol
            else:
                bot_col_path = mincol

            combine_maxmin.append(bot_row_path)
            combine_maxmin.append(bot_col_path)

            print(combine_maxmin)
            for coordinate in playable_cor:
                if combine_maxmin == coordinate:
                    print('match')
                    self.board[coordinate[0]][coordinate[1]].invoke()

            while True:
                stop = 0
                lucky_coin = random.choice(playable_cor)
                print(lucky_coin, 'lucky')
                if lucky_coin == combine_maxmin:
                    continue
                else:
                    while stop < 11:
                        self.board[lucky_coin[0]][lucky_coin[1]].invoke()
                        stop += 1
                        break
                    break
    
    # Bot เก่งเกินไป สู้ไม่ได้
    def impossible_bot(self):
        if self.im_mode == True and self.player == 'W':
            for row in range(8):
                for col in range(8):
                    getinfo = self.page3.grid_slaves(row = row, column = col)[0]
                    info = getinfo.cget('text')
                    if info == 'Black_piece':
                        print('found black')
                        continue

                    self.player = 'W'
                    self.board[row][col].config(state = 'normal')
                    self.board[row][col].invoke()

    # activate, deactivate จะทำงานเหมือนเป็นวาล์วเปิด-ปิดของแต่ละโหมด
    def activate_bot_basic(self):
        self.basic_mode = True

    def deactivate_bot_basic(self):
        self.basic_mode = False

    def activate_bot_pla(self):
        self.advance_mode = True

    def deactivate_bot_pla(self):
        self.advance_mode = False
    
    def activate_bot_im(self):
        self.im_mode = True

    def deactivate_bot_im(self):
        self.im_mode = False

    # Clear ตำแหน่งที่สามารถวางได้ (💩) ทั้งกระดาน เพื่อให้ Player Turn ถัดไปสามารถลงตำแหน่งใหม่ที่หมากของผู้เล่นนั้นสามารถวางได้
    def clear_truaj(self):
        for row in range(8):
            for col in range(8):
                self.board[row][col].config(state = 'disabled', text = '')

    # บนกระดานไม่มีตำแหน่งที่สามารถลงได้แล้ว (ไม่มี 💩) จะแสดง window สรุปผล
    def check_game_end(self):
        playavaiable = 0
        for row in range(8):
            for col in range(8):
                all_button = self.page3.grid_slaves(row = row, column = col)[0]
                info = all_button.cget("text")
                if info == '💩':
                    playavaiable += 1
        if playavaiable == 0:
            self.root = tk.Tk()
            self.root.geometry('350x200')
            self.check_amount()
            self.check_which_color_win()
            self.root.mainloop()
    
    # แสดงจำนวนหมากทั้ง 2 ฝ่าย และแสดงผลการแข่งขัน
    def check_amount(self):
        self.Black_count = 0
        self.White_count = 0
        self.black_win = False
        self.white_win = False
        self.tie = False
        for row in range(8):
            for col in range(8):
                button = self.page3.grid_slaves(row = row, column = col)[0]
                text = button.cget("text")
                if text == "Black_piece":
                    self.Black_count += 1
                elif text == "White_piece":
                    self.White_count += 1
        if self.Black_count > self.White_count:
            self.black_win = True
            return self.black_win
        elif self.Black_count < self.White_count:
            self.white_win = True
            return self.white_win
        else:
            self.tie = True
            return self.tie

    # จะมี ui แสดงข้อมูลต่างๆขึ้นในหน้าต่างจบเกม
    def check_which_color_win(self):
        self.convert_time()
        if self.black_win:
            show_b_win = tk.Label(self.root, font = ('@MS PGothic', 35), text = 'BLACK WINS!')
            show_b_win.place(relwidth = 1, y = 15)
                
        elif self.white_win:
            show_w_win = tk.Label(self.root, font = ('@MS PGothic', 35), text = 'WHITE WINS!')
            show_w_win.place(relwidth = 1, y = 15)

        elif self.tie:
            show_tie = tk.Label(self.root, font = ('@MS PGothic', 35), text = 'TIE!')
            show_tie.place(relwidth = 1, y = 15)

        score = tk.Label(self.root, text = f'Score Black : {self.Black_count} / Score White : {self.White_count}', font = ('@MS PGothic', 15))
        score.place(relwidth= 1, y = 77)

        time = tk.Label(self.root, text = self.time_text, font = ('@MS PGothic', 15))
        time.place(relwidth = 1, y = 110)

        restart_button = tk.Button(self.root, text = 'RESTART', width = 20, height = 1, command = lambda:[self.othello_board(), self.reset_time(), self.root.destroy()], bg = 'darkgray')
        restart_button. place(x = 12, y = 160)

        main_menu = tk.Button(self.root, text = 'MAIN MENU', width = 20, height = 1, command = lambda:[self.page1.tkraise(), self.deactivate_bot_basic(), self.deactivate_bot_pla(), self.deactivate_bot_im(), self.true_stop(), self.root.destroy(), self.destroy_ava_start_button()], bg = 'lightgray')
        main_menu. place(x = 187, y = 160)

    # นับหมากของผู้เล่นแบบ Real time
    def count_mhark(self):
        Black_count = 0
        White_count = 0
        for row in range(8):
            for col in range(8):
                button = self.page3.grid_slaves(row = row, column = col)[0]
                text = button.cget("text")
                if text == "Black_piece":   #⚫⚪
                    Black_count += 1
                elif text == "White_piece":
                    White_count += 1
        return self.Black_mhark.config(text = f"Black ⚫ : {Black_count}"), self.White_mhark.config(text = f"White ⚪ : {White_count}")

    def true_start_func(self):
        self.true_start = True

    def true_stop(self):
        self.true_start = False

    def create_ava_start_button(self):
        self.start_ava = tk.Button(self.page3, text = 'START', width = 20, command = lambda:[self.true_start_func()])
        self.start_ava.place(x = 730, y = 400)

    def destroy_ava_start_button(self):
        try:
            self.start_ava.place_forget()
        except:
            pass

    # นับเวลา จาก https://www.programiz.com/python-programming/time
    def nub_time(self):  
        self.converted = time.strftime("%H:%M:%S", time.gmtime(self.time_running))  # convert seconds to hour:minute:second
        self.time_display.set(self.converted) # change time display
        self.time_running += 1
        self.repeat_code = self.page3.after(1000, self.nub_time) # after 1 second repeat this function

    # แปลงให้เป็นหน่วย ชั่วโมง นาที วินาที
    def convert_time(self):
        
        second = self.time_running % 60
        minute = second // 60
        hour = minute // 60

        if hour < 10:
            hour = '0' + str(hour)
        if minute < 10:
            minute = '0' + str(minute)
        if second < 10:
            second = '0' + str(second)

        self.time_text = f'Time : {hour}:{minute}:{second}'

    # reset ให้เวลาเป็น 0 
    def reset_time(self):
        self.time_running = 0
        self.converted = time.strftime("%H:%M:%S", time.gmtime(self.time_running))
        self.time_display.set(self.converted)

    # โครงสร้าง
    def krongsang(self):

        # krongsang page1

        background1 = tk.Label(self.page1, image = self.img)
        background1.pack(pady = 40)

        modebutton = tk.Button(self.page1, height = 2, text = "SELECT MODE", command = lambda:[self.page2.tkraise()], width = 30, font = ('@MS PGothic', 10))
        modebutton.pack(pady = 40)

        quitbutton = tk.Button(self.page1, height = 1, text = "QUIT", command = self.quit, width = 30, font = ('@MS PGothic', 10))
        quitbutton.pack()

        # krongsang page2

        background2 = tk.Label(self.page2, image = self.img)
        background2.pack(pady = 40)

        PvPButton = Button(self.page2, text = "PLAYER VS PLAYER", command = lambda:[self.page3.tkraise(), self.othello_board(), self.reset_time(), self.deactivate_bot_basic(), self.deactivate_bot_pla(), self.deactivate_bot_im()], width = 30, font = ('@MS PGothic', 10))
        PvPButton.pack(pady = 15)

        PvAButton = Button(self.page2, text = "PLAYER VS BOT", command = lambda:[self.page4.tkraise()], width = 30, font = ('@MS PGothic', 10))
        PvAButton.pack(pady = 15)

        AvAButton = Button(self.page2, text = "BOT VS BOT", command = lambda:[self.page3.tkraise(), self.othello_board(), self.activate_bot_basic(), self.activate_bot_pla(), self.create_ava_start_button()], width = 30, font = ('@MS PGothic', 10))
        AvAButton.pack(pady = 15)

        backbutton2 = tk.Button(self.page2, text = 'BACK', width = 30, command = lambda:[self.page1.tkraise()], font = ('@MS PGothic', 10))
        backbutton2.pack(pady = 15)

        # krongsang page3

        backbutton3 = tk.Button(self.page3, text = 'BACK', bg = 'lightgray', font = ('@MS PGothic', 10), width = 30, command = lambda:[self.page2.tkraise(), self.deactivate_bot_basic(), self.deactivate_bot_pla(), self.deactivate_bot_im(), self.true_stop(), self.destroy_ava_start_button()])
        backbutton3.place(x = 700, y = 545)

        # restart button
        restartbutton = tk.Button(self.page3, text = "RESTART", bg = 'gray', font = ('@MS PGothic', 10), width = 20, command = lambda:[self.othello_board(), self.reset_time()])
        restartbutton.place(x = 730, y = 450)

        # แสดงจำนวนหมาก
        self.Black_mhark = tk.Label(self.page3, text = "Black :", bg = 'darkgray', font = ('@MS PGothic', 13))
        self.Black_mhark.place(x = 760, y = 140)

        self.White_mhark = tk.Label(self.page3, text = "White :", bg = 'darkgray', font = ('@MS PGothic', 13))              #😎
        self.White_mhark.place(x = 760, y = 200)

        # แสดง Turn ผู้เล่น
        self.Player_Turn = tk.Label(self.page3, font = ('@MS PGothic', 13), width = 20, height = 2)
        self.Player_Turn.place(x = 715, y = 300)

        # time label
        self.showtime = tk.Label(self.page3, textvariable = self.time_display, font = ('#ZF Terminal', 35), bg = 'darkgray')
        self.showtime.place(x = 715, y = 20)

        # krongsang page4

        background4 = tk.Label(self.page4, image = self.img)
        background4.pack(pady = 40)

        select_diff = tk.Label(self.page4, text = 'Choose BOT Difficulties', font = ('@MS PGothic', 16), bg = 'lightgreen')
        select_diff.pack(pady = 13)

        basic_button = tk.Button(self.page4, height = 1, text = 'BASIC', width = 30, command = lambda:[self.page3.tkraise(), self.othello_board(), self.reset_time(), self.activate_bot_basic()], font = ('@MS PGothic', 10))
        basic_button.pack(pady = 15)

        advance_button = tk.Button(self.page4, height = 1, text = 'ADVANCE', width = 30, command = lambda:[self.page3.tkraise(), self.othello_board(), self.reset_time(), self.activate_bot_pla()], font = ('@MS PGothic', 10))
        advance_button.pack(pady = 15)

        impossible_button = tk.Button(self.page4, height = 1, text = 'ไร้เทียมทาน', width = 30, command = lambda:[self.page3.tkraise(), self.othello_board(), self.reset_time(), self.activate_bot_im()], font = ('@MS PGothic', 10))
        impossible_button.pack(pady = 15)

        backbutton4 = tk.Button(self.page4, height = 1, text = 'BACK', width = 30, command = lambda:[self.page2.tkraise()], font = ('@MS PGothic', 10))
        backbutton4.pack(pady = 15)


if __name__ == "__main__":
    main()
