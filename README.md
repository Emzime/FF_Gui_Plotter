Work in progress...

A simple graphical interface for easy plot creation using Bladebit or gigaHorse

![image](https://github.com/Emzime/FF_Gui_Plotter/assets/3422040/eb4f6119-a2d2-4daa-9eac-d36b118fdc54)


Linux installation:
```
git clone https://github.com/Emzime/FF_Gui_Plotter.git
cd FF_Gui_Plotter
python -m venv venv
. ./venv/bin/activate
pip install psutil ttkthemes GPUtil requests logging datetime
python main.py
```

Build on Linux:
```
. ./venv/bin/activate
cd Builder
python System_Auto_Folder_Builder.py
```
or
```
. ./venv/bin/activate
cd Builder
python System_Auto_Standalone_Builder.py
```

Windows installation:
```
git clone https://github.com/Emzime/FF_Gui_Plotter.git
cd FF_Gui_Plotter
py -m venv venv
. ./venv/Scripts/activate
pip install psutil ttkthemes GPUtil requests logging datetime
py main.py
```

Build on Windows:
```
. ./venv/Scripts/activate
cd Builder
py System_Auto_Folder_Builder.py

```
or
```
. ./venv/Scripts/activate
cd Builder
py System_Auto_Standalone_Builder.py
```
