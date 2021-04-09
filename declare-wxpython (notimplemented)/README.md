Project Homepage: ~~https://github.com/likianta/declare-wxpython~~

| Overview | Info           |
| -------- | -------------- |
| Status   | NotImplemented |
| Version  |                |

# Demo Code (Concept)

```py
from declare_wxpython import *

with Application() as app:
    with Frame() as frame:
        frame.Parent = None
        frame.Id = None  # wx.ID_ANY
        frame.Title = 'Hello World'

        # execute `frame.Show()` in `frame.__exit__`

    # execute `app.Mainloop()` in `app.__exit__`
```

Which equals to:

```py
import wx

app = wx.App(False)
frame = wx.Frame(None, wx.ID_ANY, 'Hello World')
frame.Show(show=True)
app.Mainloop()
```
