#! /usr/bin/env python

from lxml import etree
from inkex import EffectExtension, utils
from inkex import BaseElement, Layer
import inkex
import re


def user_error(title, msg):
    utils.debug(msg)
    user_message = "Error {}:\n{}".format(title, msg)
    utils.errormsg(user_message)
    exit()

class Options:
    def __init__(self, effect):
        self.current_file = effect.options.input_file

        self.regex_layer = effect.options.regex_layer
        self.space_replace= effect.options.space_replace
        self.use_uid = self._str_to_bool(
            effect.options.use_uid
        )
        self.regex_name = effect.options.regex_name

    def __str__(self):
        print = "\n===> EXTENSION PARAMETERS\n"
        print += "Current file: {}\n".format(self.current_file)
        print += "\n======> Export file page\n"
        print += "Regex layer: {}\n".format(self.regex_layer)
        print += "White space replacement: {}\n".format(self.space_replace)
        print += "Use UID: {}\n".format(self.use_uid)
        print += "Regex name: {}\n".format(self.regex_name)
        print += "---------------------------------------\n"
        return print

    def _str_to_bool(self, str):
        if str.lower() == "true":
            return True
        return False


class LabelToIdEffect(EffectExtension):
    def __init__(self):
        """init the effetc library and get options from gui"""
        EffectExtension.__init__(self)

        # Export file page
        self.arg_parser.add_argument(
            "--regex-layer",
            action="store",
            type=str,
            dest="regex_layer",
            default=".*",
            help="",
        )
        self.arg_parser.add_argument(
            "--space-replace",
            action="store",
            type=str,
            dest="space_replace",
            default="-",
            help="",
        )
        self.arg_parser.add_argument(
            "--use-uid",
            action="store",
            type=str,
            dest="use_uid",
            default=True,
            help="",
        )
        self.arg_parser.add_argument(
            "--regex-name",
            action="store",
            type=str,
            dest="regex_name",
            default=".*",
            help="",
        )

        # HACK - the script is called with a "--tab controls" option as an argument from the notebook param in the inx file.
        # This argument is not used in the script. It's purpose is to suppress an error when the script is called.
        self.arg_parser.add_argument(
            "--tab", action="store", type=str, dest="tab", default="controls", help=""
        )

    def effect(self):
        options = Options(self)
        utils.debug(options)

        # Filter layers
        inkex.addNS("re", "http://exslt.org/regular-expressions")
        # and re:match(@inkscape:label, {options.regex_layer})
        svg_layers = self.document.xpath(
            f'//svg:g[@inkscape:groupmode="layer" ]', namespaces=inkex.NSS
        )

        for layer in svg_layers:
            layer_label = layer.get("inkscape:label", "")

            name_id: str = layer_label
            if options.regex_name:
                match = re.findall(options.regex_name, layer_label)
                if not match or not match[-1]:
                    user_error("No match for name", "\"{}\" have no match with \"{}\"".format(layer_label, options.regex_name))
                name_id = match[-1]

            if options.use_uid:
                new_id = self.svg.get_unique_id("_", 4)
                name_id += new_id

            name_id = name_id.replace(" ", options.space_replace)

            utils.debug("ID: {:<32}->{:>32}".format(layer.get_id(), name_id))
            layer.set_id(name_id, backlinks=True)

        utils.debug("  TOTAL NUMBER OF LAYERS RENAMED: {}\n".format(len(svg_layers)))


def _main():
    exporter = LabelToIdEffect()
    exporter.run()
    exit()


if __name__ == "__main__":
    _main()
