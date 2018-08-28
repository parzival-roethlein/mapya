//Maya ASCII 2018 scene
//Name: maya_test_scene_v003.ma
//Last modified: Tue, Aug 28, 2018 10:27:55 AM
//Codeset: 1252
requires maya "2018";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "2018";
fileInfo "cutIdentifier" "201706261615-f9658c4cfc";
fileInfo "osv" "Microsoft Windows 8 Business Edition, 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	rename -uid "45F47B87-4202-2013-5B14-DEA46677CD66";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 10.509094696878208 8.2455080452488669 16.182586725131848 ;
	setAttr ".r" -type "double3" -23.138352729603596 33.000000000000504 9.4809416325866196e-16 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "09DFDEE2-41A0-4B06-45E3-E194F1512F69";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 20.983459852670023;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "CDD21535-404F-7682-1382-51A107F0C90E";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 100.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "6E99BBF1-46AB-B78F-0D5B-FBA0D84724F6";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "A33BC050-4C8F-3FBD-150C-66AF8CA33DCC";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "D926C8C4-42D1-6AEF-42EA-C9ACA162B82B";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "ECD16B05-4E7C-7E54-2054-B0AF107E0B27";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "4728B4C6-4854-FA68-CD94-F6B368037874";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "test_transform1";
	rename -uid "018D09FF-4BEC-27F8-7725-13BB08E193EE";
	addAttr -ci true -sn "bool_user" -ln "bool_user" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "long_user" -ln "long_user" -at "long";
	addAttr -ci true -sn "short_user" -ln "short_user" -at "short";
	addAttr -ci true -sn "byte_user" -ln "byte_user" -min 0 -max 255 -at "byte";
	addAttr -ci true -sn "char_user" -ln "char_user" -min 0 -max 255 -at "char";
	addAttr -ci true -sn "enum_user" -ln "enum_user" -min 0 -max 1000 -en "zero:one:two:thousand=1000" 
		-at "enum";
	addAttr -ci true -sn "float_user" -ln "float_user" -at "float";
	addAttr -ci true -sn "double_user" -ln "double_user" -at "double";
	addAttr -ci true -sn "doubleAngle_user" -ln "doubleAngle_user" -at "doubleAngle";
	addAttr -ci true -sn "doubleLinear_user" -ln "doubleLinear_user" -at "doubleLinear";
	addAttr -ci true -sn "string_user" -ln "string_user" -dt "string";
	addAttr -ci true -sn "stringArray_user" -ln "stringArray_user" -dt "stringArray";
	addAttr -s false -ci true -sn "message_user" -ln "message_user" -at "message";
	addAttr -ci true -sn "time_user" -ln "time_user" -at "time";
	addAttr -ci true -sn "matrix_user" -ln "matrix_user" -dt "matrix";
	addAttr -ci true -sn "fltMatrix_user" -ln "fltMatrix_user" -at "fltMatrix";
	setAttr ".t" -type "double3" -1.9116521491173692 1.9782692617735567 0.26220526955182777 ;
createNode mesh -n "test_transformShape1" -p "test_transform1";
	rename -uid "45DBDAED-4DE8-D4D4-8663-F493487F1258";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".vt[0:7]"  -0.5 -0.5 0.5 0.5 -0.5 0.5 -0.5 0.5 0.5 0.5 0.5 0.5
		 -0.5 0.5 -0.5 0.5 0.5 -0.5 -0.5 -0.5 -0.5 0.5 -0.5 -0.5;
	setAttr -s 12 ".ed[0:11]"  0 1 0 2 3 0 4 5 0 6 7 0 0 2 0 1 3 0 2 4 0
		 3 5 0 4 6 0 5 7 0 6 0 0 7 1 0;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "test_transform2";
	rename -uid "792F3A8E-49C4-2562-7D5C-6B961451F644";
	addAttr -ci true -sn "bool_user" -ln "bool_user" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "long_user" -ln "long_user" -at "long";
	addAttr -ci true -sn "short_user" -ln "short_user" -at "short";
	addAttr -ci true -sn "byte_user" -ln "byte_user" -min 0 -max 255 -at "byte";
	addAttr -ci true -sn "char_user" -ln "char_user" -min 0 -max 255 -at "char";
	addAttr -ci true -sn "enum_user" -ln "enum_user" -min 0 -max 1000 -en "zero:one:two:thousand=1000" 
		-at "enum";
	addAttr -ci true -sn "float_user" -ln "float_user" -at "float";
	addAttr -ci true -sn "double_user" -ln "double_user" -at "double";
	addAttr -ci true -sn "doubleAngle_user" -ln "doubleAngle_user" -at "doubleAngle";
	addAttr -ci true -sn "doubleLinear_user" -ln "doubleLinear_user" -at "doubleLinear";
	addAttr -ci true -sn "string_user" -ln "string_user" -dt "string";
	addAttr -ci true -sn "stringArray_user" -ln "stringArray_user" -dt "stringArray";
	addAttr -s false -ci true -sn "message_user" -ln "message_user" -at "message";
	addAttr -ci true -sn "time_user" -ln "time_user" -at "time";
	addAttr -ci true -sn "matrix_user" -ln "matrix_user" -dt "matrix";
	addAttr -ci true -sn "fltMatrix_user" -ln "fltMatrix_user" -at "fltMatrix";
	setAttr ".t" -type "double3" 0.75504403690445976 2.7379246582946424 -1.7786874559744206 ;
createNode mesh -n "test_transformShape2" -p "test_transform2";
	rename -uid "6AE5005D-473C-669D-4226-E0A862D5832C";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".vt[0:7]"  -0.5 -0.5 0.5 0.5 -0.5 0.5 -0.5 0.5 0.5 0.5 0.5 0.5
		 -0.5 0.5 -0.5 0.5 0.5 -0.5 -0.5 -0.5 -0.5 0.5 -0.5 -0.5;
	setAttr -s 12 ".ed[0:11]"  0 1 0 2 3 0 4 5 0 6 7 0 0 2 0 1 3 0 2 4 0
		 3 5 0 4 6 0 5 7 0 6 0 0 7 1 0;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "7B8B5C93-4CBD-825D-6622-5E92991C730F";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode displayLayerManager -n "layerManager";
	rename -uid "3A713E16-42F9-5C61-2D12-F6A8526FB957";
createNode displayLayer -n "defaultLayer";
	rename -uid "3DF937D6-49A0-5684-EB40-6188BBF4FDB1";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "76E4EC4C-4D5A-1731-8767-97B64E2320CA";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "72FFE86B-4EE6-0D47-AFB3-82ABFD52467B";
	setAttr ".g" yes;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "F474D192-4047-233F-FCC4-6A86B636AB43";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 100 -ast 1 -aet 100 ";
	setAttr ".st" 6;
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "808B1990-4091-1E65-3B7F-91A90A1E94DD";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "43E25792-4B3C-450E-C052-B1919F5773D1";
createNode multiplyDivide -n "test_multiplyDivide1";
	rename -uid "E066DCF3-460B-AE47-2AE9-D898B3D16823";
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".etmr" no;
	setAttr ".tmr" 4096;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr -s 2 ".dsm";
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "test_transformShape1.iog" ":initialShadingGroup.dsm" -na;
connectAttr "test_transformShape2.iog" ":initialShadingGroup.dsm" -na;
// End of maya_test_scene_v003.ma
