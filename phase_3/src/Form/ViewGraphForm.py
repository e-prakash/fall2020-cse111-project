import tkinter as tk
import tkinter.ttk as ttk


class ViewGraphForm:
	def __init__(self, master=None):
		# build ui
		self.master = master
		self.toplevel_viewgraph = tk.Toplevel(master)
		self.toplevel_viewgraph.title("Earthquake View/Graph")
		self.toplevel_viewgraph.iconphoto(False, tk.PhotoImage(file='src/Common/img/icon.png'))
		self.frame_viewgraph = ttk.Frame(self.toplevel_viewgraph)
		self.frame_6 = ttk.Frame(self.frame_viewgraph)
		self.frame_12 = ttk.Frame(self.frame_6)
		self.label_year = ttk.Label(self.frame_12)
		self.label_year.config(text='Year: ')
		self.label_year.pack(side='left')
		self.spinbox_yearlow = tk.Spinbox(self.frame_12)
		self.spinbox_yearlow.config(from_='0', increment='1', to='10000')
		self.spinbox_yearlow.pack(side='left')
		self.spinbox_yearhigh = tk.Spinbox(self.frame_12)
		self.spinbox_yearhigh.config(from_='0', increment='1', to='10000')
		self.spinbox_yearhigh.pack(side='right')
		self.frame_12.config(height='200', width='200')
		self.frame_12.grid()
		self.frame_15 = ttk.Frame(self.frame_6)
		self.label_mag = ttk.Label(self.frame_15)
		self.label_mag.config(text='Magnitude: ')
		self.label_mag.pack(side='left')
		self.spinbox_maglow = tk.Spinbox(self.frame_15)
		self.spinbox_maglow.config(from_='0.1', increment='0.1', to='15')
		self.spinbox_maglow.pack(side='left')
		self.spinbox_maghigh = tk.Spinbox(self.frame_15)
		self.spinbox_maghigh.config(from_='0.1', increment='0.1', to='15')
		self.spinbox_maghigh.pack(side='right')
		self.frame_15.config(height='200', width='200')
		self.frame_15.grid(column='0', row='1')
		self.frame_6.config(height='200', width='200')
		self.frame_6.grid()
		self.frame_8 = ttk.Frame(self.frame_viewgraph)
		self.frame_16 = ttk.Frame(self.frame_8)
		self.label_region = ttk.Label(self.frame_16)
		self.label_region.config(text='Region: ')
		self.label_region.pack(side='left')
		self.combobox_region = ttk.Combobox(self.frame_16, state="readonly", width='30')
		self.combobox_region.pack(side='right')
		self.frame_16.config(height='200', width='200')
		self.frame_16.grid()
		self.frame_19 = ttk.Frame(self.frame_8)
		self.label_nation = ttk.Label(self.frame_19)
		self.label_nation.config(text='Nation: ')
		self.label_nation.pack(side='left')
		self.combobox_nation = ttk.Combobox(self.frame_19, state="readonly", width='30')
		self.combobox_nation.pack(side='right')
		self.frame_19.config(height='200', width='200')
		self.frame_19.grid(column='0', row='1')
		self.frame_20 = ttk.Frame(self.frame_8)
		self.label_state = ttk.Label(self.frame_20)
		self.label_state.config(text='State: ')
		self.label_state.pack(side='left')
		self.combobox_state = ttk.Combobox(self.frame_20, state="readonly", width='30')
		self.combobox_state.pack(side='right')
		self.frame_20.config(height='200', width='200')
		self.frame_20.grid(column='0', row='2')
		self.frame_21 = ttk.Frame(self.frame_8)
		self.label_city = ttk.Label(self.frame_21)
		self.label_city.config(text='City: ')
		self.label_city.pack(side='left')
		self.combobox_city = ttk.Combobox(self.frame_21, state="readonly", width='30')
		self.combobox_city.pack(side='right')
		self.frame_21.config(height='200', width='200')
		self.frame_21.grid(column='0', row='3')
		self.frame_8.config(height='200', width='200')
		self.frame_8.grid(column='0', row='1')
		self.frame_9 = ttk.Frame(self.frame_viewgraph)
		self.label_yield = ttk.Label(self.frame_9)
		self.label_yield.config(text='Yield: ')
		self.label_yield.pack(side='left')
		self.spinbox_yieldlow = tk.Spinbox(self.frame_9)
		self.spinbox_yieldlow.config(from_='0.1', increment='0.1', to='100000')
		self.spinbox_yieldlow.pack(side='left')
		self.spinbox_yieldhigh = tk.Spinbox(self.frame_9)
		self.spinbox_yieldhigh.config(from_='0.1', increment='0.1', to='100000')
		self.spinbox_yieldhigh.pack(side='right')
		self.frame_9.config(height='200', width='200')
		self.frame_9.grid(column='0', row='2')
		self.frame_10 = ttk.Frame(self.frame_viewgraph)
		self.frame_22 = ttk.Frame(self.frame_10)
		self.label_eqtype = ttk.Label(self.frame_22)
		self.label_eqtype.config(text='Earthquake Types')
		self.label_eqtype.pack(side='top')
		
		self.listbox_eqtype = tk.Listbox(self.frame_22)
		self.listbox_eqtype.config(height='30', width='50', selectmode='extended', exportselection=False)
		self.listbox_eqtype.pack(side='left')
		self.scrollbar_eqtype = tk.Scrollbar(self.frame_22, orient="vertical")
		self.scrollbar_eqtype.config(command=self.listbox_eqtype.yview)
		self.scrollbar_eqtype.pack(side="right", fill="y")
		self.listbox_eqtype.config(yscrollcommand=self.scrollbar_eqtype.set)
		
		self.frame_22.config(height='200', width='200')
		self.frame_22.grid()
		self.frame_24 = ttk.Frame(self.frame_10)
		self.label_eqsrc = ttk.Label(self.frame_24)
		self.label_eqsrc.config(text='Earthquake Sources')
		self.label_eqsrc.pack(side='top')
		
		self.listbox_eqsrc = tk.Listbox(self.frame_24)
		self.listbox_eqsrc.config(height='30', width='50', selectmode='extended', exportselection=False)
		self.listbox_eqsrc.pack(side='left')
		self.scrollbar_eqsrc = tk.Scrollbar(self.frame_24, orient="vertical")
		self.scrollbar_eqsrc.config(command=self.listbox_eqsrc.yview)
		self.scrollbar_eqsrc.pack(side="right", fill="y")
		self.listbox_eqsrc.config(yscrollcommand=self.scrollbar_eqsrc.set)
		
		self.frame_24.config(height='200', width='200')
		self.frame_24.grid(column='1', row='0')
		self.frame_25 = ttk.Frame(self.frame_10)
		self.label_nenation = ttk.Label(self.frame_25)
		self.label_nenation.config(text='Detonation By Countries')
		self.label_nenation.pack(side='top')
		
		self.listbox_nenation = tk.Listbox(self.frame_25)
		self.listbox_nenation.config(height='30', width='50', selectmode='extended', exportselection=False)
		self.listbox_nenation.pack(side='left')
		self.scrollbar_nenation = tk.Scrollbar(self.frame_25, orient="vertical")
		self.scrollbar_nenation.config(command=self.listbox_nenation.yview)
		self.scrollbar_nenation.pack(side="right", fill="y")
		self.listbox_nenation.config(yscrollcommand=self.scrollbar_nenation.set)

		self.frame_25.config(height='200', width='200')
		self.frame_25.grid(column='2', row='0')
		self.frame_26 = ttk.Frame(self.frame_10)
		self.label_nesrc = ttk.Label(self.frame_26)
		self.label_nesrc.config(text='Nuclear Sources')
		self.label_nesrc.pack(side='top')
		
		self.listbox_nesrc = tk.Listbox(self.frame_26)
		self.listbox_nesrc.config(height='30', width='50', selectmode='extended', exportselection=False)
		self.listbox_nesrc.pack(side='left')
		self.scrollbar_nesrc = tk.Scrollbar(self.frame_26, orient="vertical")
		self.scrollbar_nesrc.config(command=self.listbox_nesrc.yview)
		self.scrollbar_nesrc.pack(side="right", fill="y")
		self.listbox_nesrc.config(yscrollcommand=self.scrollbar_nesrc.set)
		
		self.frame_26.config(height='200', width='200')
		self.frame_26.grid(column='3', row='0')
		self.frame_10.config(height='200', width='200')
		self.frame_10.grid(column='0', row='3')
		self.frame_11 = ttk.Frame(self.frame_viewgraph)
		self.frame_30 = ttk.Frame(self.frame_11)
		self.button_view = ttk.Button(self.frame_30)
		self.button_view.config(text='View')
		self.button_view.pack(side='top')
		self.frame_30.config(height='200', width='200')
		self.frame_30.grid()
		self.frame_33 = ttk.Frame(self.frame_11)
		self.combobox_graph = ttk.Combobox(self.frame_33, state="readonly", width='30')
		self.combobox_graph.pack(side='left')
		self.button_graph = ttk.Button(self.frame_33)
		self.button_graph.config(text='Graph')
		self.button_graph.pack(side='right')
		self.frame_33.config(height='200', width='200')
		self.frame_33.grid(column='1', row='0')
		self.frame_11.config(height='200', width='200')
		self.frame_11.grid(column='0', row='4')
		self.frame_viewgraph.config(height='200', width='200')
		self.frame_viewgraph.pack(side='top')
		self.toplevel_viewgraph.config(height='200', width='200')

		# Main widget
		self.mainwindow = self.toplevel_viewgraph
		self.mainwindow.protocol("WM_DELETE_WINDOW", self.close)

	def close(self):
		if self.master is not None:
			self.master.destroy()
		else:
			pass

	def run(self):
		self.mainwindow.mainloop()

if __name__ == '__main__':
	app = ViewGraphForm()
	app.run()

