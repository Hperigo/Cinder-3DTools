
import c4d
import array
import math 
import xml.dom.minidom as minidom
import os
import re
import struct
import xml.etree.cElementTree as ET

class _c4d( object ):
	OBJECT_EMPTY_POLYGON  = 5100
	OBJECT_CONE           = 5162
	OBJECT_CUBE           = 5159
	OBJECT_CYLINDER       = 5170
	OBJECT_DISC           = 5164
	OBJECT_PLANE          = 5168
	OBJECT_POLYGON        = 5174
	OBJECT_SPHERE         = 5160
	OBJECT_TORUS          = 5163
	OBJECT_CAPSULE        = 5171
	OBJECT_OIL_TANK       = 5172
	OBJECT_TUBE           = 5165
	OBJECT_PYRAMID        = 5167
	OBJECT_PLATONIC       = 5161
	pass

## TriMesh
#
# This class is generic. Should be usable outside of Maya.
#
class TriMesh( object ):
	# noinspection PyPep8
	POSITION    = 0x00000001
	COLOR       = 0x00000002
	TEX_COORD_0 = 0x00000004
	TEX_COORD_1 = 0x00000008
	TEX_COORD_2 = 0x00000010
	TEX_COORD_3 = 0x00000020
	NORMAL      = 0x00000100
	TANGENT     = 0x00000200
	BITANGENT   = 0x00000400
	BONE_INDEX  = 0x00001000
	BONE_WEIGHT = 0x00002000
	CUSTOM_0    = 0x00010000
	CUSTOM_1    = 0x00020000
	CUSTOM_2    = 0x00040000
	CUSTOM_3    = 0x00080000
	CUSTOM_4    = 0x00100000
	CUSTOM_5    = 0x00200000
	CUSTOM_6    = 0x00400000
	CUSTOM_7    = 0x00800000
	CUSTOM_8    = 0x01000000
	CUSTOM_9    = 0x02000000	

	def __init__( self ):
		self.version    = int(2)
		self.indices    = array.array( 'L' )
		self.positions  = array.array( 'f' )
		self.colors     = array.array( 'f' )
		self.normals    = array.array( 'f' )
		self.texCoords0 = array.array( 'f' )
		self.texCoords1 = array.array( 'f' )
		self.texCoords2 = array.array( 'f' )
		self.texCoords3 = array.array( 'f' )
		self.tangents   = array.array( 'f' )
		self.bitangents = array.array( 'f' )

		self.positionsDims  = 0
		self.colorsDims     = 0
		self.normalsDims    = 0
		self.texCoords0Dims = 0
		self.texCoords1Dims = 0
		self.texCoords2Dims = 0
		self.texCoords3Dims = 0
		self.tangentsDims   = 0
		self.bitangentsDims = 0		
		pass

	def appendPosition( self, x, y, z = None, w = None ):
		self.positions.append( x )
		self.positions.append( y )
		if z is not None:
			self.positions.append( z )
		if w is not None:
			self.positions.append( w )
		if 0 == self.positionsDims:
			if w is not None:
				self.positionsDims = 4
			elif z is not None:
				self.positionsDims = 3
			else:
				self.positionsDims = 2
		pass

	def appendNormal( self, x, y, z ):
		self.normals.append( x )
		self.normals.append( y )
		self.normals.append( z )
		if 0 == self.normalsDims:
			self.normalsDims = 3
		pass

	def appendTangent( self, x, y, z ):
		self.tangents.append( x )
		self.tangents.append( y )
		self.tangents.append( z )
		if 0 == self.tangentsDims:
			self.tangentsDims = 3
		pass

	def appendBitangent( self, x, y, z ):
		self.bitangents.append( x )
		self.bitangents.append( y )
		self.bitangents.append( z )
		if 0 == self.bitangentsDims:
			self.bitangentsDims = 3
		pass

	def appendRgb( self, r, g, b ):
		self.colors.append( r )
		self.colors.append( g )
		self.colors.append( b )
		if 0 == self.colorsDims:
			self.colorsDims = 3
		pass

	def appendRgba( self, r, g, b, a ):
		self.colors.append( r )
		self.colors.append( g )
		self.colors.append( b )
		self.colors.append( a )
		if 0 == self.colorsDims:
			self.colorsDims = 4
		pass

	def appendTexCoord0( self, x, y, z = None, w = None ):
		self.texCoords0.append( x )
		self.texCoords0.append( y )
		if z is not None:
			self.texCoords0.append( z )
		if w is not None:
			self.texCoords0.append( w )
		if 0 == self.texCoords0Dims:
			if w is not None:
				self.texCoords0Dims = 4
			elif z is not None:
				self.texCoords0Dims = 3
			else:
				self.texCoords0Dims = 2			
		pass

	def appendTexCoord1( self, x, y, z = None, w = None ):
		self.texCoords1.append( x )
		self.texCoords1.append( y )
		if z is not None:
			self.texCoords1.append( z )
		if w is not None:
			self.texCoords1.append( w )
		if 0 == self.texCoords1Dims:
			if w is not None:
				self.texCoords1Dims = 4
			elif z is not None:
				self.texCoords1Dims = 3
			else:
				self.texCoords1Dims = 2
		pass

	def appendTexCoord2( self, x, y, z = None, w = None ):
		self.texCoords2.append( x )
		self.texCoords2.append( y )
		if z is not None:
			self.texCoords2.append( z )
		if w is not None:
			self.texCoords2.append( w )
		if 0 == self.texCoords2Dims:
			if w is not None:
				self.texCoords2Dims = 4
			elif z is not None:
				self.texCoords2Dims = 3
			else:
				self.texCoords2Dims = 2			
		pass

	def appendTexCoord3( self, x, y, z = None, w = None ):
		self.texCoords3.append( x )
		self.texCoords3.append( y )
		if z is not None:
			self.texCoords3.append( z )
		if w is not None:
			self.texCoords3.append( w )
		if 0 == self.texCoords3Dims:
			if w is not None:
				self.texCoords3Dims = 4
			elif z is not None:
				self.texCoords3Dims = 3
			else:
				self.texCoords3Dims = 2					
		pass

	def appendIndex( self, v ):
		self.indices.append( v )
		pass		

	def appendTriangle( self, v0, v1, v2 ):
		self.indices.append( v0 )
		self.indices.append( v1 )
		self.indices.append( v2 )
		pass

	def getNumVertices( self ):
		return len( self.indices )
		pass

	def writeAttrib( self, file, attrib, dims, size, data ):
		if 0 == size:
			return
		file.write( struct.pack( "I", attrib ) )
		file.write( struct.pack( "B", dims ) )
		file.write( struct.pack( "I", size ) )
		data.tofile( file )
		pass

	def write( self, path ):
		try:
			file = open( path, "wb" )
		except:
			print( "Failed to open file for write: %s" % path )
			return
		file.write( struct.pack( "B", self.version ) )
		file.write( struct.pack( "I", self.getNumVertices() ) )
		# Write indices
		if self.getNumVertices() > 0:
			self.indices.tofile( file )
		# Write attributes
		self.writeAttrib( file, TriMesh.POSITION, self.positionsDims, len( self.positions ), self.positions )
		self.writeAttrib( file, TriMesh.COLOR, self.colorsDims, len( self.colors ), self.colors )
		self.writeAttrib( file, TriMesh.NORMAL, self.normalsDims, len( self.normals ), self.normals )
		self.writeAttrib( file, TriMesh.TEX_COORD_0, self.texCoords0Dims, len( self.texCoords0 ), self.texCoords0 )
		self.writeAttrib( file, TriMesh.TEX_COORD_1, self.texCoords1Dims, len( self.texCoords1 ), self.texCoords1 )
		self.writeAttrib( file, TriMesh.TEX_COORD_2, self.texCoords2Dims, len( self.texCoords2 ), self.texCoords2 )
		self.writeAttrib( file, TriMesh.TEX_COORD_3, self.texCoords3Dims, len( self.texCoords3 ), self.texCoords3 )
		self.writeAttrib( file, TriMesh.TANGENT, self.tangentsDims, len( self.tangents ), self.tangents )
		self.writeAttrib( file, TriMesh.BITANGENT,  self.bitangentsDims, len( self.bitangents ), self.bitangents )
		file.close()
		pass

	# class TriMesh
	pass	

