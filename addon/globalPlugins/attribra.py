#AttriBra Addon for NVDA
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 Alberto Zanella <lapostadialberto@gmail.com>

import globalPluginHandler
import appModuleHandler
import braille
import api
import ui
import textInfos
from logHandler import log
from configobj import ConfigObj #INI file parsing
from colors import RGB
import os
import globalVars

ATTRS = {}
logTextInfo = False

def decorator(fn,str) :
    def _getTypeformFromFormatField(self, field, formatConfig):
        #convention: to mark we put 4 (bold for liblouis)
        for attr,value in ATTRS.items() :
            fval = field.get(attr,False)
            if fval in value :
                return 4
        # if COMPLCOLORS != None :
            # col = field.get("color",False)
            # if col and (col != COMPLCOLORS):
                # return 4
        return 0
    
    def addTextWithFields_edit(self, info, formatConfig, isSelection=False):
        conf = formatConfig.copy()
        conf["reportFontAttributes"]=True
        conf["reportColor"]=True
        conf["reportSpellingErrors"]=True
        if logTextInfo :
            log.info(info.getTextWithFields(conf))
        fn(self, info, conf, isSelection)


    def update(self) :
        fn(self)
        DOT7 = 64
        DOT8 = 128
        for i in range(0,len(self.rawTextTypeforms)) :
            if self.rawTextTypeforms[i] == 4 :
                self.brailleCells[i] |= DOT7 | DOT8

    if str == "addTextWithFields" :
        return addTextWithFields_edit
    if str == "update" :
        return update
    if str == "_getTypeformFromFormatField" :
        return _getTypeformFromFormatField



class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    configs = {}
    currentPid = ""
    def event_gainFocus(self,obj,nextHandler) :
        nextHandler()
        pid = obj.processID
        if self.currentPid != pid :
            self.populateAttrs(pid)
            self.currentPid = pid
    
    def populateAttrs(self,pid) :
        if (len(self.configs) == 0) : return
        global ATTRS #We are changing the global variable
        appname = appModuleHandler.getAppNameFromProcessID(pid)
        if (appname in self.configs) :
            ATTRS = self.configs[appname]
        elif ("global" in self.configs) :
            ATTRS = self.configs["global"]
        else : ATTRS = {}
        
    
    def __init__(self):
        self.configFile = os.path.join(globalVars.appArgs.configPath,"addons","attribra", "attribra.ini")
        self.parsecfgs() #parse configuration
        if len(self.configs) > 0 : #If no cfg then do not replace functions
            braille.TextInfoRegion._addTextWithFields = decorator(braille.TextInfoRegion._addTextWithFields,"addTextWithFields")
            braille.TextInfoRegion.update = decorator(braille.TextInfoRegion.update,"update")
            braille.TextInfoRegion._getTypeformFromFormatField = decorator(braille.TextInfoRegion._getTypeformFromFormatField,"_getTypeformFromFormatField")        
            
        #superclass constr.
        return super(GlobalPlugin,self).__init__()
    
    def parsecfgs(self) :
        try :
            config = ConfigObj(self.configFile, encoding="UTF-8")
            for app,map in config.iteritems() :
                mappings = {}
                for name,value in map.iteritems() :
                    if isinstance(value,str) :
                        if value.startswith("RGB(") : #it's an RGB Object
                            rgbval = value.split("RGB(")[1]
                            rgbval = rgbval.split(")")[0]
                            rgbval = rgbval.split(",")
                            mappings[name] = [RGB(int(rgbval[0]),int(rgbval[1]),int(rgbval[2]))]
                        else : 
                            try :
                                #if possible adds the value and its int
                                mappings[name] = [value,int(value)]
                            except ValueError :
                                mappings[name] = [value]
                    else : mappings[name] = value
                self.configs[app] = mappings
        except IOError:
            log.debugWarning("No attribra.ini found")
    
    #TODO
    def script_editConfig(self,gesture) :
        self.parsecfgs()
        os.system("start "+self.configFile)
    
    def script_logFieldsAtCursor(self,gesture) :
        global logTextInfo
        logTextInfo = not logTextInfo
        msg = ["stop","start"]
        ui.message("debug textInfo "+msg[logTextInfo])
        
    __gestures={
        "kb:NVDA+control+a":"editConfig",
        "kb:NVDA+control+shift+a":"logFieldsAtCursor",
    }
