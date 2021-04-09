Project Homepage: https://github.com/likianta/declare-justpy

| Overview | Info       |
| -------- | ---------- |
| Status   | Proceeding |
| Version  | 0.1.0      |

# Demo Code

```py
from declare_justpy import Application, WebPage, Div
from lk_lambdex import lambdex

with Application() as app:

    with WebPage() as page:

        with Div() as div:
            div.text = 'Hello World'
            div.click_count = 0  # custom property

            div.on_clicked(lambdex(('self', 'msg'), '''
                self.click_count += 1
                self.text = f'Hello World ({self.click_count})'
            '''))

            div.on_mouseenter(lambdex(('self', 'msg'), '''
                self.text = 'Mouse Enter'
            '''))

            div.on_mouseleave(lambdex(('self', 'msg'), '''
                self.text = 'Mouse Leave'
            '''))

            # execute `div.add_to(page)` in `div.__exit__`

    # execute `app.start(lambda: page)` in `app.__exit__`
```

Which equals to:

```py
from justpy import justpy as start
from justpy import WebPage, Div

def on_clicked(self, msg):
    self.click_count += 1
    self.text = f'Hello World ({self.click_count})'


def on_mouse_enter(self, msg):
    self.text = 'Mouse Enter'


def on_mouse_leave(self, msg):
    self.text = 'Mouse Leave'


page = WebPage()

div = Div()
div.text = 'Hello World'
div.click_count = 0  # custom property
div.on_clicked(on_clicked)
div.on_mouseenter(on_mouse_enter)
div.on_mouseleave(on_mouse_leave)
div.add_to(page)

start(lambda : page)
```
