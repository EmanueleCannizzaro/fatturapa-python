#!/usr/bin/python3
from __future__ import annotations
import argparse
import contextlib
import logging
import os.path
import shutil
import sys
from pathlib import Path
from typing import TYPE_CHECKING, BinaryIO, TextIO, Union

from a38 import codec, models

if TYPE_CHECKING:
    from .fattura import Fattura
    from .fattura_semplificata import FatturaElettronicaSemplificata

log = logging.getLogger("a38tool")


class Fail(Exception):
    pass


class App:
    NAME = None

    def __init__(self, args):
        self.args = args

    def load_fattura(self, pathname) -> Union[Fattura, FatturaElettronicaSemplificata]:
        codecs = codec.Codecs()
        codec_cls = codecs.codec_from_filename(pathname)
        return codec_cls().load(pathname)

    @classmethod
    def add_subparser(cls, subparsers):
        name = getattr(cls, "NAME", None)
        if name is None:
            name = cls.__name__.lower()
        parser = subparsers.add_parser(name, help=cls.__doc__.strip())
        parser.set_defaults(app=cls)
        return parser


class Diff(App):
    """
    show the difference between two fatture
    """
    NAME = "diff"

    def __init__(self, args):
        super().__init__(args)
        self.first = args.first
        self.second = args.second

    @classmethod
    def add_subparser(cls, subparsers):
        parser = super().add_subparser(subparsers)
        parser.add_argument("first", help="first input file (.xml or .xml.p7m)")
        parser.add_argument("second", help="second input file (.xml or .xml.p7m)")
        return parser

    def run(self):
        first = self.load_fattura(self.first)
        second = self.load_fattura(self.second)
        from a38.diff import Diff
        res = Diff()
        first.diff(res, second)
        if res.differences:
            for d in res.differences:
                print(d)
            return 1


class Validate(App):
    """
    validate the contents of a fattura
    """
    NAME = "validate"

    def __init__(self, args):
        super().__init__(args)
        self.pathname = args.file

    @classmethod
    def add_subparser(cls, subparsers):
        parser = super().add_subparser(subparsers)
        parser.add_argument("file", help="input file (.xml or .xml.p7m)")
        return parser

    def run(self):
        f = self.load_fattura(self.pathname)
        from a38.validation import Validation
        res = Validation()
        f.validate(res)
        if res.warnings:
            for w in res.warnings:
                print(str(w), file=sys.stderr)
        if res.errors:
            for e in res.errors:
                print(str(e), file=sys.stderr)
            return 1


class Exporter(App):
    def __init__(self, args):
        super().__init__(args)
        self.files = args.files
        self.output = args.output
        self.codec = self.get_codec()

    def get_codec(self) -> codec.Codec:
        """
        Instantiate the output codec to use for this exporter
        """
        raise NotImplementedError(f"{self.__class__.__name__}.get_codec is not implemented")

    def write(self, f: models.Model, file: Union[TextIO, BinaryIO]):
        self.codec.write_file(f, file)

    @contextlib.contextmanager
    def open_output(self):
        if self.output is None:
            if self.codec.binary:
                yield sys.stdout.buffer
            else:
                yield sys.stdout
        else:
            with open(self.output, "wb" if self.codec.binary else "wt") as out:
                yield out

    def run(self):
        with self.open_output() as out:
            for pathname in self.files:
                f = self.load_fattura(pathname)
                self.write(f, out)

    @classmethod
    def add_subparser(cls, subparsers):
        parser = super().add_subparser(subparsers)
        parser.add_argument("-o", "--output", help="output file (default: standard output)")
        parser.add_argument("files", nargs="+", help="input files (.xml or .xml.p7m)")
        return parser


class ExportJSON(Exporter):
    """
    output a fattura in JSON
    """
    NAME = "json"

    def get_codec(self) -> codec.Codec:
        if self.args.indent == "no":
            indent = None
        else:
            try:
                indent = int(self.args.indent)
            except ValueError:
                raise Fail("--indent argument must be an integer on 'no'")

        return codec.JSON(indent=indent)

    @classmethod
    def add_subparser(cls, subparsers):
        parser = super().add_subparser(subparsers)
        parser.add_argument("--indent", default="1",
                            help="indentation space (default: 1, use 'no' for all in one line)")
        return parser


class ExportYAML(Exporter):
    """
    output a fattura in JSON
    """
    NAME = "yaml"

    def get_codec(self) -> codec.Codec:
        return codec.YAML()


class ExportXML(Exporter):
    """
    output a fattura in XML
    """
    NAME = "xml"

    def get_codec(self) -> codec.Codec:
        return codec.XML()


class ExportPython(Exporter):
    """
    output a fattura as Python code
    """
    NAME = "python"

    def get_codec(self) -> codec.Codec:
        namespace = self.args.namespace
        if namespace == "":
            namespace = False

        return codec.Python(namespace=namespace, unformatted=self.args.unformatted)

    @classmethod
    def add_subparser(cls, subparsers):
        parser = super().add_subparser(subparsers)
        parser.add_argument("--namespace", default=None,
                            help="namespace to use for the model classes (default: the module fully qualified name)")
        parser.add_argument("--unformatted", action="store_true",
                            help="disable code formatting, outputting a single-line statement")
        return parser


