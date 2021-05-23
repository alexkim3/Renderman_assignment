import getpass
import time
import prman

ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "myCup.rib"

ri.Begin("__render")
# ArchiveRecord 
ri.ArchiveRecord(ri.COMMENT, 'File ' +filename)
ri.ArchiveRecord(ri.COMMENT, "Created by " + getpass.getuser())
ri.ArchiveRecord(ri.COMMENT, "Creation Date: " +time.ctime(time.time()))

# now we add the display element using the usual elements
ri.Display("MyCupRender2.png", "file", "rgb")
ri.Format(1920,1080,1)
ri.Hider('raytrace' ,{'int incremental' :[1],'string pixelfiltermode' : 'importance'})
ri.ShadingRate(10)
ri.PixelVariance (0.05)
ri.Integrator ('PxrPathTracer' ,'integrator',{})
ri.Option( 'statistics', {'filename'  : [ 'stats.txt' ] } )
ri.Option( 'statistics', {'endofframe' : [ 1 ] })
ri.Option('searchpath', {'string texture':".\Textures"})
ri.Option('searchpath', {'string shader':'.\Shaders'})
ri.Projection(ri.PERSPECTIVE,{ri.FOV:25}) 

def cupBody(scalex, scaley, scalez, spherex, spherey, spherez, clip):
    ri.TransformBegin()
    ri.Translate(0,0,0)
    ri.Rotate(-90,1,0,0)
    ri.Scale(scalex, scaley, scalez)
    ri.Sphere (spherex, spherey, spherez, clip)
    ri.TransformEnd()

#######################################################################
# now we start our world
ri.WorldBegin()

ri.TransformBegin()
ri.Translate(0,1,18)
ri.Rotate(-170,0,1,0)

#######################################################################
#Lighting We need geo to emit light
#######################################################################
ri.TransformBegin()
ri.AttributeBegin()
ri.Declare('domeLight' ,'string')
ri.Rotate(-84,1,0,0)
ri.Rotate(-33,0,0,1)
ri.Light( 'PxrDomeLight', 'domeLight', { 
        'string lightColorMap'  : 'myEnviroMap2.tex',
        'float intensity' : [2.0],
        'float exposure' : [1.0],
        
})
ri.AttributeEnd()
ri.TransformEnd()
#######################################################################
# end lighting
#######################################################################
ri.TransformBegin()
ri.Translate(0,-1.8,0)
ri.Rotate(-35,0,1,0)
ri.Rotate(87,1,0,0)
ri.Rotate(-8.5,0,1,0)

ri.AttributeBegin()
#outter body
ri.Attribute ("displacementbound", {"sphere" : [1], "coordinatesystem" : ["object"]})
ri.Pattern ("dispDots", "diskTx")
ri.Displace ("PxrDisplace", "mydisp", {"float dispAmount" : [0.03], 
    "reference float dispScalar" : ["diskTx:resultD"]})

ri.Pattern ("dots", "dotsShader", {})
ri.Pattern ("metallicsurfacedots","metal", {})
ri.Bxdf ("PxrDisney", "forTheCupOutter", 
    {"reference color baseColor" : ["dotsShader:Cout"],
    ("reference float metallic") : ["metal:Cout"],
    ("float roughness") : [0.5] })
cupBody(1,1,2.8, 2, -1.4, 0.3, 360)
ri.AttributeEnd()
#inner body
ri.AttributeBegin()
ri.Pattern ("cupInner", "cupInnerShader", {})
ri.Bxdf ("PxrDisney", "forTheCupOutter", {"reference color baseColor" : ["cupInnerShader:resultRGB"]})
cupBody(0.955,0.955,2.755, 2, -1.4, 0.3, 360)
ri.AttributeEnd()

ri.AttributeBegin()
ri.Pattern ("planePink", "pinkShader", {})
ri.Bxdf ("PxrDisney", "forTheCupOutter", {"reference color baseColor" : ["pinkShader:resultRGB"]})
#top bevel
ri.TransformBegin()
ri.Translate(0 ,0.8,0)
ri.Rotate(90,1,0,0)
ri.Torus(1.93,0.05,0,360,360)
ri.TransformEnd()
#outter bottom
DiscRadius = 1.42
ri.TransformBegin()
ri.Translate(0,-3.9,0)
ri.Scale(DiscRadius,DiscRadius,DiscRadius)
ri.Rotate(-90,1,0,0)
ri.Disk(0,1,360)
ri.TransformEnd() 
#inner bottom
DiscRadius2 = 1.415
ri.TransformBegin()
ri.Translate(0,-3.8,0)
ri.Scale(DiscRadius2,DiscRadius2,DiscRadius2)
ri.Rotate(-90,1,0,0)
ri.Disk(0,1,360)
ri.TransformEnd()
ri.AttributeEnd()

#the handle

ri.TransformBegin()
ri.AttributeBegin()

ri.Rotate(40,0,1,0)
ri.Translate(-2.12 ,-1.4,0)
ri.Rotate(81,0,0,1)
ri.Skew(28.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0)
ri.Scale(1,1.2,1.5)
ri.Attribute ("displacementbound", {"sphere" : [1], "coordinatesystem" : ["object"]})
ri.Pattern ("dispHandle", "diskTx")
ri.Displace ("PxrDisplace", "mydisp", {"float dispAmount" : [0.03], 
    "reference float dispScalar" : ["diskTx:resultD"]})
ri.Pattern ("planePink", "pinkShader", {})
ri.Bxdf ("PxrDisney", "forTheCupOutter", {"reference color baseColor" : ["pinkShader:resultRGB"]})
ri.Torus(1.1,0.18,0,360,210)
ri.AttributeEnd()
ri.TransformEnd()


ri.TransformEnd()

#ground plane
ri.AttributeBegin()
ri.Pattern ("wood", "woodShader", {})
ri.Bxdf ("PxrDisney", "forTheCupOutter", {"reference color baseColor" : ["woodShader:Cout"]})
DiscRadius2 = 6
ri.TransformBegin()
ri.Translate(0,-3.85,0)
ri.Scale(DiscRadius2,DiscRadius2,DiscRadius2)
ri.Rotate(-90,1,0,0)
ri.Disk(0,1,360)
ri.TransformEnd()
ri.TransformBegin()
ri.Translate(0,-3.85,0)
ri.Rotate(-90,1,0,0)
ri.Cylinder (6, -1, 0, 360) 
ri.TransformEnd()
ri.AttributeEnd()

ri.TransformEnd()
ri.WorldEnd()
# and finally end the rib file
ri.End()
