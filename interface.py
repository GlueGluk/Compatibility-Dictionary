import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from random import randint
import os
import pymorphy2
import re

class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.prepareData()
        
    def Run(self):
        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        
        qle = QLineEdit()
        qle.textChanged[str].connect(self.textInput)
        hbox.addWidget(qle)
        
        sb = QPushButton('Найти')
        sb.setCheckable(False)
        sb.setAutoFillBackground(True)
        self.button = sb
        sb.clicked.connect(self.SearchButton)
        hbox.addWidget(sb)
        vbox.addLayout(hbox)
        
        hbox = QHBoxLayout()
        self.list = QListWidget()
        self.list.itemClicked.connect(self.openContext)
        hbox.addWidget(self.list)
        self.listplace = hbox
        vbox.addLayout(hbox)
        
        self.setWindowTitle('Словарь сочетаемости')
        self.move(800, 0)
        self.show()
        return 1
        
    def textInput(self, text):
        self.WordToSearch = text
    
    def SearchButton(self):
    #    palette = self.button.palette()
    #    role = self.button.foregroundRole()
    #    palette.setColor(role, QColor('red'))
    #    colors = ['red', 'blue', 'green', 'black', 'white', 'yellow', 'purple', 'cian', 'orange']
    #    n = randint(0, 8)
    #    self.button.setStyleSheet("background-color: " + colors[n])
        self.SearchResults()
        self.show()
    
    def SearchResults(self):
        self.listplace.removeWidget(self.list)
        self.list = QListWidget()
        self.listplace.addWidget(self.list)
        self.FoundNoun = ''
        self.FoundVerb = ''
        if not self.WordToSearch:
            item = QListWidgetItem()
            item.setText('Введите слово для поиска!')
            font = QFont()
            font.setBold(True)
            item.setFont(font)
            self.list.addItem(item)
            return
        if ' ' in self.WordToSearch:
            item = QListWidgetItem()
            item.setText('Введите не более одного слова!')
            font = QFont()
            font.setBold(True)
            item.setFont(font)
            self.list.addItem(item)
            return
        morph = pymorphy2.MorphAnalyzer()
        word = self.WordToSearch.lower()
        parsed = morph.parse(word)
        noun = 0
        found = ''
        for p in parsed:
            if ('NOUN' in p.tag):
                found = p.normal_form
                noun = 1
                break
            if (('VERB' in p.tag) or ('INFN' in p.tag)):
                found = p.normal_form
                break
        if not found:
            item = QListWidgetItem()
            item.setText('Введите глагол или существительное!')
            font = QFont()
            font.setBold(True)
            item.setFont(font)
            self.list.addItem(item)
            return
        else:
            if noun:
                if (self.SearchNouns.get(found)):
                    self.FoundNoun = found
                    for v in sorted(self.SearchNouns[found].items(), key=lambda k_v: k_v[1]['amount'], reverse=True):
                        self.list.addItem(v[0])
                else:
                    item = QListWidgetItem()
                    item.setText('Не найдено')
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                    self.list.addItem(item)
                    return
            else:
                if (self.SearchVerbs.get(found)):
                    self.FoundVerb = found
                    for n in sorted(self.SearchVerbs[found].items(), key=lambda k_v: k_v[1]['amount'], reverse=True):
                        self.list.addItem(n[0])
                else:
                    item = QListWidgetItem()
                    item.setText('Не найдено')
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                    self.list.addItem(item)
                    return
            self.list.itemClicked.connect(self.openContext)
            
   
    def openContext(self, item):
        if (self.FoundVerb):
            self.openContextWindow(self.SearchVerbs[self.FoundVerb][item.text()]['context'], item.text())
        elif (self.FoundNoun):
            self.openContextWindow(self.SearchNouns[self.FoundNoun][item.text()]['context'], item.text())
        print(item.text())
        
    def openContextWindow(self, context, word):
        win = QDialog()
        vbox = QVBoxLayout(win)
        l = QListWidget()
        for c in set(context):
            l.addItem(c)
        vbox.addWidget(l)
        win.setWindowTitle('Контекст')
        win.setWindowModality(Qt.ApplicationModal)
        win.show()
        win.exec_()
        return
        
    def prepareData(self):
        self.SearchNouns = {};
        self.SearchVerbs = {};
        files = os.listdir('./1/cont_res')
        for f in files:
            print (f)
            fc = open('./1/cont_res/'+f)
            templ = fc.readline()
            m = re.search(r'N1\<([^\s,\>]*).*\>', templ)
            if m:
                noun = m.group(1)
                for line in fc:
                    print(line)
                    l = line.split(' : ', maxsplit=1)
                    print(l)
                    verb = l[0]
                    cont = l[1]
                    cont = cont[:-1]
                    if (self.SearchNouns.get(noun)):
                        if (self.SearchNouns[noun].get(verb)):
                            self.SearchNouns[noun][verb]['amount'] += 1
                            self.SearchNouns[noun][verb]['context'].append(cont)
                        else:
                            d = {'amount' : 1, 'context' : [cont]}
                            self.SearchNouns[noun].update([(verb, d)])
                    else:
                        d1 = {'amount' : 1, 'context' : [cont]}
                        d2 = {verb : d1}
                        self.SearchNouns.update([(noun, d2)])
                    if (self.SearchVerbs.get(verb)):
                        if (self.SearchVerbs[verb].get(noun)):
                            self.SearchVerbs[verb][noun]['amount'] += 1
                            self.SearchVerbs[verb][noun]['context'].append(cont)
                        else:
                            d = {'amount' : 1, 'context' : [cont]}
                            self.SearchVerbs[verb].update([(noun, d)])
                    else:
                        d1 = {'amount' : 1, 'context' : [cont]}
                        d2 = {noun : d1}
                        self.SearchVerbs.update([(verb, d2)])
        
app = QApplication(sys.argv)
obj = Interface()
obj.Run()
app.exec_()