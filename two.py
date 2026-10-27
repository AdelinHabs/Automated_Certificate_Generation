"""PRINTS ALL CERTIFICATES AND OVERWRITES THOSE THAT EXIST"""
from timeit import template

import pandas as pd
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

# --- CONSTANTS ---
font_path = r"D:\FONTS\Courgette\Courgette-Regular.ttf"
output_folder = r"D:\PROJECTS\Py Projects\Corpus\Cultural_Sunday_Certificates\Certificates_Done"
os.makedirs(output_folder, exist_ok=True)



# --- FUNCTIONS ---

def create_certificate(choice, name, template_png, post="", association=""):
    # Load background template PNG
    certificate = Image.open(template_png).convert("CMYK")
    draw = ImageDraw.Draw(certificate)

    # Font
    font = ImageFont.truetype(font_path, 120)

    # Colour
    colour = (7,100,255,0)

    # Draw text (adjust coordinates as needed)

    if choice == 1:
        draw.text((2311, 2132), name, font=font, fill=colour)
        draw.text((2311, 2152), post, font=font, fill=colour)
    elif choice == 2:
        draw.text((2311, 2132), name, font=font, fill=colour)
        draw.text((2311, 2152), association, font=font, fill=colour)
    elif choice == 3:
        draw.text((2311, 2277), name, font=font, fill=colour)

    # Save certificate
    output_path = os.path.join(output_folder, f"{name.replace(' ', '_')}_Certificate.png")
    certificate.save(output_path)
    print(f"Certificate saved for {name}")

# --- MAIN PROCESS ---
def main():
    global template_png, excel_file
    choice = int(input("Choose a number that corresponds to the needed certificate type. Press enter to continue...\n"
          "1. Organizing Committee\n"
          "2. Individual\n"
          "3. Association\n"))
    if choice == 1:
        # --- CONSTANTS ---
        excel_file = r"D:\PROJECTS\Py Projects\Corpus\Cultural_Sunday_Certificates\Organizing_Committee.csv"
        template_png = r"D:\PROJECTS\Py Projects\Corpus\Cultural_Sunday_Certificates\Templates\OrganizingCommittee.png"
        df = pd.read_excel(excel_file, usecols=["NAME", "POST"])
        for row_index, row in df.iterrows():
            name = str(row["NAME"])
            post = str(row["POST"])
            create_certificate(choice=choice, name=name, template_png=template_png, post=post)
    elif choice == 2:
        # --- CONSTANTS ---
        excel_file = r"D:\PROJECTS\Py Projects\Corpus\Cultural_Sunday_Certificates\Individual.csv"
        template_png = r"D:\PROJECTS\Py Projects\Corpus\Cultural_Sunday_Certificates\Templates\Individual.png"
        df = pd.read_excel(excel_file, usecols=["NAME", "ASSOCIATION"])
        for row_index, row in df.iterrows():
            name = str(row["NAME"])
            association = str(row["ASSOCIATION"])
            create_certificate(choice=choice, name=name, template_png=template_png, association=association)
    elif choice == 3:
        # --- CONSTANTS ---
        excel_file = r"D:\PROJECTS\Py Projects\Corpus\Cultural_Sunday_Certificates\Association.csv"
        template_png = r"D:\PROJECTS\Py Projects\Corpus\Cultural_Sunday_Certificates\Templates\Association.png"
        df = pd.read_excel(excel_file, usecols=["NAME"])
        for row_index, row in df.iterrows():
            name = str(row["NAME"])
            create_certificate(choice=choice, name=name, template_png=template_png)

    print("All certificates generated successfully!")

if __name__ == "__main__":
    main()
