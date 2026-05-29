using MathNet.Numerics;
using MathNet.Numerics.LinearAlgebra;
using MathNet.Numerics.LinearAlgebra.Complex;
using SolidWorks.Interop.sldworks;
using SwConst;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using TensegrityGeneratorSharp.Properties;
using Vector = MathNet.Numerics.LinearAlgebra.Vector<double>;

namespace TensegrityGeneratorSharp
{
    public partial class MainForm : Form
    {
        public MainForm()
        {
            InitializeComponent();
        }

        static int RGBtoSW(int r, int g, int b)
        {
            return b * 65536 + g * 256 + r;
        }

        const string stringAddress = "C:\\Program Files\\SOLIDWORKS Corp\\SOLIDWORKS\\data\\weldment profiles\\Shapeshifter Standard\\Tensegrity String 3 mm\\3mm.SLDLFP";
        const string barAddress = "C:\\Program Files\\SOLIDWORKS Corp\\SOLIDWORKS\\data\\weldment profiles\\Shapeshifter Standard\\Tensegrity Bar 6 mm\\6mm Bar.SLDLFP";
        const double nodeRadius = 0.01;

        public static ModelDoc2 part;
        public static FeatureManager featMgr;
        public static SelectionMgr selMgr;
        public static SldWorks swApp = null;
        public static ModelDocExtension swExt = null;
        public static SketchManager sketchMgr;

        class DHT
        {
            //public

            //private
            int p = 5;
            int q = 4;
            double L = 1.0;
            double a = (1 / 16);
            double Ld = 1.005;

            Vector[,] N1;
            Vector[,] N2;

            int red = RGBtoSW(255, 0, 0);
            int blue = RGBtoSW(0, 0, 255);
            int black = RGBtoSW(0, 0, 0);

            string saveFolder = "";

            public DHT(int p = 5, int q = 4, double l = 1.0, double a = 0.125, double ld = 1.01, string saveFolder = null)
            {
                this.p = p;
                this.q = q;
                this.L = l;
                this.a = a;
                this.Ld = ld;

                generateStructure();
                this.saveFolder = saveFolder;
            }

            void generateStructure()
            {
                N1 = new Vector[q + 1, p];
                N2 = new Vector[q + 1, p];

                int _l = 0;
                double z = 0;
                double theta = 0;
                double r_val = 0;


                for (int i = 0; i < q + 1; i++)
                {
                    for (int k = 0; k < p; k++)
                    {
                        N1[i, k] = Vector.Build.Dense(3, 0.0);
                        N2[i, k] = Vector.Build.Dense(3, 0.0);

                        _l = 1;
                        z = (2 * i + (_l - 1)) * (L / (2 * q));
                        theta = (2 * k + L) * (Math.PI / p);
                        r_val = Math.Sqrt(4 * a * (Ld - z));

                        N1[i, k][0] = r_val * Math.Cos(theta);
                        N1[i, k][1] = r_val * Math.Sin(theta);
                        N1[i, k][2] = z;

                        if (i < q)
                        {
                            _l = 2;
                            z = (2 * i + (_l - 1)) * (L / (2 * q));
                            theta = (2 * k + L) * (Math.PI / p);
                            r_val = Math.Sqrt(4 * a * (Ld - z));

                            N2[i, k][0] = r_val * Math.Cos(theta);
                            N2[i, k][1] = r_val * Math.Sin(theta);
                            N2[i, k][2] = z;
                        }
                        else
                        {
                            N2[i, k][0] = double.NaN;
                            N2[i, k][1] = double.NaN;
                            N2[i, k][2] = double.NaN;
                        }
                    }
                }
            }


