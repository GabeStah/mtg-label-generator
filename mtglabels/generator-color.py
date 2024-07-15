import argparse
import logging
import re
import shutil
from datetime import datetime
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import cairosvg
import jinja2
import PyPDF2
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import mtglabels.config as config

# Set up logging
logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)
log = logging.getLogger(__name__)

# Get the base directory of the script
BASE_DIR = Path(__file__).resolve().parent

# Set up the Jinja2 environment for template loading
ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(BASE_DIR / "templates"),
    autoescape=jinja2.select_autoescape(["html", "xml"]),
)

# Retry Strategy for requests
retry_strategy = Retry(
    total=3,  # Total number of retries to allow
    status_forcelist=[
        429,
        500,
        502,
        503,
        504,
    ],  # Status codes to retry    allowed_methods=
    allowed_methods=["HEAD", "GET", "OPTIONS"],  # HTTP methods to retry
    backoff_factor=1,  # Backoff factor for retries
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("https://", adapter)  # Mount the retry strategy


class LabelGenerator:
    """
    Class for generating MTG labels.
    """

    # Default output directory for generated labels
    DEFAULT_OUTPUT_DIR = Path.cwd() / "output"

    # Label templates
    LABEL_TEMPLATE_FILENAME = "symbols.svg"
    DEFAULT_IS_OUTLINED = False
    DEFAULT_LABELS_PER_SHEET = 30
    DEFAULT_LABEL_TYPES = 'all'
    DEFAULT_LABEL_REPEAT = False
    DEFAULT_OFFSET_Y = 90

    # Margins and starting positions on the label page
    MARGIN = 40  # in 1/10 mm

    def __init__(self,
                 labels_per_sheet=None,
                 output_dir=None,
                 label_types=None,
                 label_repeat=None,
                 offset_y=None,
                 outline=None):
        """
        Initialize the LabelGenerator.

        Args:
            labels_per_sheet (int): The number of labels per sheet.
            output_dir (str): The output directory for the generated labels. Defaults to DEFAULT_OUTPUT_DIR.
        """
        self.set_codes = []
        self.symbols = []
        self.labels_per_sheet = labels_per_sheet or self.DEFAULT_LABELS_PER_SHEET
        self.label_types = label_types or self.DEFAULT_LABEL_TYPES
        self.label_repeat = label_repeat or self.DEFAULT_LABEL_REPEAT
        self.offset_y = offset_y or self.DEFAULT_OFFSET_Y
        self.is_outlined = outline or self.DEFAULT_IS_OUTLINED
        self.output_dir = Path(output_dir or self.DEFAULT_OUTPUT_DIR)

        # Starting positions on the label page
        self.START_X = self.MARGIN
        self.START_Y = self.MARGIN + self.offset_y

        self.tmp_png_dir = None
        self.tmp_svg_dir = None
        self.setup_directories()

        self.delta_y = None
        self.delta_x = None
        self.calculate_label_dimensions()

    def setup_directories(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.tmp_png_dir = Path("/tmp/mtglabels/png")
        self.tmp_png_dir.mkdir(parents=True, exist_ok=True)
        self.tmp_svg_dir = Path("/tmp/mtglabels/svg")
        self.tmp_svg_dir.mkdir(parents=True, exist_ok=True)

    def calculate_label_dimensions(self):
        self.delta_x = (config.LETTER_WIDTH - (2 * self.MARGIN)) / 3 + 10
        self.delta_y = (config.LETTER_HEIGHT - (2 * self.MARGIN)) / (
            self.labels_per_sheet / 3
        ) - 18
        # self.delta_y = (config.LETTER_HEIGHT - (2 * self.MARGIN)) / (
        #     self.labels_per_sheet / 3
        # ) - 18

    def generate_labels(self, sets=None):
        """
        Generate the MTG labels.

        Args:
            sets (list): List of set codes to include. If None, all sets will be included.
        """
        # Clean up any existing PDF files in the output directory
        clean_up_pdfs(self.output_dir)

        if sets:
            config.IGNORED_SETS = ()
            config.MINIMUM_SET_SIZE = 0
            config.SET_TYPES = ()
            self.set_codes = [exp.lower() for exp in sets]

        page = 1

        symbol_data = self.get_symbol_data()
        self.download_symbol_icons(symbol_data)

        labels = []
        if self.label_types == 'all':
            labels = self.create_symbol_label_data(config.ALL_SYMBOLS, repeat=self.label_repeat)
        elif self.label_types == 'tca':
            labels = self.create_symbol_label_data(config.TYPE_COST_ALPHA_SYMBOLS, repeat=self.label_repeat)
        elif self.label_types == 'type':
            labels = self.create_symbol_label_data(config.TYPE_SYMBOLS, repeat=self.label_repeat)
        elif self.label_types == 'cost':
            labels = self.create_symbol_label_data(config.COST_SYMBOLS, repeat=self.label_repeat)
        elif self.label_types == 'alpha':
            labels = self.create_symbol_label_data(config.ALPHABETICAL_SYMBOLS, repeat=self.label_repeat)

        label_batches = [
            labels[i : i + self.labels_per_sheet]
            for i in range(0, len(labels), self.labels_per_sheet)
        ]

        template_name = self.LABEL_TEMPLATE_FILENAME  # Use the defined constant

        template = ENV.get_template(template_name)
        for batch in label_batches:
            output = template.render(
                labels=batch, WIDTH=config.LETTER_WIDTH, HEIGHT=config.LETTER_HEIGHT, IS_OUTLINED=self.is_outlined
            )
            outfile_svg = (
                self.output_dir / f"labels-{self.labels_per_sheet}-{page:02}.svg"
            )
            outfile_pdf = (
                self.output_dir / f"labels-{self.labels_per_sheet}-{page:02}.pdf"
            )

            log.info(f"Writing {outfile_svg}...")
            with outfile_svg.open("w") as fd:
                fd.write(output)

            log.info(f"Writing {outfile_pdf}...")
            cairosvg.svg2pdf(
                url=str(outfile_svg), write_to=str(outfile_pdf), unsafe=True
            )

            page += 1

        combine_pdfs(self.output_dir)

    def get_set_data(self):
        """
        Fetch set data from Scryfall API.

        Example:
          "data": [
            {
              "object": "set",
              "id": "a7ecb771-d1b6-4dec-8cf5-8d45179f21e0",
              "code": "fdn",
              "mtgo_code": "fdn",
              "arena_code": "fdn",
              "name": "Foundations",
              "uri": "https://api.scryfall.com/sets/a7ecb771-d1b6-4dec-8cf5-8d45179f21e0",
              "scryfall_uri": "https://scryfall.com/sets/fdn",
              "search_uri": "https://api.scryfall.com/cards/search?include_extras=true&include_variations=true&order=set&q=e%3Afdn&unique=prints",
              "released_at": "2024-11-15",
              "set_type": "core",
              "card_count": 10,
              "digital": false,
              "nonfoil_only": false,
              "foil_only": false,
              "icon_svg_uri": "https://svgs.scryfall.io/sets/default.svg?1719806400"
            },
          ]

        Returns:
            list: List of set data dictionaries.
        """

        try:
            log.info("Getting set data and icons from Scryfall")

            resp = session.get("https://api.scryfall.com/sets")
            resp.raise_for_status()

            data = resp.json().get("data", [])

            known_sets = {exp["code"] for exp in data}
            specified_sets = (
                {code.lower() for code in self.set_codes} if self.set_codes else set()
            )
            unknown_sets = specified_sets - known_sets

            if unknown_sets:
                log.warning("Unknown sets: %s", ", ".join(unknown_sets))

            set_data = [
                exp
                for exp in data
                if (
                    exp["code"] not in config.IGNORED_SETS
                    and exp["card_count"] >= config.MINIMUM_SET_SIZE
                    and (not config.SET_TYPES or exp["set_type"] in config.SET_TYPES)
                    and (not self.set_codes or exp["code"].lower() in specified_sets)
                )
            ]

            return set_data

        except requests.exceptions.RequestException as e:
            log.error("Error occurred while fetching set data: %s", str(e))
            return []

    def get_symbol_data(self):
        """
        Fetch card symbol data from Scryfall API.
        Card symbols: https://scryfall.com/docs/api/card-symbols
        HTTP GET https://api.scryfall.com/symbology

        Example:
          "data": [
            {
              "object": "card_symbol",
              "symbol": "{T}",
              "svg_uri": "https://svgs.scryfall.io/card-symbols/T.svg",
              "loose_variant": null,
              "english": "tap this permanent",
              "transposable": false,
              "represents_mana": false,
              "appears_in_mana_costs": false,
              "mana_value": 0,
              "hybrid": false,
              "phyrexian": false,
              "cmc": 0,
              "funny": false,
              "colors": [],
              "gatherer_alternates": [
                "ocT",
                "oT"
              ]
            }
          ]

        Returns:
            list: List of symbol data dictionaries.
        """

        try:
            log.info("Getting symbol data and icons from Scryfall")

            resp = session.get(config.API_ENDPOINT + "/symbology")
            resp.raise_for_status()

            data = resp.json().get("data", [])

            known_symbols = {exp["symbol"] for exp in data}
            specified_symbols = (
                {symbol.lower() for symbol in self.symbols} if self.symbols else set()
            )
            unknown_symbols = specified_symbols - known_symbols

            if unknown_symbols:
                log.warning("Unknown symbols: %s", ", ".join(unknown_symbols))

            # set_data = [
            #     exp
            #     for exp in data
            #     if (
            #         exp["code"] not in config.IGNORED_SETS
            #         and exp["card_count"] >= config.MINIMUM_SET_SIZE
            #         and (not config.SET_TYPES or exp["set_type"] in config.SET_TYPES)
            #         and (not self.set_codes or exp["code"].lower() in specified_symbols)
            #     )
            # ]

            symbol_data = [
                exp
                for exp in data
                # if (
                #     exp["code"] not in config.IGNORED_SETS
                #     and exp["card_count"] >= config.MINIMUM_SET_SIZE
                #     and (not config.SET_TYPES or exp["set_type"] in config.SET_TYPES)
                #     and (not self.set_codes or exp["code"].lower() in specified_symbols)
                # )
            ]

            return symbol_data

        except requests.exceptions.RequestException as e:
            log.error("Error occurred while fetching symbol data: %s", str(e))
            return []

    def create_set_label_data(self):
        """
        Create label data for the sets.

        Returns:
            list: List of label data dictionaries.
        """
        labels = []
        x = self.START_X
        y = self.START_Y

        set_data = self.get_set_data()

        for exp in reversed(set_data):
            name = config.RENAME_SETS.get(exp["name"], exp["name"])
            icon_url = exp["icon_svg_uri"]
            filename = Path(icon_url).name.split("?")[0]
            file_path = self.tmp_svg_dir / filename

            if file_path.exists():
                log.debug(f"Skipping download. File already exists: {icon_url}")
                icon_filename = filename
            else:
                try:
                    response = session.get(icon_url)
                    response.raise_for_status()
                    with file_path.open("wb") as file:
                        file.write(response.content)
                    icon_filename = filename
                except requests.exceptions.RequestException as e:
                    log.error(f"Failed to download file: {icon_url}")
                    log.error("Error occurred while downloading file: %s", str(e))
                    icon_filename = None

            if icon_filename:
                shutil.copy(file_path, self.output_dir)
                labels.append(
                    {
                        "name": name,
                        "code": exp["code"],
                        "date": datetime.strptime(
                            exp["released_at"], "%Y-%m-%d"
                        ).date(),
                        "icon_filename": icon_filename,
                        "x": x,
                        "y": y,
                    }
                )

            y += self.delta_y

            # Start a new column if needed
            if len(labels) % (self.labels_per_sheet / 3) == 0:
                x += self.delta_x
                y = self.START_Y

            # Start a new page if needed
            if len(labels) % self.labels_per_sheet == 0:
                x = self.START_X
                y = self.START_Y

        return labels

    def download_symbol_icons(self, symbol_data):
        """
        Download the symbol icons.
        """

        for item in symbol_data:
            icon_url = item["svg_uri"]
            filename = Path(icon_url).name.split("?")[0]
            file_path = self.tmp_svg_dir / filename

            if file_path.exists():
                log.debug(f"Skipping download. File already exists: {icon_url}")
            else:
                try:
                    response = session.get(icon_url)
                    response.raise_for_status()
                    with file_path.open("wb") as file:
                        file.write(response.content)
                except requests.exceptions.RequestException as e:
                    log.error(f"Failed to download file: {icon_url}")
                    log.error("Error occurred while downloading file: %s", str(e))

    def create_symbol_label_data(self, symbols_list, repeat=False):
        """
        Create label data for the symbols.

        Args:
            symbols_list: List of symbol data dictionaries.
            repeat: Boolean indicating if labels should be repeated to fill the page.

        Returns:
            symbols_list: List of symbol data dictionaries with X/Y coordinates.
        """
        labels = []
        x = self.START_X
        y = self.START_Y

        pattern = re.compile(r'\{([A-Z0-9]+)\}')

        def add_labels():
            nonlocal x, y
            for item in symbols_list:
                label = {
                    "title": item["title"],
                    "x": x,
                    "y": y,
                }

                if 'symbol' in item:
                    symbols = pattern.findall(item['symbol'])
                    item['symbols_list'] = symbols
                    item['icon_paths'] = [str(self.tmp_svg_dir / f"{symbol}.svg") for symbol in symbols]
                    for icon_path in item["icon_paths"]:
                        shutil.copy(icon_path, self.output_dir)

                    label["symbol"] = item["symbol"]
                elif 'icon' in item:
                    local_icon_path = Path(f"mtglabels/templates/png/{item['icon']}")
                    tmp_icon_path = self.tmp_png_dir / item['icon']
                    shutil.copy(local_icon_path, tmp_icon_path)
                    item['icon_paths'] = [str(tmp_icon_path)]

                if "icon_paths" in item:
                    label["icon_paths"] = item["icon_paths"]

                labels.append(label)

                y += self.delta_y

                # Start a new column if needed
                if len(labels) % (self.labels_per_sheet / 3) == 0:
                    x += self.delta_x
                    y = self.START_Y

                # Start a new page if needed
                if len(labels) % self.labels_per_sheet == 0:
                    x = self.START_X
                    y = self.START_Y

        # Add the initial labels
        add_labels()

        # If repeat is True, add repeated labels to fill the page
        if repeat:
            while len(labels) < self.labels_per_sheet:
                add_labels()

        return labels


def clean_up_pdfs(output_dir, pattern="labels-*.pdf"):
    # List all PDF files in the output directory that match the specified pattern
    pdf_files = sorted(output_dir.glob(pattern))

    for pdf_file in pdf_files:
        try:
            pdf_file.unlink()
            log.info(f"Deleted {pdf_file}")
        except Exception as e:
            log.error(f"Error deleting {pdf_file}: {e}")


def combine_pdfs(output_dir, pattern="labels-*.pdf"):
    pdf_merger = PyPDF2.PdfMerger()

    # List all PDF files in the output directory that match the specified pattern
    pdf_files = sorted(output_dir.glob(pattern))

    for pdf_file in pdf_files:
        pdf_merger.append(str(pdf_file))

    # Output combined PDF
    combined_pdf_path = output_dir / "combined_labels.pdf"
    with combined_pdf_path.open("wb") as combined_pdf:
        pdf_merger.write(combined_pdf)
        log.info(f"Writing {combined_pdf_path}...")


def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Generate MTG labels")
    parser.add_argument(
        "--output-dir",
        default=LabelGenerator.DEFAULT_OUTPUT_DIR,
        help="Output labels to this directory",
    )
    parser.add_argument(
        "--labels-per-sheet",
        type=int,
        default=LabelGenerator.DEFAULT_LABELS_PER_SHEET,
        choices=[24, 30],
        help="Number of labels per sheet (default: 30)",
    )
    parser.add_argument(
        '--type',
        type=str,
        default=LabelGenerator.DEFAULT_LABEL_TYPES,
        choices=['all', 'tca', 'type', 'cost', 'alpha'],
        help="Type of labels to generate (default: all)"
    )
    parser.add_argument(
        '--offset-y',
        type=int,
        default=LabelGenerator.DEFAULT_OFFSET_Y,
        help="Adjust the vertical offset (default: 90)"
    )
    parser.add_argument(
        '--repeat',
        action='store_true',
        default=LabelGenerator.DEFAULT_LABEL_REPEAT,
        help="Repeat label types to fill current page (default: False)"
    )
    parser.add_argument(
        '--outline',
        action='store_true',
        default=LabelGenerator.DEFAULT_IS_OUTLINED,
        help="Prints a rounded outline to simulate label dimensions; ideal for testing (default: False)"
    )
    parser.add_argument(
        "sets",
        nargs="*",
        help=(
            "Only output sets with the specified set code (e.g., MH1, NEO). "
            "This can be used multiple times."
        ),
        metavar="SET",
    )

    return parser.parse_args()


def main():
    """
    Main function for running the label generation.
    """

    try:
        args = parse_arguments()
        generator = LabelGenerator(args.labels_per_sheet,
                                   args.output_dir,
                                   args.type,
                                   args.repeat,
                                   args.offset_y,
                                   args.outline)
        generator.generate_labels(args.sets)
    except requests.exceptions.RequestException as e:
        log.error("Error occurred while making a request: %s", str(e))
    except Exception as e:
        log.exception("An unexpected error occurred: %s", str(e))


if __name__ == "__main__":
    main()
