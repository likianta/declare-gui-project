Project Homepage: ~~https://github.com/likianta/declare-tkinter~~

| Overview | Info           |
| -------- | -------------- |
| Status   | NotImplemented |
| Version  |                |

# Demo Code (Concept)

```py
from declare_tkinter import *
from lk_lambdex import lambdex

with Application() as app:  # -> tkinter.Tk
    app.title('Hello World Demo')

    with Button() as btn:
        # set `btn.master` to `app` in `btn.__enter__`
        btn.configure(text='Hello World')
        btn.configure(command=lambdex((), '''
            # say hello
            global click_count
            click_count += 1
            print(f'Hello ({btn.click_count})')
        '''), click_count=0)
        # execute `btn.pack()` in `btn.__exit__`

    # execute `app.mainloop()` in `app.__exit__`
```

Which equals to:

```py
from tkinter import *

click_count = 0

def say_hello():
    global click_count
    click_count += 1
    print(f'Hello {click_count}')

app = Tk()
app.title('Hello World Demo')
btn = Button(app)
btn.configure(text='Hello World')
btn.configure(command=say_hello)
btn.pack()
app.mainloop()
```