            public void generateInSolidworks()
            {
                if (swApp == null) { MessageBox.Show("Solidworks App Null, terminating."); return; }

                part.ClearSelection2(true);

                bool frontPlaneSelected = swExt.SelectByID2("Front Plane", "PLANE", 0, 0, 0, false, 0, null, 0);

                if (!frontPlaneSelected) { throw new Exception("Failed to select the front plane."); }

                #region Generate Joint Ball
                sketchMgr.InsertSketch(true);

                SketchSegment axisLine = sketchMgr.CreateLine(0, nodeRadius, 0, 0, -nodeRadius, 0);
                axisLine.ConstructionGeometry = true;
                sketchMgr.CreateArc(0, 0, 0, 0, nodeRadius, 0, 0, -nodeRadius, 0, -1);

                sketchMgr.InsertSketch(true);

                Feature jointBall = featMgr.FeatureRevolve2(true, true, false, false, false, false, 0, 0, 2 * Math.PI, 0, false, false, 0.01, 0.01, 0, 0, 0, true, true, true);

                jointBall.Name = "Joint Ball";

                part.ClearSelection2(true);
                #endregion

                part.IActiveView.EnableGraphicsUpdate = false;
                sketchMgr.Insert3DSketch(true);

                Feature insertedFeature = (Feature)part.IGetActiveSketch2();
                insertedFeature.Name = "Point Sketch";

                int kp1 = 0;
                int km1 = 0;

                //first generate the points, then loop again to generate the rod

                for (int i = 0; i < q + 1; i++)
                {
                    for (int k = 0; k < p; k++)
                    {
                        sketchMgr.CreatePoint(N1[i, k][0], N1[i, k][1], N1[i, k][2]).Color = red;
                        if (i < q)
                        {
                            sketchMgr.CreatePoint(N2[i, k][0], N2[i, k][1], N2[i, k][2]).Color = blue;
                        }
                    }
                }

                sketchMgr.Insert3DSketch(true); //close the point sketch

                part.ClearSelection2(true);

                #region Weldment Addition

                sketchMgr.Insert3DSketch(true);

                insertedFeature = (Feature)part.IGetActiveSketch2();
                insertedFeature.Name = "Rods Sketch";

                List<SketchSegment> helix1Rods = new List<SketchSegment>();
                List<SketchSegment> helix2Rods = new List<SketchSegment>();
                List<SketchSegment> strings = new List<SketchSegment>();

                for (int i = 0; i < q + 1; i++)
                {
                    for (int k = 0; k < p; k++)
                    {
                        if (i < q)
                        {
                            kp1 = (k + 1) % p;
                            km1 = (k - 1) % p;

                            if (km1 < 0)
                            {
                                km1 = p + km1;
                            }

                            Vector<double> n1_ik = N1[i, k];
                            Vector<double> n2_ik = N2[i, k];
                            Vector<double> n1_ip1_kp1 = N1[i + 1, kp1];
                            Vector<double> n1_ip1_k = N1[i + 1, k];
                            Vector<double> n2_i_km1 = N2[i, km1];
                            Vector<double> n1_ip1_km1 = N1[i + 1, km1];

                            SketchSegment h1Rod = sketchMgr.CreateLine(n1_ik[0], n1_ik[1], n1_ik[2], n1_ip1_kp1[0], n1_ip1_kp1[1], n1_ip1_kp1[2]);
                            h1Rod.Color = red;
                            helix1Rods.Add(h1Rod);

                            SketchSegment h2Rod = null;

                            if (i < q - 1)
                            {
                                Vector<double> n2_ip1_km1 = N2[i + 1, km1];

                                h2Rod = sketchMgr.CreateLine(n2_ik[0], n2_ik[1], n2_ik[2], n2_ip1_km1[0], n2_ip1_km1[1], n2_ip1_km1[2]);
                                h2Rod.Color = blue;
                                helix2Rods.Add(h2Rod);

                                SketchSegment s8 = sketchMgr.CreateLine(n2_i_km1[0], n2_i_km1[1], n2_i_km1[2], n2_ip1_km1[0], n2_ip1_km1[1], n2_ip1_km1[2]);
                                s8.Color = black;
                                strings.Add(s8);
                            }
                            else
                            {
                                Vector<double> n1_top = N1[i + 1, k];

                                h2Rod = sketchMgr.CreateLine(n2_ik[0], n2_ik[1], n2_ik[2], n1_top[0], n1_top[1], n1_top[2]);
                                h2Rod.Color = blue;
                                helix2Rods.Add(h2Rod);
                            }

                            SketchSegment s1 = sketchMgr.CreateLine(n2_ik[0], n2_ik[1], n2_ik[2], n1_ik[0], n1_ik[1], n1_ik[2]);
                            s1.Color = black;
                            strings.Add(s1);

                            SketchSegment s2 = sketchMgr.CreateLine(n2_ik[0], n2_ik[1], n2_ik[2], n1_ip1_k[0], n1_ip1_k[1], n1_ip1_k[2]);
                            s2.Color = black;
                            strings.Add(s2);

                            SketchSegment s3 = sketchMgr.CreateLine(n1_ip1_k[0], n1_ip1_k[1], n1_ip1_k[2], n2_i_km1[0], n2_i_km1[1], n2_i_km1[2]);
                            s3.Color = black;
                            strings.Add(s3);

                            SketchSegment s4 = sketchMgr.CreateLine(n2_i_km1[0], n2_i_km1[1], n2_i_km1[2], n1_ik[0], n1_ik[1], n1_ik[2]);
                            s4.Color = black;
                            strings.Add(s4);

                            SketchSegment s5 = sketchMgr.CreateLine(n2_i_km1[0], n2_i_km1[1], n2_i_km1[2], n2_ik[0], n2_ik[1], n2_ik[2]);
                            s5.Color = black;
                            strings.Add(s5);

                            SketchSegment s6 = sketchMgr.CreateLine(n1_ik[0], n1_ik[1], n1_ik[2], n1_ip1_k[0], n1_ip1_k[1], n1_ip1_k[2]);
                            s6.Color = black;
                            strings.Add(s6);

                            SketchSegment s7 = sketchMgr.CreateLine(n1_ip1_km1[0], n1_ip1_km1[1], n1_ip1_km1[2], n1_ip1_k[0], n1_ip1_k[1], n1_ip1_k[2]);
                            s7.Color = black;
                            strings.Add(s7);

                        }
                    }
                }

                //Sketches are created

                sketchMgr.Insert3DSketch(true);

                //Adding weldments

                featMgr.InsertWeldmentFeature();

                part.ClearSelection2(true);

                //Add them
                part.Extension.SetUserPreferenceToggle(
    (int)swUserPreferenceToggle_e.swWeldmentEnableAutomaticCutList,
    (int)swUserPreferenceOption_e.swDetailingNoOptionSpecified,
    false);
                List<StructuralMemberGroup> groupsList = new List<StructuralMemberGroup>();
                StructuralMemberGroup group = default(StructuralMemberGroup);

                foreach (SketchSegment h1Rod in helix1Rods)
                {
                    group = featMgr.CreateStructuralMemberGroup();
                    group.Segments = new SketchSegment[] { h1Rod };

                    groupsList.Add(group);
                }

                Feature h1Rods = featMgr.InsertStructuralWeldment4(barAddress, 1, false, groupsList.ToArray());

                h1Rods.Name = "Helix 1 Rods";

                groupsList.Clear();

                foreach (SketchSegment h2Rod in helix2Rods)
                {
                    group = featMgr.CreateStructuralMemberGroup();
                    group.Segments = new SketchSegment[] { h2Rod };

                    groupsList.Add(group);
                }

                Feature h2Rods = featMgr.InsertStructuralWeldment4(barAddress, 1, false, groupsList.ToArray());

                h2Rods.Name = "Helix 2 Rods";

                groupsList.Clear();

                foreach (SketchSegment @string in strings)
                {
                    group = featMgr.CreateStructuralMemberGroup();
                    group.Segments = new SketchSegment[] { @string };

                    groupsList.Add(group);
                }

                Feature stringsFeature = featMgr.InsertStructuralWeldment4(stringAddress, 1, false, groupsList.ToArray());

                stringsFeature.Name = "Strings";

                #endregion

                part.IActiveView.EnableGraphicsUpdate = true;

                part.Extension.SetUserPreferenceToggle(
    (int)swUserPreferenceToggle_e.swWeldmentEnableAutomaticCutList,
    (int)swUserPreferenceOption_e.swDetailingNoOptionSpecified,
    true);

                part.ForceRebuild3(false);

                #region Populate Joint Ball
                part.ClearSelection2(true);

                bool ballSelected = swExt.SelectByID2("Joint Ball", "SOLIDBODY", 0, 0, 0, false, 256, null, 0);
                bool sketchSelected = swExt.SelectByID2("Point Sketch", "SKETCH", 0, 0, 0, true, 64, null, 0);

                if (!ballSelected || !sketchSelected)
                {
                    throw new Exception("Sketches couldn't be selected");
                }

                SketchPatternFeatureData swSketchPatt = (SketchPatternFeatureData)featMgr.CreateDefinition((int)swFeatureNameID_e.swFmSketchPattern);
                swSketchPatt.GeometryPattern = false;
                swSketchPatt.UseCentroid = true;

                Feature ballPattern = featMgr.CreateFeature(swSketchPatt);
                ballPattern.Name = "Joint Ball Pattern";

                part.ClearSelection2(true);

                bool seedBallSelected = swExt.SelectByID2("Joint Ball", "SOLIDBODY", 0, 0, 0, false, 0, null, 0);
                Body2 seedBody = (Body2)selMgr.GetSelectedObject6(1, -1);

                seedBody.HideBody(true);

                part.ClearSelection2(true);
                #endregion



                #region Save the thing
                string[] addresses = { saveFolder, p.ToString() + "x" + q.ToString() + "_Paraboloid_DHT.stl" };

                string combinedPath = System.IO.Path.Combine(addresses);

                int errors = 0, warnings = 0;

                swExt.SaveAs2(combinedPath,
    (int)swSaveAsVersion_e.swSaveAsCurrentVersion,
    (int)swSaveAsOptions_e.swSaveAsOptions_Silent,
    null,
    "",
    false,
    ref errors,
    ref warnings);
                #endregion

            }


        }

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                swApp = (SldWorks)Marshal.GetActiveObject("SldWorks.Application");

