import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

        mxd = arcpy.mapping.MapDocument("current")
        
        arcpy.mapping.ListLayers(mxd)[0].definitionQuery = ""
        arcpy.mapping.ListLayers(mxd)[1].definitionQuery = ""
        arcpy.mapping.ListLayers(mxd)[2].definitionQuery = "" 


    def getParameterInfo(self):
        """Define parameter definitions"""
        
        # Field to select the layer to use to define selection
        param0 = arcpy.Parameter(
            displayName = "Definition Layer",
            name = "def_layer",
            datatype = "GPFeatureLayer",
            parameterType = "Required",
            direction = "Input")

        # Define field to select BLOCK if selected
        param1 = arcpy.Parameter(
            displayName = 'Block Key',
            name = "block_key",
            datatype = "GPDouble",
            parameterType = "Optional",
            direction = "Input")

        # Define field to select SECTION if selected
        param2 = arcpy.Parameter(
            displayName = 'Section ID',
            name = "section_id",
            datatype = "GPLong",
            parameterType = "Optional",
            direction = "Input")

        # Define field to select DIVISION if selected
        param3 = arcpy.Parameter(
            displayName = 'Division Code',
            name = "division_code",
            datatype = "GPLong",
            parameterType = "Optional",
            direction = "Input")

        # Define field for fun
        param4 = arcpy.Parameter(
            displayName = 'Display Blocks',
            name = "blocks_checkbox",
            datatype = "GPBoolean",
            parameterType = "Optional",
            direction = "Input")

        # Define field for fun
        param5 = arcpy.Parameter(
            displayName = 'Display Sections',
            name = "sections_checkbox",
            datatype = "GPBoolean",
            parameterType = "Optional",
            direction = "Input")

        # Define field for fun
        param6 = arcpy.Parameter(
            displayName = 'Display Divisions',
            name = "divisions_checkbox",
            datatype = "GPBoolean",
            parameterType = "Optional",
            direction = "Input")
        
        param1.enabled = False
        param2.enabled = False
        param3.enabled = False
        param4.enabled = False
        param5.enabled = False
        param6.enabled = False

        mxd = arcpy.mapping.MapDocument("current")
        
        arcpy.mapping.ListLayers(mxd)[0].definitionQuery = ""
        arcpy.mapping.ListLayers(mxd)[1].definitionQuery = ""
        arcpy.mapping.ListLayers(mxd)[2].definitionQuery = ""        
        parameters = [param0, param1, param2, param3, param4, param5, param6]

        return parameters 


    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        # If "Blocks" is selected
        if parameters[0].valueAsText == 'Blocks':

            fc = parameters[0].value
            col = 'BLOCK_KEY'

            # Enable "Blocks" field
            parameters[1].enabled = True

            # Disable "Sections" field
            parameters[2].enabled = False

            # Disable "Divisions" field
            parameters[3].enabled = False

            # Disable "Blocks" checkbox
            parameters[4].enabled = False

            # Enable "Sections" checkbox
            parameters[5].enabled = True
            parameters[5].value = True

            # Enable "Divisions" checkbox
            parameters[6].enabled = True
            parameters[6].value = True

            parameters[1].filter.list = [val for val in sorted(set(row.getValue(col) for row in arcpy.SearchCursor(fc, None, None, col)))]

        # If "Sections" is selected
        elif parameters[0].valueAsText == 'Sections':

            # Disable "Blocks" field
            parameters[1].enabled = False

            # Enable "Sections" field
            parameters[2].enabled = True

            # Disable "Divisions" field
            parameters[3].enabled = False

            # Enable "Blocks" checkbox
            parameters[4].enabled = True
            parameters[4].value = True

            # Disable "Sections" checkbox
            parameters[5].enabled = False

            # Enable "Divisions" checkbox
            parameters[6].enabled = True
            parameters[6].value = True
            
            fc = parameters[0].value
            col = 'SECTION_ID'

            parameters[2].filter.list = [val for val in sorted(set(row.getValue(col) for row in arcpy.SearchCursor(fc, None, None, col)))]

        # If "Divisions" is selected
        elif parameters[0].valueAsText == 'Divisions':

            # Disable "Blocks" field
            parameters[1].enabled = False

            # Disable "Sections" field
            parameters[2].enabled = False

            # Enable "Divisions" field
            parameters[3].enabled = True
            
            # Enable "Blocks" checkbox
            parameters[4].enabled = True
            parameters[4].value = True
            
            # Enable "Sections" checkbox
            parameters[5].enabled = True
            parameters[5].value = True

            # Disable "Divisions" checkbox
            parameters[6].enabled = False
            
            fc = parameters[0].value
            col = 'DIVISION_CODE'

            parameters[3].filter.list = [val for val in sorted(set(row.getValue(col) for row in arcpy.SearchCursor(fc, None, None, col)))]
            
        else:
            parameters[1].enabled = False
            parameters[2].enabled = False
            parameters[3].enabled = False
            parameters[4].enabled = False
            parameters[5].enabled = False
            parameters[6].enabled = False


        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""


        # If "Blocks" is selected
        if parameters[0].valueAsText == 'Blocks':

            mxd = arcpy.mapping.MapDocument("current")

	    dataFrame = arcpy.mapping.ListDataFrames(mxd)[0]

            for lyr in arcpy.mapping.ListLayers(mxd):
                lyr.visible = False

            parameters[0].value.visible = True
            
            parameters[0].value.definitionQuery = "BLOCK_KEY = " + parameters[1].valueAsText
            arcpy.mapping.ListLayers(mxd)[1].definitionQuery = ""
            arcpy.mapping.ListLayers(mxd)[2].definitionQuery = ""
            
	    dataFrame.extent = parameters[0].value.getExtent(True) # visible extent of layer

	    dataFrame.scale = dataFrame.scale*2

            layer = arcpy.mapping.ListLayers(mxd)[0]
            layer.labelClasses[0].expression = "[BLOCK_KEY]"
            
            parameters[0].value.showLabels = True
            arcpy.mapping.ListLayers(mxd)[1].showLabels = False
            arcpy.mapping.ListLayers(mxd)[2].showLabels = False
            
        # If "Sections" is selected
        elif parameters[0].valueAsText == 'Sections':

            mxd = arcpy.mapping.MapDocument("current")

	    dataFrame = arcpy.mapping.ListDataFrames(mxd)[0]

            for lyr in arcpy.mapping.ListLayers(mxd):
                lyr.visible = False

            parameters[0].value.visible = True

            
            parameters[0].value.definitionQuery = "SECTION_ID = " + parameters[2].valueAsText
            arcpy.mapping.ListLayers(mxd)[0].definitionQuery = ""
            arcpy.mapping.ListLayers(mxd)[2].definitionQuery = ""
            
	    dataFrame.extent = parameters[0].value.getExtent(True) # visible extent of layer

	    dataFrame.scale = dataFrame.scale*2

            layer = arcpy.mapping.ListLayers(mxd)[1]
            layer.labelClasses[0].expression = "[SECTION_ID]"
            
            parameters[0].value.showLabels = True
            arcpy.mapping.ListLayers(mxd)[0].showLabels = False
            arcpy.mapping.ListLayers(mxd)[2].showLabels = False

        # If "Divisions" is selected
        elif parameters[0].valueAsText == 'Divisions':

            mxd = arcpy.mapping.MapDocument("current")

	    dataFrame = arcpy.mapping.ListDataFrames(mxd)[0]

            for lyr in arcpy.mapping.ListLayers(mxd):
                lyr.visible = False

            parameters[0].value.visible = True
            parameters[0].value.definitionQuery = "DIVISION_CODE = " + parameters[3].valueAsText
            arcpy.mapping.ListLayers(mxd)[0].definitionQuery = ""
            arcpy.mapping.ListLayers(mxd)[1].definitionQuery = ""
            
	    dataFrame.extent = parameters[0].value.getExtent(True) # visible extent of layer

	    dataFrame.scale = dataFrame.scale*2

            layer = arcpy.mapping.ListLayers(mxd)[2]
            layer.labelClasses[0].expression = "[DIVISION_CODE]"
            
            parameters[0].value.showLabels = True
            arcpy.mapping.ListLayers(mxd)[0].showLabels = False
            arcpy.mapping.ListLayers(mxd)[1].showLabels = False

        if parameters[4].value:
            arcpy.mapping.ListLayers(mxd)[0].visible = True
        if parameters[5].value:
            arcpy.mapping.ListLayers(mxd)[1].visible = True
        if parameters[6].value:
            arcpy.mapping.ListLayers(mxd)[2].visible = True

