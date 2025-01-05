from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,
                            QListWidget, QInputDialog, QHBoxLayout, QVBoxLayout,
                            QFormLayout, QLineEdit, QTextEdit)

app = QApplication([])

notes = []

notes_win = QWidget()
notes_win.setWindowTitle('Smart Notes')
notes_win.resize(800, 600)

list_notes = QListWidget()
list_notes_label = QLabel('Список заміток:')

button_note_create = QPushButton('Створити замітку')
button_note_del = QPushButton('Видалити замітку')
button_note_save = QPushButton('Зберегти замітку')

field_taq = QLineEdit()
field_taq.setPlaceholderText('Введіть тег...')

field_text = QTextEdit()

button_taq_add = QPushButton('Додати тег')
button_taq_del = QPushButton('Видалити тег')
button_taq_search = QPushButton('Пошук тегів')

list_tags = QListWidget()
list_tags_label = QLabel('Список тегів')

layout_notes = QHBoxLayout()

col1 = QVBoxLayout()
col1.addWidget(field_text)

col2 = QVBoxLayout()
col2.addWidget(list_notes_label)
col2.addWidget(list_notes)

row1 = QHBoxLayout()
row1.addWidget(button_note_create)
row1.addWidget(button_note_del)

row2 = QHBoxLayout()
row2.addWidget(button_note_save)

col2.addLayout(row1)
col2.addLayout(row2)

col2.addWidget(list_tags_label)
col2.addWidget(list_tags)
col2.addWidget(field_taq)

row3 = QHBoxLayout()
row3.addWidget(button_taq_add)
row3.addWidget(button_taq_del)

row4 = QHBoxLayout()
row4.addWidget(button_taq_search)

col2.addLayout(row3)
col2.addLayout(row4)

layout_notes.addLayout(col1, stretch=2)
layout_notes.addLayout(col2, stretch=1)
notes_win.setLayout(layout_notes)

def show_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        print(key)
        for note in notes:
            if note[0] == key:
                field_text.setText(note[1])
                list_tags.clear()
                list_tags.addItems(note[2])
            else:
                print('Замітки не знайдено')

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'Додати замітку', 'Введіть назву замітки')
    if ok and note_name != "":
        note = [note_name, '', []]
        notes.append(note)
        list_notes.addItem(note[0])
        list_tags.addItem(note[2])
        print(notes)
        with open(str(len(notes)) + '.txt', 'w') as file:
            file.write(note[0] + '\n')
            
def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        index = 0 
        for note in notes:
            if note[0] == key:
                note[1] = field_text.toPlainText()
                with open(str(index) + '.txt', 'w') as file:
                    file.write(note[0] + '\n')
                    file.write(note[1] + '\n')
                    for tag in note[2]:
                        file.write(tag + '\n')
                    file.write('\n')
            index += 1
        print(notes)
    else:
        print('Замітка не вибрана!')

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        for note in notes:
            if note[0] == key:
                notes.remove(note)
                list_notes.addItems([note][0][0] for note in notes)
                clear_note_fields()
                save_note_to_file()
    else:
        print('Замітка не обрана!')

def clear_note_fields():
    field_text.clear()
    list_notes.clear()
    list_tags.clear()
    field_taq.clear()

def save_note_to_file():
    for index, note in enumerate(notes):
        filename = f'{index}.txt'
        with open(filename, 'w') as file:
            file.write(note[0] + '\n')
            file.write(note[1] + '\n')
            for tag in note[2]:
                file.write(tag + '\n')
            file.write('\n')

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        for note in notes:
            if notes[0] == key:
                tag, ok = QInputDialog.getText(notes_win, 'Додати тег', 'Введіть назву тегу:')
                if ok and tag != "":
                    note[2].append(tag)
                    list_tags.addItem(tag)
                    save_note()
    else:
        print('Замітка не вибрана!')

def del_tag():
    if list_notes.selectedItems() and list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        for note in notes:
            if note[0] == key and tag in note[2]:
                note[2].remove(tag)
                list_tags.clear()
                list_tags.addItems(note[2])
                save_note()
                break
    else:
        print('Тег не обрано')
    
def search_tag():
    tag, ok = QInputDialog.getText(notes_win, 'Пошук тегів', 'Назва тегу')
    if ok and tag != '':
        matching_notes = [note[0] for note in notes if tag in note [2]]
        list_notes.clear()
        list_notes.addItems(matching_notes)
    else:
        print('Тегів не обрано!')

list_notes.itemClicked.connect(show_note)

button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)

button_taq_add.clicked.connect(add_tag)
button_taq_del.clicked.connect(del_tag)
button_taq_search.clicked.connect(search_tag)

notes_win.show()

name = 0
note = []

print(notes)
for note in notes:
    list_notes.addItem(note[0])

app.exec_()