                try
                {
                    part = swApp.ActiveDoc;

                    selMgr = part.SelectionManager;
                    featMgr = part.FeatureManager;
                    swExt = part.Extension;
                    sketchMgr = part.SketchManager;

                    btn_connectSolid.BackColor = Color.LightSeaGreen;
                }
                catch
                {
                    MessageBox.Show("No active part");
                    btn_connectSolid.BackColor = Color.PaleVioletRed;
                }
            }
            catch
            {
                MessageBox.Show("Most likely no active instance present");
                btn_connectSolid.BackColor = Color.PaleVioletRed;
            }
        }

        private void btn_Generate_Click(object sender, EventArgs e)
        {
            Dictionary<string, string> parameters = dhT_Paraboloid1.GetParameters();

            DHT myStructure = new DHT(int.Parse(parameters["p"]), int.Parse(parameters["q"]), double.Parse(parameters["l"]), double.Parse(parameters["a"]), double.Parse(parameters["ld"]), tbox_saveAddress.Text);

            myStructure.generateInSolidworks();
        }

        private void MainForm_Load(object sender, EventArgs e)
        {
            tbox_saveAddress.Text = System.Environment.GetFolderPath(System.Environment.SpecialFolder.Desktop);
        }

        private void btn_selectFolder_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog folderBrowserDialog = new FolderBrowserDialog();

            if (folderBrowserDialog.ShowDialog() == DialogResult.OK)
            {
                tbox_saveAddress.Text = folderBrowserDialog.SelectedPath;
            }
        }
    }
}
