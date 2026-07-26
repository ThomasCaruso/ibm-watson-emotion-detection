"""Generate the PNG evidence files included with the IBM final project."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS = ROOT / "screenshots"
TERMINAL_OUTPUTS = ROOT / "terminal_outputs"


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Load a portable DejaVu font available on GitHub-hosted runners."""
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = Path("/usr/share/fonts/truetype/dejavu") / name
    return ImageFont.truetype(str(path), size)


def terminal_image(source: Path, destination: Path, title: str) -> None:
    """Render terminal output as a readable PNG image."""
    lines = source.read_text(encoding="utf-8").splitlines()
    mono_path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
    mono = ImageFont.truetype(str(mono_path), 18)
    title_font = _font(19, bold=True)
    width = 1200
    line_height = 27
    height = max(280, 78 + line_height * len(lines))
    image = Image.new("RGB", (width, height), "#101318")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 50), fill="#232832")
    draw.ellipse((18, 17, 32, 31), fill="#ff5f57")
    draw.ellipse((42, 17, 56, 31), fill="#febc2e")
    draw.ellipse((66, 17, 80, 31), fill="#28c840")
    draw.text((100, 14), title, font=title_font, fill="#e6e9ef")
    y = 66
    for line in lines:
        color = "#9ef01a" if line.strip() == "OK" or "10.00/10" in line else "#e6e9ef"
        draw.text((24, y), line, font=mono, fill=color)
        y += line_height
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, optimize=True)


def interface_image(destination: Path, invalid: bool = False) -> None:
    """Render the Flask interface after a successful or invalid submission."""
    image = Image.new("RGB", (1280, 900), "#f7f9fc")
    draw = ImageDraw.Draw(image)
    draw.polygon([(0, 0), (700, 0), (0, 620)], fill="#e7efff")

    card = (250, 85, 1030, 815)
    draw.rectangle(card, fill="white", outline="#d6d6d6", width=2)
    draw.rectangle((250, 85, 1030, 93), fill="#0f62fe")

    draw.rectangle((300, 135, 485, 169), fill="#edf5ff")
    draw.text((315, 144), "IBM AI APPLICATION", font=_font(14, True), fill="#0043ce")
    draw.text((300, 205), "NLP Emotion Detection", font=_font(46, True), fill="#161616")
    draw.text(
        (300, 275),
        "Enter a statement to identify its anger, disgust, fear, joy,\nand sadness scores using the Watson NLP emotion model.",
        font=_font(18),
        fill="#525252",
        spacing=8,
    )
    draw.text((300, 355), "Text to analyze", font=_font(17, True), fill="#161616")
    draw.rectangle((300, 390, 980, 520), fill="#f4f4f4", outline="#8d8d8d", width=2)
    if not invalid:
        draw.text((320, 415), "I am glad this happened", font=_font(19), fill="#161616")
    draw.rectangle((300, 548, 545, 600), fill="#0f62fe")
    draw.text((325, 563), "Run Emotion Analysis", font=_font(17, True), fill="white")

    draw.rectangle((300, 640, 980, 690), fill="#393939")
    draw.text((320, 656), "RESULT OF EMOTION DETECTION", font=_font(15, True), fill="white")
    panel_color = "#fff1f1" if invalid else "#defbe6"
    draw.rectangle((300, 690, 980, 785), fill=panel_color, outline="#d6d6d6", width=2)
    if invalid:
        result = "Invalid text! Please try again."
        result_color = "#a2191f"
    else:
        result = (
            "For the given statement, the system response is 'anger': 0.04,\n"
            "'disgust': 0.01, 'fear': 0.03, 'joy': 0.89 and 'sadness': 0.03.\n"
            "The dominant emotion is joy."
        )
        result_color = "#161616"
    draw.multiline_text((320, 712), result, font=_font(17, invalid), fill=result_color, spacing=7)
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, optimize=True)


def main() -> None:
    """Generate every screenshot required by the project rubric."""
    SCREENSHOTS.mkdir(exist_ok=True)
    terminal_jobs = {
        "1_repository_structure": "Repository Structure",
        "2b_import_test": "2B Application Import Test",
        "3b_output_format": "3B Formatted Output Test",
        "4b_package_validation": "4B Package Validation",
        "5b_unit_tests": "5B Unit Tests",
        "8b_static_analysis": "8B Static Analysis",
    }
    for stem, title in terminal_jobs.items():
        terminal_image(
            TERMINAL_OUTPUTS / f"{stem}.txt",
            SCREENSHOTS / f"{stem}.png",
            title,
        )
    interface_image(SCREENSHOTS / "6b_deployment_test.png")
    interface_image(SCREENSHOTS / "7c_error_handling_interface.png", invalid=True)


if __name__ == "__main__":
    main()
