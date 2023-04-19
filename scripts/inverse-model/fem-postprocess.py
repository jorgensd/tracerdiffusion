import h5py
import argparse
from tracerdiffusion.fenics2mri import function_to_image
import os
import dolfin
import nibabel
import numpy as np
import pathlib
import matplotlib.pyplot as plt
import re

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--hdffile", required=True,
                        help="""Path to hdf file storing the simulation results"""
                        )

    parser.add_argument("--mask", default="./roi12/parenchyma_mask_roi.mgz", required=True,
                    help="path to mask from which mesh was made.")
    

    parserargs = vars(parser.parse_args())

    parserargs["outfolder"] = pathlib.Path(parserargs["hdffile"]).parent

    files = ["J.txt", "D.txt", "r.txt"]
    labels = ["$L^2$-error", "D ($10^{-4}$ mm$^2$/s)", "r ($10^{-5}$/s)"]
    scales = [1, 1e4, 1e5]




    for file, label, scale in zip(files, labels, scales):
        


        plt.figure()
        history = np.genfromtxt(parserargs["outfolder"] / file, delimiter=",")
        if file == "D.txt":
            print("D final ", format(history[-1] * scale), "1e-4 mm^2/s")
            print("D final ", format(history[-1] * 3600), "mm^2/h")
        if file == "r.txt":
            print("r final ", format(history[-1] * scale), "1e-5 /s")
            print("r final ", format(history[-1] * 3600), "/h")

        plt.plot(np.array(range(history.size)), history * scale)
        plt.xlabel("Iteration")
        plt.ylabel(label)
    
    os.makedirs(parserargs["outfolder"], exist_ok=True)

    template_image = nibabel.load(parserargs["mask"])

    mask = template_image.get_fdata()

    hdffile = parserargs["hdffile"]

    assert os.path.isfile(hdffile)
    assert str(hdffile).endswith(".hdf")


    f = h5py.File(hdffile, 'r')
    print(list(f.keys()))

    roimesh= dolfin.Mesh()
    hdf = dolfin.HDF5File(roimesh.mpi_comm(), hdffile, "r")
    hdf.read(roimesh, "/mesh", False)
    
    V = dolfin.FunctionSpace(roimesh, "CG", 1)


    for key in list(f.keys()):
        if key == "mesh":
            continue

        u = dolfin.Function(V)

        hdf.read(u, key)

        function_nii, _ = function_to_image(function=u, template_image=template_image, extrapolation_value=np.nan, 
                                            mask = mask,
                                            # mask=template_image
                                            )

        nibabel.save(function_nii, str(parserargs["outfolder"] / (re.sub("[^0-9]","", key) + "h.mgz")))

    hdf.close()


    plt.show()

    # function_to_image()
    # 