## TriMeshExporter
#
#
class TriMeshExporter( object ):
	def __init__( self ):
		pass

	## createFilePath
	def createFilePath( self, polyObj, path, ext ):
		# Use object name
		fileName = polyObj.GetName()
		# Remove the first instance of | 
		if fileName.startswith( "|" ):
			fileName = re.sub( "\|", "", fileName, count = 1 )
		# Replace all remaining instances of | with _
		fileName = re.sub( "\|", "_", fileName )
		# Replace all instances of : with _
		fileName = re.sub( ":", "_", fileName )		
		# Create full path
		if ext.startswith( "." ):
			fileName = os.path.join( path, fileName ) + ext	
		else: 			
			fileName = os.path.join( path, fileName ) + "." + ext	
		# Replace all \ with /
		fileName = fileName.replace( "\\", "/" )
		# Return it!
		return fileName
		pass			

	def createTriMesh( self, polyObj ):
		# TriMesh
		triMesh = TriMesh()
		# Return
		return triMesh
		pass		

	def writeTriMeshFile( self, polyObj, path, xmlParent ):
		# Write initial data to XML
		xml = ET.SubElement( xmlParent, "shaderSet", name = polyObj.GetName() )
		xml.set( "type", "lambert" )			
		# Get buffers
		triMesh = self.createTriMesh( polyObj );
		# Write buffers
		geoXml = ET.SubElement( xml, "geometry" )
		geoXml.set( "vertexCount", str( triMesh.getNumVertices() ) ) 
		# Generate file path
		filePath = self.createFilePath( polyObj, path, ".mesh" );
		triMesh.write( filePath )
		# Add triMeshFile attribute 
		relFilePath = os.path.relpath( filePath, os.path.dirname( self.xmlFilePath ) )
		relFilePath = relFilePath.replace( "\\", "/" )
		geoXml.set( "triMeshFile", relFilePath )
		# Write out data
		print( "Exported %s to %s" % ( polyObj.GetName(), filePath ) )			
		pass

	## exportMesh
	def exportMesh( self, polyObj, path, xmlParent ):
		xml = ET.SubElement( xmlParent, "mesh", name = polyObj.GetName() )
		self.writeTriMeshFile( polyObj, path, xmlParent )
		pass

	## exportSelected
	def exportSelected( self, path, bakeTranform, angleWeightedNormals ):
		doc = c4d.documents.GetActiveDocument()

		validObjectTypes = [
			_c4d.OBJECT_CONE,
			_c4d.OBJECT_CUBE,
			_c4d.OBJECT_CYLINDER,
			_c4d.OBJECT_DISC,
			_c4d.OBJECT_PLANE,
			_c4d.OBJECT_POLYGON,
			_c4d.OBJECT_SPHERE,
			_c4d.OBJECT_TORUS,
			_c4d.OBJECT_CAPSULE,
			_c4d.OBJECT_OIL_TANK,
			_c4d.OBJECT_TUBE,
			_c4d.OBJECT_PYRAMID,
			_c4d.OBJECT_PLATONIC
		]

		polyObjs = []
	
		selected = doc.GetActiveObjects( c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER )
		for itObj in selected:
			obj = itObj
			objType = obj.GetType()
			if _c4d.OBJECT_POLYGON != objType:
				if objType in validObjectTypes:
					try:
						tmpObj = obj.GetClone()
						tmpList = c4d.utils.SendModelingCommand( command = c4d.MCOMMAND_CURRENTSTATETOOBJECT, list = [tmpObj], mode = c4d.MODELINGCOMMANDMODE_ALL, doc = doc )
						c4d.utils.SendModelingCommand( command = c4d.MCOMMAND_TRIANGULATE, list = tmpList, doc = doc )
						if len( tmpList ) > 0:
							obj = tmpList[0]
							pass
					except Exception, e:
						print( "Failed to convert %s (type=%d) to triangles: %s" % ( obj.GetName(), obj.GetType(), e ) )
						obj = None
						pass
				else:
					print( "Unsupported object %s (type=%d)" % ( obj.GetName(), obj.GetType() ) )
					obj = None
					pass

			if obj is not None:
				polyObjs.append( obj )
				pass

		# Create a directory using the scene name
		sceneFileName = doc.GetDocumentName()
		if sceneFileName is None:
			sceneFileName = "untitled"
			pass
		sceneFileName = sceneFileName.replace( " ", "_" )
		[sceneFile, sceneExt] = os.path.splitext( os.path.basename( sceneFileName ) )
		path = os.path.join( path, sceneFile )
		print( "Exporting as Cinder TriMesh data to %s" % path )
		if not os.path.exists( path ):
			os.makedirs( path )
		# XML scene file path
		self.xmlFilePath = os.path.join( path, sceneFile + ".xml" )
		self.xmlFilePath = self.xmlFilePath.replace( "\\", "/" )	
		# Create XML doc
		xmlRoot = ET.Element( "simplescene" )

		# Export mesh geometry
		for polyObj in polyObjs:
			self.exportMesh( polyObj, path, xmlRoot )
			pass

		# Write XML
		if len( list( xmlRoot ) ) > 0:
			tree = ET.ElementTree( xmlRoot )
			prettyXml = minidom.parseString( ET.tostring( xmlRoot ) ).toprettyxml( indent = "   " )
			file = open( self.xmlFilePath, "w" )
			file.write( prettyXml )	
			print( "Wrote %s" % self.xmlFilePath )
			pass
			
		pass

	# class TriMeshExporter 		
	pass

def exportSelected( path, *args, **kwargs ):
	# Error check arguments
	validKeys = ["bakeTransform", "angleWeightedNormals"]
	for key in kwargs.keys():
		if key not in validKeys:
			raise RuntimeError( "Unknown paramemter: %s" % key )
	# Grab arguemnts
	bakeTransform = kwargs.get( "bakeTransform", False )
	angleWeightedNormals = kwargs.get( "angleWeightedNormals", False )
	# Run exporter
	# Run exporter
	exporter = TriMeshExporter()
	exporter.exportSelected( path, bakeTransform, angleWeightedNormals )
	pass