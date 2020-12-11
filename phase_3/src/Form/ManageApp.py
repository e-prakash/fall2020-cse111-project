import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk

from ..Handlers.DBInteraction import *
from ..Common import DBTypes

from .Manage import Manage
from .ManageForm import ManageForm

ResFields = DBTypes.EnumRes

class FormVariables(object):
	def __init__(self):
		self.key = tk.StringVar()
		self.year = tk.StringVar()
		self.month = tk.StringVar()
		self.day = tk.StringVar()
		self.hour = tk.StringVar()
		self.minute = tk.StringVar()
		self.second = tk.StringVar()
		self.longitude = tk.StringVar()
		self.latitude = tk.StringVar()
		self.depth = tk.StringVar()
		self.magnitude = tk.StringVar()
		self.yieldVal = tk.StringVar()
		self.eqsrcs = tk.StringVar()
		self.nesrcs = tk.StringVar()
	def bind(self, form):
		assert isinstance(form, ManageForm)
		form.label_keyval.configure(textvariable=self.key)
		form.spinbox_year.configure(textvariable=self.year)
		form.spinbox_month.configure(textvariable=self.month)
		form.spinbox_day.configure(textvariable=self.day)
		form.spinbox_hr.configure(textvariable=self.hour)
		form.spinbox_min.configure(textvariable=self.minute)
		form.spinbox_sec.configure(textvariable=self.second)
		form.spinbox_long.configure(textvariable=self.longitude)
		form.spinbox_lat.configure(textvariable=self.latitude)
		form.spinbox_depth.configure(textvariable=self.depth)
		form.spinbox_mag.configure(textvariable=self.magnitude)
		form.spinbox_yield.configure(textvariable=self.yieldVal)
		form.listbox_eqsrc.configure(listvariable=self.eqsrcs)
		form.listbox_nesrc.configure(listvariable=self.nesrcs)

def typeChangeListener(mf, event):
	assert isinstance(mf, ManageForm)
	value = mf.combobox_type.get()
	if(value == 'nuclear explosion'):
		mf.combobox_nation.configure(state="readonly")
		mf.spinbox_yield.configure(state=tk.NORMAL)
		mf.listbox_nesrc.configure(state=tk.NORMAL)
	else:
		mf.combobox_nation.configure(state=tk.DISABLED)
		mf.spinbox_yield.configure(state=tk.DISABLED)
		mf.listbox_nesrc.configure(state=tk.DISABLED)

def pushChangesListener(ma, fv, event):
	assert isinstance(ma, ManageApp)
	assert isinstance(fv, FormVariables)
	m = ma.m
	mf = ma.mf

	year = fv.year.get()
	month = fv.month.get()
	day = fv.day.get()
	hour = fv.hour.get()
	minute = fv.minute.get()
	second = fv.second.get()
	longitude = fv.longitude.get()
	latitude = fv.latitude.get()
	depth = fv.depth.get()
	magnitude = fv.magnitude.get()
	eqtype = mf.combobox_type.get()
	nation = mf.combobox_nation.get()
	yieldVal = fv.yieldVal.get()
	eqsrcIndexes = mf.listbox_eqsrc.curselection()
	nesrcIndexes = mf.listbox_nesrc.curselection()

	if(eqtype != 'nuclear explosion'):
		nation = None
		yieldVal = None
		nesrcIndexes = None

	print(
		year, month, day, hour, minute, second,
		longitude, latitude, depth,
		magnitude, eqtype, nation, yieldVal,
		eqsrcIndexes, nesrcIndexes
	)

	msg = m.validateOptions(
		year, month, day, hour, minute, second,
		longitude, latitude, depth,
		magnitude, eqtype, nation, yieldVal
	)

	if msg is None:
		res = m.commit(
			year, month, day, hour, minute, second,
			longitude, latitude, depth,
			magnitude, eqtype, nation, yieldVal,
			eqsrcIndexes, nesrcIndexes
		)
		if(res[0]):
			tkinter.messagebox.showinfo("Done", "Change Made")
			mf.close()
		else:
			tkinter.messagebox.showerror("Error", res[1])
	else:
		tkinter.messagebox.showerror("Error", msg)

def initComponents(ma):
	assert isinstance(ma, ManageApp)
	
	m = ma.m
	mf = ma.mf
	fv = FormVariables()
	fv.bind(mf)

	mf.combobox_type.bind('<<ComboboxSelected>>', lambda e: typeChangeListener(mf, e))
	mf.button_ok.bind('<ButtonRelease-1>', lambda e: pushChangesListener(ma, fv, e))

	setif = lambda val, check, valtrue, valfalse: val.set(valtrue) if check else val.set(valfalse)
	setif(fv.key,True,m.current_eqentry[ResFields.Earthquake.Key],"Error")

	mf.combobox_type['values'] = m.selectionList['types'][ResFields.Earthquake.Type]
	mf.combobox_type.current(m.current_selection['type'])
	mf.combobox_nation['values'] = m.selectionList['nations'][ResFields.Nation.Name]
	fv.eqsrcs.set(m.selectionList['eqsrcs'][ResFields.EarthquakeSource.Name])
	fv.nesrcs.set(m.selectionList['nesrcs'][ResFields.NuclearSource.Name])

	if(ResFields.Earthquake.Time in m.current_eqentry):
		time = m.getDate()
		fv.year.set(time[0])
		fv.month.set(time[1])
		fv.day.set(time[2])
		fv.hour.set(time[3])
		fv.minute.set(time[4])
		fv.second.set(time[5])
		fv.longitude.set(m.current_eqentry[ResFields.Earthquake.Longitude])
		fv.latitude.set(m.current_eqentry[ResFields.Earthquake.Latitude])
		fv.depth.set(m.current_eqentry[ResFields.Earthquake.Depth])
		fv.magnitude.set(m.current_eqentry[ResFields.Earthquake.Mag])

		for i in m.current_selection['eqsrcs']:
			mf.listbox_eqsrc.selection_set(i)
	else:
		fv.year.set("2020")
		fv.month.set("1")
		fv.day.set("1")
		fv.hour.set("0")
		fv.minute.set("0")
		fv.second.set("0")
		fv.longitude.set("0.00")
		fv.latitude.set("0")
		fv.depth.set("0.00")
		fv.magnitude.set("0.0")
	
	if m.current_neentry is not None and ResFields.Nuclear.Yield in m.current_neentry:
		mf.combobox_nation.current(m.current_selection['nation'])
		fv.yieldVal.set(m.current_neentry[ResFields.Nuclear.Yield])
		for idx in m.current_selection['nesrcs']:
			mf.listbox_nesrc.selection_set(idx)
	else:
		fv.yieldVal.set("0.0")

	typeChangeListener(mf, None)


class ManageApp(object):

	def __init__(self, dbi, eqkey = None):
		self.m = Manage(dbi, eqkey)
		self.mf = None
		if self.m.current_eqentry is not None:
			self.root = tk.Tk()
			self.root.withdraw()
			self.mf = ManageForm(self.root)
			initComponents(self)

	def run(self):
		if self.mf is None:
			print("Error: Invalid Key")
		else:
			self.mf.run()

def test_1():
	print("test 1...")
	dbi = DBInteraction(r'data/data.sqlite')
	ma = ManageApp(dbi, 39484)
	ma.run()

if __name__ == "__main__":
	test_1()