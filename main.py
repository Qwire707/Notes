
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit,\
    QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout
import json

# notes = {
#     'природа':{
#         "текст": "Певний текст замітки про природу",
#         "теги": ['дерева', "гриби", "кущі"]
#     }
# }

# with open ('notes_data.json', 'w',  encoding='utf-8') as file:
#     json.dump(notes, file)

style = '''
QWidget {
    background-color: rgb(123, 7, 173);
}
QLabel {
    color: rgb(123, 7, 173);
    font-size: 10pt;
    font-weight: bold;
}
QTextEdit {
    background-color: rgb(64, 0, 123);
    color: red;
    font-size: 15px;
    border-radius: 15px
}
QPushButton {
    background-color: rgb(0, 56, 123);
    border-radius: 4px;
    
}
QLineEdit {
    background-color: rgb(64, 0, 123);
    border-radius: 4px;
    font-weight: bold;
}
QListWidget {
    background-color: rgb(64, 0, 123);
}
'''

app = QApplication([])#створення додатку 
app.setStyleSheet(style)

window = QWidget()#створення вiкна
window.setWindowTitle("Розумнi замiтки")#створення заголовка
window.resize(900, 600)#розміри выкна

#створення віджетiв 
field_text = QTextEdit()

lbl_list_notes = QLabel("Список замiток")

list_notes = QListWidget()

btn_create_note = QPushButton("Створити замiтку")
btn_del_note = QPushButton("Видалити замiтку")
btn_save_note = QPushButton("Зберегти замiтку")

lbl_list_tags = QLabel("Список тегiв")
list_tags = QListWidget()
input_tag = QLineEdit()
input_tag.setPlaceholderText("Введіть тег...")

btn_add_tag = QPushButton("Додати до замiток")
btn_del_tag = QPushButton("Вiдкрiпити вiд замiток")
btn_search_note = QPushButton("Шукати замiтки по тегу")

#створення лiнiй
col1 = QVBoxLayout()
col1.addWidget(field_text)

col2 = QVBoxLayout()
col2.addWidget(lbl_list_notes)
col2.addWidget(list_notes)

line1 = QHBoxLayout()
line1.addWidget(btn_create_note)
line1.addWidget(btn_del_note)

col2.addLayout(line1)
col2.addWidget(btn_save_note)
col2.addWidget(lbl_list_tags)
col2.addWidget(list_tags)
col2.addWidget(input_tag)

line2 = QHBoxLayout()
line2.addWidget(btn_add_tag)
line2.addWidget(btn_del_tag)

col2.addLayout(line2)
col2.addWidget(btn_search_note)

main_line = QHBoxLayout()
main_line.addLayout(col1)
main_line.addLayout(col2)

window.setLayout(main_line)

def show_note():
    '''функцiя для показу замiтки'''
    name = list_notes.selectedItems()[0].text()#отримуємо назву замітки
    field_text.setText(notes[name]['текст'])#відображаемо текст замітки
    list_tags.clear()#чистимо список тегів
    list_tags.addItems(notes[name]['теги'])#відображаємо теги

def create_note():
    '''зробити замітку'''
    note_name, ok = QInputDialog.getText(window, "Додати замітку", "Назва замітки")
    if ok and note_name != '':
        notes[note_name] = {'текст': '', 'теги': []}
        list_notes.addItem(note_name)

def del_note():
    '''видалити замітку'''
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        del notes[name]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open ('notes_data.json', 'w') as file:
            json.dump(notes, file)
    else:
        print('Замiтка не вибрана')        

def save_note():
    '''зберігання заміток'''
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        notes[name]['текст'] = field_text.toPlainText()
        with open ('notes_data.json', 'w') as file:
            json.dump(notes, file)
    else:
        print('Замiтка не вибрана')

def add_tag():
    '''додавання тега'''
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        tag = input_tag.text()
        if not tag in notes[name]['теги']:
            notes[name]['теги'].append(tag)
            list_tags.addItem(tag)
            input_tag.clear()
        with open ('notes_data.json', 'w') as file:
                json.dump(notes, file)
    else:
        print('Замiтка не вибрана')

def del_tag():
    '''видалення тега'''
    if list_tags.selectedItems():
        name = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[name]['теги'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[name]['теги'])
        with open ('notes_data.json', 'w') as file:
                json.dump(notes, file)
    else:
        print('тег не вибрано')

def search_note():
    '''пошук замітки по тегу'''
    tag = input_tag.text()
    if tag and btn_search_note.text() == "Шукати замiтки по тегу":
        notes_filtred = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtred[note] = notes[note]
        btn_search_note.setText('Скинути пошук')
        list_tags.clear()
        list_notes.clear()
        list_notes.addItems(notes_filtred)
    elif btn_search_note.text() == 'Скинути пошук':
        input_tag.clear() 
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        btn_search_note.setText("Шукати замiтки по тегу")

#пiдключення кнопок
list_notes.itemClicked.connect(show_note)
btn_create_note.clicked.connect(create_note)
btn_del_note.clicked.connect(del_note)
btn_save_note.clicked.connect(save_note)
btn_add_tag.clicked.connect(add_tag)
btn_del_tag.clicked.connect(del_tag)
btn_search_note.clicked.connect(search_note)

with open('notes_data.json', 'r') as file:
    notes = json.load(file)
list_notes.addItems(notes)

window.show()  #показуэмо вiкно
app.exec_()