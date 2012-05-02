-- Standard awesome library
require("awful")
require("awful.autofocus")
require("awful.rules")
-- Theme handling library
require("beautiful")
-- Notification library
require("naughty")
-- Load Debian menu entries
require("debian.menu")

-- {{{ Variable definitions
-- myconfdir = os.getenv("HOME") .. "/.config/awesome"
myconfdir = awful.util.getdir("config")
myicon = os.getenv("HOME") .. "/.icons/el-80x80.png"

-- Themes define colours, icons, and wallpapers
-- beautiful.init("/usr/share/awesome/themes/sky/theme.lua")
beautiful.init(myconfdir .. "/mysky.lua")

-- This is used later as the default terminal and editor to run.
--terminal = "x-terminal-emulator"
terminal = "urxvt"
editor = os.getenv("EDITOR") or "editor"
editor_cmd = terminal .. " -e " .. editor

-- Default modkey.
-- Usually, Mod4 is the key with a logo between Control and Alt.
-- If you do not like this or do not have such a key,
-- I suggest you to remap Mod4 to another key using xmodmap or other tools.
-- However, you can use another modifier like Mod1, but it may interact with others.
modkey = "Mod4"

-- Table of layouts to cover with awful.layout.inc, order matters.
layouts = {
   awful.layout.suit.floating,
   awful.layout.suit.tile,
   awful.layout.suit.tile.left,
   awful.layout.suit.tile.bottom,
   awful.layout.suit.tile.top,
   awful.layout.suit.fair,
   awful.layout.suit.fair.horizontal,
   awful.layout.suit.spiral,
   awful.layout.suit.spiral.dwindle,
   awful.layout.suit.max,
   awful.layout.suit.max.fullscreen,
   awful.layout.suit.magnifier
}
-- }}}

-- {{{ Tags
-- Define a tag table which hold all screen tags.
-- tags = {}
-- for s = 1, screen.count() do
--    -- Each screen has its own tag table.
--    tags[s] = awful.tag({ 1, 2, 3, 4, 5, 6, 7, 8, 9 }, s, layouts[1])
-- end
tags = {
   names = { "file", 2, "net", 4, "emacs", 6, "doc", 8, "misc" },
   layout = { layouts[1], layouts[1], layouts[1], layouts[1], layouts[2],
	      layouts[1], layouts[1], layouts[1], layouts[1] }
}
for s = 1, screen.count() do
   tags[s] = awful.tag(tags.names, s, tags.layout)
end
-- }}}

-- {{{ Menu
-- Create a laucher widget and a main menu
myawesomemenu = {
   { "Manual", terminal .. " -e man awesome" },
   { "Edit config", editor_cmd .. " " .. awful.util.getdir("config") .. "/rc.lua" },
   { "Restart", awesome.restart },
   { "Quit", awesome.quit },
   { "GDM Switch",  "gdmflexiserver", "/usr/share/pixmaps/gdm.png"},
}

mycommons = {
   -- {"Emacs 23",     "emacs23",       "/usr/share/pixmaps/gnome-emacs.png" },
   {"Emacs23 Client", "emacsclient.emacs23 -nc", "/usr/share/pixmaps/gnome-emacs.png" },
   {"ipython", terminal .. " -e ipython" },
   {"bpython", terminal .. " -e bpython", "/usr/share/pixmaps/python.xpm" },
   {"bpython-gtk", "bpython-gtk", "/usr/share/pixmaps/bpython.png" },
   -- { "File Manager", "pcmanfm",    "/usr/share/pixmaps/gnome-folder.png" },
   {"Dolphin", "dolphin", "/usr/share/icons/oxygen/64x64/places/folder.png"},
   {"Nautilus","nautilus --no-desktop","/usr/share/pixmaps/gnome-folder.png" },
   {"VirtualBox",   "VirtualBox",    "/usr/share/pixmaps/VBox.png" },
   {"Google Chrome","google-chrome", "/opt/google/chrome/product_logo_64.png" },
   -- { "Iceweasel",    "iceweasel",  "/usr/share/pixmaps/iceweasel.png" },
   -- { "Pidgin",       "pidgin",     "/usr/share/pixmaps/pidgin-menu.xpm" },
}

mymainmenu = awful.menu(
   {
      items = {
	 {"Awesome", myawesomemenu, beautiful.awesome_icon },
	 {"Debian", debian.menu.Debian_menu.Debian,
	  "/usr/share/pixmaps/debian-logo.png" },
	 {"My Apps", mycommons, myicon },
	 {"Open Term", terminal, "/usr/share/pixmaps/gnome-xterm.png" },
   }})

mylauncher = awful.widget.launcher({ image = image(beautiful.awesome_icon),
                                     menu = mymainmenu })
-- }}}