class Edit(App):
    """
    Open a fattura for modification in a text editor
    """
    def __init__(self, args):
        super().__init__(args)
        if self.args.style == "yaml":
            self.edit_codec = codec.YAML()
        elif self.args.style == "python":
            self.edit_codec = codec.Python(loadable=True)
        else:
            raise Fail(f"Unsupported edit style {self.args.style!r}")

    def write_out(self, f):
        """
        Write a fattura, as much as possible over the file being edited
        """
        codecs = codec.Codecs()
        codec_cls = codecs.codec_from_filename(self.args.file)
        if codec_cls == codec.P7M:
            with open(self.args.file[:-4], "wb") as fd:
                codec_cls().write_file(f, fd)
        elif codec_cls.binary:
            with open(self.args.file, "wb") as fd:
                codec_cls().write_file(f, fd)
        else:
            with open(self.args.file, "wt") as fd:
                codec_cls().write_file(f, fd)

    def run(self):
        f = self.load_fattura(self.args.file)
        f1 = self.edit_codec.interactive_edit(f)
        if f1 is not None and f != f1:
            self.write_out(f1)

    @classmethod
    def add_subparser(cls, subparsers):
        parser = super().add_subparser(subparsers)
        parser.add_argument("-s", "--style", default="yaml",
                            help="editable representation to use, one of 'yaml' or 'python'. Default: $(default)s")
        parser.add_argument("file", help="file to edit")
        return parser


class Renderer(App):
    """
    Base class for CLI commands that render a Fattura
    """

    def __init__(self, args):
        from a38.render import HAVE_LXML
        if not HAVE_LXML:
            raise Fail("python3-lxml is needed for XSLT based rendering")

        super().__init__(args)
        self.stylesheet = args.stylesheet
        self.files = args.files
        self.output = args.output
        self.force = args.force

        from a38.render import XSLTTransform
        self.transform = XSLTTransform(self.stylesheet)

    def render(self, f, output: str):
        """
        Render the Fattura to the given destination file
        """
        raise NotImplementedError(self.__class__.__name__ + ".render is not implemented")

    def run(self):
        for pathname in self.files:
            dirname = os.path.normpath(os.path.dirname(pathname))
            basename = os.path.basename(pathname)
            basename, ext = os.path.splitext(basename)
            output = self.output.format(dirname=dirname, basename=basename, ext=ext)
            if not self.force and os.path.exists(output):
                log.warning("%s: output file %s already exists: skipped", pathname, output)
            else:
                log.info("%s: writing %s", pathname, output)
            f = self.load_fattura(pathname)
            self.render(f, output)

    @classmethod
    def add_subparser(cls, subparsers):
        parser = super().add_subparser(subparsers)
        parser.add_argument("-f", "--force", action="store_true", help="overwrite existing output files")
        default_output = "{dirname}/{basename}{ext}." + cls.NAME
        parser.add_argument("-o", "--output",
                            default=default_output,
                            help="output file; use {dirname} for the source file path,"
                                 " {basename} for the source file name"
                                 " (default: '" + default_output + "'")
        parser.add_argument("stylesheet", help=".xsl/.xslt stylesheet file to use for rendering")
        parser.add_argument("files", nargs="+", help="input files (.xml or .xml.p7m)")
        return parser


class RenderHTML(Renderer):
    """
    render a Fattura as HTML using a .xslt stylesheet
    """
    NAME = "html"

    def render(self, f, output):
        html = self.transform(f)
        html.write(output)


class RenderPDF(Renderer):
    """
    render a Fattura as PDF using a .xslt stylesheet
    """
    NAME = "pdf"

    def __init__(self, args):
        super().__init__(args)
        self.wkhtmltopdf = shutil.which("wkhtmltopdf")
        if self.wkhtmltopdf is None:
            raise Fail("wkhtmltopdf is needed for PDF rendering")

    def render(self, f, output: str):
        self.transform.to_pdf(self.wkhtmltopdf, f, output)


class UpdateCAPath(App):
    """
    create/update an openssl CApath with CA certificates that can be used to
    validate digital signatures
    """
    NAME = "update_capath"

    def __init__(self, args):
        super().__init__(args)
        self.destdir = Path(args.destdir)
        self.remove_old = args.remove_old

    @classmethod
    def add_subparser(cls, subparsers):
        parser = super().add_subparser(subparsers)
        parser.add_argument("destdir", help="CA certificate directory to update")
        parser.add_argument("--remove-old", action="store_true", help="remove old certificates")
        return parser

    def run(self):
        from a38 import trustedlist as tl
        tl.update_capath(self.destdir, remove_old=self.remove_old)


def main():
    parser = argparse.ArgumentParser(description="Handle fattura elettronica files")
    parser.add_argument("--verbose", "-v", action="store_true", help="verbose output")
    parser.add_argument("--debug", action="store_true", help="debug output")

    subparsers = parser.add_subparsers(help="actions", required=True)
    subparsers.dest = "command"

    ExportJSON.add_subparser(subparsers)
    ExportYAML.add_subparser(subparsers)
    ExportXML.add_subparser(subparsers)
    ExportPython.add_subparser(subparsers)
    Edit.add_subparser(subparsers)
    Diff.add_subparser(subparsers)
    Validate.add_subparser(subparsers)
    RenderHTML.add_subparser(subparsers)
    RenderPDF.add_subparser(subparsers)
    UpdateCAPath.add_subparser(subparsers)

    args = parser.parse_args()

    log_format = "%(levelname)s %(message)s"
    level = logging.WARN
    if args.debug:
        level = logging.DEBUG
    elif args.verbose:
        level = logging.INFO
    logging.basicConfig(level=level, stream=sys.stderr, format=log_format)

    app = args.app(args)
    res = app.run()
    if isinstance(res, int):
        sys.exit(res)


if __name__ == "__main__":
    try:
        main()
    except Fail as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except Exception:
        log.exception("uncaught exception")
