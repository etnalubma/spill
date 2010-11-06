import optparse

class PlainHelpFormatter(optparse.IndentedHelpFormatter):

    def __init__(self,
                 indent_increment=2,
                 max_help_position=24,
                 width=None,
                 short_first=1):

        optparse.IndentedHelpFormatter.__init__(
            self, indent_increment, max_help_position, width, short_first)

    def format_description(self, description):
        if description:
            return description + "\n"
        else:
            return ""
