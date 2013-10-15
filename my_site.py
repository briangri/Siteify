#!/usr/local/bin/python
import cgi, cgitb
from Site import Site

def main():
  my_site = Site()
  site_init(my_site)

  # retrieve info
  form = cgi.FieldStorage()

  # run site
  if "req" in form:
    display(my_site.run(form["req"].value))
  # display(my_site.run("home"))

def site_init(my_site):  
  my_site.set_template()
  my_site.set_import(("assets/style.css")) 
  my_site.add_page("Home", "content/home.html")
  my_site.add_page("Resume", "content/resume.html")
  my_site.add_page("ReColor It", "contents/recolorit.html", category="Projects")

def display(message):
  print "Content-Type: text/html\n\n"
  print message

main()  
