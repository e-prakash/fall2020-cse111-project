import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk

from ..Handlers.DBInteraction import *
from ..Common import DBTypes

from .ViewGraph import ViewGraph
from .ViewGraphForm import ViewGraphForm

ResFields = DBTypes.EnumRes

class FormVariables(object):
	def __init__(self):
		self.yearLow = tk.StringVar()
		self.yearHigh = tk.StringVar()
		self.magLow = tk.StringVar()
		self.magHigh = tk.StringVar()
		self.yieldLow = tk.StringVar()
		self.yieldHigh = tk.StringVar()
		self.eqtypes = tk.StringVar()
		self.eqsrcs = tk.StringVar()
		self.nenations = tk.StringVar()
		self.nesrcs = tk.StringVar()
	def bind(self, form):
		assert isinstance(form, ViewGraphForm)
		form.spinbox_yearlow.configure(textvariable=self.yearLow)
		form.spinbox_yearhigh.configure(textvariable=self.yearHigh)
		form.spinbox_maglow.configure(textvariable=self.magLow)
		form.spinbox_maghigh.configure(textvariable=self.magHigh)
		form.spinbox_yieldlow.configure(textvariable=self.yieldLow)
		form.spinbox_yieldhigh.configure(textvariable=self.yieldHigh)
		form.listbox_eqtype.configure(listvariable=self.eqtypes)
		form.listbox_eqsrc.configure(listvariable=self.eqsrcs)
		form.listbox_nenation.configure(listvariable=self.nenations)
		form.listbox_nesrc.configure(listvariable=self.nesrcs)

def typeChangeListener(v, event):
	assert isinstance(v, ViewGraphApp)
	selection = v.vf.listbox_eqtype.curselection()
	types = list(map(lambda i: v.v.selectionList['types'][ResFields.Earthquake.Type][i], selection))
	if(len(types) == 1 and types[0] == 'nuclear explosion'):
		v.vf.spinbox_yieldlow.configure(state=tk.NORMAL)
		v.vf.spinbox_yieldhigh.configure(state=tk.NORMAL)
		v.vf.listbox_nenation.configure(state=tk.NORMAL)
		v.vf.listbox_nesrc.configure(state=tk.NORMAL)
	else:
		v.vf.spinbox_yieldlow.configure(state=tk.DISABLED)
		v.vf.spinbox_yieldhigh.configure(state=tk.DISABLED)
		v.vf.listbox_nenation.configure(state=tk.DISABLED)
		v.vf.listbox_nesrc.configure(state=tk.DISABLED)

def locationChangeListener(v, event):
	assert isinstance(v, ViewGraphApp)
	r_name = v.vf.combobox_region.get()
	n_name = v.vf.combobox_nation.get()
	s_name = v.vf.combobox_state.get()
	c_name = v.vf.combobox_city.get()
	v.v.updateLocationSelection(r_name, n_name, s_name, c_name)

	v.vf.combobox_region['values'] = v.v.locationSelectionList['regions'][ResFields.Region.Name]
	v.vf.combobox_nation['values'] = v.v.locationSelectionList['nations'][ResFields.Nation.Name]
	v.vf.combobox_state['values'] = v.v.locationSelectionList['states'][ResFields.State.Name]
	v.vf.combobox_city['values'] = v.v.locationSelectionList['cities'][ResFields.City.Name]

	v.vf.combobox_region.current(v.v.locationSelectionList['r_idx'])
	v.vf.combobox_nation.current(v.v.locationSelectionList['n_idx'])
	v.vf.combobox_state.current(v.v.locationSelectionList['s_idx'])
	v.vf.combobox_city.current(v.v.locationSelectionList['c_idx'])

	v.vf.combobox_graph['values'] = list(v.v.graphSelectionDictionary.values())
	if not v.vf.combobox_graph.get() in v.vf.combobox_graph['values']:
		v.vf.combobox_graph.current(0)

