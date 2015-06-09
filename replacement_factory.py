import re

def replacement_factory(replacement_dict):
    for k in replacement_dict:
        if len(k) <= 1:
            print("----")
            print("Warning: potential error in replacement dictionary")
            print("Very short key found: '{}'".format(k))
            print("!!! Ignoring these records.")
            print("----")

    # Create a regular expression from the dictionary keys
    keys = sorted([k for k in replacement_dict.keys() if len(k) > 2],
                  key=len, reverse=True)
    expression = [re.escape(item) for item in keys]
    regex = re.compile("({})".format("|".join(expression)))


    def multiple_replace(text):
        """Replace in 'text' all occurences of any key in the given
        dictionary by its corresponding value.  Returns the new string.

        Avoids situation where key gets translated to value, and if value is a
        key gets translated again.

        http://code.activestate.com/recipes/81330-single-pass-multiple-replace/
        """


        # For each match, look-up corresponding value in dictionary
        return regex.sub(lambda mo: replacement_dict[mo.string[mo.start():mo.end()]], text)

    return multiple_replace
