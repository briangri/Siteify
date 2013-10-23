class Site:
  '''This object holds an instance of a "site", and is used to return HTML representing that site

  >>> my_site = Site()
  >>> my_site.set_template() # defaults to basic template
  >>> my_site.add_page("PAGE TITLE", "link_to_content")
  >>> site_html = my_site.run(page_requested)
  '''

  def __init__(self, site_title):
    '''Initializes containers that form the backbone of the program'''
    self.imports = []
    self.pages = {}
    self.categories = {}
    self.site_title = site_title

  def set_template(self, template_source=""):
    '''Loads a provided template file. If none is provided, defaults to the basic template in "siteify/"
    Check the default to view template format

    >>> my_site = Site()
    >>> my_site.set_template('my_template.tmpl') # specify a custom template
    >>> my_site.set_template() # use basic template'''

    if not template_source:
      # then we just need to specify our own template
      template_source = "siteify/default_template.tmpl"
    try:
      template_file = open(template_source, "rb")
      self.template = template_file.read()
    except IOError as error:
      # We default back to the normal template
      template_source = "siteify/default_template.tmpl"

  def set_import(self, import_links):
    '''Sets resources to be appended -- supports css and javascript files
    
    >>> my_site = Site()
    >>> my_site.set_import(["style.css", "script.js"])
    >>> my_site.set_import(("another_style.css"))
    '''
    for import_link in import_links:
      self.imports.append(import_link)

  def add_page(self, page_title, page_source, category=None):
    if category is None:
      self.pages[page_title] = page_source 
    else:
      if category not in self.categories:
        self.categories[category] = {}
      self.categories[category][page_title] = page_source

  def template_parse(self):
    tags = [("{{NAV_ELEMENT}}", "{{/NAV_ELEMENT}}"), ("{{SUB_NAV}}", "{{/SUB_NAV}}"), ("{{SUB_NAV_ELEMENT}}", "{{/SUB_NAV_ELEMENT}}") ]
    template_formats = {}
    # loop over once to get the formats
    for (open_tag, close_tag) in tags:
      template_formats[open_tag] = self.template[self.template.find(open_tag) + len(open_tag):self.template.find(close_tag)]
    
    # loop over again to get a cleaned form
    for (open_tag, close_tag) in tags:
      if open_tag in self.template:
         self.template = self.template[:self.template.find(open_tag)] + self.template[self.template.find(close_tag) + len(close_tag):]
    
    return template_formats

  def run(self, request):
    request = request.replace("_", " ")
    content_location = ""

    if request in self.pages:
      content_location = self.pages[request]
      if self.pages[request].startswith("http") or not self.pages[request].endswith(".html"):
        return "Location: " + self.pages[request] + "\n\n" 
    else:
      for category, elements in self.categories.iteritems():
        if request in elements:
          content_location = elements[request]
          if elements[request].startswith("http") or not elements[request].endswith(".html"):
            return "Location: " + elements[request] + "\n\n" 

    if not content_location:
      return "Requested page not found"

    # Parse the template
    template_formats = self.template_parse()

    # set up our imports 
    import_statements = ""
    for an_import in self.imports:
      if an_import.endswith(".css"):
        import_statements += "<link rel=\"stylesheet\" type=\"text/css\" href=\"{link}\" />".format(link=an_import)
      elif an_import.endswith(".js"):
        import_statements += "<script src=\"{link}\"></script>".format(link=an_import)

    # set up our navigation
    nav_code = ""
    for nav_element in self.pages.keys():
      nav_code += template_formats["{{NAV_ELEMENT}}"].format(URL="?req=" + nav_element.replace(" ", "_"), TITLE=nav_element)

    for category, elements in self.categories.iteritems():
      category_format = template_formats["{{SUB_NAV}}"]
      sub_nav_holder = ""
      for nav_element, nav_element_url in elements.iteritems():
         sub_nav_holder += template_formats["{{SUB_NAV_ELEMENT}}"].format(URL="?req=" + nav_element.replace(" ", "_"), TITLE=nav_element)
      category_format = category_format[:category_format.find("{{SUB_NAV_ELEMENT")] + category_format[category_format.find("{{/SUB_NAV_ELEMENT}}") + 20:]
      nav_code += category_format.format(SUB_NAV_ELEMENT_SPOT=sub_nav_holder)

    # and set up content
    page_content = ""
    try:
      page_content = open(content_location).read()
    except IOError as error:
      return "failed to open content file"
    
    return "Content-Type: text/html\n\n" + self.template.format(IMPORTS=import_statements, NAV=nav_code, CONTENT=page_content, PAGE_TITLE=request, SITE_TITLE=self.site_title) 
