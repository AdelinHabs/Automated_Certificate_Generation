
"""Generate PDF certificates without JPEG conversion.
Existing certificates with matching filenames are overwritten.
"""
import os
import re
import tempfile

import img2pdf
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


# Project paths
base_folder = (
    r"D:\PROJECTS\Py Projects\Corpus\Cultural_Sunday_Certificates"
)

font_path = r"D:\FONTS\Courgette\Courgette-Regular.ttf"

output_folder = os.path.join(base_folder, "Certificates_Done")
templates_folder = os.path.join(base_folder, "Templates")

os.makedirs(output_folder, exist_ok=True)


# RGB text colour: red, green, blue (0-255)
# Fully opaque because RGB has no alpha channel.
colour = (248, 155, 0, 255)

# Print resolution
DPI = 300
POINTS_TO_PIXELS = DPI / 72


def points_to_pixels(position):
    return tuple(
        round(value * POINTS_TO_PIXELS)
        for value in position
    )


def draw_centered_text(draw, y, text, font, fill, image_width):
    """Centre text horizontally at the specified y-coordinate."""
    center_x = image_width / 2

    draw.text(
        (center_x, y),
        text,
        font=font,
        fill=fill,
        anchor="mt",
    )


# Certificate text positions in points, converted to pixels
name_organizing_certificate_in_pixels = points_to_pixels(
    (421.5555, 203.072)
)

post_organizing_certificate_in_pixels = points_to_pixels(
    (421.5555, 381.2718)
)

name_individual_in_pixels = points_to_pixels(
    (420.9449, 250.7441)
)

association_individual_in_pixels = points_to_pixels(
    (420.9449, 390.1108)
)

association_in_pixels = points_to_pixels(
    (297.4523, 324.9756)
)


def create_certificate(
    choice,
    name,
    template_path,
    post="",
    association="",
):
    """Create one certificate and save it as a PDF."""

    name = re.sub(r'\d+\.\s*', '', name).title()

    # Open the template as RGB and retain its embedded ICC profile.
    with Image.open(template_path) as image:
        icc_profile = image.info.get("icc_profile")
        certificate = image.convert("RGB")

    try:
        draw = ImageDraw.Draw(certificate)

        # Draw the required text
        if choice == 1:
            font_name = ImageFont.truetype(
                font_path, round(36 * POINTS_TO_PIXELS)
            )
            draw_centered_text(
                draw,
                name_organizing_certificate_in_pixels[1],
                name,
                font_name,
                colour,
                certificate.width,
            )

            font_post = ImageFont.truetype(
                font_path, round(31 * POINTS_TO_PIXELS)
            )
            draw_centered_text(
                draw,
                post_organizing_certificate_in_pixels[1],
                # post + " - Organizing Committee" if post != "Social Cultural Associations Coordinator" or post != "V/Cp Social Cultural Associations" else post,
                post + " - Organizing Committee" if post not in ("Social Cultural Associations Coordinator", "V/Cp Social Cultural Associations", "Master of Ceremonies") else post,
                font_post,
                colour,
                certificate.width,
            )

        elif choice == 2:
            font_name = ImageFont.truetype(
                font_path, round(30 * POINTS_TO_PIXELS)
            )
            draw_centered_text(
                draw,
                name_individual_in_pixels[1],
                name,
                font_name,
                colour,
                certificate.width,
            )

            font_association = ImageFont.truetype(
                font_path, round(30 * POINTS_TO_PIXELS)
            )
            draw_centered_text(
                draw,
                association_individual_in_pixels[1],
                association,
                font_association,
                colour,
                certificate.width,
            )

        elif choice == 3:
            font_association = ImageFont.truetype(
                font_path, round(36 * POINTS_TO_PIXELS)
            )
            draw_centered_text(
                draw,
                association_in_pixels[1],
                name.upper(),
                font_association,
                colour,
                certificate.width,
            )

        # Create a safe output filename
        safe_name = "".join(
            "_" if char in '<>:"/\\|?*' else char
            for char in name
        ).strip().rstrip(".")

        if not safe_name:
            safe_name = "Unnamed"

        output_path = os.path.join(
            f"{output_folder}\\{choice}",
            f"{safe_name}_Certificate.pdf",
        )

        # Save a temporary lossless TIFF, never a JPEG.
        with tempfile.NamedTemporaryFile(
            suffix=".tif",
            delete=False,
        ) as temp_file:
            temp_tiff = temp_file.name

        try:
            save_options = {
                "format": "TIFF",
                "compression": "tiff_lzw",
                "dpi": (DPI, DPI),
            }

            if icc_profile:
                save_options["icc_profile"] = icc_profile

            certificate.save(temp_tiff, **save_options)

            # Embed the TIFF image into a PDF.
            with open(output_path, "wb") as pdf_file:
                pdf_file.write(img2pdf.convert(temp_tiff))

        finally:
            if os.path.exists(temp_tiff):
                os.remove(temp_tiff)

        print(f"Certificate saved: {output_path}")

    finally:
        certificate.close()


def main():
    print(
        "\nChoose a certificate type:\n"
        "1. Organizing Committee\n"
        "2. Individual\n"
        "3. Association"
    )

    try:
        choice = int(input("Enter choice (1-3): "))
    except ValueError:
        print("Invalid choice. Enter 1, 2, or 3.")
        return

    configurations = {
        1: (
            os.path.join("Data", "Organizing_Committee.csv"),
            "OrganizingCommittee.png",
            ["NAME", "POST"],
        ),
        2: (
            os.path.join("Data", "Individual.csv"),
            "Individual.png",
            ["NAME", "ASSOCIATION"],
        ),
        3: (
            os.path.join("Data", "Association.csv"),
            "Association.png",
            ["NAME"],
        ),
    }

    if choice not in configurations:
        print("Invalid choice. Enter 1, 2, or 3.")
        return

    csv_name, template_name, columns = configurations[choice]

    csv_path = os.path.join(base_folder, csv_name)
    template_path = os.path.join(templates_folder, template_name)

    # Confirm required files exist
    for path, description in (
        (csv_path, "CSV file"),
        (template_path, "Template"),
        (font_path, "Font file"),
    ):
        if not os.path.isfile(path):
            print(f"{description} not found: {path}")
            return

    # Read CSV data and normalize column names
    try:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
        df.columns = df.columns.str.strip().str.upper()

        missing_columns = [
            column for column in columns
            if column not in df.columns
        ]

        if missing_columns:
            print(f"Required columns not found: {missing_columns}")
            print(f"Available columns: {df.columns.tolist()}")
            return

        df = df[columns]

    except Exception as error:
        print(f"Could not read CSV file: {error}")
        return

    # Generate a certificate for each valid row
    for _, row in df.iterrows():
        name = str(row["NAME"]).strip()

        if not name or name.lower() == "nan":
            print("Skipping row with an empty name.")
            continue

        post = ""
        association = ""

        if "POST" in columns and pd.notna(row["POST"]):
            post = str(row["POST"]).strip()

        if "ASSOCIATION" in columns and pd.notna(
            row["ASSOCIATION"]
        ):
            association = str(row["ASSOCIATION"]).strip()

        try:
            create_certificate(
                choice=choice,
                name=name,
                template_path=template_path,
                post=post,
                association=association,
            )
        except Exception as error:
            print(f"Failed to create certificate for {name}: {error}")

    print("\nCertificate generation completed.")


if __name__ == "__main__":
    main()
