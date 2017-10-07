from Resource import Resource


class PanelResource(Resource):
    def __init__(self, name, texture_path, width, height, consumption, production):
        """ Constructor.

        :param name: resources's name
        :param texture_path: path to resource's texture
        """
        Resource.__init__(self, name, texture_path, width, height)
        self.name = name
        self.consumption = consumption
        self.production = production

        self.popup_text = '{}\n ' \
                          'Consumption: {}\n ' \
                          'Production: {} '.format(self.name, self.consumption, self.production)

    def update_popup_text(self):
        self.popup_text = '{}\n ' \
                          'Consumption: {}\n ' \
                          'Production: {} '.format(self.name, self.consumption, self.production)
