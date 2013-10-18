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
    if request not in self.pages: 
      print request
      print self.pages
      return "Not Found"
    
    # set up our imports 
    import_statements = ""
    for an_import in self.imports:
      if an_import.endswith(".css"):
        import_statements += "<link rel=\"stylesheet\" type=\"text/css\" href=\"{link}\" />".format(link=an_import)
      elif an_import.endswith(".js"):
        import_statements += "<script src=\"{link}\"></script>".format(link=an_import)

    # set up our navigation
    nav_elements = ""
    for nav_element in self.pages.keys():
      if isinstance(self.pages[nav_element], basestring):
        # Then it is not a sub page
        nav_elements += "<a href=\"{link}\">{title}</a>".format(link=self.pages[nav_element], title=nav_element)
  
    # and set up content
    page_content = ""
    try: 
        page_content = open(self.pages[request]).read()
    except IOError as error:
      print "Failed to open content file"

    return self.template.format(IMPORTS=import_statements, NAV=nav_elements, CONTENT=page_content, SUBNAV="") 




