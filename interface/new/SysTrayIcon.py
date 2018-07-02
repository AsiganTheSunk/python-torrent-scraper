<html><head>
<meta http-equiv="content-type" content="text/html; charset=windows-1252">
<title>SysTrayIcon.py</title>
<style type="text/css"><!--
.syntax0 {
color: #000000;
}
.syntax1 {
color: #009900;
}
.syntax2 {
color: #6eb357;
font-weight: bold;
font-style: italic;
}
.syntax3 {
color: #cc3300;
}
.syntax4 {
color: #cc6600;
}
.syntax5 {
color: #008080;
}
.syntax6 {
color: #000099;
}
.syntax7 {
color: #ff0000;
font-weight: bold;
}
.syntax8 {
color: #0033cc;
}
.syntax9 {
color: #006600;
}
.syntax10 {
color: #660099;
}
.syntax11 {
color: #66ccff;
font-weight: bold;
}
.syntax12 {
color: #990033;
font-weight: bold;
font-style: italic;
}
.syntax13 {
color: #7c0000;
}
.syntax14 {
color: #770077;
}
.syntax15 {
color: #9900cc;
}
.syntax16 {
color: #6600cc;
}
.syntax17 {
color: #4065fc;
}
.syntax18 {
color: #9933ff;
}
-->
</style>
</head>
<body bgcolor="#FFFFFF">
<pre><span class="syntax1">#</span><span class="syntax1">!/usr/bin/env</span><span class="syntax1"> </span><span class="syntax1">python</span>
<span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1">Module</span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1">:</span><span class="syntax1"> </span><span class="syntax1">SysTrayIcon.py</span>
<span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1">Synopsis</span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1">:</span><span class="syntax1"> </span><span class="syntax1">Windows</span><span class="syntax1"> </span><span class="syntax1">System</span><span class="syntax1"> </span><span class="syntax1">tray</span><span class="syntax1"> </span><span class="syntax1">icon.</span>
<span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1">Programmer</span><span class="syntax1"> </span><span class="syntax1">:</span><span class="syntax1"> </span><span class="syntax1">Simon</span><span class="syntax1"> </span><span class="syntax1">Brunning</span><span class="syntax1"> </span><span class="syntax1">-</span><span class="syntax1"> </span><span class="syntax1">simon@brunningonline.net</span>
<span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1">Date</span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1">:</span><span class="syntax1"> </span><span class="syntax1">11</span><span class="syntax1"> </span><span class="syntax1">April</span><span class="syntax1"> </span><span class="syntax1">2005</span>
<span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1">Notes</span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1">:</span><span class="syntax1"> </span><span class="syntax1">Based</span><span class="syntax1"> </span><span class="syntax1">on</span><span class="syntax1"> </span><span class="syntax1">(i.e.</span><span class="syntax1"> </span><span class="syntax1">ripped</span><span class="syntax1"> </span><span class="syntax1">off</span><span class="syntax1"> </span><span class="syntax1">from)</span><span class="syntax1"> </span><span class="syntax1">Mark</span><span class="syntax1"> </span><span class="syntax1">Hammond's</span>
<span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1">win32gui_taskbar.py</span><span class="syntax1"> </span><span class="syntax1">and</span><span class="syntax1"> </span><span class="syntax1">win32gui_menu.py</span><span class="syntax1"> </span><span class="syntax1">demos</span><span class="syntax1"> </span><span class="syntax1">from</span><span class="syntax1"> </span><span class="syntax1">PyWin32</span>
<span class="syntax14">'''</span><span class="syntax14">TODO</span>

<span class="syntax14">For</span><span class="syntax14"> </span><span class="syntax14">now</span><span class="syntax14">,</span><span class="syntax14"> </span><span class="syntax14">the</span><span class="syntax14"> </span><span class="syntax14">demo</span><span class="syntax14"> </span><span class="syntax14">at</span><span class="syntax14"> </span><span class="syntax14">the</span><span class="syntax14"> </span><span class="syntax14">bottom</span><span class="syntax14"> </span><span class="syntax14">shows</span><span class="syntax14"> </span><span class="syntax14">how</span><span class="syntax14"> </span><span class="syntax14">to</span><span class="syntax14"> </span><span class="syntax14">use</span><span class="syntax14"> </span><span class="syntax14">it</span><span class="syntax14">.</span><span class="syntax14">.</span><span class="syntax14">.</span><span class="syntax14">'''</span>
         