-- {{{ Wibox
mycombutton = awful.widget.launcher(
   { image = image(myicon), menu = awful.menu({items = mycommons}) })

-- Create a textclock widget
mytextclock = awful.widget.textclock({ align = "right" })

-- Create a systray
mysystray = widget({ type = "systray" })

-- Create a wibox for each screen and add it
mywibox = {}
mypromptbox = {}
mylayoutbox = {}
mytaglist = {}
mytaglist.buttons = awful.util.table.join(
   awful.button({ }, 1, awful.tag.viewonly),
   awful.button({ modkey }, 1, awful.client.movetotag),
   awful.button({ }, 3, awful.tag.viewtoggle),
   awful.button({ modkey }, 3, awful.client.toggletag),
   awful.button({ }, 4, awful.tag.viewnext),
   awful.button({ }, 5, awful.tag.viewprev)
)
mytasklist = {}
mytasklist.buttons = awful.util.table.join(
   awful.button({ }, 1,
		function (c)
		   if not c:isvisible() then
		      awful.tag.viewonly(c:tags()[1])
		   end
		   client.focus = c
		   c:raise()
		end),
   awful.button({ }, 3,
		function ()
		   if instance then
		      instance:hide()
		      instance = nil
		   else
		      instance = awful.menu.clients({ width=250 })
		   end
		end),
   awful.button({ }, 4,
		function ()
		   awful.client.focus.byidx(1)
		   if client.focus then client.focus:raise() end
		end),
   awful.button({ }, 5,
		function ()
		   awful.client.focus.byidx(-1)
		   if client.focus then client.focus:raise() end
		end))

for s = 1, screen.count() do
   -- Create a promptbox for each screen
   mypromptbox[s] = awful.widget.prompt(
      { layout = awful.widget.layout.horizontal.leftright })
   -- Create an imagebox widget which will contains an icon indicating which
   -- layout we're using.  We need one layoutbox per screen.
   mylayoutbox[s] = awful.widget.layoutbox(s)
   mylayoutbox[s]:buttons(
      awful.util.table.join(
	 awful.button({}, 1, function () awful.layout.inc(layouts,  1) end),
	 awful.button({}, 3, function () awful.layout.inc(layouts, -1) end),
	 awful.button({}, 4, function () awful.layout.inc(layouts,  1) end),
	 awful.button({}, 5, function () awful.layout.inc(layouts, -1) end)))
   -- Create a taglist widget
   mytaglist[s] = awful.widget.taglist(
      s, awful.widget.taglist.label.all, mytaglist.buttons)

   -- Create a tasklist widget
   mytasklist[s] = awful.widget.tasklist(
      function(c)
	 return awful.widget.tasklist.label.currenttags(c, s)
      end, mytasklist.buttons)

   -- Create the wibox
   mywibox[s] = awful.wibox({ position = "top", screen = s })
   -- Add widgets to the wibox - order matters
   mywibox[s].widgets = {
      {
	 mylauncher,
	 mytaglist[s],
	 mycombutton,
	 mypromptbox[s],
	 layout = awful.widget.layout.horizontal.leftright
      },
      mylayoutbox[s],
      mytextclock,
      s == 1 and mysystray or nil,
      mytasklist[s],
      layout = awful.widget.layout.horizontal.rightleft
   }
end
-- }}}

-- {{{ Mouse bindings
root.buttons(awful.util.table.join(
		awful.button({ }, 3, function () mymainmenu:toggle() end),
		awful.button({ }, 4, awful.tag.viewnext),
		awful.button({ }, 5, awful.tag.viewprev)
	  ))
-- }}}

