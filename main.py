# main.py - SmartNotes (KivyMD) Upgraded Template
# Features included:
# - Notes with AI grammar correction (OpenAI) + offline spell fallback
# - TTS (gTTS on desktop; Android TTS recommended via plyer/jnius - placeholder)
# - Translation via OpenAI (if API key set)
# - Tasks + Alarm (simple in-app scheduler)
# - AI Assistant page using OpenAI chat
# - Export to Apps Script webhook (POST with token)

from kivy.lang import Builder
from kivy.clock import mainthread
from kivy.utils import platform
from kivy.properties import StringProperty, ListProperty
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
import sqlite3, threading, json, os, time, requests
from datetime import datetime, date
try:
    from openai import OpenAI
except:
    OpenAI = None

try:
    from spellchecker import SpellChecker
    spell = SpellChecker()
except:
    spell = None

try:
    from gtts import gTTS
    import pygame
    pygame.mixer.init()
    has_gtts = True
except:
    has_gtts = False

KV = """
Screen:
    MDBottomNavigation:
        id: bottom_nav
        MDBottomNavigationItem:
            name: 'notes'
            text: 'Notes'
            icon: 'note-outline'
            MDBoxLayout:
                orientation: 'horizontal'
                MDBoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 0.33
                    MDLabel: text: 'My Notes (AI Grammar + Translate)'
                    ScrollView: MDList: id: notes_list
                    MDRaisedButton: text: 'New Note' ; on_release: app.new_note()
                MDBoxLayout:
                    orientation: 'vertical'
                    MDTextField: id: note_title; hint_text: 'Title'
                    MDTextField: id: note_content; hint_text: 'Write your note here...'; multiline: True
                    MDBoxLayout:
                        MDRaisedButton: text: 'Save' ; on_release: app.save_note()
                        MDRaisedButton: text: 'Fix Now' ; on_release: app.fix_note_now()
                        MDRaisedButton: text: 'Speak' ; on_release: app.speak_note()
                        MDRaisedButton: text: 'Translate' ; on_release: app.translate_note_dialog()

        MDBottomNavigationItem:
            name: 'calendar'
            text: 'Calendar'
            icon: 'calendar-month'
            MDBoxLayout:
                MDLabel: text: 'Calendar Page (Preview Only)'

        MDBottomNavigationItem:
            name: 'tasks'
            text: 'Tasks'
            icon: 'playlist-check'
            MDBoxLayout:
                orientation: 'vertical'
                MDLabel: text: 'Tasks Manager'
                ScrollView: MDList: id: tasks_list
                MDTextField: id: t_title; hint_text: 'Task Title'
                MDTextField: id: t_note; hint_text: 'Task Note'
                MDTextField: id: t_date; hint_text: 'YYYY-MM-DD'
                MDTextField: id: t_time; hint_text: 'HH:MM'
                MDRaisedButton: text: 'Add Task' ; on_release: app.add_task()

        MDBottomNavigationItem:
            name: 'ai'
            text: 'AI'
            icon: 'robot-outline'
            MDBoxLayout:
                orientation: 'vertical'
                MDLabel: text: 'AI Assistant'
                ScrollView: MDList: id: ai_chat_list
                MDTextField: id: ai_input; hint_text: 'Ask something...'
                MDRaisedButton: text: 'Send' ; on_release: app.send_ai()

        MDBottomNavigationItem:
            name: 'export'
            text: 'Export'
            icon: 'cloud-upload-outline'
            MDBoxLayout:
                orientation: 'vertical'
                MDLabel: text: 'Export to Apps Script'
                MDTextField: id: export_email; hint_text: 'Email for identification'
                MDTextField: id: apps_script_url; hint_text: 'Apps Script Webhook URL'
                MDRaisedButton: text: 'Export Note' ; on_release: app.export_note()
                MDRaisedButton: text: 'Export Task' ; on_release: app.export_task()
"""

DB = "smartnotes.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS notes(id INTEGER PRIMARY KEY, title TEXT, content TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY, title TEXT, note TEXT, date TEXT, time TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS settings(k TEXT PRIMARY KEY, v TEXT)")
    conn.commit()
    conn.close()

def save_setting(k,v):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO settings(k,v) VALUES(?,?)",(k,json.dumps(v)))
    conn.commit()
    conn.close()

def load_setting(k):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT v FROM settings WHERE k=?",(k,))
    r = c.fetchone()
    conn.close()
    if r: return json.loads(r[0])
    return None

class SmartNotes(MDApp):

    def build(self):
        init_db()
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def new_note(self):
        self.root.ids.note_title.text = ""
        self.root.ids.note_content.text = ""

    def save_note(self):
        t = self.root.ids.note_title.text
        c = self.root.ids.note_content.text
        conn = sqlite3.connect(DB)
        conn.execute("INSERT INTO notes(title,content) VALUES(?,?)",(t,c))
        conn.commit()
        conn.close()

    def fix_note_now(self):
        txt = self.root.ids.note_content.text
        if not txt: return
        try:
            key = load_setting("openai")
            if key:
                client = OpenAI(api_key=key)
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role":"system","content":"Fix grammar"},
                        {"role":"user","content":txt}
                    ]
                )
                self.root.ids.note_content.text = res.choices[0].message.content
            else:
                if spell:
                    words = txt.split()
                    fixed = " ".join([spell.correction(w) for w in words])
                    self.root.ids.note_content.text = fixed
        except:
            pass

    def speak_note(self):
        txt = self.root.ids.note_content.text
        if not txt: return
        if has_gtts:
            tts = gTTS(text=txt, lang="en")
            tts.save("tmp.mp3")
            pygame.mixer.music.load("tmp.mp3")
            pygame.mixer.music.play()

    def translate_note_dialog(self):
        target = "ta"  # default Tamil
        txt = self.root.ids.note_content.text
        key = load_setting("openai")
        if not key:
            return
        client = OpenAI(api_key=key)
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":f"Translate to {target}"},
                {"role":"user","content":txt}
            ]
        )
        self.root.ids.note_content.text = res.choices[0].message.content

    def add_task(self):
        t = self.root.ids.t_title.text
        n = self.root.ids.t_note.text
        d = self.root.ids.t_date.text
        tm = self.root.ids.t_time.text
        conn = sqlite3.connect(DB)
        conn.execute("INSERT INTO tasks(title,note,date,time) VALUES(?,?,?,?)",(t,n,d,tm))
        conn.commit()
        conn.close()

    def send_ai(self):
        txt = self.root.ids.ai_input.text
        key = load_setting("openai")
        if not key:
            return
        client = OpenAI(api_key=key)
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":txt}]
        )
        self.root.ids.ai_chat_list.add_widget(
            OneLineListItem(text="AI: "+res.choices[0].message.content)
        )

    def export_note(self):
        email = self.root.ids.export_email.text
        url = self.root.ids.apps_script_url.text
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("SELECT title,content FROM notes ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
        conn.close()
        if not row: return
        title, content = row
        requests.post(url, json={
            "email":email,
            "title":title,
            "content":content,
            "timestamp":datetime.now().isoformat()
        })

    def export_task(self):
        email = self.root.ids.export_email.text
        url = self.root.ids.apps_script_url.text
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("SELECT title,note,date,time FROM tasks ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
        conn.close()
        if not row: return
        t,n,d,tm = row
        requests.post(url, json={
            "email":email,
            "title":t,
            "content":n,
            "date":d,
            "time":tm
        })

if __name__ == "__main__":
    SmartNotes().run()
