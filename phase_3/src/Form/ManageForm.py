import tkinter as tk
import tkinter.ttk as ttk

# move form building to another file

class ManageForm:
	def __init__(self, master=None):
		# build ui
		self.master = master
		self.toplevel_manage = tk.Toplevel(master)
		self.toplevel_manage.title("Earthquake Database - Manage")
		self.toplevel_manage.iconphoto(False, tk.PhotoImage(file='src/Common/img/icon.png'))
		self.frame_manage = ttk.Frame(self.toplevel_manage)
		self.frame_2 = ttk.Frame(self.frame_manage)
		self.label_key = ttk.Label(self.frame_2)
		self.label_key.config(text='Key: ')
		self.label_key.grid()
		self.label_keyval = tk.Label(self.frame_2)
		self.label_keyval.grid(column='1', row='0')
		self.frame_2.config(height='200', width='200')
		self.frame_2.grid()
		self.frame_6 = ttk.Frame(self.frame_manage)
		self.label_time = ttk.Label(self.frame_6)
		self.label_time.config(text='Time (Y-M-D Hr:Min:Sec): ')
		self.label_time.grid()
		self.spinbox_year = tk.Spinbox(self.frame_6)
		self.spinbox_year.config(from_='0', increment='1', to='2050')
		self.spinbox_year.grid(column='1', row='0')
		self.spinbox_month = tk.Spinbox(self.frame_6)
		self.spinbox_month.config(from_='1', increment='1', to='12')
		self.spinbox_month.grid(column='2', row='0')
		self.spinbox_day = tk.Spinbox(self.frame_6)
		self.spinbox_day.config(from_='1', increment='1', to='31')
		self.spinbox_day.grid(column='3', row='0')
		self.label_8 = ttk.Label(self.frame_6)
		self.label_8.grid(column='4', row='0')
		self.label_9 = ttk.Label(self.frame_6)
		self.label_9.grid(column='0', row='1')
		self.spinbox_hr = tk.Spinbox(self.frame_6)
		self.spinbox_hr.config(from_='0', increment='1', to='23')
		self.spinbox_hr.grid(column='1', row='1')
		self.spinbox_min = tk.Spinbox(self.frame_6)
		self.spinbox_min.config(from_='0', increment='1', to='59')
		self.spinbox_min.grid(column='2', row='1')
		self.spinbox_sec = tk.Spinbox(self.frame_6)
		self.spinbox_sec.config(from_='0', increment='1', to='59')
		self.spinbox_sec.grid(column='3', row='1')
		self.label_utc = ttk.Label(self.frame_6)
		self.label_utc.config(text='UTC')
		self.label_utc.grid(column='4', row='1')
		self.frame_6.config(height='200', width='200')
		self.frame_6.grid(column='0', row='1')
		self.frame_7 = ttk.Frame(self.frame_manage)
		self.label_long = ttk.Label(self.frame_7)
		self.label_long.config(text='Longitude: ')
		self.label_long.grid()
		self.spinbox_long = tk.Spinbox(self.frame_7)
		self.spinbox_long.config(from_='-180', increment='0.001', to='180')
		self.spinbox_long.grid(column='1', row='0')
		self.label_lat = ttk.Label(self.frame_7)
		self.label_lat.config(text='Latitude: ')
		self.label_lat.grid(column='2', row='0')
		self.spinbox_lat = tk.Spinbox(self.frame_7)
		self.spinbox_lat.config(from_='-90', increment='0.001', to='90')
		self.spinbox_lat.grid(column='3', row='0')
		self.label_depth = ttk.Label(self.frame_7)
		self.label_depth.config(text='Depth: ')
		self.label_depth.grid(column='4', row='0')
		self.spinbox_depth = tk.Spinbox(self.frame_7)
		self.spinbox_depth.config(from_='-10000', increment='0.01', to='10000')
		self.spinbox_depth.grid(column='5', row='0')
		self.label_mag = ttk.Label(self.frame_7)
		self.label_mag.config(text='Magnitude: ')
		self.label_mag.grid(column='2', row='1')
		self.spinbox_mag = tk.Spinbox(self.frame_7)
		self.spinbox_mag.config(from_='0.1', increment='0.1', to='15')
		self.spinbox_mag.grid(column='3', row='1')
		self.label_type = ttk.Label(self.frame_7)
		self.label_type.config(text='Type: ')
		self.label_type.grid(column='2', row='2')
		self.combobox_type = ttk.Combobox(self.frame_7, state="readonly")
		self.combobox_type.grid(column='3', row='2')
		self.frame_7.config(height='200', width='200')
		self.frame_7.grid(column='0', row='2')
		self.frame_8 = ttk.Frame(self.frame_manage)
		self.label_nation = ttk.Label(self.frame_8)
		self.label_nation.config(text='Detonated by Nation: ')
		self.label_nation.grid(column='0')
		self.combobox_nation = ttk.Combobox(self.frame_8, state="readonly")
		self.combobox_nation.grid(column='1', row='0')
		self.label_yield = ttk.Label(self.frame_8)
		self.label_yield.config(text='Yield: ')
		self.label_yield.grid(column='0', row='1')
		self.spinbox_yield = tk.Spinbox(self.frame_8)
		self.spinbox_yield.config(from_='0.01', increment='0.01', to='100000')
		self.spinbox_yield.grid(column='1', row='1')
		self.frame_8.config(height='200', width='200')
		self.frame_8.grid(column='0', row='3')
		self.frame_9 = ttk.Frame(self.frame_manage)
		self.frame_11 = ttk.Frame(self.frame_9)
		self.label_eqsrc = ttk.Label(self.frame_11)
		self.label_eqsrc.config(text='Earthquake Source')
		self.label_eqsrc.pack(side='top')
		
		self.listbox_eqsrc = tk.Listbox(self.frame_11)
		self.listbox_eqsrc.config(height='30', width='50', selectmode='extended', exportselection=False)
		self.listbox_eqsrc.pack(side='left')
		self.scrollbar_eqsrc = tk.Scrollbar(self.frame_11, orient="vertical")
		self.scrollbar_eqsrc.config(command=self.listbox_eqsrc.yview)
		self.scrollbar_eqsrc.pack(side="right", fill="y")
		self.listbox_eqsrc.config(yscrollcommand=self.scrollbar_eqsrc.set)

		self.frame_11.config(height='200', width='200')
		self.frame_11.grid()
		self.frame_12 = ttk.Frame(self.frame_9)
		self.label_nesrc = ttk.Label(self.frame_12)
		self.label_nesrc.config(text='Nuclear Source')
		self.label_nesrc.pack(side='top')
		
		self.listbox_nesrc = tk.Listbox(self.frame_12)
		self.listbox_nesrc.config(height='30', width='50', selectmode='extended', exportselection=False)
		self.listbox_nesrc.pack(side='left')
		self.scrollbar_nesrc = tk.Scrollbar(self.frame_12, orient="vertical")
		self.scrollbar_nesrc.config(command=self.listbox_nesrc.yview)
		self.scrollbar_nesrc.pack(side="right", fill="y")
		self.listbox_nesrc.config(yscrollcommand=self.scrollbar_nesrc.set)
		
		self.frame_12.config(height='200', width='200')
		self.frame_12.grid(column='1', row='0')
		self.frame_9.config(height='200', width='200')
		self.frame_9.grid(column='0', row='4')
		self.frame_10 = ttk.Frame(self.frame_manage)
		self.button_ok = ttk.Button(self.frame_10)
		self.button_ok.config(text='Push Changes')
		self.button_ok.grid()
		self.frame_10.config(height='200', width='200')
		self.frame_10.grid(column='0', row='5')
		self.frame_manage.config(height='200', width='200')
		self.frame_manage.pack(side='top')
		self.toplevel_manage.config(height='200', width='200')

		# Main widget
		self.mainwindow = self.toplevel_manage
		# lambda a: self.close(a) - if want to use with arguments
		self.mainwindow.protocol("WM_DELETE_WINDOW", self.close)

	def close(self):
		if self.master is not None:
			self.master.destroy()
		else:
			pass

	def run(self):
		self.mainwindow.mainloop()

if __name__ == '__main__':
	root = tk.Tk()
	root.withdraw()
	app = ManageForm(root)
	app.run()

