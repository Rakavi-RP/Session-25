# basic import 
print("Starting imports...")
try:
    from mcp.server.fastmcp import FastMCP, Image
    print("Imported FastMCP")
    from mcp.server.fastmcp.prompts import base
    print("Imported prompts")
    from mcp.types import TextContent
    print("Imported TextContent")
    from mcp import types
    print("Imported types")
    from PIL import Image as PILImage
    print("Imported PIL")
    import math
    import sys
    from pywinauto.application import Application
    print("Imported pywinauto")
    import win32gui
    import win32con
    import time
    from win32api import GetSystemMetrics
    print("All imports successful")
    import pyautogui
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    import os
    import pickle
    import base64
    from email.mime.text import MIMEText
except Exception as e:
    print(f"Error during imports: {str(e)}")
    raise

# Global variable to hold Paint application reference
paint_app = None

# instantiate an MCP server client
mcp = FastMCP("Calculator")

# DEFINE TOOLS

#addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("CALLED: add(a: int, b: int) -> int:")
    return int(a + b)

@mcp.tool()
def add_list(l: list) -> int:
    """Add all numbers in a list"""
    print("CALLED: add(l: list) -> int:")
    return sum(l)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)

# square root tool
@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    print("CALLED: sqrt(a: int) -> float:")
    return float(a ** 0.5)

# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> int:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> int:")
    return int(a - b - b)

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(string: str) -> list[int]:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(string: str) -> list[int]:")
    return [int(ord(char)) for char in string]

@mcp.tool()
def int_list_to_exponential_sum(int_list: list) -> float:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(int_list: list) -> float:")
    # Convert all inputs to integers if they're strings
    if isinstance(int_list, str):
        int_list = [int(x.strip()) for x in int_list.split(',')]
    elif not isinstance(int_list, list):
        int_list = [int(int_list)]
    return sum(math.exp(i) for i in int_list)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]

def print_screen_resolution():
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)
    print(f"Screen resolution: {width}x{height}")
    return width, height

@mcp.tool()
async def open_paint() -> dict:
    """Open Microsoft Paint"""
    global paint_app
    try:
        print("Opening Paint...")
        paint_app = Application().start('mspaint.exe')
        time.sleep(1)
        
        paint_window = paint_app.window(class_name='MSPaintApp')
        win32gui.ShowWindow(paint_window.handle, win32con.SW_MAXIMIZE)
        time.sleep(1)
        
        return {"content": [TextContent(type="text", text="Paint opened successfully")]}
    except Exception as e:
        print(f"PAINT ERROR: {str(e)}")
        return {"content": [TextContent(type="text", text=f"Error: {str(e)}")]}

@mcp.tool()
async def draw_rectangle(x1: int, y1: int, x2: int, y2: int) -> dict:
    """Draw a rectangle in Paint from (x1,y1) to (x2,y2)"""
    global paint_app
    try:
        if not paint_app:
            return {"content": [TextContent(type="text", text="Paint is not open.")]}
        
        print("Drawing rectangle...")
        paint_window = paint_app.window(class_name='MSPaintApp')
        paint_window.set_focus()
        time.sleep(1)
        
        # Rectangle tool with working coordinate
        print("Clicking rectangle tool")
        paint_window.click_input(coords=(658, 105))
        time.sleep(1)
        
        # Draw rectangle with working coordinates
        print("Drawing rectangle")
        pyautogui.mouseDown(x=677, y=581)
        time.sleep(0.5)
        pyautogui.dragTo(x=1254, y=841, duration=1)
        time.sleep(0.5)
        pyautogui.mouseUp()
        time.sleep(1)
        
        return {"content": [TextContent(type="text", text="Rectangle drawn")]}
    except Exception as e:
        print(f"PAINT ERROR: {str(e)}")
        return {"content": [TextContent(type="text", text=f"Error: {str(e)}")]}

@mcp.tool()
async def add_text_in_paint(text: str) -> dict:
    """Add text in Paint"""
    global paint_app
    try:
        if not paint_app:
            return {"content": [TextContent(type="text", text="Paint is not open.")]}
        
        print(f"Adding text: {text}")
        paint_window = paint_app.window(class_name='MSPaintApp')
        paint_window.set_focus()
        time.sleep(0.5)
        
        # Use text tool shortcut
        pyautogui.press('t')
        time.sleep(1)
        
        # Click for text placement
        pyautogui.click(x=753, y=650)
        time.sleep(0.5)
        
        # Write the text
        pyautogui.write("The result is ")
        time.sleep(0.5)
        pyautogui.write(str(text))
        time.sleep(0.5)
        
        # Click outside to finish
        pyautogui.click(x=500, y=500)
        time.sleep(0.5)
        
        return {"content": [TextContent(type="text", text=f"Text added: {text}")]}
    except Exception as e:
        print(f"PAINT ERROR: {str(e)}")
        return {"content": [TextContent(type="text", text=f"Error: {str(e)}")]}

@mcp.tool()
async def send_email_with_result(result: str) -> dict:
    """Send email with the calculation result"""
    try:
        # Gmail authentication
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', 
                    ['https://www.googleapis.com/auth/gmail.send']
                )
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        service = build('gmail', 'v1', credentials=creds)
        
        # Create simple email with just the result
        message = MIMEText(f'The result is {result}')
        message['to'] = 'rakavirp@gmail.com'
        message['subject'] = 'Math Calculation Result'
        message['from'] = 'Math Calculation Agent <rakavirp@gmail.com>'
        
        # Send email
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        service.users().messages().send(userId='me', body={'raw': raw}).execute()
        
        return {"content": [TextContent(type="text", text="Result sent via email")]}
    except Exception as e:
        print(f"Email error: {str(e)}")
        return {"content": [TextContent(type="text", text=f"Error sending email: {str(e)}")]}

# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution

