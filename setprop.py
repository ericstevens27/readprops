import wx
from wx.lib.pubsub import pub
import modules.readbase as rb


########################################################################
class OtherFrame(wx.Frame):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "Set Property")
        panel = wx.Panel(self)

        msg = "Enter the property to search for"
        instructions = wx.StaticText(panel, label=msg)
        self.msgTxt = wx.TextCtrl(panel, value="")
        closeBtn = wx.Button(panel, label="Set Property to Find")
        closeBtn.Bind(wx.EVT_BUTTON, self.onSendAndClose)

        sizer = wx.BoxSizer(wx.VERTICAL)
        flags = wx.ALL | wx.CENTER
        sizer.Add(instructions, 0, flags, 5)
        sizer.Add(self.msgTxt, 0, flags, 5)
        sizer.Add(closeBtn, 0, flags, 5)
        panel.SetSizer(sizer)

    # ----------------------------------------------------------------------
    def onSendAndClose(self, event):
        """
        Send a message and close frame
        """
        msg = self.msgTxt.GetValue()
        pub.sendMessage("panelListener", message=msg)
        # pub.sendMessage("panelListener", message="test2", arg2="2nd argument!")
        self.Close()


########################################################################
class MyPanel(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        pub.subscribe(self.myListener, "panelListener")
        self.prop = None

        btn = wx.Button(self, -1, "Set Property", (25,50))
        btn.Bind(wx.EVT_BUTTON, self.onOpenFrame)
        self.btnSearch = wx.Button(self, -1, "Search for Property", (25, 75))
        self.btnSearch.Bind(wx.EVT_BUTTON, self.search)
        self.btnSearch.Disable()
        self.btnCount = wx.Button(self, -1, "Count Occurances of Property", (25, 100))
        self.btnCount.Bind(wx.EVT_BUTTON, self.count)
        self.btnCount.Disable()
        btnList = wx.Button(self, -1, "List all Properties", (25,125))
        btnList.Bind(wx.EVT_BUTTON, self.list)

        self.label = "Looking for property: {}".format(self.prop)
        self.st = wx.StaticText(self, label=self.label, pos=(25,25))
        font = self.st.GetFont()
        # font.PointSize += 10
        font = font.Bold()
        self.st.SetFont(font)


    # ----------------------------------------------------------------------
    def myListener(self, message, arg2=None):
        """
        Listener function
        """
        # print("Received the following message: " + message)
        self.prop = message
        self.label = "Looking for property: {}".format(self.prop)
        self.st.SetLabel(self.label)
        self.btnCount.Enable(True)
        self.btnSearch.Enable(True)
        # if arg2:
        #     print("Received another arguments: " + str(arg2))

    # ----------------------------------------------------------------------
    def onOpenFrame(self, event):
        """
        Opens secondary frame
        """
        frame = OtherFrame()
        frame.Show()

    def search(self, event):
        """Display an About Dialog"""
        bp = rb.ReadJson('', '', 'allprops-20180131.json')
        bp.readinput()
        msg = ''
        for tag, data in bp.data.items():
            if self.prop in data['props']:
                msg = msg + "{} {} [MIUI {}] {} is {}\n".format(data['model'], data['region'], data['version'], self.prop, data['props'][self.prop])
            else:
                print("MISSING: {} {} [MIUI {}] {} missing for this model\n".format(data['model'], data['region'], data['version'], self.prop))
        wx.MessageBox(msg, "Searching...", wx.OK|wx.ICON_INFORMATION)

    def count(self, event):
        """Display an About Dialog"""
        bp = rb.ReadJson('', '', 'allprops-20180131.json')
        bp.readinput()
        propscount = 0
        devicecount = 0
        for tag, data in bp.data.items():
            devicecount += 1
            for p in data['props']:
                if p == self.prop:
                    propscount += 1
        msg = "There are {} out of {} devices with the property {}".format(propscount, devicecount, self.prop)

        wx.MessageBox(msg, "Counting...", wx.OK|wx.ICON_INFORMATION)

    def list(self, event):
        """Display an About Dialog"""
        # assemble property list
        bp = rb.ReadJson('', '', 'allprops-20180131.json')
        bp.readinput()

        props = []
        for tag, data in bp.data.items():
            for p in data['props']:
                if p not in props:
                    props.append(p)
        msg = ''
        for p in props:
            msg = msg + p + "\n"
        wx.MessageBox(msg, "Listing...", wx.OK|wx.ICON_INFORMATION)


########################################################################
class MyFrame(wx.Frame):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Search for Property")
        panel = MyPanel(self)
        self.Show()


# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()