import math

import win32com.client
from win32com.client import VARIANT
import numpy as np
import matplotlib.pyplot as plt
import pythoncom

# Make sure both Python and Solidworks are running at the same administrative level, otherwise we get "operation unavailable" error

class DHT:

    def RGBtoSW(self, r, g, b):
        return b * 65536 + g * 256 + r

    stringAddress = "C:\\Program Files\\SOLIDWORKS Corp\\SOLIDWORKS\\data\\weldment profiles\\Shapeshifter Standard\\Tensegrity String 3 mm\\3mm.SLDLFP"
    barAddress = "C:\\Program Files\\SOLIDWORKS Corp\\SOLIDWORKS\\data\\weldment profiles\\Shapeshifter Standard\\Tensegrity Bar 6 mm\\6mm Bar.SLDLFP"
    nodeRadius = 0.01

    def __init__(self, p = 5, q = 4, L = 1, a = (1/16), Ld = 1.005):
        self.p = p
        self.q = q
        self.L = L
        self.a = a
        self.Ld = Ld

        self.N1 = np.zeros((self.q + 1, self.p, 3))
        self.N2 = np.zeros((self.q + 1, self.p, 3))

        self.generate()
    
    def generate(self):
        for i in range(self.q+1):
            for k in range(self.p):

                l = 1
                z1 = (2 * i + (l-1)) * (self.L / (2 * self.q))
                theta1 = (2 * k + l) * (np.pi / self.p)
                r1_val = np.sqrt(4 * self.a * (self.Ld - z1))

                self.N1[i, k, 0] = r1_val * np.cos(theta1)
                self.N1[i, k, 1] = r1_val * np.sin(theta1)
                self.N1[i, k, 2] = z1

                if i < self.q:
                    l = 2
                    z2 = (2 * i + (l-1)) * (self.L / (2 * self.q))
                    theta2 = (2*k+l)*(np.pi/self.p)
                    r2_val = np.sqrt(4 * self.a * (self.Ld - z2))

                    self.N2[i, k, 0] = r2_val * np.cos(theta2)
                    self.N2[i, k, 1] = r2_val * np.sin(theta2)
                    self.N2[i, k, 2] = z2
                else:
                    self.N2[i,k,:] = np.nan

    def visualize(self, showList):

        fig = plt.figure("Double Helix Paraboloid Tensegrity", figsize = (8,8), facecolor="w")
        ax = fig.add_subplot(111, projection='3d')

        ax.set_xlabel('X [m]')
        ax.set_ylabel('Y [m]')
        ax.set_zlabel('Z [m]')
        ax.set_title(f'p = {self.p}, q = {self.q}, L = {self.L}, a = {self.a}, L = {self.L}')

        for i in range(self.q+1):
            for k in range(self.p):

                #Nodes
                ax.plot([self.N1[i, k, 0]], [self.N1[i, k, 1]], [self.N1[i, k, 2]], 'ko', markerfacecolor='k', markersize=4)
                if i < self.q:
                    ax.plot([self.N2[i, k, 0]], [self.N2[i, k, 1]], [self.N2[i, k, 2]], 'ro', markerfacecolor='r', markersize=4)
                
                #Bars
                if i < self.q:
                    k_curr = k
                    kp1 = (k+1) % self.p
                    km1 = (k-1) % self.p

                    n1_ik      = self.N1[i, k_curr]
                    n2_ik      = self.N2[i, k_curr]
                
                    n1_ip1_kp1 = self.N1[i + 1, kp1]
                    n2_ip1_km1 = self.N2[i + 1, km1]
                
                    n1_ip1_k   = self.N1[i + 1, k_curr]
                    n2_i_km1   = self.N2[i, km1]
                    n1_ip1_km1 = self.N1[i + 1, km1]

                    ax.plot([n1_ik[0], n1_ip1_kp1[0]], [n1_ik[1], n1_ip1_kp1[1]], [n1_ik[2], n1_ip1_kp1[2]], 'b-', linewidth=2)

                    if i < self.q -1:
                        ax.plot([n2_ik[0], n2_ip1_km1[0]], [n2_ik[1], n2_ip1_km1[1]], [n2_ik[2], n2_ip1_km1[2]], 'b-', linewidth=2)
                        # --- STRINGS ---
                        if showList[0]: # s1
                            ax.plot([n1_ik[0], n2_ik[0]], [n1_ik[1], n2_ik[1]], [n1_ik[2], n2_ik[2]], 'r--', linewidth=1)
                        if showList[1]: # s2
                            ax.plot([n2_ik[0], n1_ip1_k[0]], [n2_ik[1], n1_ip1_k[1]], [n2_ik[2], n1_ip1_k[2]], 'g--', linewidth=1)
                        if showList[2]: # s3
                            ax.plot([n1_ip1_k[0], n2_i_km1[0]], [n1_ip1_k[1], n2_i_km1[1]], [n1_ip1_k[2], n2_i_km1[2]], 'm--', linewidth=1)
                        if showList[3]: # s4
                            ax.plot([n2_i_km1[0], n1_ik[0]], [n2_i_km1[1], n1_ik[1]], [n2_i_km1[2], n1_ik[2]], 'k--', linewidth=1)
                        if showList[4]: # s5
                            ax.plot([n2_i_km1[0], n2_ik[0]], [n2_i_km1[1], n2_ik[1]], [n2_i_km1[2], n2_ik[2]], 'k--', linewidth=1)
                        if showList[5]: # s6
                            ax.plot([n1_ik[0], n1_ip1_k[0]], [n1_ik[1], n1_ip1_k[1]], [n1_ik[2], n1_ip1_k[2]], 'r-', linewidth=1)
                        if showList[6]: # s7
                            ax.plot([n1_ip1_km1[0], n1_ip1_k[0]], [n1_ip1_km1[1], n1_ip1_k[1]], [n1_ip1_km1[2], n1_ip1_k[2]], 'g-', linewidth=1)
                        if showList[7]: # s8
                            ax.plot([n2_i_km1[0], n2_ip1_km1[0]], [n2_i_km1[1], n2_ip1_km1[1]], [n2_i_km1[2], n2_ip1_km1[2]], 'c--', linewidth=1)
                    else:
                        n1_top = self.N1[i + 1, k_curr]
                        ax.plot([n2_ik[0], n1_top[0]], [n2_ik[1], n1_top[1]], [n2_ik[2], n1_top[2]], 'c-', linewidth=2)
        plt.show()

    def exportCoordinatesTXT(self, filename, scaling = 10):

        N1_flat = self.N1.reshape(-1, 3)
        N1_flat = N1_flat[~np.isnan(N1_flat).any(axis=1)]
        N1_flat = N1_flat * scaling

        N2_flat = self.N2.reshape(-1, 3)
        N2_flat = N2_flat[~np.isnan(N2_flat).any(axis=1)]
        N2_flat = N2_flat * scaling

        np.savetxt(filename, np.vstack((N1_flat, N2_flat)), delimiter=',', header='X,Y,Z', comments='')
        
        print("Coordinates exported to", filename)
    
    def exportCoordinatesSW(self, scaling = 10):

        red_color = self.RGBtoSW(255, 0, 0)
        blue_color = self.RGBtoSW(0, 0, 255)
        black_color = self.RGBtoSW(0, 0, 0)

        helix1Rods = []
        helix2Rods = []
        strings = []

        try:
            sw_app = win32com.client.GetActiveObject("SldWorks.Application")

            if not sw_app:
                raise Exception("Error: SolidWorks application not found. Make sure SolidWorks is running.")
            else:
                print("Application connected")

            sw_model = sw_app.ActiveDoc

            if not sw_model:
                raise Exception("Error: No active SolidWorks document found. Open a Part file first.")
            else:
                print("Document attached")
        
        
            sw_sketch_mgr = sw_model.SketchManager
            sw_feature_mgr = sw_model.FeatureManager
            sw_sel_mgr = sw_model.SelectionManager

            sw_sketch_mgr.Insert3DSketch(True)
            sw_model.ActiveView.EnableGraphicsUpdate = False

            '''
            #Generate the initial node sphere
            sw_model.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, None, 0)
            sw_sketch_mgr.InsertSketch(True)
            axis_line = sw_sketch_mgr.CreateLine(0, DHT.nodeRadius, 0, 0, -DHT.nodeRadius, 0)

            axis_line.ConstructionGeometry = True 
            sw_sketch_mgr.CreateArc(0, 0, 0, 0, DHT.nodeRadius, 0, 0, -DHT.nodeRadius, 0, -1)
            sw_sketch_mgr.InsertSketch(True) 
            angle_rad = 2 * math.pi 

            revolve_feat = sw_feature_mgr.FeatureRevolve2(True, True, False, False, False, False, 0, 0, angle_rad, 0, False, False, 0.01, 0.01, 0, 0, 0, True, True, True)

            '''

            for i in range(self.q+1):
                    for k in range(self.p):
                        x1, y1, z1 = self.N1[i, k, 0]*scaling, self.N1[i, k, 1]*scaling, self.N1[i, k, 2]*scaling
                        sw_sketch_mgr.CreatePoint(x1, y1, z1).Color = int(red_color)

                        if i < self.q:
                            x2, y2, z2 = self.N2[i, k, 0]*scaling, self.N2[i, k, 1]*scaling, self.N2[i, k, 2]*scaling
                            sw_sketch_mgr.CreatePoint(x2, y2, z2).Color = int(blue_color)
                        
                        if i < self.q:
                            k_curr = k
                            kp1 = (k+1) % self.p
                            km1 = (k-1) % self.p

                            n1_ik      = self.N1[i, k_curr] * scaling
                            n2_ik      = self.N2[i, k_curr] * scaling
                        
                            n1_ip1_kp1 = self.N1[i + 1, kp1] * scaling
                            
                            n1_ip1_k   = self.N1[i + 1, k_curr] * scaling
                            n2_i_km1   = self.N2[i, km1] * scaling
                            n1_ip1_km1 = self.N1[i + 1, km1] * scaling

                            h1Rod = sw_sketch_mgr.CreateLine(n1_ik[0], n1_ik[1], n1_ik[2], n1_ip1_kp1[0], n1_ip1_kp1[1], n1_ip1_kp1[2])
                            h1Rod.Color = int(red_color)
                            helix1Rods.append(h1Rod)

                            if i < self.q - 1:
                                n2_ip1_km1 = self.N2[i + 1, km1] * scaling
                                n2_x1, n2_y1, n2_z1 = self.N2[i, k_curr] * scaling
                                n2_x2, n2_y2, n2_z2 = self.N2[i + 1, km1] * scaling
                                
                                h2Rod = sw_sketch_mgr.CreateLine(n2_x2, n2_y2, n2_z2, n2_x1, n2_y1, n2_z1)
                                h2Rod.Color = int(blue_color)
                                helix2Rods.append(h2Rod)

                                s8 = sw_sketch_mgr.CreateLine(n2_i_km1[0], n2_i_km1[1], n2_i_km1[2], n2_ip1_km1[0], n2_ip1_km1[1], n2_ip1_km1[2])
                                s8.Color = int(black_color)
                                strings.append(s8)
                            else:
                                n1_top = self.N1[i+1, k_curr] * scaling

                                h2Rod = sw_sketch_mgr.CreateLine(n2_ik[0], n2_ik[1], n2_ik[2], n1_top[0], n1_top[1], n1_top[2])
                                h2Rod.Color = int(blue_color)
                                helix2Rods.append(h2Rod)

                            # s1
                            s1 = sw_sketch_mgr.CreateLine(n2_ik[0], n2_ik[1], n2_ik[2], n1_ik[0], n1_ik[1], n1_ik[2])
                            s1.Color = int(black_color)
                            strings.append(s1)
                            # s2
                            s2 = sw_sketch_mgr.CreateLine(n2_ik[0], n2_ik[1], n2_ik[2], n1_ip1_k[0], n1_ip1_k[1], n1_ip1_k[2])
                            s2.Color = int(black_color)
                            strings.append(s2)
                            # s3
                            s3 = sw_sketch_mgr.CreateLine(n1_ip1_k[0], n1_ip1_k[1], n1_ip1_k[2], n2_i_km1[0], n2_i_km1[1], n2_i_km1[2])
                            s3.Color = int(black_color)
                            strings.append(s3)
                            # s4
                            s4 = sw_sketch_mgr.CreateLine(n2_i_km1[0], n2_i_km1[1], n2_i_km1[2], n1_ik[0], n1_ik[1], n1_ik[2])
                            s4.Color = int(black_color)
                            strings.append(s4)
                            # s5
                            s5 = sw_sketch_mgr.CreateLine(n2_i_km1[0], n2_i_km1[1], n2_i_km1[2], n2_ik[0], n2_ik[1], n2_ik[2])
                            s5.Color = int(black_color)
                            strings.append(s5)
                            # s6
                            s6 = sw_sketch_mgr.CreateLine(n1_ik[0], n1_ik[1], n1_ik[2], n1_ip1_k[0], n1_ip1_k[1], n1_ip1_k[2])
                            s6.Color = int(black_color)
                            strings.append(s6)
                            # s7
                            s7 = sw_sketch_mgr.CreateLine(n1_ip1_km1[0], n1_ip1_km1[1], n1_ip1_km1[2], n1_ip1_k[0], n1_ip1_k[1], n1_ip1_k[2])
                            s7.Color = int(black_color)
                            strings.append(s7)

            print("3D sketches created")

            sw_sketch_mgr.Insert3DSketch(True)

            print("Finalized sketch addition")

            sw_feature_mgr.InsertWeldmentFeature

            print("Weldment feature inserted")

            sw_model.ClearSelection2(True)

            print("Selections cleared")

            for rod in helix1Rods:
                rodGroup = sw_feature_mgr.CreateStructuralMemberGroup
                rodGroup.Segments = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, tuple([rod]))
                rodGroupArray = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [rodGroup])
                sw_feature_mgr.InsertStructuralWeldment4(DHT.barAddress, 1, False, rodGroupArray)
            
            for rod in helix2Rods:
                rodGroup = sw_feature_mgr.CreateStructuralMemberGroup
                rodGroup.Segments = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, tuple([rod]))
                rodGroupArray = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [rodGroup])
                sw_feature_mgr.InsertStructuralWeldment4(DHT.barAddress, 1, False, rodGroupArray)
            
            for string in strings:
                stringGroup = sw_feature_mgr.CreateStructuralMemberGroup
                stringGroup.Segments = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, tuple([string]))
                stringGroupArray = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [stringGroup])
                sw_feature_mgr.InsertStructuralWeldment4(DHT.stringAddress, 1, False, stringGroupArray)

            print("Rods inserted")

            sw_model.ClearSelection2(True)
    
            '''
            # Step 1: Select the base sphere feature 
            # Use Mark = 1 for the feature to be patterned.
            # Change "Revolve1" to match your base feature's name in the tree.
            feat_selected = sw_model.Extension.SelectByID2("Revolve1", "BODYFEATURE", 0, 0, 0, False, 1, None, 0)
            
            # Step 2: Append the 3D Sketch containing your points to the selection
            # Use Mark = 4 to denote the driving sketch for the pattern.
            # Change "3DSketch1" to match your sketch's name.
            sketch_selected = sw_model.Extension.SelectByID2("3DSketch1", "SKETCH", 0, 0, 0, True, 4, None, 0)

            if not (feat_selected and sketch_selected):
                print("Selection failed. Double-check your feature and sketch names.")
                return

            # Step 3: Execute the Sketch Driven Pattern
            swFeatMgr = sw_model.FeatureManager
            
            # InsertSketchDrivenPattern3 parameters depend on your exact geometric needs, 
            # but the defaults (using the sketch centroid/points) usually work perfectly.
            # Signature: (ReferencePoint, UseCentroid, GeometryPattern, ... )
            pattern_feature = swFeatMgr.InsertSketchDrivenPattern3(1, False, False, False, False, False)
            
            if pattern_feature:
                print("Success: Spheres patterned at all 3D sketch points.")
            else:
                print("Error: Failed to generate the pattern.")

            '''

            sw_model.ActiveView.EnableGraphicsUpdate = True

            print("Graphics update is enabled")
        
            sw_model.ForceRebuild3(False)

        except Exception as e:
            print("Error exporting to SolidWorks:", e)

structure = DHT(p=4, q=4, L=0.5, a=(1/16), Ld=0.6)
#structure.visualize(showList=[True, True, True, True, True, True, True, True])
structure.exportCoordinatesSW(scaling=1)