import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from pathlib import Path
import random

class AnagramsGame(toga.App):
    num_words=0
    word_length_min=3
    word_length_max=4
    score=0
    dictionary_filename='popular.txt'
    dictionary=[]
    word='test'
    scrambled_word='stet'
    value=1
    success=True
    step=0
    table_data=[]
    def startup(self):
        self.resources_folder = Path(__file__).joinpath('../resources').resolve()
        self.dictionary_filepath = self.resources_folder.joinpath(self.dictionary_filename)
        with open(self.dictionary_filepath,'r') as f:
            self.dictionary=f.readlines()
        self.num_words=len(self.dictionary)
        
        self.main_box=toga.Box(style=Pack(direction=COLUMN, padding=5))
        lbl_fontlabel = toga.Label("Font size:",style=Pack(padding=(5,0)))
        self.lbl_fontsize = toga.Label("10",style=Pack(padding=5))
        btn_reduce_size = toga.Button(
            " - ", on_press=self.reduce_fontsize, style=Pack(width=40)
        )
        btn_increase_size = toga.Button(
            " + ", on_press=self.increase_fontsize, style=Pack(width=40)
        )
        font_box = toga.Box(
            children=[
                lbl_fontlabel,
                btn_reduce_size,
                self.lbl_fontsize,
                btn_increase_size,
            ],
            style=Pack(direction=ROW),
        )
        num_words_label=toga.Label(
            'Dictionary words: {:d}'.format(self.num_words),
            style=Pack(padding=(5, 15))
        )
        word_min_length_label=toga.Label(
            'Word length min: ',
            style=Pack(padding=(5, 0))
        )
        word_max_length_label=toga.Label(
            'max: ',
            style=Pack(padding=(5, 0))
        )
        self.word_min_length_input = toga.NumberInput(style=Pack(flex=1,padding=(5, 15)),default=self.word_length_min,on_change=self.set_word_length_min)
        self.word_max_length_input = toga.NumberInput(style=Pack(flex=1,padding=(5, 15)),default=self.word_length_max,on_change=self.set_word_length_max)
        config_box=toga.Box(style=Pack(direction=ROW, padding=5))
        config_box.add(font_box)
        config_box.add(num_words_label)
        config_box2=toga.Box(style=Pack(direction=ROW, padding=5))
        config_box2.add(word_min_length_label)
        config_box2.add(self.word_min_length_input)
        config_box2.add(word_max_length_label)
        config_box2.add(self.word_max_length_input)
        self.console_box=toga.Table(headings=['Step','Score','Letters','Guess'],data=self.table_data,style=Pack(
                flex=1,
                padding_right=5,
                font_family="monospace",
                font_size=int(self.lbl_fontsize.text),
            ))
        guess_label = toga.Label(
            'Your guess: ',
            style=Pack(padding=(5, 0))
        )
        self.guess_input = toga.TextInput(style=Pack(flex=1,padding=(5, 15)),on_lose_focus=self.guess_input_lose,on_gain_focus=self.guess_input_gain)
        guess_box = toga.Box(style=Pack(direction=ROW, padding=5))
        guess_box.add(guess_label)
        guess_box.add(self.guess_input)
        guess_button = toga.Button(
            'Submit',
            on_press=self.apply_guess,
            style=Pack(direction=ROW, padding=5,flex=1)
        )
        shuffle_button = toga.Button(
            'Shuffle',
            on_press=self.apply_shuffle,
            style=Pack(direction=ROW, padding=5,flex=1)
        )
        solve_button = toga.Button(
            'Solve',
            on_press=self.apply_solve,
            style=Pack(direction=ROW, padding=5,flex=1)
        )
        other_box=toga.Box(style=Pack(direction=ROW, padding=5))
        other_box.add(guess_button)
        other_box.add(shuffle_button)
        other_box.add(solve_button)
        self.main_box.add(config_box)
        self.main_box.add(config_box2)
        self.main_box.add(guess_box)
        self.main_box.add(other_box)
        self.main_box.add(self.console_box)
        # shuffle_button = toga.Button(
            # 'Shuffle',
            # on_press=self.shuffle,
            # style=Pack(direction=ROW, padding=5)
        # )
        # answer_button = toga.Button(
            # 'Give up',
            # on_press=self.answer,
            # style=Pack(direction=ROW, padding=5)
        # )
        # button_box = toga.Box(style=Pack(direction=COLUMN))
        # button_box.add(guess_box)
        # button_box.add(guess_button)
        # button_box.add(shuffle_button)
        # button_box.add(answer_button)
        # main_box.add(button_box)
        
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()
        
        self.run_step()
        
    def set_word_length_min(self,widget):
        if self.word_min_length_input.value<1: self.word_min_length_input.value=1
        if self.word_min_length_input.value>self.word_max_length_input.value: self.word_min_length_input.value=self.word_max_length_input.value
        self.word_length_min=self.word_min_length_input.value
    def set_word_length_max(self,widget):
        if self.word_max_length_input.value<1: self.word_max_length_input.value=1
        if self.word_max_length_input.value<self.word_min_length_input.value: self.word_max_length_input.value=self.word_min_length_input.value
        self.word_length_max=self.word_max_length_input.value
    
    # def update_guess(self, widget):
        # guess=self.guess_input.value
        # if guess[-1]=='\n':
            # self.guess_input.value=guess[:-1]
            # self.apply_guess_action()
            # self.guess_input.focus()
            
    
    def guess_input_lose(self,widget):
        self.main_window.show()
    
    def guess_input_gain(self,widget):
        self.main_window.show()
    
    def apply_guess(self, widget):
        self.apply_guess_action()
        self.guess_input.focus()
    
    def apply_guess_action(self):
        guess=self.guess_input.value
        self.guess_input.value=''
        if self.anagrams(guess,self.word):
            if guess==self.word:
                self.score=self.score+self.value
                self.console_box.data.remove(self.console_box.data[-1])
                self.console_box.data.insert(0,'{:d}'.format(self.step+1),'{:.2f}'.format(self.score),self.scrambled_word,guess)
                self.value=1
                self.run_step()
            elif guess+'\n' in self.dictionary:
                self.console_box.data.remove(self.console_box.data[-1])
                self.console_box.data.insert(0,'{:d}'.format(self.step+1),'{:.2f}'.format(self.score),self.scrambled_word,self.word)
                self.score=self.score+self.value
                self.console_box.data.insert(0,'{:d}'.format(self.step+1),'{:.2f}'.format(self.score),self.scrambled_word,guess)
                self.value=1
                self.run_step()
            else:
                self.console_box.data.remove(self.console_box.data[-1])
                self.console_box.data.insert(0,'{:d}'.format(self.step+1),'{:.2f}'.format(self.score),self.scrambled_word,guess)
                self.console_box.data.insert(0,'{:d}'.format(self.step+1),'{:.2f}'.format(self.score),self.scrambled_word,'')
                self.value=self.value/2
    
    def apply_shuffle(self, widget):
        self.scramble_word()
        self.console_box.data.insert(0,'{:d}'.format(self.step+1),'{:.2f}'.format(self.score),self.scrambled_word,'')
        self.guess_input.focus()
    
    def apply_solve(self, widget):
        self.console_box.data.remove(self.console_box.data[-1])
        self.console_box.data.insert(0,'{:d}'.format(self.step+1),'{:.2f}'.format(self.score),self.scrambled_word,self.word)
        self.run_step()
        self.value=1
        self.guess_input.focus()
    
    def anagrams(self,s1,s2):
        return [False, True][sum([ord(x) for x in s1]) == sum([ord(x) for x in s2])]
    
    def choose_word(self):
        self.word=random.choice(self.dictionary)
        self.word=self.word[:-1]
        while len(self.word)>self.word_length_max or len(self.word)<self.word_length_min:
            self.word=random.choice(self.dictionary)
            self.word=self.word[:-1]
    
    def scramble_word(self):
        self.scrambled_word=list(self.word)
        random.shuffle(self.scrambled_word)
        self.scrambled_word=''.join(self.scrambled_word)
        while self.scrambled_word in self.dictionary:
            self.scrambled_word=list(self.word)
            random.shuffle(self.scrambled_word)
            self.scrambled_word=''.join(self.scrambled_word)
        
    
    def run_step(self):
        self.choose_word()
        self.scramble_word()
        self.step=self.step+1
        self.console_box.data.insert(0,'{:d}'.format(self.step+1),'{:.2f}'.format(self.score),self.scrambled_word,'')
    
    def reduce_fontsize(self, widget):
        font_size = int(self.lbl_fontsize.text) - 1
        self.lbl_fontsize.text = str(font_size)
        font = toga.Font("monospace", font_size)
        self.console_box._impl.set_font(font)

    def increase_fontsize(self, widget):
        font_size = int(self.lbl_fontsize.text) + 1
        self.lbl_fontsize.text = str(font_size)
        font = toga.Font("monospace", font_size)
        self.console_box._impl.set_font(font)
    

def main():
    return AnagramsGame()
