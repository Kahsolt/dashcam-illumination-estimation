#!/usr/bin/env python3
# Author: Armit
# Create Time: 周日 2024/12/08 

# 查看制作的目标分布列

import tkinter as tk
import tkinter.ttk as ttk
from traceback import print_exc

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from utils import vMF

FIG_SIZE = (8, 3)
MOUSE_WHEEL_SPD = 120


class App:

  def __init__(self):
    self.setup_gui()
    self.redraw()

    try:
      self.wnd.mainloop()
    except KeyboardInterrupt:
      self.wnd.quit()
    except: print_exc()

  def setup_gui(self):
    # window
    wnd = tk.Tk()
    wnd.title('Target Viewer')
    wnd.protocol('WM_DELETE_WINDOW', wnd.quit)
    self.wnd = wnd

    self.var_tht = tk.IntVar(wnd, 0)
    self.var_phi = tk.IntVar(wnd, 0)
    self.var_k   = tk.IntVar(wnd, 80)
    
    # top: img-idx
    frm1 = ttk.Label(wnd)
    frm1.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)
    if True:
      frm11 = ttk.LabelFrame(frm1, text='theta')
      frm11.pack(expand=tk.YES, fill=tk.X)
      if True:
        sc = tk.Scale(frm11, command=lambda _: self.redraw(), variable=self.var_tht, orient=tk.HORIZONTAL, from_=-180, to=180, resolution=1, tickinterval=45)
        sc.pack(expand=tk.YES, fill=tk.X)

      frm12 = ttk.LabelFrame(frm1, text='phi')
      frm12.pack(expand=tk.YES, fill=tk.X)
      if True:
        sc = tk.Scale(frm12, command=lambda _: self.redraw(), variable=self.var_phi, orient=tk.HORIZONTAL, from_=0, to=90, resolution=1, tickinterval=45)
        sc.pack(expand=tk.YES, fill=tk.X)

      frm13 = ttk.LabelFrame(frm1, text='kappa')
      frm13.pack(expand=tk.YES, fill=tk.X)
      if True:
        sc = tk.Scale(frm13, command=lambda _: self.redraw(), variable=self.var_k, orient=tk.HORIZONTAL, from_=1, to=100, resolution=1, tickinterval=100)
        sc.pack(expand=tk.YES, fill=tk.X)

    # bottom: plot
    frm2 = ttk.Frame(wnd)
    frm2.pack(expand=tk.YES, fill=tk.BOTH)
    if True:
      fig = plt.gcf()
      ax = plt.subplot()
      fig.tight_layout()
      fig.set_size_inches(FIG_SIZE)
      cvs = FigureCanvasTkAgg(fig, frm2)
      toolbar = NavigationToolbar2Tk(cvs)
      toolbar.update()
      cvs.get_tk_widget().pack(expand=tk.YES, fill=tk.BOTH)
      self.fig, self.ax, self.cvs = fig, ax, cvs

  def redraw(self):
    tht = self.var_tht.get()    # [-180, 180], 32 bins
    phi = self.var_phi.get()    # [0, 90], 8 bins
    k   = self.var_k.get()

    pdist = vMF([tht, phi], kappa=k)
    pmap = pdist.reshape(8, 32)

    self.ax.cla()
    self.ax.imshow(pmap, cmap='gray')
    self.ax.invert_yaxis()
    self.fig.tight_layout()
    self.cvs.draw()


if __name__ == '__main__':
  App()