##
##
##            if arcpy.mapping.ListLayers(mxd)[0].supports("LABELCLASSES"):
##                print "this"
##            else:
##                print "not this"
###                lblClass = parameters[0].value.listLabelClasses("Block_Key")[0]
###                lblClass.expression = "BLOCK_KEY"
###                lblClass.SQLQuery = "Type_ = 'summit' And Elevation > 2000"
###                lblClass.visible = True






            arcpy.RefreshActiveView()







##        # If "Sections" is selected
##        elif parameters[0].valueAsText == 'Sections':
##
##            # Disable "Blocks" field
##            parameters[1].enabled = False
##
##            # Enable "Sections" field
##            parameters[2].enabled = True
##
##            # Disable "Divisions" field
##            parameters[3].enabled = False
##            
##            fc = parameters[0].value
##            col = 'SECTION_ID'
##
##            parameters[2].filter.list = [val for val in sorted(set(row.getValue(col) for row in arcpy.SearchCursor(fc, None, None, col)))]
##
##        # If "Divisions" is selected
##        elif parameters[0].valueAsText == 'Divisions':
##
##            # Disable "Blocks" field
##            parameters[1].enabled = False
##
##            # Disable "Sections" field
##            parameters[2].enabled = False
##
##            # Enable "Divisions" field
##            parameters[3].enabled = True
##            
##            fc = parameters[0].value
##            col = 'DIVISION_CODE'



            
        return




##    def FindLabel([BLOCK_KEY]):
##        return [BLOCK_KEY]



    
