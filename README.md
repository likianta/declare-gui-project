# Declare GUI Project

这是一项致力于提升 Python GUI 开发体验的计划.

Declare GUI Project 为主流的 Python GUI 框架封装一层声明式的语法, 开发者可以以 "树形结构" 组织代码, 从而为可视化界面编写出结构更加清晰的代码.

它们看起来长这样:

*注: 以下仅为实验性内容.*

```py
# declare-qt: https://github.com/likianta/declare-qt
from declare_qt import Application, MainWindow, Label

with Application() as app:
    app.setApplicationName('Hello Declare Qt')

    with MainWindow() as win:
        win.setGeometry(500, 500, 600, 400)

        with Label() as label:
            Label.setText('Hello World')
```

```py
# declare-qtquick: https://github.com/likianta/declare-qtquick
from declare_qtquick import Applicatin
from declare_qtquick.windows import MouseArea, Rectangle, Text, Window
from lk_lambdex import lambdex

with Application() as app:
    with Window() as win:
        win.width = 800
        win.height = 600
        win.color = 'white'
        win.visible = True

        with Rectangle() as rect:
            rect.anchors.center = win.center
            rect.width = 400
            rect.height = 300
            rect.color = 'navyblue'
            rect.radius = 12

            with Text() as txt:
                txt.anchors.center = rect.center
                txt.text = 'Hello World'

            with MouseArea() as area:
                area.anchors.fill = rect
                area.on_clicked.connect(lambdex((), '''
                    txt.text += '!'
                '''))
```

```py
# declare-justpy: https://github.com/likianta/declare-justpy
from declare_justpy import Application, WebPage, Div
from lk_lambdex import lambdex

with Application() as app:
    with WebPage() as page:
        with Div() as div:
            div.text = 'Hello World'
            div.count = 0
            div.on_click(lambdex(('self', 'msg'), '''
                self.count += 1
                self.text = f'Text Clicked ({self.count})'
            '''))
    app.start(page, open_browser=True)
```

它们具有以下共同特性:

1. 声明式语法的支持由 [declare-foundation](./declare-foundation) 库统一实现, 在语法上具有一致性
2. 通常来说, 与原有的界面库相比较, 编写同一应用的代码量有所减少
3. 开发者只需编写纯 Python 代码, 其他工作由 GUI 库完成

# 子项目说明

Declare GUI Project 分为以下几个子项目:

| 项目 | 状态 |
| ---- | ---- |
| [declare-justpy](https://github.com/likianta/declare-justpy) | 未启动 |
| [declare-qml](https://github.com/likianta/declare-qml) | 已停止 |
| [declare-qt](https://github.com/likianta/declare-qt) | 进行中 |
| [declare-qtquick](https://github.com/likianta/declare-qtquick) | 进行中 |
| [declare-tkinter](https://github.com/likianta/declare-tkinter) | 未启动 |
| [declare-wxpython](https://github.com/likianta/declare-wxpython) | 未启动 |

# 开发说明

*TODO*