-- {{{ Key bindings
globalkeys = awful.util.table.join(
   awful.key({ modkey,           }, "Left",   awful.tag.viewprev       ),
   awful.key({ modkey,           }, "Right",  awful.tag.viewnext       ),
   awful.key({ modkey,           }, "Escape", awful.tag.history.restore),
   awful.key({ modkey,           }, "j",
	     function ()
		awful.client.focus.byidx( 1)
		if client.focus then client.focus:raise() end
	     end),
   awful.key({ modkey,           }, "k",
	     function ()
		awful.client.focus.byidx(-1)
		if client.focus then client.focus:raise() end
	     end),
   awful.key({ modkey,           }, "w",
	     function () mymainmenu:show({keygrabber=true}) end),

   -- Layout manipulation
   awful.key({ modkey, "Shift"   }, "j",
	     function () awful.client.swap.byidx(  1)    end),
   awful.key({ modkey, "Shift"   }, "k",
	     function () awful.client.swap.byidx( -1)    end),
   awful.key({ modkey, "Control" }, "j",
	     function () awful.screen.focus_relative( 1) end),
   awful.key({ modkey, "Control" }, "k",
	     function () awful.screen.focus_relative(-1) end),
   awful.key({ modkey,           }, "u", awful.client.urgent.jumpto),
   awful.key({ modkey,           }, "Tab",
	     function ()
		awful.client.focus.history.previous()
		if client.focus then
		   client.focus:raise()
		end
	     end),

   -- Standard program
   awful.key({ modkey,           }, "Return",
	     function () awful.util.spawn(terminal) end),
   awful.key({ modkey, "Control" }, "r", awesome.restart),
   awful.key({ modkey, "Shift"   }, "q", awesome.quit),

   awful.key({ modkey,           }, "l",
	     function () awful.tag.incmwfact( 0.05)    end),
   awful.key({ modkey,           }, "h",
	     function () awful.tag.incmwfact(-0.05)    end),
   awful.key({ modkey, "Shift"   }, "h",
	     function () awful.tag.incnmaster( 1)      end),
   awful.key({ modkey, "Shift"   }, "l",
	     function () awful.tag.incnmaster(-1)      end),
   awful.key({ modkey, "Control" }, "h",
	     function () awful.tag.incncol( 1)         end),
   awful.key({ modkey, "Control" }, "l",
	     function () awful.tag.incncol(-1)         end),
   awful.key({ modkey,           }, "space",
	     function () awful.layout.inc(layouts,  1) end),
   awful.key({ modkey, "Shift"   }, "space",
	     function () awful.layout.inc(layouts, -1) end),

   -- Prompt
   awful.key({ modkey },            "r",
	     function () mypromptbox[mouse.screen]:run() end),

   awful.key({ modkey }, "x",
	     function ()
		awful.prompt.run({ prompt = "Run Lua code: " },
				 mypromptbox[mouse.screen].widget,
				 awful.util.eval, nil,
				 awful.util.getdir("cache") .. "/history_eval")
	     end),

   -- toggle wibox visibility
   awful.key({ modkey }, "b",
	     function ()
		mywibox[mouse.screen].visible = not mywibox[mouse.screen].visible
	     end),

   -- Xscreensaver
   awful.key({ modkey, "Control" }, "l",
	     function () awful.util.spawn("xscreensaver-command -lock") end)
)

clientkeys = awful.util.table.join(
   awful.key({ modkey,           }, "f",
	     function (c) c.fullscreen = not c.fullscreen  end),
   awful.key({ modkey, "Shift"   }, "c",
	     function (c) c:kill()                         end),
   awful.key({ modkey, "Control" }, "space",
	     awful.client.floating.toggle                     ),
   awful.key({ modkey, "Control" }, "Return",
	     function (c) c:swap(awful.client.getmaster()) end),
   awful.key({ modkey,           }, "o",
	     awful.client.movetoscreen                        ),
   awful.key({ modkey, "Shift"   }, "r",
	     function (c) c:redraw()                       end),
   awful.key({ modkey,           }, "t",
	     function (c) c.ontop = not c.ontop            end),
   awful.key({ modkey,           }, "n",
	     function (c) c.minimized = not c.minimized    end),
   awful.key({ modkey,           }, "m",
	     function (c)
		c.maximized_horizontal = not c.maximized_horizontal
		c.maximized_vertical   = not c.maximized_vertical
	     end)
)

-- Compute the maximum number of digit we need, limited to 9
keynumber = 0
for s = 1, screen.count() do
   keynumber = math.min(9, math.max(#tags[s], keynumber));
end

-- Bind all key numbers to tags.
-- Be careful: we use keycodes to make it works on any keyboard layout.
-- This should map on the top row of your keyboard, usually 1 to 9.
for i = 1, keynumber do
   globalkeys = awful.util.table.join(
      globalkeys,
      awful.key({ modkey }, "#" .. i + 9,
		function ()
		   local screen = mouse.screen
		   if tags[screen][i] then
		      awful.tag.viewonly(tags[screen][i])
		   end
		end),
      awful.key({ modkey, "Control" }, "#" .. i + 9,
		function ()
		   local screen = mouse.screen
		   if tags[screen][i] then
		      awful.tag.viewtoggle(tags[screen][i])
		   end
		end),
      awful.key({ modkey, "Shift" }, "#" .. i + 9,
		function ()
		   if client.focus and tags[client.focus.screen][i] then
		      awful.client.movetotag(tags[client.focus.screen][i])
		   end
		end),
      awful.key({ modkey, "Control", "Shift" }, "#" .. i + 9,
		function ()
		   if client.focus and tags[client.focus.screen][i] then
		      awful.client.toggletag(tags[client.focus.screen][i])
		   end
		end))
end

clientbuttons = awful.util.table.join(
   awful.button({ }, 1, function (c) client.focus = c; c:raise() end),
   awful.button({ modkey }, 1, awful.mouse.client.move),
   awful.button({ modkey }, 3, awful.mouse.client.resize))

-- Set keys
root.keys(globalkeys)
-- }}}

-- {{{ Rules
awful.rules.rules = {
   -- All clients will match this rule.
   { rule = { },
     properties = { border_width = beautiful.border_width,
		    border_color = beautiful.border_normal,
		    focus = true,
		    keys = clientkeys,
		    buttons = clientbuttons } },
   { rule = { class = "MPlayer" },
     properties = { floating = true } },
   { rule = { class = "Gimp" },
     properties = { floating = true } },
   -- Set file-browser to tag 1: pcmanfm
   { rule = { class = "Pcmanfm" },
     properties = { tag = tags[1][1] } },
   -- Set emacs to tag 5: Emacs
   -- { rule = { class = "Emacs" },
   --   properties = { tag = tags[1][5] } },
   -- Set chrome to always map on tags number 4 of screen 1.
   { rule = { class = "Google-chrome" },
     properties = { tag = tags[1][3], floating = true } },
   -- Set Firefox to always map on tags number 5 of screen 1.
   { rule = { class = "Firefox" },
     properties = { tag = tags[1][2], floating = true } },
   ---------------------------------------------------------
   -- my settings: goldendict
   { rule = { class = "Goldendict" },
     properties = { floating = true } },
}
-- }}}

-- {{{ Signals
-- Signal function to execute when a new client appears.
client.add_signal(
   "manage",
   function (c, startup)
      -- Add a titlebar
      -- awful.titlebar.add(c, { modkey = modkey })

      -- Enable sloppy focus
      c:add_signal(
	 "mouse::enter",
	 function(c)
	    if awful.layout.get(c.screen) ~= awful.layout.suit.magnifier
	    and awful.client.focus.filter(c) then
	    client.focus = c
	 end
      end)
      if not startup then
	 -- Set the windows at the slave, i.e. put it at the end
	 -- of others instead of setting it master.
	 -- awful.client.setslave(c) Put windows in a smart way,
	 -- only if they does not set an initial position.
	 if not c.size_hints.user_position and
	    not c.size_hints.program_position then
	    awful.placement.no_overlap(c)
	    awful.placement.no_offscreen(c)
	 end
      end
   end)

client.add_signal(
   "focus",
   function(c) c.border_color = beautiful.border_focus end)
client.add_signal(
   "unfocus",
   function(c) c.border_color = beautiful.border_normal end)
-- }}}


-- Autorun programs
autorun = true
autorunApps = {
   "xrdb -load " .. os.getenv("HOME") .. "/.Xdefaults",
   "gnome-settings-daemon",
   "goldendict",
   "xscreensaver -nosplash",
}
if autorun then
   for app = 1, #autorunApps do
      awful.util.spawn(autorunApps[app])
   end
end

