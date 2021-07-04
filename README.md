## voronoi-mapper
Plot a series of places on a map in the style of a Voronoi diagram, based on an input csv/txt file formatted in the following style (columns in any order):

| Labels / Places | X-Coord / Latitude | Y-Coord / Longitude | Colour Place / Been to Place |
|:---------------:|:------------------:|:-------------------:|:----------------------------:|
|     England     |            52.3555 |              1.1743 |               Y              |
|   Isle of Man   |            54.2361 |              4.5481 |               N              |
|    N Ireland    |            54.7877 |              6.4923 |               N              |
|     Scotland    |            56.4907 |              4.2026 |               Y              |
|      Wales      |            52.1307 |              3.7837 |               Y              |

# Step 1: Clone `voronoi-mapper` repo
Clone the `voronoi-mapper` repo to your area. Note you may need to set up ssh keys and add them to your GitHub account first.

```bash
git clone ssh://git@github.com:GluonicPenguin/voronoi-mapper.git
```

# Step 2: Install requirements

`voronoi-mapper` uses a conda installer, with the conda environment set up in Miniconda. To set up Miniconda3 and install the mapper requirements, do the following:

```bash
MINICONDA_DIR=~/. # change this to somewhere outside the voronoi-mapper repo
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $MINICONDA_DIR
rm Miniconda3-latest-Linux-x86_64.sh
cd $MINICONDA_DIR

source $MINICONDA_DIR/etc/profile.d/conda.sh
conda update -y -n base -c defaults conda
export PYTHONNOUSERSITE=true
```

Then back in your `voronoi-mapper` directory, set up the environment:

```bash
conda env create -f voronoi_mapper_env_requirements.yaml
conda activate voronoi_mapper_env
```

# Step 3: Use mapper





