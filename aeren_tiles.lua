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

-- Function to resize and reposition windows to occupy 4 quarters of the screen
local function resizeWindows()
    -- Get the screen's dimensions
    local screenFrame = screen.mainScreen():frame()
    local width = screenFrame.w / 2
    local height = screenFrame.h / 2

    -- Define the target window positions
    local positions = {
        {x = 0, y = 0},                   -- Top-left corner
        {x = width, y = 0},               -- Top-right corner
        {x = 0, y = screenFrame.h / 2},   -- Bottom-left corner
        {x = width, y = screenFrame.h / 2} -- Bottom-right corner
    }

    -- List of window titles or application names to resize and reposition
    local windowTitlesOrAppNames = {"Books", "Deepwork", "Schedule", "Food"}

    -- Resize and reposition each window to its corresponding position
    for i, titleOrAppName in ipairs(windowTitlesOrAppNames) do
        local win = findWindowByTitleOrAppName(titleOrAppName)
        if win and positions[i] then
            print("Resizing window: " .. titleOrAppName)
            local frame = {x = positions[i].x, y = positions[i].y, w = width, h = height}
            win:setFrame(frame)
        else
            print("Window not found or no position available for: " .. titleOrAppName)
        end
    end
end

-- Execute the function
resizeWindows()