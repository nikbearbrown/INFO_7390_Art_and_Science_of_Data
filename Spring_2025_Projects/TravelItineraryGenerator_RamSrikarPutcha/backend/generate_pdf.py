import re
from fpdf import FPDF
from io import BytesIO
import requests
from PIL import Image
import io
from datetime import datetime, timedelta

def clean_text(text):
    text = text.encode("latin-1", "replace").decode("latin-1")  
    return re.sub(r'\s+', ' ', text).strip()

class ItineraryPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        try:
            self.image('https://cdn-icons-png.flaticon.com/512/201/201623.png', 10, 8, 20)
        except:
            pass
        self.set_font('Arial', 'B', 16)
        self.cell(20)
        self.cell(0, 10, 'Smart Travel Itinerary', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def section_title(self, title):
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 51, 102)
        self.set_fill_color(230, 240, 255)
        self.cell(0, 10, clean_text(title), 0, 1, 'L', True)
        self.ln(4)

    def subsection(self, title):
        self.set_font("Arial", "B", 12)
        self.set_text_color(50, 50, 100)
        self.cell(0, 8, clean_text(title), 0, 1)
        self.ln(2)

    def paragraph(self, text):
        self.set_font("Arial", "", 11)
        self.set_text_color(0, 0, 0)
        for line in text.split('\n'):
            if line.strip():
                self.multi_cell(0, 6, clean_text(line.strip()))
                self.ln(1)
        self.ln(3)

    def bullet(self, text):
        self.set_font("Arial", "", 11)
        self.cell(5)
        cleaned_text = clean_text(text.replace("•", "-"))
        self.multi_cell(0, 6, f"- {cleaned_text}")
        self.ln(1)

    def add_image(self, img_url, caption=None):
        try:
            r = requests.get(img_url, timeout=5)
            if r.status_code == 200:
                img = Image.open(io.BytesIO(r.content))
                img = img.convert("RGB") if img.mode != "RGB" else img
                b = BytesIO()
                img.save(b, format='JPEG')
                b.seek(0)
                self.image(b, w=100)
                if caption:
                    self.set_font("Arial", "I", 9)
                    self.cell(0, 6, caption, 0, 1, 'C')
                self.ln(5)
        except Exception as e:
            print(f"Image error: {e}")

def parse_and_structure(itinerary):
    days_raw = itinerary.split("Day ")
    days = []

    for chunk in days_raw[1:]:
        lines = chunk.strip().split("\n")
        if not lines:
            continue

        title = lines[0].strip()
        content = "\n".join(lines[1:])
        day_data = {"title": title, "Accommodation": "", "Tours": "", "Attractions": ""}
        current_section = None
        seen_lines = set()

        for line in lines[1:]:
            line = line.strip()
            if not line or line in seen_lines:
                continue 
            seen_lines.add(line)

            if "Hotel:" in line or "Address:" in line:
                current_section = "Accommodation"
            elif "Tour" in line or "Tours" in line:
                current_section = "Tours"
            elif any(label in line for label in ["Ticket Details:", "Description:", "How to Reach:", "Hours:", "Attractions"]):
                current_section = "Attractions"

            if current_section:
                day_data[current_section] += line + "\n"

        days.append(day_data)

    return days


def create_itinerary_pdf(city, itinerary_text, start_date_str=""):
    pdf = ItineraryPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 20, f"{clean_text(city)} Travel Itinerary", 0, 1, 'C')
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(20)
    pdf.paragraph(f"This itinerary is customized for your trip to {clean_text(city)}. Explore top-rated spots and hidden gems curated just for you.")

    try:
        default_img = {
            "New York": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9"
        }
        if city in default_img:
            pdf.add_image(default_img[city], f"Welcome to {city}")
    except:
        pass

    days = parse_and_structure(itinerary_text)
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None

    for i, day in enumerate(days):
        pdf.add_page()
        date_str = f": {start_date.strftime('%B %d, %Y')}" if start_date else ""
        pdf.section_title(f"Day {i+1}{date_str}")
        if start_date:
            start_date += timedelta(days=1)
        for section in ["Accommodation", "Tours", "Attractions"]:
            if day[section].strip():
                pdf.subsection(section)
                pdf.paragraph(day[section])

    if "HIDDEN GEMS" in itinerary_text:
        pdf.add_page()
        pdf.section_title("Hidden Gems")
        gems = itinerary_text.split("HIDDEN GEMS")[1]
        for line in gems.split("\n"):
            if line.strip() and not any(x in line.lower() for x in ["tips", "beyond the typical"]):
                pdf.bullet(line)

    output = BytesIO()
    pdf.output(output)
    output.seek(0)

    if output.getbuffer().nbytes == 0:
        raise ValueError("Generated PDF is empty.")

    return output
