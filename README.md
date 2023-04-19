# Requirements

## For data processing

- FreeSurfer needs to be installed
- The following folders/files are needed and can be obtained from ??? and should be put into the top level in your cloned reposity as:
- the conda environment `diffusion-fenics-env` needs to be installed (see below)
```
├──data
    ├──freesurfer
        ├── PREREG
        |   ├── 20220230_070707.mgz
        |   ├── 20220230_080808.mgz
        |   ├── ...
        ├── mri
        │   ├── aseg.mgz

        
        │   ├── parenchyma_mask.mgz
```

## For inverse problems (PINN and FEM)

This data can be obtained from ??? and should be put into the top level in your cloned reposity as:
```
├──data
    ├──freesurfer
        ├── CONCENTRATIONS
        |   ├── 0.00.mgz
        |   ├── 06.25.mgz
        |   ├── ...
        ├── mri
        │   ├── parenchyma_mask.mgz
        ├── meshes
        │   ├── lh.xml
├──roi12
    ├──parenchyma_mask_roi.mgz
    ├──parenchyma_mask_boundary.mgz
```

# Setup

For FEniCS scripts and data processing, run in terminal:

```
git clone https://github.com/bzapf/tracerdiffusion.git
cd tracerdiffusion
conda env create -f fenics-env.yml
conda activate diffusion-fenics-env
pip install -e .
export WORKDIR=./data/freesurfer/
```



For Jax PINN scripts, run
```
$ python scripts/inverse-model/pinn-inverse-diffusion.py
```
