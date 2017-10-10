from Resource import Resource


class PanelResource(Resource):
    """ This class represents an instance of panel resource. """
    def __init__(self, name, texture_path, width, height, consumption, production):
        """ Constructor.

        :param name: resources's name
        :param texture_path: path to resource's texture
        :param width: resource's width [px]
        :param height: resource's height [px]
        :param consumption: resource actual consumption
        :param production: resource actual production
        """
        Resource.__init__(self, name, texture_path, width, height)
        self.name = name
        self.consumption = consumption
        self.production = production

        self.update_popup_text()

    def update_popup_text(self):
        """ Update text displayed in popup """
        self.popup_text = '{}\n ' \
                          'Consumption: {}\n ' \
                          'Production: {} '.format(self.name, self.consumption, self.production)
