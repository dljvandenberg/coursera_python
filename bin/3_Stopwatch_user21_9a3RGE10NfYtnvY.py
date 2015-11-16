# "Stopwatch: The Game"

# Import modules
import simplegui


# Define helper function format that converts integer
# counting tenths of seconds into formatted string A:BC.D
def format(t):
    tenths = t % 10
    seconds = (t // 10) % 60
    minutes = t // 600
    if seconds < 10:
        prefix = "0"
    else:
        prefix = ""
    return str(minutes) + ":" + prefix + str(seconds) + "." + str(tenths)


# Define event handlers for drawing on canvas
def draw_handler(canvas):
    canvas.draw_text(str(format(time)), [100,110], 30, "Red")
    canvas.draw_text(str(success) + "/" + str(attempt), [270,15], 15, "Red")


# Define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    global running
    timer.start()
    running = True

def stop_handler():
    global running, success, attempt
    if running == True:
        timer.stop()
        running = False
        attempt += 1
        if time % 10 == 0:
            success += 1

def init():
    global time, success, attempt, running
    time = 0
    success = 0
    attempt = 0
    timer.stop()
    running = False


# Define event handler for timer with 0.1 sec interval
def timer_handler():
    global time
    time += 1


# Create frame
frame = simplegui.create_frame("Stopwatch",300,200)


# Register event handlers
frame.set_draw_handler(draw_handler)
button_start = frame.add_button("Start", start_handler)
button_stop = frame.add_button("Stop", stop_handler)
button_reset = frame.add_button("Reset", init)
timer = simplegui.create_timer(100,timer_handler)


# Start timer and frame
init()
frame.start()
