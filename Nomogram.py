import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.simpledialog import askstring
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

def se(k, d, ml, ms):
    if ml / ms >= 10:
        return (k * (d ** 3)) / (1 / ms - 1 / ml)
    else:
        return (k * (d ** 3)) / ms

def plt_size_line(ax, d, m_max=10**5, k=1):
    ax.plot([10**0, m_max], [se(k, d, 10**0, 10**0), se(k, d, m_max, m_max)], label=d)

def plt_mass_red(ax, k, d, ml, ms, s, error):
    se0, se1 = se(k, d, ml, ml), se(k, d, ms, ms)
    ax.plot([ml, ms], [se0, se1], color='black', marker='o')
    if s == 1:
        ax.annotate(s, (ml + 0.1 * ml, se0 + 0.5 * se0), fontsize=10)
    ax.annotate(s, (ms + 0.1 * ms, se1 + 0.5 * se1), fontsize=10)
    error.append(se1)
    return s + 1

def plt_size_red(ax, k0, k1, d0, d1, ml, ms, s):
    se0, se1 = se(k0, d0, ml, ms), se(k1, d1, ml, ms)
    ax.plot([ml, ms], [se0, se1], color='black', marker='o')
    if s == 1:
        ax.annotate(s, (ms + 0.1 * ms, se0 + 0.5 * se0), fontsize=10)
    ax.annotate(s, (ms + 0.1 * ms, se1 + 0.5 * se1), fontsize=10)
    return s + 1

def plot_data(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_yscale('log')
    ax.set_ylabel('Fundamental error (σ²)', fontsize=12)
    ax.set_xscale('log')
    ax.set_xlabel('Sample mass (g)', fontsize=12)
    ax.grid(linestyle='--', alpha=0.5, which='both')
    ax.set_title('Sampling protocol', fontsize=12)

    unique_d, indexes = np.unique(df['d'], return_index=True)
    argsort = np.flip(np.argsort(unique_d))
    unique_d = unique_d[argsort]
    indexes = indexes[argsort]
    for d, idx in zip(unique_d, indexes):
        plt_size_line(ax, d, m_max=10**5, k=df.loc[idx, 'k'])

    error = []
    s = 1
    for idx in range(1, df.shape[0]):
        if df.loc[idx, 'ml'] > df.loc[idx, 'ms']:
            s = plt_mass_red(ax, k=df.loc[idx, 'k'], d=df.loc[idx, 'd'], ml=df.loc[idx, 'ml'], ms=df.loc[idx, 'ms'], s=s, error=error)

        if df.loc[idx, 'd'] < df.loc[idx - 1, 'd']:
            s = plt_size_red(ax, k0=df.loc[idx - 1, 'k'], k1=df.loc[idx, 'k'], d0=df.loc[idx - 1, 'd'], d1=df.loc[idx, 'd'], ml=df.loc[idx, 'ml'], ms=df.loc[idx, 'ms'], s=s)

    ax.legend(bbox_to_anchor=(1.06, 1), loc='upper left', frameon=False, title='Top sizes (cm):')
    text = '''
    σ²: {}
    σ: {}
    '''.format(round(np.sum(error), 5), round(np.sqrt(np.sum(error)), 5))
    ax.annotate(text, xycoords='axes fraction', xy=(0.02, 0), fontsize=12)

    plt.tight_layout()

    return fig

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            df = pd.read_csv(file_path)
            if not all(elem in df.columns for elem in ['ml', 'ms', 'd', 'k']):
                messagebox.showerror("Error", "Invalid CSV header!")
                return
            
            fig = plot_data(df)
            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            global fig_for_saving
            fig_for_saving = fig
            messagebox.showinfo("Info", "File successfully uploaded.")
        except Exception as e:
            messagebox.showerror("Error", f"There was an error processing this file: {e}")

def save_image():
    if fig_for_saving:
        image_name = askstring("Save Image", "Enter image name (default: nomogram):")
        if not image_name:
            image_name = 'nomogram'
        image_name = image_name + '.png'
        
        buf = io.BytesIO()
        fig_for_saving.savefig(buf, format='png')
        buf.seek(0)
        with open(image_name, 'wb') as f:
            f.write(buf.getvalue())
        messagebox.showinfo("Info", f"Image saved as '{image_name}'!")
    else:
        messagebox.showwarning("Warning", "No plot available to save.")

window = tk.Tk()
window.title("FSE Dashboard (Dev by JBD)")
window.geometry("800x600")
window.resizable(True, True) 

fig_for_saving = None

upload_button = tk.Button(window, text="Upload CSV File", command=open_file)
upload_button.pack(pady=10)

save_button = tk.Button(window, text="Save Image", command=save_image)
save_button.pack(pady=10)

window.mainloop()
