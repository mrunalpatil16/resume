import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from backend import rank_multiple_resumes

selected_files = []
jd_file = ""

# ---------------- Resume Upload ---------------- #
def browse_files():
    global selected_files
    selected_files = list(filedialog.askopenfilenames(
        title="Select Resumes",
        filetypes=[("PDF Files", "*.pdf")]
    ))

    if selected_files:
        file_label.config(text=f"{len(selected_files)} resumes selected", bootstyle="info")

# ---------------- JD Upload ---------------- #
def browse_jd():
    global jd_file
    jd_file = filedialog.askopenfilename(
        title="Select Job Description",
        filetypes=[("PDF Files", "*.pdf"), ("Text Files", "*.txt")]
    )

    if jd_file:
        jd_label.config(text="Job Description Uploaded", bootstyle="info")

# ---------------- Analyze ---------------- #
def analyze_resumes():
    if not selected_files:
        result_label.config(text="Please upload resumes!", bootstyle="danger")
        return

    if not jd_file:
        result_label.config(text="Please upload Job Description file!", bootstyle="danger")
        return

    rankings = rank_multiple_resumes(selected_files, jd_file)

    result_text = "📊 Resume Ranking:\n\n"
    for i, (name, score) in enumerate(rankings, start=1):
        result_text += f"{i}. {name} → {score}%\n"

    result_label.config(text=result_text, bootstyle="success")


# ---------------- UI ---------------- #
app = tb.Window(title="MatchMyResume", themename="darkly", size=(900, 900))

tb.Label(app, text="🔍📑 MatchMyResume",
         font=("Times New Roman", 26, "bold")).pack(pady=20)

# Resume Upload
tb.Button(app, text="Upload Resumes",
          bootstyle="info-outline",
          command=browse_files).pack(pady=10)

file_label = tb.Label(app, text="No resumes selected")
file_label.pack()

# JD Upload
tb.Button(app, text="Upload Job Description",
          bootstyle="warning-outline",
          command=browse_jd).pack(pady=20)

jd_label = tb.Label(app, text="No Job Description uploaded")
jd_label.pack()

# Analyze Button
tb.Button(app, text="Analyze & Rank Resumes",
          bootstyle="success",
          command=analyze_resumes).pack(pady=30)

result_label = tb.Label(app, text="", font=("Times New Roman", 14), justify="left")
result_label.pack(pady=20)

app.mainloop()
