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
# declare-qml: https://github.com/likianta/declare-qml
from declare_qml import Applicatin
from declare_qml.qtquick import Rectangle, Text, MouseArea
from declare_qml.qtquick.windows import Window
from lk_lambdex import lambdex

with Application() as app:
    with Window() as win:
        win.width = 800
        win.height = 600
        win.color = 'white'
        win.visible = True

        with Rectangle() as rect:
            rect.width = 400
            rect.height = 300
            rect.anchors.center = win.center
            rect.color = 'navyblue'
            rect.radius = 12

            with Text() as txt:
                txt.anchors.center = rect.center
                txt.text = 'Hello World'
                txt.count = 0

            with MouseArea() as area:
                area.anchors.fill = rect
                area.on_clicked.connect(lambdex((), '''
                    txt.count += 1
                    txt.text = f'Text Clicked ({txt.count})'
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

1. 声明式语法的支持由 [declare-foundation](./declare-foundation) 库统一实现, 因此写法上具有一致性
2. 通常来说, 与原有的界面库相比较, 编写同一应用的代码量明显减少
3. 纯 Python 实现

# 子项目说明

Declare GUI Project 分为以下几个子项目:

| 项目 | 状态 |
| ---- | ---- |
| [declare-justpy](https://github.com/likianta/declare-justpy) | 开发中 |
| [declare-qml](https://github.com/likianta/declare-qml) | 已停止 |
| [declare-qt](https://github.com/likianta/declare-qt) | 开发中 |
| [declare-tkinter](https://github.com/likianta/declare-qt) | 未启动 |
| [declare-wxpython](https://github.com/likianta/declare-wxpython) | 未启动 |

# 开发说明

1. 每个子项目都应依赖于 declare-foundation 库, 并通过子类继承的方式修改细节实现
2. 如果您对此项目感兴趣, 您可以通过聊天群组, 飞书文档 (主要) 或邮件方式进行即时和非即时的协作与沟通
    1. 飞书文档邀请链接: TODO

**时间表**

预计将在 2021 年 6 月中旬完成 declare-qt 的核心开发工作. 其他子项目暂无明确时间.
