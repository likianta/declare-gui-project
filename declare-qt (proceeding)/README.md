Project Homepage: https://github.com/likianta/declare-qt

| Overview | Info       |
| -------- | ---------- |
| Status   | Proceeding |
| Version  | 0.1.0      |

# Demo Code

```py
from declare_qt import Application, MainWindow, Label

with Application() as app:
    with MainWindow() as win:
        win.setGeometry(300, 200, 600, 400)
        with Label() as label:
            # execute `label.setParent()` in `label.__enter__`
            Label.setText('Hello World')
            # execute `label.show()` in `label.__exit__`
        # execute `win.show()` in `win.__exit__`
    # execute `sys.exit(app.exec_())` in `app.__exit__`
```

Which equals to:

```py
from sys import exit
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel

app = QApplication()

win = QMainWindow()
win.setGeometry(300, 200, 600, 400)

label = QLabel(win)
label.setText('Hello World')

label.show()
win.show()
exit(app.exec_())
```