def initComponents(v):
	assert isinstance(v, ViewGraphApp)
	fv = FormVariables()
	fv.bind(v.vf)
	
	fv.yearLow.set("1900")
	fv.yearHigh.set("2050")
	fv.magLow.set("0.1")
	fv.magHigh.set("15.0")
	fv.yieldLow.set("0.1")
	fv.yieldHigh.set("100000.0")
	
	v.vf.combobox_region.set("...")
	v.vf.combobox_nation.set("...")
	v.vf.combobox_state.set("...")
	v.vf.combobox_city.set("...")

	fv.eqtypes.set(v.v.selectionList['types'][ResFields.Earthquake.Type])
	fv.eqsrcs.set(v.v.selectionList['eqsrcs'][ResFields.EarthquakeSource.Name])
	fv.nenations.set(v.v.selectionList['nations'][ResFields.Nation.Name])
	fv.nesrcs.set(v.v.selectionList['nesrcs'][ResFields.NuclearSource.Name])

	v.vf.listbox_eqtype.bind('<<ListboxSelect>>', lambda e: typeChangeListener(v, e))
	v.vf.combobox_region.bind('<<ComboboxSelected>>', lambda e: locationChangeListener(v,e))
	v.vf.combobox_nation.bind('<<ComboboxSelected>>', lambda e: locationChangeListener(v,e))
	v.vf.combobox_state.bind('<<ComboboxSelected>>', lambda e: locationChangeListener(v,e))
	v.vf.combobox_city.bind('<<ComboboxSelected>>', lambda e: locationChangeListener(v,e))

	v.vf.button_graph.bind('<ButtonRelease-1>', lambda e: generate(v, fv, False, e))
	v.vf.button_view.bind('<ButtonRelease-1>', lambda e: generate(v, fv, True, e))
	
	v.vf.combobox_graph['values'] = list(v.v.graphSelectionDictionary.values())
	v.vf.combobox_graph.current(0)

	typeChangeListener(v, None)
	locationChangeListener(v, None)

def generate(v, fv, isView, e):
	assert isinstance(v, ViewGraphApp)
	assert isinstance(fv, FormVariables)

	yearLow = fv.yearLow.get()
	yearHigh = fv.yearHigh.get()
	magLow = fv.magLow.get()
	magHigh = fv.magHigh.get()
	yieldLow = fv.yieldLow.get()
	yieldHigh = fv.yieldHigh.get()
	eqtypeIndexes = v.vf.listbox_eqtype.curselection()
	eqsrcIndexes = v.vf.listbox_eqsrc.curselection()
	nenationIndexes = v.vf.listbox_nenation.curselection()
	nesrcIndexes = v.vf.listbox_nesrc.curselection()
	# isView
	graphSelection = v.vf.combobox_graph.get()

	msg = v.v.validateOptions(
		yearLow, yearHigh,
		magLow, magHigh,
		yieldLow, yieldHigh
	)

	if msg is None:
		result = v.v.commit(
			yearLow, yearHigh, magLow, magHigh,
			yieldLow, yieldHigh,
			eqtypeIndexes, eqsrcIndexes, nenationIndexes, nesrcIndexes,
			isView, graphSelection
		)
		if result[0]:
			if result[1]:
				tkinter.messagebox.showinfo("Done", "Generated file with name " + result[2])
			else:
				pass
		else:
			tkinter.messagebox.showerror("Error", result[1])
	else:
		tkinter.messagebox.showerror("Error", msg)

class ViewGraphApp(object):

	def __init__(self, dbi):
		self.v = ViewGraph(dbi)
		self.root = tk.Tk()
		self.root.withdraw()
		self.vf = ViewGraphForm(self.root)
		initComponents(self)

	def run(self):
		self.vf.run()

def test_1():
	print("test 1...")
	dbi = DBInteraction(r'data/data.sqlite')
	va = ViewGraphApp(dbi)
	va.run()

if __name__ == "__main__":
	test_1()