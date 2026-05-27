import win32com.client
import numpy as np
import matplotlib.pyplot as plt

class DHT:

    def RGBtoSW(self, r, g, b):
        return b * 65536 + g * 256 + r

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

        try:
            sw_app = win32com.client.GetActiveObject("SldWorks.Application")
            sw_model = sw_app.ActiveDoc

            if not sw_model:
                raise Exception("Error: No active SolidWorks document found. Open a Part file first.")
        
            sw_sketch_mgr = sw_model.SketchManager

            sw_sketch_mgr.Insert3DSketch(True)
            sw_model.ActiveView.EnableGraphicsUpdate = False

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

                            sw_sketch_mgr.CreateLine(n1_ik[0], n1_ik[1], n1_ik[2], n1_ip1_kp1[0], n1_ip1_kp1[1], n1_ip1_kp1[2]).Color = int(red_color)

                            if i < self.q - 1:
                                n2_ip1_km1 = self.N2[i + 1, km1] * scaling
                                n2_x1, n2_y1, n2_z1 = self.N2[i, k_curr] * scaling
                                n2_x2, n2_y2, n2_z2 = self.N2[i + 1, km1] * scaling
                                
                                sw_sketch_mgr.CreateLine(n2_x2, n2_y2, n2_z2, n2_x1, n2_y1, n2_z1).Color = int(blue_color)
                                
                                sw_sketch_mgr.CreateLine(n2_i_km1[0], n2_i_km1[1], n2_i_km1[2], n2_ip1_km1[0], n2_ip1_km1[1], n2_ip1_km1[2]).Color = int(black_color)
                            else:
                                n1_top = self.N1[i+1, k_curr] * scaling
                                sw_sketch_mgr.CreateLine(n2_ik[0], n2_ik[1], n2_ik[2], n1_top[0], n1_top[1], n1_top[2]).Color = int(blue_color)

                            # s1
                            sw_sketch_mgr.CreateLine(n2_ik[0], n2_ik[1], n2_ik[2], n1_ik[0], n1_ik[1], n1_ik[2]).Color = int(black_color)
                            # s2
                            sw_sketch_mgr.CreateLine(n2_ik[0], n2_ik[1], n2_ik[2], n1_ip1_k[0], n1_ip1_k[1], n1_ip1_k[2]).Color = int(black_color)
                            # s3
                            sw_sketch_mgr.CreateLine(n1_ip1_k[0], n1_ip1_k[1], n1_ip1_k[2], n2_i_km1[0], n2_i_km1[1], n2_i_km1[2]).Color = int(black_color)
                            # s4
                            sw_sketch_mgr.CreateLine(n2_i_km1[0], n2_i_km1[1], n2_i_km1[2], n1_ik[0], n1_ik[1], n1_ik[2]).Color = int(black_color)
                            # s5
                            sw_sketch_mgr.CreateLine(n2_i_km1[0], n2_i_km1[1], n2_i_km1[2], n2_ik[0], n2_ik[1], n2_ik[2]).Color = int(black_color)
                            # s6
                            sw_sketch_mgr.CreateLine(n1_ik[0], n1_ik[1], n1_ik[2], n1_ip1_k[0], n1_ip1_k[1], n1_ip1_k[2]).Color = int(black_color)
                            # s7
                            sw_sketch_mgr.CreateLine(n1_ip1_km1[0], n1_ip1_km1[1], n1_ip1_km1[2], n1_ip1_k[0], n1_ip1_k[1], n1_ip1_k[2]).Color = int(black_color)
            
            sw_sketch_mgr.Insert3DSketch(True)
            sw_model.ActiveView.EnableGraphicsUpdate = True
            sw_model.ForceRebuild3(False)

        except Exception as e:
            print("Error exporting to SolidWorks:", e)

structure = DHT(p=4, q=5, L=1, a=(1/16), Ld=1.1)
#structure.visualize(showList=[True, True, True, True, True, True, True, True])
structure.exportCoordinatesSW(scaling=1)