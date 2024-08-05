-- Make cli command `hs` available: 
 -- After an update of hammerspoon run following two commmands once in the hammerspoon console 
 -- hs.ipc.cliUninstall(); hs.ipc.cliInstall() 
 
 require("hs.ipc") 
 
 hs.hotkey.bind({"cmd", "alt", "ctrl"}, "W", function()
  hs.alert.show("Hello World!")
end)

hs.loadSpoon("AClock")
hs.hotkey.bind({"cmd", "alt", "ctrl"}, "C", function()
  spoon.AClock:toggleShow()
end)


hs.hotkey.bind({"cmd", "alt", "ctrl"}, "Left", function()
  local win = hs.window.focusedWindow()
  local f = win:frame()
  local screen = win:screen()
  local max = screen:frame()

  f.x = max.x
  f.y = max.y
  f.w = max.w / 2
  f.h = max.h
  win:setFrame(f)
end)

hs.hotkey.bind({"cmd", "alt", "ctrl"}, "Right", function()
  local win = hs.window.focusedWindow()
  local f = win:frame()
  local screen = win:screen()
  local max = screen:frame()

  f.x = max.x + (max.w / 2)
  f.y = max.y
  f.w = max.w / 2
  f.h = max.h
  win:setFrame(f)
end)

hs.hotkey.bind({"cmd", "alt", "ctrl"}, "Up", function()
  local win = hs.window.focusedWindow()
  local f = win:frame()
  local screen = win:screen()
  local max = screen:frame()

  f.x = max.x
  f.y = max.y
  f.w = max.w
  f.h = max.h
  win:setFrame(f)
end)

  
--  local function intersect(m,n) 
--   local r={} 
--   for i,v1 in ipairs(m) do 
--    for k,v2 in pairs(n) do 
--     if (v1==v2) then 
--      return true 
--     end 
--    end 
--   end 
--   return false 
--  end 
  
--  local function has_value (tab, val) 
--      for index, value in ipairs(tab) do 
--          if value == val then 
--              return true 
--          end 
--      end 
--      return false 
--  end 
  
--  function create_svg_and_paste(keys) 
  
--      pt = 1.327 -- pixels 
--      w = .5 * pt 
--      thick_width = 1 * pt 
--      very_thick_width = 2 * pt 
  
--      style = {} 
--      style["stroke-opacity"] = 1 
  
--      if intersect({"s", "a", "d", "g", "h", "x", "e"}, keys) 
--      then 
--          style["stroke"] = "black" 
--          style["stroke-width"] = w 
--          style["marker-end"] = "none" 
--          style["marker-start"] = "none" 
--          style["stroke-dasharray"] = "none" 
--      else 
--          style["stroke"] = "none" 
--      end 
  
--      if has_value(keys, "g") 
--      then 
--          w = thick_width 
--          style["stroke-width"] = w 
--      end 
  
--      if has_value(keys, "v") 
--      then 
--          w = very_thick_width 
--          style["stroke-width"] = w 
--      end 
  
--      if has_value(keys, "a") 
--      then 
--          style['marker-end'] = 'url(#marker-arrow-' .. tostring(w) .. ')' 
--      end 
  
--      if has_value(keys, "x") 
--      then 
--          style['marker-start'] = 'url(#marker-arrow-' .. tostring(w) .. ')' 
--          style['marker-end'] = 'url(#marker-arrow-' .. tostring(w) .. ')' 
--      end 
  
--      if has_value(keys, "d") 
--      then 
--          style['stroke-dasharray'] = tostring(w) .. ',' .. tostring(2*pt) 
--      end 
  
--      if has_value(keys, "e") 
--      then 
--          style['stroke-dasharray'] = tostring(3*pt) .. ',' .. tostring(3*pt) 
--      end 
  
--      if has_value(keys, "f") 
--      then 
--          style['fill'] = 'black' 
--          style['fill-opacity'] = 0.12 
--      end 
  
--      if has_value(keys, "b") 
--      then 
--          style['fill'] = 'black' 
--          style['fill-opacity'] = 1 
--      end 
  
--      if has_value(keys, "w") 
--      then 
--          style['fill'] = 'white' 
--          style['fill-opacity'] = 1 
--      end 
  
--      if intersect(keys, {"f", "b", "w"}) 
--      then 
--          style['marker-end'] = 'none' 
--          style['marker-start'] = 'none' 
--      end 
  
--      if not intersect(keys, {"f", "b", "w"}) 
--      then 
--          style['fill'] = 'none' 
--          style['fill-opacity'] = 1 
--      end 
  
--      svg = [[ 
--  <?xml version="1.0" encoding="UTF-8" standalone="no"?> 
--  <svg> 
--  ]] 
  
--      if (style['marker-end'] ~= nil and style['marker-end'] ~= 'none') or 
--         (style['marker-start'] ~= nil and style['marker-start'] ~= 'none') 
--      then 
--          svgtemp = [[ 
--  <defs id="marker-defs"> 
--  <marker 
--  ]] 
--          svgtemp = svgtemp .. 'id="marker-arrow-' .. tostring(w) .. "\"\n" 
--          svgtemp = svgtemp .. 'orient="auto-start-reverse"' .. "\n" 
--          svgtemp = svgtemp .. 'refY="0" refX="0"' .. "\n" 
--          svgtemp = svgtemp .. 'markerHeight="3" markerWidth="2">' .. "\n" 
  
