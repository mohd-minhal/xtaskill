import ctypes as c
from ctypes import wintypes as w
import os
import signal
import sys

# Define constants
WH_MOUSE_LL = 14
WM_LBUTTONDOWN = 0x0201
WM_CLOSE = 0x0010

class MSLLHOOKSTRUCT(c.Structure):
    _fields_ = [
        ("pt", w.POINT),
        ("mouseData", w.DWORD),
        ("dwExtraInfo", c.c_ulong),
        ("flags", w.DWORD),
        ("time", w.DWORD)
    ]

LOW_LEVEL_MOUSE_PROC = c.WINFUNCTYPE(
    c.c_long, c.c_int, c.c_uint, c.POINTER(MSLLHOOKSTRUCT)
)

user32 = c.WinDLL('user32', use_last_error=True)
kernel32 = c.WinDLL('kernel32', use_last_error=True)

def low_level_mouse_proc(nCode, wParam, lParam):
    if nCode >= 0 and wParam == WM_LBUTTONDOWN:
        pt = w.POINT()
        user32.GetCursorPos(c.byref(pt))
        hwnd = user32.WindowFromPoint(pt)

        if hwnd:
            # If command is to get window handle
            if get_window_handle:
                print(f"Window Handle: {hwnd}")
                try:
                    c.windll.user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)
                    print(f"Window with handle {hwnd} has been closed.")
                except Exception as e:
                    print(f"Error closing window: {e}")

            # Retrieve process ID from window handle
            pid = w.DWORD()
            user32.GetWindowThreadProcessId(hwnd, c.byref(pid))

            # If command is to get process ID
            if not get_window_handle:
                print(f"Process ID: {pid.value}")
                try:
                    os.kill(pid.value, signal.SIGTERM)
                    print(f"Process {pid.value} has been terminated.")
                except ProcessLookupError:
                    print(f"No process with PID {pid.value} found.")
                except PermissionError:
                    print(f"No permission to terminate process {pid.value}.")

            # Stop processing further hooks
            c.windll.user32.PostQuitMessage(0)
    return user32.CallNextHookEx(None, nCode, wParam, lParam)

# Set up the hook
def set_hook():
    hook_proc = LOW_LEVEL_MOUSE_PROC(low_level_mouse_proc)

    hook_id = user32.SetWindowsHookExW(WH_MOUSE_LL, hook_proc, None, 0)
    if not hook_id:
        raise RuntimeError(f'Failed to set hook. Error code: {c.GetLastError()}')

    try:
        msg = w.MSG()
        while user32.GetMessageW(c.byref(msg), None, 0, 0) != 0:
            user32.TranslateMessage(c.byref(msg))
            user32.DispatchMessageW(c.byref(msg))
    except Exception as e:
        print(f"An error occurred during message processing: {e}")
    finally:
        user32.UnhookWindowsHookEx(hook_id)

if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else None
    get_window_handle = command == "-win"

    if get_window_handle:
        print("Click on the window to close it")
    else:
        print("Click on the window to close the process")
    
    set_hook()