<span class="syntax8">import</span> os
<span class="syntax8">import</span> sys
<span class="syntax8">import</span> win32api
<span class="syntax8">import</span> win32con
<span class="syntax8">import</span> win32gui_struct
<span class="syntax8">try</span>:
    <span class="syntax8">import</span> winxpgui <span class="syntax8">as</span> win32gui
<span class="syntax8">except</span> <span class="syntax10">ImportError</span>:
    <span class="syntax8">import</span> win32gui

<span class="syntax8">class</span> <span class="syntax6">SysTrayIcon</span>(<span class="syntax9">object</span>):
    <span class="syntax14">'''</span><span class="syntax14">TODO</span><span class="syntax14">'''</span>
    QUIT <span class="syntax18">=</span> <span class="syntax13">'</span><span class="syntax13">QUIT</span><span class="syntax13">'</span>
    SPECIAL_ACTIONS <span class="syntax18">=</span> [QUIT]
    
    FIRST_ID <span class="syntax18">=</span> <span class="syntax5">1023</span>
    
    <span class="syntax8">def</span> <span class="syntax10">__init__</span>(self,
                 icon,
                 hover_text,
                 menu_options,
                 on_quit<span class="syntax18">=</span><span class="syntax10">None</span>,
                 default_menu_index<span class="syntax18">=</span><span class="syntax10">None</span>,
                 window_class_name<span class="syntax18">=</span><span class="syntax10">None</span>,):
        
        self.icon <span class="syntax18">=</span> icon
        self.hover_text <span class="syntax18">=</span> hover_text
        self.on_quit <span class="syntax18">=</span> on_quit
        
        menu_options <span class="syntax18">=</span> menu_options <span class="syntax18">+</span> ((<span class="syntax13">'</span><span class="syntax13">Quit</span><span class="syntax13">'</span>, <span class="syntax10">None</span>, self.QUIT),)
        self._next_action_id <span class="syntax18">=</span> self.FIRST_ID
        self.menu_actions_by_id <span class="syntax18">=</span> <span class="syntax9">set</span>()
        self.menu_options <span class="syntax18">=</span> self.<span class="syntax6">_add_ids_to_menu_options</span>(<span class="syntax9">list</span>(menu_options))
        self.menu_actions_by_id <span class="syntax18">=</span> <span class="syntax9">dict</span>(self.menu_actions_by_id)
        <span class="syntax8">del</span> self._next_action_id
        
        
        self.default_menu_index <span class="syntax18">=</span> (default_menu_index <span class="syntax8">or</span> <span class="syntax5">0</span>)
        self.window_class_name <span class="syntax18">=</span> window_class_name <span class="syntax8">or</span> <span class="syntax13">"</span><span class="syntax13">SysTrayIconPy</span><span class="syntax13">"</span>
        
        message_map <span class="syntax18">=</span> {win32gui.<span class="syntax6">RegisterWindowMessage</span>(<span class="syntax13">"</span><span class="syntax13">TaskbarCreated</span><span class="syntax13">"</span>): self.restart,
                       win32con.WM_DESTROY: self.destroy,
                       win32con.WM_COMMAND: self.command,
                       win32con.WM_USER<span class="syntax18">+</span><span class="syntax5">20</span> : self.notify,}
        <span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1">Register</span><span class="syntax1"> </span><span class="syntax1">the</span><span class="syntax1"> </span><span class="syntax1">Window</span><span class="syntax1"> </span><span class="syntax1">class.</span>
        window_class <span class="syntax18">=</span> win32gui.<span class="syntax6">WNDCLASS</span>()
        hinst <span class="syntax18">=</span> window_class.hInstance <span class="syntax18">=</span> win32gui.<span class="syntax6">GetModuleHandle</span>(<span class="syntax10">None</span>)
        window_class.lpszClassName <span class="syntax18">=</span> self.window_class_name
        window_class.style <span class="syntax18">=</span> win32con.CS_VREDRAW <span class="syntax18">|</span> win32con.CS_HREDRAW;
        window_class.hCursor <span class="syntax18">=</span> win32gui.<span class="syntax6">LoadCursor</span>(<span class="syntax5">0</span>, win32con.IDC_ARROW)
        window_class.hbrBackground <span class="syntax18">=</span> win32con.COLOR_WINDOW
        window_class.lpfnWndProc <span class="syntax18">=</span> message_map <span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1">could</span><span class="syntax1"> </span><span class="syntax1">also</span><span class="syntax1"> </span><span class="syntax1">specify</span><span class="syntax1"> </span><span class="syntax1">a</span><span class="syntax1"> </span><span class="syntax1">wndproc.</span>
        classAtom <span class="syntax18">=</span> win32gui.<span class="syntax6">RegisterClass</span>(window_class)
        <span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1">Create</span><span class="syntax1"> </span><span class="syntax1">the</span><span class="syntax1"> </span><span class="syntax1">Window.</span>
        style <span class="syntax18">=</span> win32con.WS_OVERLAPPED <span class="syntax18">|</span> win32con.WS_SYSMENU
        self.hwnd <span class="syntax18">=</span> win32gui.<span class="syntax6">CreateWindow</span>(classAtom,
                                          self.window_class_name,
                                          style,
                                          <span class="syntax5">0</span>,
                                          <span class="syntax5">0</span>,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          <span class="syntax5">0</span>,
                                          <span class="syntax5">0</span>,
                                          hinst,
                                          <span class="syntax10">None</span>)
        win32gui.<span class="syntax6">UpdateWindow</span>(self.hwnd)
        self.notify_id <span class="syntax18">=</span> <span class="syntax10">None</span>
        self.<span class="syntax6">refresh_icon</span>()
        
        win32gui.<span class="syntax6">PumpMessages</span>()

    <span class="syntax8">def</span> <span class="syntax6">_add_ids_to_menu_options</span>(self, menu_options):
        result <span class="syntax18">=</span> []
        <span class="syntax8">for</span> menu_option <span class="syntax8">in</span> menu_options:
            option_text, option_icon, option_action <span class="syntax18">=</span> menu_option
            <span class="syntax8">if</span> <span class="syntax9">callable</span>(option_action) <span class="syntax8">or</span> option_action <span class="syntax8">in</span> self.SPECIAL_ACTIONS:
                self.menu_actions_by_id.<span class="syntax6">add</span>((self._next_action_id, option_action))
                result.<span class="syntax6">append</span>(menu_option <span class="syntax18">+</span> (self._next_action_id,))
            <span class="syntax8">elif</span> <span class="syntax6">non_string_iterable</span>(option_action):
                result.<span class="syntax6">append</span>((option_text,
                               option_icon,
                               self.<span class="syntax6">_add_ids_to_menu_options</span>(option_action),
                               self._next_action_id))
            <span class="syntax8">else</span>:
                <span class="syntax8">print</span> <span class="syntax13">'</span><span class="syntax13">Unknown</span><span class="syntax13"> </span><span class="syntax13">item</span><span class="syntax13">'</span>, option_text, option_icon, option_action
            self._next_action_id <span class="syntax18">+</span><span class="syntax18">=</span> <span class="syntax5">1</span>
        <span class="syntax8">return</span> result
        
    <span class="syntax8">def</span> <span class="syntax6">refresh_icon</span>(self):
        <span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1">Try</span><span class="syntax1"> </span><span class="syntax1">and</span><span class="syntax1"> </span><span class="syntax1">find</span><span class="syntax1"> </span><span class="syntax1">a</span><span class="syntax1"> </span><span class="syntax1">custom</span><span class="syntax1"> </span><span class="syntax1">icon</span>
        hinst <span class="syntax18">=</span> win32gui.<span class="syntax6">GetModuleHandle</span>(<span class="syntax10">None</span>)
        <span class="syntax8">if</span> os.path.<span class="syntax6">isfile</span>(self.icon):
            icon_flags <span class="syntax18">=</span> win32con.LR_LOADFROMFILE <span class="syntax18">|</span> win32con.LR_DEFAULTSIZE
            hicon <span class="syntax18">=</span> win32gui.<span class="syntax6">LoadImage</span>(hinst,
                                       self.icon,
                                       win32con.IMAGE_ICON,
                                       <span class="syntax5">0</span>,
                                       <span class="syntax5">0</span>,
                                       icon_flags)
        <span class="syntax8">else</span>:
            <span class="syntax8">print</span> <span class="syntax13">"</span><span class="syntax13">Can</span><span class="syntax13">'</span><span class="syntax13">t</span><span class="syntax13"> </span><span class="syntax13">find</span><span class="syntax13"> </span><span class="syntax13">icon</span><span class="syntax13"> </span><span class="syntax13">file</span><span class="syntax13"> </span><span class="syntax13">-</span><span class="syntax13"> </span><span class="syntax13">using</span><span class="syntax13"> </span><span class="syntax13">default</span><span class="syntax13">.</span><span class="syntax13">"</span>
            hicon <span class="syntax18">=</span> win32gui.<span class="syntax6">LoadIcon</span>(<span class="syntax5">0</span>, win32con.IDI_APPLICATION)

        <span class="syntax8">if</span> self.notify_id: message <span class="syntax18">=</span> win32gui.NIM_MODIFY
        <span class="syntax8">else</span>: message <span class="syntax18">=</span> win32gui.NIM_ADD
        self.notify_id <span class="syntax18">=</span> (self.hwnd,
                          <span class="syntax5">0</span>,
                          win32gui.NIF_ICON <span class="syntax18">|</span> win32gui.NIF_MESSAGE <span class="syntax18">|</span> win32gui.NIF_TIP,
                          win32con.WM_USER<span class="syntax18">+</span><span class="syntax5">20</span>,
                          hicon,
                          self.hover_text)
        win32gui.<span class="syntax6">Shell_NotifyIcon</span>(message, self.notify_id)

    <span class="syntax8">def</span> <span class="syntax6">restart</span>(self, hwnd, msg, wparam, lparam):
        self.<span class="syntax6">refresh_icon</span>()

    <span class="syntax8">def</span> <span class="syntax6">destroy</span>(self, hwnd, msg, wparam, lparam):
        <span class="syntax8">if</span> self.on_quit: self.<span class="syntax6">on_quit</span>(self)
        nid <span class="syntax18">=</span> (self.hwnd, <span class="syntax5">0</span>)
        win32gui.<span class="syntax6">Shell_NotifyIcon</span>(win32gui.NIM_DELETE, nid)
        win32gui.<span class="syntax6">PostQuitMessage</span>(<span class="syntax5">0</span>) <span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1">Terminate</span><span class="syntax1"> </span><span class="syntax1">the</span><span class="syntax1"> </span><span class="syntax1">app.</span>

    <span class="syntax8">def</span> <span class="syntax6">notify</span>(self, hwnd, msg, wparam, lparam):
        <span class="syntax8">if</span> lparam<span class="syntax18">=</span><span class="syntax18">=</span>win32con.WM_LBUTTONDBLCLK:
            self.<span class="syntax6">execute_menu_option</span>(self.default_menu_index <span class="syntax18">+</span> self.FIRST_ID)
        <span class="syntax8">elif</span> lparam<span class="syntax18">=</span><span class="syntax18">=</span>win32con.WM_RBUTTONUP:
            self.<span class="syntax6">show_menu</span>()
        <span class="syntax8">elif</span> lparam<span class="syntax18">=</span><span class="syntax18">=</span>win32con.WM_LBUTTONUP:
            <span class="syntax8">pass</span>
        <span class="syntax8">return</span> <span class="syntax10">True</span>
        
    <span class="syntax8">def</span> <span class="syntax6">show_menu</span>(self):
        menu <span class="syntax18">=</span> win32gui.<span class="syntax6">CreatePopupMenu</span>()
        self.<span class="syntax6">create_menu</span>(menu, self.menu_options)
        <span class="syntax1">#</span><span class="syntax1">win32gui.SetMenuDefaultItem(menu,</span><span class="syntax1"> </span><span class="syntax1">1000,</span><span class="syntax1"> </span><span class="syntax1">0)</span>
        
        pos <span class="syntax18">=</span> win32gui.<span class="syntax6">GetCursorPos</span>()
        <span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1">See</span><span class="syntax1"> </span><span class="syntax1">http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp</span>
        win32gui.<span class="syntax6">SetForegroundWindow</span>(self.hwnd)
        win32gui.<span class="syntax6">TrackPopupMenu</span>(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[<span class="syntax5">0</span>],
                                pos[<span class="syntax5">1</span>],
                                <span class="syntax5">0</span>,
                                self.hwnd,
                                <span class="syntax10">None</span>)
        win32gui.<span class="syntax6">PostMessage</span>(self.hwnd, win32con.WM_NULL, <span class="syntax5">0</span>, <span class="syntax5">0</span>)
    
    <span class="syntax8">def</span> <span class="syntax6">create_menu</span>(self, menu, menu_options):
        <span class="syntax8">for</span> option_text, option_icon, option_action, option_id <span class="syntax8">in</span> menu_options[::<span class="syntax18">-</span><span class="syntax5">1</span>]:
            <span class="syntax8">if</span> option_icon:
                option_icon <span class="syntax18">=</span> self.<span class="syntax6">prep_menu_icon</span>(option_icon)
            
            <span class="syntax8">if</span> option_id <span class="syntax8">in</span> self.menu_actions_by_id:                
                item, extras <span class="syntax18">=</span> win32gui_struct.<span class="syntax6">PackMENUITEMINFO</span>(text<span class="syntax18">=</span>option_text,
                                                                hbmpItem<span class="syntax18">=</span>option_icon,
                                                                wID<span class="syntax18">=</span>option_id)
                win32gui.<span class="syntax6">InsertMenuItem</span>(menu, <span class="syntax5">0</span>, <span class="syntax5">1</span>, item)
            <span class="syntax8">else</span>:
                submenu <span class="syntax18">=</span> win32gui.<span class="syntax6">CreatePopupMenu</span>()
                self.<span class="syntax6">create_menu</span>(submenu, option_action)
                item, extras <span class="syntax18">=</span> win32gui_struct.<span class="syntax6">PackMENUITEMINFO</span>(text<span class="syntax18">=</span>option_text,
                                                                hbmpItem<span class="syntax18">=</span>option_icon,
                                                                hSubMenu<span class="syntax18">=</span>submenu)
                win32gui.<span class="syntax6">InsertMenuItem</span>(menu, <span class="syntax5">0</span>, <span class="syntax5">1</span>, item)

    <span class="syntax8">def</span> <span class="syntax6">prep_menu_icon</span>(self, icon):
        <span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1">First</span><span class="syntax1"> </span><span class="syntax1">load</span><span class="syntax1"> </span><span class="syntax1">the</span><span class="syntax1"> </span><span class="syntax1">icon.</span>
        ico_x <span class="syntax18">=</span> win32api.<span class="syntax6">GetSystemMetrics</span>(win32con.SM_CXSMICON)
        ico_y <span class="syntax18">=</span> win32api.<span class="syntax6">GetSystemMetrics</span>(win32con.SM_CYSMICON)
        hicon <span class="syntax18">=</span> win32gui.<span class="syntax6">LoadImage</span>(<span class="syntax5">0</span>, icon, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

        hdcBitmap <span class="syntax18">=</span> win32gui.<span class="syntax6">CreateCompatibleDC</span>(<span class="syntax5">0</span>)
        hdcScreen <span class="syntax18">=</span> win32gui.<span class="syntax6">GetDC</span>(<span class="syntax5">0</span>)
        hbm <span class="syntax18">=</span> win32gui.<span class="syntax6">CreateCompatibleBitmap</span>(hdcScreen, ico_x, ico_y)
        hbmOld <span class="syntax18">=</span> win32gui.<span class="syntax6">SelectObject</span>(hdcBitmap, hbm)
        <span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1">Fill</span><span class="syntax1"> </span><span class="syntax1">the</span><span class="syntax1"> </span><span class="syntax1">background.</span>
        brush <span class="syntax18">=</span> win32gui.<span class="syntax6">GetSysColorBrush</span>(win32con.COLOR_MENU)
        win32gui.<span class="syntax6">FillRect</span>(hdcBitmap, (<span class="syntax5">0</span>, <span class="syntax5">0</span>, <span class="syntax5">16</span>, <span class="syntax5">16</span>), brush)
        <span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1">unclear</span><span class="syntax1"> </span><span class="syntax1">if</span><span class="syntax1"> </span><span class="syntax1">brush</span><span class="syntax1"> </span><span class="syntax1">needs</span><span class="syntax1"> </span><span class="syntax1">to</span><span class="syntax1"> </span><span class="syntax1">be</span><span class="syntax1"> </span><span class="syntax1">feed.</span><span class="syntax1"> </span><span class="syntax1"> </span><span class="syntax1">Best</span><span class="syntax1"> </span><span class="syntax1">clue</span><span class="syntax1"> </span><span class="syntax1">I</span><span class="syntax1"> </span><span class="syntax1">can</span><span class="syntax1"> </span><span class="syntax1">find</span><span class="syntax1"> </span><span class="syntax1">is:</span>
        <span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1">"GetSysColorBrush</span><span class="syntax1"> </span><span class="syntax1">returns</span><span class="syntax1"> </span><span class="syntax1">a</span><span class="syntax1"> </span><span class="syntax1">cached</span><span class="syntax1"> </span><span class="syntax1">brush</span><span class="syntax1"> </span><span class="syntax1">instead</span><span class="syntax1"> </span><span class="syntax1">of</span><span class="syntax1"> </span><span class="syntax1">allocating</span><span class="syntax1"> </span><span class="syntax1">a</span><span class="syntax1"> </span><span class="syntax1">new</span>
        <span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1">one."</span><span class="syntax1"> </span><span class="syntax1">-</span><span class="syntax1"> </span><span class="syntax1">implies</span><span class="syntax1"> </span><span class="syntax1">no</span><span class="syntax1"> </span><span class="syntax1">DeleteObject</span>
        <span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1">draw</span><span class="syntax1"> </span><span class="syntax1">the</span><span class="syntax1"> </span><span class="syntax1">icon</span>
        win32gui.<span class="syntax6">DrawIconEx</span>(hdcBitmap, <span class="syntax5">0</span>, <span class="syntax5">0</span>, hicon, ico_x, ico_y, <span class="syntax5">0</span>, <span class="syntax5">0</span>, win32con.DI_NORMAL)
        win32gui.<span class="syntax6">SelectObject</span>(hdcBitmap, hbmOld)
        win32gui.<span class="syntax6">DeleteDC</span>(hdcBitmap)
        
        <span class="syntax8">return</span> hbm

    <span class="syntax8">def</span> <span class="syntax6">command</span>(self, hwnd, msg, wparam, lparam):
        <span class="syntax9">id</span> <span class="syntax18">=</span> win32gui.<span class="syntax6">LOWORD</span>(wparam)
        self.<span class="syntax6">execute_menu_option</span>(<span class="syntax9">id</span>)
        
    <span class="syntax8">def</span> <span class="syntax6">execute_menu_option</span>(self, <span class="syntax9">id</span>):
        menu_action <span class="syntax18">=</span> self.menu_actions_by_id[<span class="syntax9">id</span>]      
        <span class="syntax8">if</span> menu_action <span class="syntax18">=</span><span class="syntax18">=</span> self.QUIT:
            win32gui.<span class="syntax6">DestroyWindow</span>(self.hwnd)
        <span class="syntax8">else</span>:
            <span class="syntax6">menu_action</span>(self)
            
<span class="syntax8">def</span> <span class="syntax6">non_string_iterable</span>(obj):
    <span class="syntax8">try</span>:
        <span class="syntax9">iter</span>(obj)
    <span class="syntax8">except</span> <span class="syntax10">TypeError</span>:
        <span class="syntax8">return</span> <span class="syntax10">False</span>
    <span class="syntax8">else</span>:
        <span class="syntax8">return</span> <span class="syntax8">not</span> <span class="syntax9">isinstance</span>(obj, basestring)

<span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1">Minimal</span><span class="syntax1"> </span><span class="syntax1">self</span><span class="syntax1"> </span><span class="syntax1">test.</span><span class="syntax1"> </span><span class="syntax1">You'll</span><span class="syntax1"> </span><span class="syntax1">need</span><span class="syntax1"> </span><span class="syntax1">a</span><span class="syntax1"> </span><span class="syntax1">bunch</span><span class="syntax1"> </span><span class="syntax1">of</span><span class="syntax1"> </span><span class="syntax1">ICO</span><span class="syntax1"> </span><span class="syntax1">files</span><span class="syntax1"> </span><span class="syntax1">in</span><span class="syntax1"> </span><span class="syntax1">the</span><span class="syntax1"> </span><span class="syntax1">current</span><span class="syntax1"> </span><span class="syntax1">working</span>
<span class="syntax1">#</span><span class="syntax1"> </span><span class="syntax1">directory</span><span class="syntax1"> </span><span class="syntax1">in</span><span class="syntax1"> </span><span class="syntax1">order</span><span class="syntax1"> </span><span class="syntax1">for</span><span class="syntax1"> </span><span class="syntax1">this</span><span class="syntax1"> </span><span class="syntax1">to</span><span class="syntax1"> </span><span class="syntax1">work...</span>
<span class="syntax8">if</span> <span class="syntax10">__name__</span> <span class="syntax18">=</span><span class="syntax18">=</span> <span class="syntax13">'</span><span class="syntax13">__main__</span><span class="syntax13">'</span>:
    <span class="syntax8">import</span> itertools, glob
    
    icons <span class="syntax18">=</span> itertools.<span class="syntax6">cycle</span>(glob.<span class="syntax6">glob</span>(<span class="syntax13">'</span><span class="syntax13">*</span><span class="syntax13">.</span><span class="syntax13">ico</span><span class="syntax13">'</span>))
    hover_text <span class="syntax18">=</span> <span class="syntax13">"</span><span class="syntax13">SysTrayIcon</span><span class="syntax13">.</span><span class="syntax13">py</span><span class="syntax13"> </span><span class="syntax13">Demo</span><span class="syntax13">"</span>
    <span class="syntax8">def</span> <span class="syntax6">hello</span>(sysTrayIcon): <span class="syntax8">print</span> <span class="syntax13">"</span><span class="syntax13">Hello</span><span class="syntax13"> </span><span class="syntax13">World</span><span class="syntax13">.</span><span class="syntax13">"</span>
    <span class="syntax8">def</span> <span class="syntax6">simon</span>(sysTrayIcon): <span class="syntax8">print</span> <span class="syntax13">"</span><span class="syntax13">Hello</span><span class="syntax13"> </span><span class="syntax13">Simon</span><span class="syntax13">.</span><span class="syntax13">"</span>
    <span class="syntax8">def</span> <span class="syntax6">switch_icon</span>(sysTrayIcon):
        sysTrayIcon.icon <span class="syntax18">=</span> icons.<span class="syntax6">next</span>()
        sysTrayIcon.<span class="syntax6">refresh_icon</span>()
    menu_options <span class="syntax18">=</span> ((<span class="syntax13">'</span><span class="syntax13">Say</span><span class="syntax13"> </span><span class="syntax13">Hello</span><span class="syntax13">'</span>, icons.<span class="syntax6">next</span>(), hello),
                    (<span class="syntax13">'</span><span class="syntax13">Switch</span><span class="syntax13"> </span><span class="syntax13">Icon</span><span class="syntax13">'</span>, <span class="syntax10">None</span>, switch_icon),
                    (<span class="syntax13">'</span><span class="syntax13">A</span><span class="syntax13"> </span><span class="syntax13">sub</span><span class="syntax13">-</span><span class="syntax13">menu</span><span class="syntax13">'</span>, icons.<span class="syntax6">next</span>(), ((<span class="syntax13">'</span><span class="syntax13">Say</span><span class="syntax13"> </span><span class="syntax13">Hello</span><span class="syntax13"> </span><span class="syntax13">to</span><span class="syntax13"> </span><span class="syntax13">Simon</span><span class="syntax13">'</span>, icons.<span class="syntax6">next</span>(), simon),
                                                  (<span class="syntax13">'</span><span class="syntax13">Switch</span><span class="syntax13"> </span><span class="syntax13">Icon</span><span class="syntax13">'</span>, icons.<span class="syntax6">next</span>(), switch_icon),
                                                 ))
                   )
    <span class="syntax8">def</span> <span class="syntax6">bye</span>(sysTrayIcon): <span class="syntax8">print</span> <span class="syntax13">'</span><span class="syntax13">Bye</span><span class="syntax13">,</span><span class="syntax13"> </span><span class="syntax13">then</span><span class="syntax13">.</span><span class="syntax13">'</span>
    
    <span class="syntax6">SysTrayIcon</span>(icons.<span class="syntax6">next</span>(), hover_text, menu_options, on_quit<span class="syntax18">=</span>bye, default_menu_index<span class="syntax18">=</span><span class="syntax5">1</span>)
</pre>


</body></html>