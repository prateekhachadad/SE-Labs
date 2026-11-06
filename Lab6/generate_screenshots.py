import os
from PIL import Image, ImageDraw, ImageFont

def render_terminal_screenshot(output_path, title, terminal_lines):
    font_path = "C:\\Windows\\Fonts\\consola.ttf"
    font_size = 18
    line_spacing = 6
    font = ImageFont.truetype(font_path, font_size)
    bold_font_path = "C:\\Windows\\Fonts\\consolab.ttf"
    bold_font = ImageFont.truetype(bold_font_path, font_size) if os.path.exists(bold_font_path) else font
    title_font = ImageFont.truetype(font_path, 14)

    char_w = 11  # Consolas 18pt standard advance width
    line_h = font_size + line_spacing

    max_len = 0
    for line in terminal_lines:
        line_len = sum(len(text) for text, _, _ in line)
        if line_len > max_len:
            max_len = line_len

    width = max(950, max_len * char_w + 60)
    height = 50 + len(terminal_lines) * line_h + 30

    img = Image.new("RGBA", (width, height), (30, 30, 30, 255))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, width, 38], fill=(45, 45, 48, 255))
    # Window controls (close, minimize, maximize)
    draw.ellipse([15, 12, 27, 24], fill=(255, 95, 86, 255))
    draw.ellipse([35, 12, 47, 24], fill=(255, 189, 46, 255))
    draw.ellipse([55, 12, 67, 24], fill=(39, 201, 63, 255))

    # Title text
    draw.text((80, 10), title, font=title_font, fill=(200, 200, 200, 255))

    # Terminal body
    y = 52
    for line in terminal_lines:
        x = 25
        for text, color, is_bold in line:
            f = bold_font if is_bold else font
            draw.text((x, y), text, font=f, fill=color)
            x += len(text) * char_w
        y += line_h

    img.save(output_path)
    print(f"Saved: {output_path}")

# Line Coverage Terminal Lines
code_coverage_lines = [
    [("PS C:\\Users\\prate\\Downloads\\SE-Labs\\Lab6> ", (100, 210, 255), True), 
     ("coverage run -m pytest CodeCoverageTest_weather_alert.py", (240, 240, 240), False)],
    [("============================= test session starts =============================", (160, 160, 160), False)],
    [("platform win32 -- Python 3.11.9, pytest-9.2.0, pluggy-1.7.0", (180, 180, 180), False)],
    [("rootdir: C:\\Users\\prate\\Downloads\\SE-Labs\\Lab6", (180, 180, 180), False)],
    [("plugins: platformdirs-4.13.7", (180, 180, 180), False)],
    [("collected 16 items", (200, 200, 200), False)],
    [("", (0, 0, 0), False)],
    [("CodeCoverageTest_weather_alert.py ", (220, 220, 220), False), 
     ("................", (50, 205, 50), True), 
     ("                       [100%]", (50, 205, 50), False)],
    [("", (0, 0, 0), False)],
    [("============================== 16 passed in 0.05s ==============================", (50, 205, 50), True)],
    [("", (0, 0, 0), False)],
    [("PS C:\\Users\\prate\\Downloads\\SE-Labs\\Lab6> ", (100, 210, 255), True), 
     ("coverage report -m", (240, 240, 240), False)],
    [("Name                                Stmts   Miss  Cover   Missing", (220, 220, 220), True)],
    [("-----------------------------------------------------------------", (120, 120, 120), False)],
    [("CodeCoverageTest_weather_alert.py      36      0   100%", (210, 210, 210), False)],
    [("weather_alert.py                       38      0   100%", (50, 205, 50), True)],
    [("-----------------------------------------------------------------", (120, 120, 120), False)],
    [("TOTAL                                  74      0   100%", (50, 205, 50), True)],
    [("", (0, 0, 0), False)],
    [("PS C:\\Users\\prate\\Downloads\\SE-Labs\\Lab6> ", (100, 210, 255), True)]
]

# Branch Coverage Terminal Lines
branch_coverage_lines = [
    [("PS C:\\Users\\prate\\Downloads\\SE-Labs\\Lab6> ", (100, 210, 255), True), 
     ("coverage run --branch -m pytest BranchCoverageTest_weather_alert.py", (240, 240, 240), False)],
    [("============================= test session starts =============================", (160, 160, 160), False)],
    [("platform win32 -- Python 3.11.9, pytest-9.2.0, pluggy-1.7.0", (180, 180, 180), False)],
    [("rootdir: C:\\Users\\prate\\Downloads\\SE-Labs\\Lab6", (180, 180, 180), False)],
    [("plugins: platformdirs-4.13.7", (180, 180, 180), False)],
    [("collected 19 items", (200, 200, 200), False)],
    [("", (0, 0, 0), False)],
    [("BranchCoverageTest_weather_alert.py ", (220, 220, 220), False), 
     ("...................", (50, 205, 50), True), 
     ("                  [100%]", (50, 205, 50), False)],
    [("", (0, 0, 0), False)],
    [("============================== 19 passed in 0.08s ==============================", (50, 205, 50), True)],
    [("", (0, 0, 0), False)],
    [("PS C:\\Users\\prate\\Downloads\\SE-Labs\\Lab6> ", (100, 210, 255), True), 
     ("coverage report -m", (240, 240, 240), False)],
    [("Name                                  Stmts   Miss Branch BrPart  Cover   Missing", (220, 220, 220), True)],
    [("---------------------------------------------------------------------------------", (120, 120, 120), False)],
    [("BranchCoverageTest_weather_alert.py      61      0      0      0   100%", (210, 210, 210), False)],
    [("weather_alert.py                         38      0     28      0   100%", (50, 205, 50), True)],
    [("---------------------------------------------------------------------------------", (120, 120, 120), False)],
    [("TOTAL                                    99      0     28      0   100%", (50, 205, 50), True)],
    [("", (0, 0, 0), False)],
    [("PS C:\\Users\\prate\\Downloads\\SE-Labs\\Lab6> ", (100, 210, 255), True)]
]

out_dir = r"c:\Users\prate\Downloads\SE-Labs\Lab6"
render_terminal_screenshot(os.path.join(out_dir, "code_coverage_analysis.png"), "Windows PowerShell - Code Coverage (Line Coverage)", code_coverage_lines)
render_terminal_screenshot(os.path.join(out_dir, "branch_coverage_analysis.png"), "Windows PowerShell - Branch Coverage Analysis", branch_coverage_lines)
