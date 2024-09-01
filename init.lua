-- Import necessary Hammerspoon modules
local hotkey = require "hs.hotkey"
local window = require "hs.window"
local screen = require "hs.screen"

-- Import necessary Hammerspoon modules
local hotkey = require "hs.hotkey"
local window = require "hs.window"
local screen = require "hs.screen"

-- Function to find a window by its title or application name
local function findWindowByTitleOrAppName(titleOrAppName)
    local windows = window.allWindows()
    for _, win in ipairs(windows) do
        if string.find(win:title(), titleOrAppName) or string.find(win:application():name(), titleOrAppName) then
            return win
        end
    end
    return nil
end

-- Function to reset the size of a window to its original size
local function resetWindowSize(win)
    if win then
        local originalFrame = win:screen():frame()
        win:setFrame(originalFrame)
    end
end

-- Function to resize and reposition windows to occupy specific portions of the screen
local function resizeWindows()
    -- Get the screen's dimensions
    local screenFrame = screen.mainScreen():frame()
    local halfWidth = screenFrame.w / 2
    local halfHeight = screenFrame.h / 2
    local quarterWidth = screenFrame.w / 4
    local quarterHeight = screenFrame.h / 4
    local eighthWidth = screenFrame.w / 8
    local eighthHeight = screenFrame.h / 8

    -- Define separate sizes for "Schedule" and "Aggregator"
    local commonHeight = halfHeight
    local scheduleWidth = eighthWidth * 2
    local aggregatorWidth = eighthWidth * 2
    local scoresWidth = halfWidth
    local scoresHeight = quarterHeight

    -- Define the target window positions
    local positions = {
        {x = 0, y = 0, w = quarterWidth, h = halfHeight},                   -- Top-left corner
        {x = halfWidth, y = 0, w = halfWidth, h = scoresHeight},           -- Top-right corner
        {x = 0, y = halfHeight, w = halfWidth, h = halfHeight},          -- Bottom-left corner
        {x = screenFrame.w - 4* eighthWidth, y = screenFrame.h - commonHeight, w = scheduleWidth, h = commonHeight}, -- Bottom-right corner (1/8 for "Schedule")
        {x = screenFrame.w - aggregatorWidth, y = screenFrame.h - commonHeight, w = aggregatorWidth, h = commonHeight}, -- Bottom-right corner (1/8 for "Aggregator")
        {x = scoresWidth, y = scoresHeight, w = scoresWidth, h = scoresHeight},
        {x = quarterWidth, y = 0, w = quarterWidth, h = halfHeight}
    }

    -- List of window titles or application names to resize and reposition
    local windowTitlesOrAppNames = {"Focus", "Food", "Lifting", "Schedule", "Aggregator", "Scores", "Tasks"}

    -- Resize and reposition each window to its corresponding position
    for i, titleOrAppName in ipairs(windowTitlesOrAppNames) do
        local win = findWindowByTitleOrAppName(titleOrAppName)
        if win and positions[i] then
            resetWindowSize(win) -- Reset the window size before resizing
            print("Resizing window: " .. titleOrAppName .. " to x: " .. positions[i].x .. ", y: " .. positions[i].y .. ", w: " .. positions[i].w .. ", h: " .. positions[i].h)
            local frame = positions[i]
            win:setFrame(frame)
        else
            print("Window not found or no position available for: " .. titleOrAppName)
        end
    end
end

-- Bind the hotkey to run the function
hotkey.bind({"ctrl", "alt", "cmd"}, "P", function()
    resizeWindows()
end)

-- Existing script functionalities
hs.ipc.cliUninstall()
hs.ipc.cliInstall()

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

-- Import necessary Hammerspoon modules
local hotkey = require "hs.hotkey"
local window = require "hs.window"

-- Function to find a window by its title or application name
local function findWindowByTitleOrAppName(titleOrAppName)
    local windows = window.allWindows()
    for _, win in ipairs(windows) do
        if string.find(win:title(), titleOrAppName) or string.find(win:application():name(), titleOrAppName) then
            return win
        end
    end
    return nil
end

-- Function to close windows by their titles or application names
local function closeWindows()
    -- List of window titles or application names to close
    local windowTitlesOrAppNames = {"Focus", "Food", "Lifting", "Schedule", "Aggregator", "Scores", "Tasks"}

    -- Close each window
    for _, titleOrAppName in ipairs(windowTitlesOrAppNames) do
        local win = findWindowByTitleOrAppName(titleOrAppName)
        if win then
            win:close()
            print("Closed window: " .. titleOrAppName)
        else
            print("Window not found: " .. titleOrAppName)
        end
    end
end

-- Bind the hotkey to run the function
hotkey.bind({"cmd", "alt", "ctrl"}, "O", function()
    closeWindows()
end)