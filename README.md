Magic: the Gathering Printable Set Label Generator
==================================================

## Credits

This is a fork of the original project by [davidfischer](https://github.com/davidfischer/mtg-printable-set-label-generator).  I added the new `generator-color.py` script to allow for the generation of color coded labels, but most of the original credit goes to him.

## Color generator usage

*To generate set-specific labels, use the original `generator.py` script by David.  See below for details.*

To generate color-coded labels, use the new `generator-color.py` script.  This script will generate a set of labels for each color and color combination in the game, along with some extra labels for card types, mana costs, and lettered labels for custom organization.

To run the script and view possible options use the following command:

```bash
py mtglabels/generator-color.py -h
```

-------------------------
| ORIGINAL README BELOW |
-------------------------

This is a script for generating Magic: the Gathering (MTG) printable set labels
in order to organize a collection of cards.
The code is powered by the [Scryfall API](https://scryfall.com/docs/api/sets).
As soon as a new set is up on Scryfall,
the label for that set can be generated and printed.

- Print on Avery Address Labels
  - for inkjet printer [Avery 8460](https://www.amazon.com/Avery-Address-Printers-Permanent-Adhesive/dp/B00004Z6JX)
  - for laser printer [Avery 5160](https://www.amazon.com/Avery-Address-Labels-Laser-Printers/dp/B00006B8FZ)
- Attach set labels to [BCW Tall Trading Card Dividers](https://www.amazon.com/dp/B00S3FF1PI)

<img src="readme-img/organized-cards.jpg">


## Usage

If you're just interested in downloading and printing these set labels,
check out the [web frontend](https://mtg-printable-label.fly.dev/)
([code](https://github.com/gofrolist/mtg-printable-set-label-frontend))
and generate your own labels.


### Advanced

If you want to further customize things, read on!

The script `generator.py` is a Python script to generate the printable labels.
It requires Python 3.6+ and has a few dependencies.

    brew install cairo                # Install vector graphics library
    pip install poetry                # Install python dependency management tool
    poetry install                    # Install python dependencies
    pip install --editable .
    python mtglabels/generator.py     # Creates SVG & PDF files in output/

By default, this will create SVG & PDF files.
The SVG files are vector image files that can be customized further.
The PDF files are ready to print.

The SVGs use the free fonts [EB Garamond](https://fonts.google.com/specimen/EB+Garamond) bold and [Source Sans Pro](https://fonts.google.com/specimen/Source+Sans+Pro) regular.


### Customizing

A lot of features can be customized by changing constants at the top of `generator.py`.
For example, sets can be excluded one-by-one or in groups by type or sets can be renamed.

The labels are designed for US Letter paper but this can be customized:

    python mtglabels/generator.py --paper-size=a4   # Use A4 paper size
    python mtglabels/generator.py --help            # Show all options

You can generate labels for specific sets as well:

    python mtglabels/generator.py lea mh1 mh2 neo


You can change how the labels are actually displayed and rendered by customizing `templates/labels.svg`.
If you change the fonts, you may also need to resize things to fit.


### Tips for printing SVGs

If you're just using the default PDFs, you probably won't need this.
However, if you are customizing the SVGs and printing them, this section is for you.

The output SVGs are precisely sized for a sheet of paper (US Letter by default).
Make sure while printing in your browser or otherwise to set the margins to None.

<img src="readme-img/browser-printing.png">

You can also "print" to a PDF.


## License

The code is available at [GitHub](https://github.com/gofrolist/mtg-printable-set-label-generator) under the [MIT license](https://opensource.org/licenses/MIT).

Some data such as set icons are unofficial Fan Content permitted under the Wizards of the Coast Fan Content Policy
and is copyright Wizards of the Coast, LLC, a subsidiary of Hasbro, Inc.
This code is not produced by, endorsed by, supported by, or affiliated with Wizards of the Coast.


## Credits

Special thanks goes to the users behind other printable set labels
such as those found [here](https://github.com/xsilium/MTG-Printable-Labels)
Using these fantastic labels definitely provided inspiration and direction
and made me want something more customizable and updatable.
