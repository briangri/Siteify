class Site:

  def __init__(self):
    # initialize our containers
    self.imports = []
    self.pages = {}

  def set_template(self, template_source=""):
    if not template_source:
      # then we just need to specify our own template
      template_source = "siteify/default_template.tmpl"
    try:
      template_file = open(template_source, "rb")
      self.template = template_file.read()
    except IOError as error:
      print "Error opening file" 

  def set_import(self, import_link):
    self.imports.append(import_link)

  def add_page(self, page_title, page_source, category=None):
    if category is None:
      self.pages[page_title] = page_source 
    else:
      if category not in self.pages:
        self.pages[category] = {}
      self.pages[category][page_title] = page_source

  def run(self, request):
    # check if the request is something we can deal with
    return request 
