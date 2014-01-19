#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import re
from string import letters
import CBM
import hashlib
#import bcrypt

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               
                               autoescape = True)
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):

        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

        ##########################################

class LoadPlan(BaseHandler):
    formnames_num = ["weight","pcs","length","width","height"] 
    formnames_str =["measure","Weight_Type","hazardous"]
    variables = [("Weight_Type","sel_weight"),("measure","sel_measure"),("hazardous","sel_haz")]
    

    def isfloat(self,str):
      try:
        float(str)
        return True
      except ValueError:
        return False

    def get(self):

        self.render("Container.html",M3="",CFT="",pcs="",length="",width="",height="",weight="",
            weightlb="",weightkg="",sel_measure="",sel_weight="",error_message="",sel_haz="",Weight="",hazardous="",dim="")
    
    def renderload(self,dict):#takes dictionary --or cookie ? and renders page- finish this
        return


    def post(self): #if all the fields aren't entered in Container.html, an error message is returned. If not, this returns the cubic meters, cubic feet, weight in kilograms 
                    #weight in pounds,
        
        # this needs to ba unit? a class that is passed through each field has a note if it correct or not. And error message?
        #when a line is added this is saved and then a new unit is going to show up?- check the expense and how it is stored.
        #each line needs to passed through to the data and not data?

        complete = True
        pcsdata ={}
        error_message = "Please enter"

        for form in self.formnames_num:
            data = str(self.request.get(form))
            pcsdata[form] = data
            

            if data=="":
                complete = False
                error_message +=" "+form+","
            if not self.isfloat(data):
                complete = False
                error_message +=" only numbers in "+form+","

        for form in self.formnames_str:
            data = str(self.request.get(form))
            pcsdata[form] = data

            if data=="":
                complete = False
                error_message +=" "+form+","
            


        for variable in self.variables:
            if pcsdata[variable[0]]=='selected': #the way I setup the html, an empty dropdown returns 'selected'
                complete = False
                pcsdata[variable[0]] = ""
                error_message +=" "+variable[1]+"," 
            pcsdata[variable[1]] = pcsdata[variable[0]]
                


        if complete :# better way of writing? make sure to make this part of the replacement piece class
        #needs a better  check digit option


            pcs = float(pcsdata["pcs"])




            # look for exception error options on this.

            if pcsdata["measure"] == "IN":
     
                length = float(pcsdata["length"])
                width =float(pcsdata["width"])
                height = float(pcsdata["height"])

            else:

                 
                length = CBM.Calc_IN(float(self.request.get("length")))
                width =CBM.Calc_IN(float(self.request.get("width")))
                height = CBM.Calc_IN(float(self.request.get("height")))


            if pcsdata["Weight_Type"] == "KG":
                pcsdata["weightkg"] = float(pcsdata["weight"])
                pcsdata["weightlb"] = CBM.Calc_LB(float(pcsdata["weight"]))

            if pcsdata["Weight_Type"] == "LB":
                pcsdata["weightkg"]  = CBM.Calc_KG(float(pcsdata["weight"]))
                pcsdata["weightlb"] = float(pcsdata["weight"])




            pcsdata["M3"] =  CBM.Calc_M3(pcs,length,width,height)# in this class this should only be stored after valid options are entered
            pcsdata["CFT"] =  CBM.Calc_CFT(pcs,length,width,height)
            pcsdata["DIM"]=  CBM.Calc_DIM(pcs,length,width,height) #dim weight for an international IATA shipment

            # I want to make a cookie to pass here and have the formating of the number be on the 

        
            self.render("Container.html", M3= "%.3f" % pcsdata["M3"] +" Cubic Meters", CFT="%.2f" % pcsdata["CFT"]+" Cubic Feet", pcs=pcsdata["pcs"],length=pcsdata["length"],
                        width=pcsdata["width"],height=pcsdata["height"], weight=pcsdata["weight"], weightlb="%.2f" % pcsdata["weightlb"] + " Pounds",
                        weightkg="%.2f" % pcsdata["weightkg"] +" Kilograms",sel_measure=pcsdata["measure"],sel_weight=pcsdata["Weight_Type"],
                        sel_haz=pcsdata["hazardous"],dim= "%.0f" % pcsdata["DIM"] +" Kgs Dimensional Weight (IATA)",)
            
            



        else:# need a single reformater to handle this named reload, adds an incomplete cookie ... marked incomplete. Need away to highlight bad forms
            self.render("Container.html", pcs= pcsdata["pcs"],length=pcsdata["length"],
                        width=pcsdata["width"],height=pcsdata["height"], weight=pcsdata["weight"], sel_measure=pcsdata["measure"],sel_weight=pcsdata["Weight_Type"], error_message=error_message[:-1], sel_haz=pcsdata["hazardous"])

            



        else:# need a single reformater to handle this
            self.render("Container.html", pcs= pcsdata["pcs"],length=pcsdata["length"],
                        width=pcsdata["width"],height=pcsdata["height"], weight=pcsdata["weight"], sel_measure=pcsdata["measure"],sel_weight=pcsdata["Weight_Type"], error_message=error_message[:-1], sel_haz=pcsdata["hazardous"])



  
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/container', LoadPlan),
   