--          svgtemp = svgtemp .. '    <g transform="scale('.. tostring((2.40 * w + 3.87)/(4.5*w)) .. ')">' .. "\n" 
--          svg = svg .. svgtemp 
--          svgtemp = [[ 
--      <path 
--         d="M -1.55415,2.0722 C -1.42464,1.29512 0,0.1295 0.38852,0 0,-0.1295 -1.42464,-1.29512 -1.55415,-2.0722" 
--         style="fill:none;stroke:#000000;stroke-width:{0.6};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:10;stroke-dasharray:none;stroke-opacity:1 
--         inkscape:connector-curvature="0" /> 
--     </g> 
--  </marker> 
--  </defs> 
--  ]] 
--          svg = svg .. svgtemp 
--      end 
   
--      style_string = '' 
--      for key, value in pairs(style) do 
--          -- skips nil? 
--          style_string = style_string .. key .. ":" .. " " .. value .. ";" 
--      end 
  
--      svg = svg .. '<inkscape:clipboard style="' .. style_string .. '" />' .. "\n</svg>" 
  
--      hs.pasteboard.writeDataForUTI("dyn.ah62d4rv4gu80w5pbq7ww88brrf1g065dqf2gnppxs3xu", svg) 
--      -- get UTI via https://github.com/sindresorhus/Pasteboard-Viewer 
--      hs.eventtap.keyStroke({"shift", "cmd"}, "v") 
--  end 
 --[[
-- Function to get the currently focused window and the window directly behind it, and place them side by side
function arrangeClosestWindows()
    -- Get the currently focused window
    local focusedWindow = hs.window.focusedWindow()
    
    if not focusedWindow then
        hs.alert.show("No focused window found")
        print("No focused window found")
        return
    end
    
    -- Get all visible windows
    local windows = hs.window.filter.new():setCurrentSpace(true):getWindows()
    print(windows)
    
    -- Find the index of the focused window
    local focusedIndex = nil
    for i, window in ipairs(windows) do
        if window == focusedWindow then
            focusedIndex = i
            break
        end
    end
    
    -- Check if we have found the focused window and there's another window behind it
    if not focusedIndex or focusedIndex == #windows then
        hs.alert.show("Not enough windows available")
        print("Not enough windows available")
        return
    end
    
    -- Get the window directly behind the focused window
    local behindWindow = windows[focusedIndex + 1]
    
    -- Get the main screen and its dimensions
    local screen = hs.screen.mainScreen()
    local screenFrame = screen:frame()
    
    -- Calculate half the screen width
    local halfWidth = screenFrame.w / 2
    
    -- Define the new frames for the windows
    local focusedWindowFrame = {
        x = screenFrame.x,
        y = screenFrame.y,
        w = halfWidth,
        h = screenFrame.h
    }
    
    local behindWindowFrame = {
        x = screenFrame.x + halfWidth,
        y = screenFrame.y,
        w = halfWidth,
        h = screenFrame.h
    }
    
    -- Move and resize the windows
    focusedWindow:setFrame(focusedWindowFrame)
    behindWindow:setFrame(behindWindowFrame)
    
end

-- Bind the function to a hotkey, for example, Ctrl + Alt + Cmd + I
hs.hotkey.bind({"ctrl", "alt", "cmd"}, "I", arrangeClosestWindows)

]]

-- Load necessary modules
local window = require "hs.window"
local screen = require "hs.screen"
local application = require "hs.application"

-- Function to find a window by its title
local function findWindowByTitle(title)
    local wins = window.filter.default:getWindows()
    for _, win in ipairs(wins) do
        if string.find(win:title(), title) then
            return win
        end
    end
    return nil
end

-- Function to get the currently focused window and the specified window, and place them side by side
local function arrangeFocusedAndSpecifiedWindow(title)
    -- Get the currently focused window
    local focusedWindow = hs.window.focusedWindow()
    
    if not focusedWindow then
        hs.alert.show("No focused window found")
        return
    end
    
    -- Get the window with the specified title
    local specifiedWindow = findWindowByTitle(title)
    if not specifiedWindow then
        hs.alert.show("Specified window not found: " .. title)
        return
    end
    
    -- Get the main screen and its dimensions
    local screenFrame = screen.mainScreen():frame()
    
    -- Calculate half the screen width
    local halfWidth = screenFrame.w / 2
    
    -- Define the new frames for the windows
    local focusedWindowFrame = {
        x = screenFrame.x,
        y = screenFrame.y,
        w = halfWidth,
        h = screenFrame.h
    }
    
    local specifiedWindowFrame = {
        x = screenFrame.x + halfWidth,
        y = screenFrame.y,
        w = halfWidth,
        h = screenFrame.h
    }
    
    -- Move and resize the windows
    focusedWindow:setFrame(focusedWindowFrame)
    specifiedWindow:setFrame(specifiedWindowFrame)
    
end

-- Bind the function to a hotkey and provide a default title for demonstration
hs.hotkey.bind({"cmd", "alt", "ctrl"}, "P", function()
    arrangeFocusedAndSpecifiedWindow("Schedule") -- Replace with the title of the window you want to arrange with the focused window
end)