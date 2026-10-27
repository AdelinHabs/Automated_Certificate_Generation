"""PRINTS ONLY TICKETS THAT DO NOT EXIST"""

import pandas as pd
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

# --- CONSTANTS ---
EXCEL_FILE = r"D:\PROJECTS\Py Projects\NGO-NGA_E-Ticket\Data.xlsx"
TEMPLATE_PNG = r"D:\Posters\DONE\NGO-NGA\Template.png"
OUTPUT_FOLDER = r"D:\PROJECTS\Py Projects\NGO-NGA_E-Ticket\eTicketsDone"
FONT_PATH = r"D:\FONTS\Montserrat_Alternates\MontserratAlternates-Regular.ttf"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# --- FUNCTIONS ---

def check_whether_ticket_exists(filepath):
    if os.path.exists(filepath):
        return True
    return False


def determine_price(ticket_type):
    ticket_type_str = str(ticket_type).lower()
    if ticket_type_str == "single":
        return "UGX 65,000"
    elif ticket_type_str == "couple":
        return "UGX 120,000"
    elif ticket_type_str == "alumni":
        return "UGX 100,000"
    elif ticket_type_str == "table":
        return "UGX 360,000"
    else:
        return "N/A"

def generate_qr_code(row_index, name, ticket_type, price, email, size=1300):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=3,
        border=2
    )

    label_width = 14
    data = (f"{'Ticket No.:'.ljust(label_width)}     {(row_index + 1):03}\n"
            f"{'Name:'.ljust(label_width)}      {name}\n"
            f"{'Ticket Type:'.ljust(label_width)}   {ticket_type}\n"
            f"{'Price:'.ljust(label_width)}         {price}\n"
            f"{'Email:'.ljust(label_width)}        {email}")

    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size, size))
    return img

def create_ticket(row_index, name, ticket_type, price, email):
    # Load background template PNG
    ticket = Image.open(TEMPLATE_PNG).convert("RGBA")
    draw = ImageDraw.Draw(ticket)

    # Font
    font = ImageFont.truetype(FONT_PATH, 120)

    # Draw text (adjust coordinates as needed)
    draw.text((2311, 2132), name, font=font, fill="white")
    draw.text((2311, 2277), ticket_type, font=font, fill="white")
    draw.text((2311, 2432), price, font=font, fill="white")
    draw.text((2311, 2575), email, font=font, fill="white")

    # Generate QR code
    qr_img = generate_qr_code(row_index, name, ticket_type, price, email)
    ticket.paste(qr_img, (1650, 3525))

    # Save ticket
    output_path = os.path.join(OUTPUT_FOLDER, f"{name.replace(' ', '_')}_Ticket.png")
    ticket.save(output_path)
    print(f"Ticket saved for {name}")

# --- MAIN PROCESS ---
def main():
    df = pd.read_excel(EXCEL_FILE, usecols=["NAME", "TICKET TYPE", "EMAIL"])
    for row_index, row in df.iterrows():
        name = str(row["NAME"])
        ticket_type = str(row["TICKET TYPE"])
        email = str(row["EMAIL"])
        price = determine_price(ticket_type)

        ticket_exists = check_whether_ticket_exists(f"{OUTPUT_FOLDER + "\\" +name.replace(' ', '_')}_Ticket.png")
        if not ticket_exists:
            create_ticket(row_index, name, ticket_type, price, email)
        else:
            print(f"Ticket for {name} already exists")
    print("All tickets generated successfully!")

if __name__ == "__main__":
    main()
